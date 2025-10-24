import json
import os
import subprocess
import threading
import queue
import time
import numpy as np

import cv2
import requests
from flask import Flask, Response, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from ultralytics import YOLO

from utils import predictImgY, chatApi

# 空行占位，已统一使用 FFmpeg 进行视频转换


# FFmpeg摄像头捕获类（解决OpenCV在Windows 11上的兼容性问题）
class FFmpegCamera:
    """使用FFmpeg捕获摄像头帧，兼容Windows 11"""
    
    @staticmethod
    def list_cameras(ffmpeg_path=None):
        """列出可用摄像头"""
        if ffmpeg_path:
            ffmpeg_exe = os.path.join(ffmpeg_path, 'ffmpeg.exe')
        else:
            ffmpeg_exe = 'ffmpeg'
        
        try:
            cmd = [ffmpeg_exe, '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy']
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            output = result.stderr
            
            cameras = []
            for line in output.split('\n'):
                if '"' in line and '(video)' in line:
                    start = line.find('"') + 1
                    end = line.find('"', start)
                    if start > 0 and end > start:
                        cameras.append(line[start:end])
            return cameras
        except:
            return []
    
    def __init__(self, device_name=None, width=640, height=480, fps=20, ffmpeg_path=None):
        self.width = width
        self.height = height
        self.fps = fps
        self.process = None
        self.frame_queue = queue.Queue(maxsize=10)
        self.is_running = False
        self.thread = None
        self.init_success = False
        
        if ffmpeg_path:
            ffmpeg_exe = os.path.join(ffmpeg_path, 'ffmpeg.exe')
        else:
            ffmpeg_exe = 'ffmpeg'
        
        if device_name is None:
            cameras = self.list_cameras(ffmpeg_path)
            if cameras:
                device_name = cameras[0]
                print(f"使用摄像头: {device_name}")
            else:
                self.device_name = None
                self.process = None
                return
        
        self.device_name = device_name
        
        try:
            cmd = [
                ffmpeg_exe,
                '-f', 'dshow',
                '-video_size', f'{width}x{height}',
                '-framerate', str(fps),
                '-i', f'video={device_name}',
                '-f', 'image2pipe',
                '-pix_fmt', 'bgr24',
                '-vcodec', 'rawvideo',
                '-'
            ]
            
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=10**8
            )
            
            import time
            time.sleep(0.5)
            
            if self.process.poll() is not None:
                _, stderr = self.process.communicate()
                print(f"摄像头启动失败: {stderr.decode('utf-8', errors='ignore')[:200]}")
                self.process = None
                return
            
            self.is_running = True
            self.thread = threading.Thread(target=self._read_frames, daemon=True)
            self.thread.start()
            time.sleep(0.5)
            self.init_success = True
            
        except Exception as e:
            print(f"摄像头异常: {e}")
            self.process = None
    
    def _read_frames(self):
        frame_size = self.width * self.height * 3
        while self.is_running and self.process:
            try:
                raw_frame = self.process.stdout.read(frame_size)
                if len(raw_frame) != frame_size:
                    break
                frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((self.height, self.width, 3))
                if self.frame_queue.full():
                    try:
                        self.frame_queue.get_nowait()
                    except:
                        pass
                self.frame_queue.put(frame)
            except:
                break
    
    def isOpened(self):
        """检查摄像头是否已打开"""
        return self.process is not None and self.is_running
    
    def read(self):
        """读取一帧"""
        try:
            frame = self.frame_queue.get(timeout=1.0)
            return True, frame
        except queue.Empty:
            return False, None
    
    def release(self):
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=2.0)
            except:
                self.process.kill()
            self.process = None


# Flask 应用设置
class VideoProcessingApp:
    def __init__(self, host='0.0.0.0', port=5000):
        """初始化 Flask 应用并设置路由"""
        self.app = Flask(__name__)
        
        # 启用CORS，允许所有域名访问（解决前端跨域问题）
        CORS(self.app, resources={r"/*": {"origins": "*"}})
        
        self.socketio = SocketIO(
            self.app, 
            cors_allowed_origins="*",
            async_mode='threading',
            logger=False,
            engineio_logger=False,
            ping_timeout=60,
            ping_interval=25,
            transports=['polling', 'websocket']  # 先使用polling，再升级到websocket
        )  # 初始化 SocketIO
        self.host = host
        self.port = port
        self.setup_routes()
        self.data = {}  # 存储接收参数
        self.paths = {
            'download': './runs/video/download.mp4',
            'output': './runs/video/output.mp4',
            'video_output': "./runs/video/video_output.avi",  # 视频检测用的临时 AVI 文件
            'camera_output': "./runs/video/camera_output.avi"  # 摄像头检测用的临时 AVI 文件
        }
        self.recording = False  # 标志位，判断是否正在录制视频
        # API密钥配置
        self.DeepSeek = 'sk-e81dacdd9f93432b831de696176df1a6'
        self.Qwen = 'sk-lluefpkltgpoobuybmjbsjfpqmrngxpaqfpkesbqwwmhgykz'

    def setup_routes(self):
        """设置所有路由"""
        self.app.add_url_rule('/file_names', 'file_names', self.file_names, methods=['GET'])
        self.app.add_url_rule('/predictImg', 'predictImg', self.predictImg, methods=['POST'])
        self.app.add_url_rule('/predictVideo', 'predictVideo', self.predictVideo)
        self.app.add_url_rule('/predictCamera', 'predictCamera', self.predictCamera)
        self.app.add_url_rule('/stopCamera', 'stopCamera', self.stopCamera, methods=['GET'])
        self.app.add_url_rule('/test_think_mode', 'test_think_mode', self.test_think_mode, methods=['POST'])

        # 添加 WebSocket 事件
        @self.socketio.on('connect')
        def handle_connect():
            print("WebSocket connected!")
            emit('message', {'data': 'Connected to WebSocket server!'})

        @self.socketio.on('disconnect')
        def handle_disconnect():
            print("WebSocket disconnected!")

    def run(self):
        """启动 Flask 应用"""
        self.socketio.run(self.app, host=self.host, port=self.port, allow_unsafe_werkzeug=True)

    def file_names(self):
        """模型列表接口"""
        weight_items = [{'value': name, 'label': name} for name in self.get_file_names("./weights")]
        return jsonify({'weight_items': weight_items})

    def predictImg(self):
        """图片预测接口"""
        data = request.get_json()
        # 打印完整请求数据
        print("接收到的完整请求数据:", data)
        print("原始thinkMode值:", data.get('thinkMode'), "类型:", type(data.get('thinkMode')))
        
        # 处理thinkMode的各种可能情况
        think_mode_value = data.get('thinkMode')
        if think_mode_value is None:
            think_mode_result = False
        elif isinstance(think_mode_value, bool):
            think_mode_result = think_mode_value
        elif isinstance(think_mode_value, str):
            think_mode_result = think_mode_value.lower() == 'true'
        else:
            think_mode_result = bool(think_mode_value)
        
        self.data.clear()
        self.data.update({
            "username": data['username'], "weight": data['weight'],
            "conf": data['conf'], "startTime": data['startTime'],
            "inputImg": data['inputImg'], "ai": data['ai'],
            "thinkMode": think_mode_result
        })
        # 打印处理后的thinkMode值
        print("处理后thinkMode值:", self.data["thinkMode"], "类型:", type(self.data["thinkMode"]))
        print(self.data)
        predict = predictImgY.ImagePredictor(weights_path=f'./weights/{self.data["weight"]}',
                                            img_path=self.data["inputImg"], save_path='./runs/result.jpg',
                                            conf=float(self.data["conf"]))
        # 执行预测
        results = predict.predict()
        uploadedUrl = self.upload('./runs/result.jpg')
        if results['labels'] != '预测失败':
            self.data["status"] = 200
            self.data["message"] = "预测成功"
            self.data["outImg"] = uploadedUrl
            self.data["allTime"] = results['allTime']
            self.data["confidence"] = json.dumps(results['confidences'])
            self.data["label"] = json.dumps(results['labels'])
        else:
            self.data["status"] = 400
            self.data["message"] = "该图片无法识别，请重新上传！"
        
        # 根据选择的AI模型生成建议
        if self.data["status"] == 200:
            chat = chatApi.ChatAPI(
                deepseek_api_key=self.DeepSeek,
                qwen_api_key=self.Qwen
            )
            list_input = self.process_list(results['labels'])
            text = "我用YOLO检测出"
            for i in list_input:
                text += i
                text += "，"
            text += "请你作为一名经验丰富的教育专家，针对这些课堂行为问题，帮我生成一些实质性的建议，包括如何改善课堂纪律、提高学生专注度、优化教学方法等。只需回答我要的结果。"
            messages = [
                {"role": "user", "content": text}
            ]
            
            if self.data["ai"] == 'Deepseek-R1':
                self.socketio.emit('message', {'data': '已检测完成，正在生成DeepSeekAI建议！'})
                self.data["suggestion"] = chat.deepseek_request(messages)
            elif self.data["ai"] == 'Qwen':
                self.socketio.emit('message', {'data': '已检测完成，正在生成QwenAI建议！'})
                self.data["suggestion"] = chat.qwen_request(messages)
            elif self.data["ai"] == 'Deepseek-R1-LAN':
                self.socketio.emit('message', {'data': '已检测完成，正在生成局域网Deepseek-R1建议！'})
                self.data["suggestion"] = chat.lan_deepseek_request(messages)
            elif self.data["ai"] == 'Deepseek-R1-Local':
                self.socketio.emit('message', {'data': '已检测完成，正在生成本地Deepseek-R1建议！'})
                self.data["suggestion"] = chat.local_deepseek_request(messages)
            elif self.data["ai"] == 'Gemma3-Local':
                self.socketio.emit('message', {'data': '已检测完成，正在生成本地Gemma3建议！'})
                self.data["suggestion"] = chat.local_gemma_request(messages)
            elif self.data["ai"] == 'Gemma3-LAN':
                self.socketio.emit('message', {'data': '已检测完成，正在生成局域网Gemma3建议！'})
                self.data["suggestion"] = chat.lan_gemma_request(messages)
            elif self.data["ai"] == 'Qwen3.0-Local':
                self.socketio.emit('message', {'data': '已检测完成，正在生成本地qwen3.0建议！'})
                self.data["suggestion"] = chat.local_qwen3_request(messages, think_mode=bool(self.data.get("thinkMode", False)))
            elif self.data["ai"] == 'Qwen3.0-LAN':
                self.socketio.emit('message', {'data': '已检测完成，正在生成局域网qwen3.0建议！'})
                self.data["suggestion"] = chat.lan_qwen3_request(messages, think_mode=bool(self.data.get("thinkMode", False)))
            elif self.data["ai"] == 'Qwen2.5-VL-Local':
                self.socketio.emit('message', {'data': '已检测完成，正在生成本地qwen2.5-VL建议！'})
                self.data["suggestion"] = chat.local_qwen25vl_request(messages)
            elif self.data["ai"] == 'Qwen2.5-VL-LAN':
                self.socketio.emit('message', {'data': '已检测完成，正在生成局域网qwen2.5-VL建议！'})
                self.data["suggestion"] = chat.lan_qwen25vl_request(messages)
            else:
                # 当选择"不使用AI"或未选择时，设置为空字符串
                self.data["suggestion"] = ""
        else:
            self.data["suggestion"] = ""
        path = self.data["inputImg"].split('/')[-1]
        if os.path.exists('./' + path):
            os.remove('./' + path)
        return jsonify(self.data)

    def predictVideo(self):
        """视频预测接口"""
        startTime = time.time()  # 记录开始时间
        
        self.data.clear()
        
        # 打印原始请求参数
        print("视频预测原始请求参数:", request.args)
        print("视频预测原始thinkMode值:", request.args.get('thinkMode'), "类型:", type(request.args.get('thinkMode')))
        
        # 处理thinkMode的各种可能情况
        think_mode_value = request.args.get('thinkMode')
        if think_mode_value is None:
            think_mode_result = False
        elif isinstance(think_mode_value, bool):
            think_mode_result = think_mode_value
        elif isinstance(think_mode_value, str):
            think_mode_result = think_mode_value.lower() == 'true'
        else:
            think_mode_result = bool(think_mode_value)
            
        self.data.update({
            "username": request.args.get('username'),
            "weight": request.args.get('weight'),
            "conf": request.args.get('conf'),
            "startTime": request.args.get('startTime'),
            "ai": request.args.get('ai'),
            "thinkMode": think_mode_result
        })
        
        # 打印处理后的thinkMode值
        print("视频预测处理后thinkMode值:", self.data["thinkMode"], "类型:", type(self.data["thinkMode"]))
        
        if not all([self.data["username"], self.data["weight"], self.data["conf"]]):
            return jsonify({"status": 400, "message": "参数不完整", "code": -1})
            
        self.socketio.emit('message', {'data': '正在加载，请稍等！'})
        model = YOLO(f'./weights/{self.data["weight"]}')
        
        # 下载视频文件
        video_url = request.args.get('inputVideo')
        if not video_url:
            return jsonify({"status": 400, "message": "未上传视频", "code": -1})
            
        # 使用download方法下载视频
        os.makedirs(os.path.dirname(self.paths['download']), exist_ok=True)
        try:
            with requests.get(video_url, stream=True) as response:
                response.raise_for_status()
                with open(self.paths['download'], 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
            print(f"视频已成功下载并保存到 {self.paths['download']}")
        except requests.RequestException as e:
            print(f"视频下载失败: {e}")
            return jsonify({"status": 400, "message": f"视频下载失败: {str(e)}", "code": -1})
            
        self.data["inputVideo"] = video_url
        
        cap = cv2.VideoCapture(self.paths['download'])
        if not cap.isOpened():
            return jsonify({"status": 400, "message": "无法打开视频文件", "code": -1})
            
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # 先生成 AVI 格式（更稳定），然后转换为浏览器兼容的 MP4
        video_writer = cv2.VideoWriter(
            self.paths['video_output'],  # 写入临时 AVI 文件
            cv2.VideoWriter_fourcc(*'XVID'),  # 使用 XVID 编码
            30,
            (640, 480)
        )
        
        all_labels = []  # 存储所有检测到的标签
        all_confidences = []  # 存储所有检测到的置信度

        def generate():
            try:
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    frame = cv2.resize(frame, (640, 480))
                    results = model.predict(source=frame, conf=float(self.data['conf']), show=False)
                    processed_frame = results[0].plot()
                    video_writer.write(processed_frame)
                    
                    # 收集当前帧的标签
                    if len(results[0].boxes) > 0:
                        current_labels = results[0].names
                        current_boxes = results[0].boxes
                        for box in current_boxes:
                            label_id = int(box.cls[0])
                            if label_id in current_labels:
                                all_labels.append(current_labels[label_id])
                                all_confidences.append(float(box.conf[0]))
                    
                    _, jpeg = cv2.imencode('.jpg', processed_frame)
                    yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n'
            finally:
                print("\n" + "="*50)
                print("开始后处理流程")
                print("="*50)
                
                # 1. 释放资源
                try:
                    self.cleanup_resources(cap, video_writer)
                    print("✅ 资源释放完成")
                except Exception as e:
                    print(f"❌ 资源释放失败: {e}")
                
                self.socketio.emit('message', {'data': '处理完成，正在保存！'})
                
                # 2. 处理AI建议（如果出错不影响后续流程）
                try:
                    if self.data.get("ai"):
                        print("开始生成AI建议...")
                        chat = chatApi.ChatAPI(
                            deepseek_api_key=self.DeepSeek,
                            qwen_api_key=self.Qwen
                        )
                        unique_labels = self.process_list(all_labels)
                        text = "我用YOLO检测出"
                        for label in unique_labels:
                            text += label + "，"
                        text += "请你作为一名经验丰富的教育专家，针对这些课堂行为问题，帮我生成一些实质性的建议，包括如何改善课堂纪律、提高学生专注度、优化教学方法等。只需回答我要的结果。"
                        messages = [{"role": "user", "content": text}]
                        
                        suggestion = ""
                        if self.data["ai"] == 'Deepseek-R1':
                            self.socketio.emit('message', {'data': '已检测完成，正在生成DeepSeekAI建议！'})
                            suggestion = chat.deepseek_request(messages)
                        elif self.data["ai"] == 'Qwen':
                            self.socketio.emit('message', {'data': '已检测完成，正在生成QwenAI建议！'})
                            suggestion = chat.qwen_request(messages)
                        elif self.data["ai"] == 'Deepseek-R1-LAN':
                            self.socketio.emit('message', {'data': '已检测完成，正在生成局域网Deepseek-R1建议！'})
                            suggestion = chat.lan_deepseek_request(messages)
                        elif self.data["ai"] == 'Deepseek-R1-Local':
                            self.socketio.emit('message', {'data': '已检测完成，正在生成本地Deepseek-R1建议！'})
                            suggestion = chat.local_deepseek_request(messages)
                        elif self.data["ai"] == 'Gemma3-Local':
                            self.socketio.emit('message', {'data': '已检测完成，正在生成本地Gemma3建议！'})
                            suggestion = chat.local_gemma_request(messages)
                        elif self.data["ai"] == 'Gemma3-LAN':
                            self.socketio.emit('message', {'data': '已检测完成，正在生成局域网Gemma3建议！'})
                            suggestion = chat.lan_gemma_request(messages)
                        elif self.data["ai"] == 'Qwen3.0-Local':
                            self.socketio.emit('message', {'data': '已检测完成，正在生成本地qwen3.0建议！'})
                            suggestion = chat.local_qwen3_request(messages, think_mode=bool(self.data.get("thinkMode", False)))
                        elif self.data["ai"] == 'Qwen3.0-LAN':
                            self.socketio.emit('message', {'data': '已检测完成，正在生成局域网qwen3.0建议！'})
                            suggestion = chat.lan_qwen3_request(messages, think_mode=bool(self.data.get("thinkMode", False)))
                        elif self.data["ai"] == 'Qwen2.5-VL-Local':
                            self.socketio.emit('message', {'data': '已检测完成，正在生成本地qwen2.5-VL建议！'})
                            suggestion = chat.local_qwen25vl_request(messages)
                        elif self.data["ai"] == 'Qwen2.5-VL-LAN':
                            self.socketio.emit('message', {'data': '已检测完成，正在生成局域网qwen2.5-VL建议！'})
                            suggestion = chat.lan_qwen25vl_request(messages)
                        
                        if suggestion:
                            print(f"生成AI建议成功，长度: {len(suggestion)}，前100个字符: {suggestion[:100]}")
                            self.data["suggestion"] = suggestion
                            self.socketio.emit('suggestion', suggestion)
                            print("已发送suggestion事件到前端")
                            self.socketio.emit('message', {'data': 'AI建议生成完成，请查看页面底部！'})
                            print("✅ AI建议生成完成")
                except Exception as e:
                    print(f"❌ AI建议生成失败: {e}")
                    import traceback
                    traceback.print_exc()
                
                # 3. 转换视频为浏览器兼容的 MP4 格式
                uploadedUrl = ""
                try:
                    # 使用FFmpeg转换AVI为MP4
                    ffmpeg_exe = os.path.join(os.path.dirname(__file__), '..', 'ffmpeg-8.0-full_build', 'bin', 'ffmpeg.exe')
                    ffmpeg_cmd = [
                        ffmpeg_exe, '-y', '-i', self.paths['video_output'],
                        '-vcodec', 'libx264', '-preset', 'fast',
                        '-crf', '23', self.paths['output']
                    ]
                    subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                    
                    if os.path.exists(self.paths['output']):
                        file_size = os.path.getsize(self.paths['output'])
                        print(f"输出文件: {self.paths['output']}, 大小: {file_size} 字节")
                    else:
                        print(f"错误：输出文件不存在: {self.paths['output']}")
                except Exception as e:
                    print(f"视频格式转换失败: {e}")
                
                # 计算检测时长
                endTime = time.time()
                allTime = f"{(endTime - startTime):.1f}秒"
                
                # 上传视频文件
                try:
                    uploadedUrl = self.upload(self.paths['output'])
                    if uploadedUrl:
                        self.data["outVideo"] = uploadedUrl
                        self.data["label"] = json.dumps(all_labels)
                        self.data["confidence"] = json.dumps(all_confidences)
                        self.data["allTime"] = allTime
                        
                        # 推送完整的检测结果
                        self.socketio.emit('video_complete', {
                            'url': uploadedUrl,
                            'label': all_labels,
                            'confidence': all_confidences,
                            'allTime': allTime,
                            'suggestion': self.data.get("suggestion", "")
                        })
                        print(f"✅ 视频检测完成！标签数: {len(all_labels)}, 置信度数: {len(all_confidences)}, 耗时: {allTime}")
                    else:
                        self.socketio.emit('message', {'data': '视频处理完成，但上传失败！'})
                except Exception as e:
                    print(f"视频上传异常: {e}")
                
                # 保存检测记录
                try:
                    self.save_data(json.dumps(self.data), 'http://localhost:9999/videoRecords')
                except Exception as e:
                    print(f"❌ 检测记录保存失败: {e}")
                    import traceback
                    traceback.print_exc()
                
                # 6. 清理临时文件
                try:
                    # 清理下载和临时 AVI 文件，保留最终输出的 MP4
                    self.cleanup_files([self.paths['download'], self.paths['video_output']])
                    print("✅ 临时文件清理完成")
                except Exception as e:
                    print(f"❌ 临时文件清理失败: {e}")
                
                print("="*50)
                print("后处理流程结束")
                print("="*50 + "\n")

        return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def predictCamera(self):
        """摄像头视频流处理接口"""
        self.data.clear()
        self.data.update({
            "username": request.args.get('username'), "weight": request.args.get('weight'),
            "conf": request.args.get('conf'), "startTime": request.args.get('startTime'),
            "ai": request.args.get('ai', '不使用AI')
        })
        self.socketio.emit('message', {'data': '正在加载，请稍等！'})
        model = YOLO(f'./weights/{self.data["weight"]}')
        
        # 使用FFmpegCamera类（使用FFmpeg捕获摄像头）
        ffmpeg_dir = os.path.join(os.path.dirname(__file__), '..', 'ffmpeg-8.0-full_build', 'bin')
        cap = FFmpegCamera(device_name=None, width=640, height=480, fps=20, ffmpeg_path=ffmpeg_dir)
        
        if not cap.isOpened():
            self.socketio.emit('message', {'data': '无法打开摄像头'})
            self.data["outVideo"] = ""
            self.save_data(json.dumps(self.data), 'http://localhost:9999/cameraRecords')
            return Response(b'', mimetype='multipart/x-mixed-replace; boundary=frame')
        
        os.makedirs(os.path.dirname(self.paths['camera_output']), exist_ok=True)
        video_writer = cv2.VideoWriter(self.paths['camera_output'], cv2.VideoWriter_fourcc(*'XVID'), 20, (640, 480))
        self.recording = True

        def generate():
            try:
                while self.recording:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    results = model.predict(source=frame, imgsz=640, conf=float(self.data['conf']), show=False)
                    processed_frame = results[0].plot()
                    
                    if self.recording and video_writer:
                        video_writer.write(processed_frame)
                    _, jpeg = cv2.imencode('.jpg', processed_frame)
                    yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n'
            finally:
                self.cleanup_resources(cap, video_writer)
                
                import time
                time.sleep(0.5)
                
                uploadedUrl = ""
                print(f"检查文件: {self.paths['camera_output']}")
                if os.path.exists(self.paths['camera_output']):
                    file_size = os.path.getsize(self.paths['camera_output'])
                    print(f"文件大小: {file_size} 字节")
                    
                    if file_size > 0:
                        self.socketio.emit('message', {'data': '正在保存视频...'})
                        try:
                            # 尝试转换为MP4
                            for progress in self.convert_avi_to_mp4(self.paths['camera_output']):
                                self.socketio.emit('progress', {'data': progress})
                            
                            # 如果转换成功，上传MP4文件
                            uploadedUrl = self.upload(self.paths['output'])
                            if uploadedUrl:
                                self.socketio.emit('video_complete', {'url': uploadedUrl})
                        except Exception as e:
                            print(f"❌ 视频转换失败: {e}")
                            # 如果转换失败，直接上传原始AVI文件
                            print("⚠️ 尝试直接上传原始AVI文件...")
                            uploadedUrl = self.upload(self.paths['camera_output'])
                            if uploadedUrl:
                                self.socketio.emit('video_complete', {'url': uploadedUrl})
                    else:
                        print("视频文件为空")
                else:
                    print("视频文件不存在")
                
                # 保存检测数据（仅保存基本信息）
                self.data["outVideo"] = uploadedUrl
                
                print(f"✅ 摄像头检测完成！视频已保存")
                self.save_data(json.dumps(self.data), 'http://localhost:9999/cameraRecords')
                self.cleanup_files([self.paths['output'], self.paths['camera_output']])

        return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def stopCamera(self):
        """停止摄像头预测"""
        self.recording = False
        return jsonify({"status": 200, "message": "预测成功", "code": 0})

    def process_list(self, input_list):
        # 去除重复元素并保持原顺序
        unique_list = []
        seen = set()
        for item in input_list:
            if item not in seen:
                seen.add(item)
                unique_list.append(item)

        # 判断是否需要删除'正常'
        if '正常' in unique_list and len(unique_list) > 1:
            unique_list = [item for item in unique_list if item != '正常']

        return unique_list

    def save_data(self, data, path):
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(path, data=data, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"记录保存失败，状态码: {response.status_code}")
        except requests.RequestException as e:
            print(f"上传记录时发生错误: {e}")

    def convert_avi_to_mp4(self, temp_output):
        """使用FFmpeg转换AVI为MP4"""
        if not os.path.exists(temp_output):
            yield 0
            return
        
        ffmpeg_exe = os.path.join(os.path.dirname(__file__), '..', 'ffmpeg-8.0-full_build', 'bin', 'ffmpeg.exe')
        ffmpeg_command = [
            ffmpeg_exe, '-y', '-i', temp_output,
            '-vcodec', 'libx264', '-preset', 'fast',
            '-crf', '23', self.paths['output']
        ]
        
        process = subprocess.Popen(
            ffmpeg_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        total_duration = self.get_video_duration(temp_output)

        for line in process.stderr:
            if "time=" in line:
                try:
                    time_str = line.split("time=")[1].split(" ")[0]
                    h, m, s = map(float, time_str.split(":"))
                    processed_time = h * 3600 + m * 60 + s
                    if total_duration > 0:
                        progress = (processed_time / total_duration) * 100
                        yield progress
                except:
                    pass

        return_code = process.wait()
        yield 100

    def get_video_duration(self, path):
        """获取视频总时长（秒）"""
        try:
            cap = cv2.VideoCapture(path)
            if not cap.isOpened():
                return 0
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            cap.release()
            return total_frames / fps if fps > 0 else 0
        except Exception:
            return 0

    def get_file_names(self, directory):
        """获取指定文件夹中的所有文件名"""
        try:
            return [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
        except Exception as e:
            print(f"发生错误: {e}")
            return []

    def upload(self, out_path):
        """上传处理后的图片或视频文件到远程服务器"""
        upload_url = "http://localhost:9999/files/upload"
        try:
            # 检查文件是否存在
            if not os.path.exists(out_path):
                print(f"❌ 错误：文件不存在，无法上传: {out_path}")
                return ""
            
            # 检查文件大小
            file_size = os.path.getsize(out_path)
            if file_size == 0:
                print(f"❌ 错误：文件大小为0，无法上传: {out_path}")
                return ""
            
            print(f"准备上传文件: {out_path}, 大小: {file_size} 字节")
            
            with open(out_path, 'rb') as file:
                files = {'file': (os.path.basename(out_path), file)}
                response = requests.post(upload_url, files=files, timeout=30)
                if response.status_code == 200:
                    uploaded_url = response.json()['data']
                    print(f"✅ 文件上传成功！URL: {uploaded_url}")
                    return uploaded_url
                else:
                    print(f"❌ 文件上传失败！状态码: {response.status_code}, 响应: {response.text}")
                    return ""
        except Exception as e:
            print(f"❌ 上传文件时发生错误: {str(e)}")
            import traceback
            traceback.print_exc()
            return ""

    def download(self, url, save_path):
        """下载文件并保存到指定路径"""
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        try:
            with requests.get(url, stream=True) as response:
                response.raise_for_status()
                with open(save_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
            print(f"文件已成功下载并保存到 {save_path}")
        except requests.RequestException as e:
            print(f"下载失败: {e}")

    def cleanup_files(self, file_paths):
        """清理文件"""
        for path in file_paths:
            if os.path.exists(path):
                os.remove(path)

    def cleanup_resources(self, cap, video_writer):
        """释放资源"""
        try:
            if cap and cap.isOpened():
                cap.release()
        except:
            pass
        try:
            if video_writer is not None:
                video_writer.release()
        except:
            pass
        try:
            cv2.destroyAllWindows()
        except:
            pass

    def test_think_mode(self):
        """测试思考模式参数传递接口"""
        data = request.get_json()
        print("测试接口接收到的完整请求数据:", data)
        print("测试接口原始thinkMode值:", data.get('thinkMode'), "类型:", type(data.get('thinkMode')))
        return jsonify({"status": "success", "received": data.get('thinkMode')})


# 启动应用
if __name__ == '__main__':
    video_app = VideoProcessingApp()
    video_app.run()
