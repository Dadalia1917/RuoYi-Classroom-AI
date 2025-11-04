package com.ruoyi.web.controller.classroom;

import com.alibaba.fastjson2.JSONObject;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.system.domain.ImgRecords;
import com.ruoyi.system.mapper.ImgRecordsMapper;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import jakarta.annotation.Resource;

/**
 * 预测控制器 - 与Flask服务交互
 * 
 * @author ruoyi
 */
@RestController
@RequestMapping("/flask")
public class PredictionController {
    
    @Resource
    private ImgRecordsMapper imgRecordsMapper;

    private final RestTemplate restTemplate = new RestTemplate();

    /**
     * 预测请求类
     */
    public static class PredictRequest {
        private String startTime;
        private String weight;
        private String username;
        private String inputImg;
        private String conf;
        private String ai;
        private String suggestion;
        private Boolean thinkMode;

        // Getters and Setters
        public String getStartTime() {
            return startTime;
        }

        public void setStartTime(String startTime) {
            this.startTime = startTime;
        }

        public String getWeight() {
            return weight;
        }

        public void setWeight(String weight) {
            this.weight = weight;
        }

        public String getUsername() {
            return username;
        }

        public void setUsername(String username) {
            this.username = username;
        }

        public String getInputImg() {
            return inputImg;
        }

        public void setInputImg(String inputImg) {
            this.inputImg = inputImg;
        }

        public String getConf() {
            return conf;
        }

        public void setConf(String conf) {
            this.conf = conf;
        }

        public String getAi() {
            return ai;
        }

        public void setAi(String ai) {
            this.ai = ai;
        }

        public String getSuggestion() {
            return suggestion;
        }

        public void setSuggestion(String suggestion) {
            this.suggestion = suggestion;
        }

        public Boolean getThinkMode() {
            return thinkMode;
        }

        public void setThinkMode(Boolean thinkMode) {
            this.thinkMode = thinkMode;
        }
    }

    /**
     * 图片预测接口
     */
    @PostMapping("/predict")
    public AjaxResult predict(@RequestBody PredictRequest request) {
        if (request == null || request.getInputImg() == null || request.getInputImg().isEmpty()) {
            return AjaxResult.error("未提供图片链接");
        }
        if (request.getWeight() == null || request.getWeight().isEmpty()) {
            return AjaxResult.error("未提供权重");
        }

        try {
            // 创建请求体
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<PredictRequest> requestEntity = new HttpEntity<>(request, headers);

            // 调用 Flask API
            String response = restTemplate.postForObject("http://localhost:5000/predictImg", requestEntity, String.class);
            System.out.println("Received response: " + response);
            
            JSONObject responses = JSONObject.parseObject(response);
            if (responses.get("status").equals(400)) {
                return AjaxResult.error((String) responses.get("message"));
            } else {
                ImgRecords imgRecords = new ImgRecords();
                imgRecords.setWeight(request.getWeight());
                imgRecords.setConf(request.getConf());
                imgRecords.setInputImg(request.getInputImg());
                imgRecords.setUsername(request.getUsername());
                imgRecords.setStartTime(request.getStartTime());
                imgRecords.setAi(request.getAi());
                imgRecords.setLabel(String.valueOf(responses.get("label")));
                imgRecords.setConfidence(String.valueOf(responses.get("confidence")));
                imgRecords.setAllTime(String.valueOf(responses.get("allTime")));
                imgRecords.setOutImg(String.valueOf(responses.get("outImg")));
                imgRecords.setSuggestion(String.valueOf(responses.get("suggestion")));
                imgRecordsMapper.insert(imgRecords);
                
                // 🔥 重要：确保Flask响应在 data 字段，而不是 msg 字段
                AjaxResult result = AjaxResult.success("检测成功");
                result.put("data", response);  // Flask的JSON字符串放在data字段
                return result;
            }
        } catch (Exception e) {
            return AjaxResult.error("Error: " + e.getMessage());
        }
    }

    /**
     * 获取模型文件列表
     */
    @GetMapping("/file_names")
    public AjaxResult getFileNames() {
        try {
            String response = restTemplate.getForObject("http://127.0.0.1:5000/file_names", String.class);
            System.out.println("Flask返回的原始数据: " + response);
            if (response == null || response.isEmpty()) {
                System.out.println("警告：Flask返回的数据为空！");
                return AjaxResult.error("Flask返回的数据为空");
            }
            // 明确指定将 response 作为 data 参数，而不是 msg 参数
            return AjaxResult.success("操作成功", response);
        } catch (Exception e) {
            System.out.println("获取模型列表失败: " + e.getMessage());
            e.printStackTrace();
            return AjaxResult.error("Error: " + e.getMessage());
        }
    }
    
    /**
     * 停止摄像头录制
     */
    @GetMapping("/stopCamera")
    public AjaxResult stopCamera() {
        try {
            System.out.println("收到停止摄像头录制请求");
            String flaskUrl = "http://127.0.0.1:5000/stopCamera";
            String response = restTemplate.getForObject(flaskUrl, String.class);
            System.out.println("Flask响应（停止摄像头）: " + response);
            
            return AjaxResult.success("操作成功");
        } catch (Exception e) {
            System.out.println("停止摄像头录制失败: " + e.getMessage());
            e.printStackTrace();
            return AjaxResult.error("停止录制失败: " + e.getMessage());
        }
    }
}

