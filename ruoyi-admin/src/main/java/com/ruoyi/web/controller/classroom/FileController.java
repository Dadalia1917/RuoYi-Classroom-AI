package com.ruoyi.web.controller.classroom;

import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.utils.StringUtils;
import com.ruoyi.common.utils.file.FileUtils;
import com.ruoyi.common.utils.uuid.IdUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import jakarta.servlet.http.HttpServletResponse;
import java.io.*;
import java.net.URLEncoder;
import java.nio.file.Files;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 文件上传控制器
 * 
 * @author ruoyi
 */
@RestController
@RequestMapping("/files")
public class FileController {
    
    @Value("${server.port}")
    private String port;

    @Value("${file.ip}")
    private String ip;

    /**
     * 上传接口
     */
    @PostMapping("/upload")
    public AjaxResult upload(MultipartFile file) throws IOException {
        try {
            if (file == null || file.isEmpty()) {
                return AjaxResult.error("上传文件不能为空");
            }
            
            String originalFilename = file.getOriginalFilename();
            System.out.println("收到文件上传请求: " + originalFilename);
            
            // 定义文件的唯一标识（前缀）
            String flag = IdUtils.fastSimpleUUID();
            String rootFilePath = System.getProperty("user.dir") + "/files/" + flag + "_" + originalFilename;
            File saveFile = new File(rootFilePath);
            
            // 确保目录存在
            if (!saveFile.getParentFile().exists()) {
                saveFile.getParentFile().mkdirs();
            }
            
            // 保存文件
            file.transferTo(saveFile);
            
            // 返回完整的 URL 地址，用于浏览器访问
            String fileUrl = "http://" + ip + ":" + port + "/files/" + flag + "_" + originalFilename;
            System.out.println("文件上传成功，URL: " + fileUrl);
            
            // 重要：明确指定将 fileUrl 放在 data 字段中
            AjaxResult result = AjaxResult.success();
            result.put("data", fileUrl);
            result.put("url", fileUrl);  // 同时也放在url字段，提高兼容性
            result.put("fileName", flag + "_" + originalFilename);
            return result;
        } catch (Exception e) {
            System.err.println("文件上传失败: " + e.getMessage());
            e.printStackTrace();
            return AjaxResult.error("文件上传失败: " + e.getMessage());
        }
    }

    /**
     * 富文本文件上传接口
     */
    @PostMapping("/editor/upload")
    public Map<String, Object> editorUpload(MultipartFile file) throws IOException {
        String originalFilename = file.getOriginalFilename();
        String flag = IdUtils.fastSimpleUUID();
        String rootFilePath = System.getProperty("user.dir") + "/files/" + flag + "_" + originalFilename;
        File saveFile = new File(rootFilePath);
        if (!saveFile.getParentFile().exists()) {
            saveFile.getParentFile().mkdirs();
        }
        file.transferTo(saveFile);
        
        String url = "http://" + ip + ":" + port + "/files/" + flag;
        Map<String, Object> json = new HashMap<>();
        json.put("errno", 0);
        Map<String, String> data = new HashMap<>();
        data.put("url", url);
        json.put("data", new Object[]{data});
        return json;
    }

    /**
     * 下载接口
     */
    @GetMapping("/{flag}")
    public void getFiles(@PathVariable String flag, HttpServletResponse response) {
        OutputStream os;
        String basePath = System.getProperty("user.dir") + "/files/";
        File baseDir = new File(basePath);
        if (!baseDir.exists()) {
            return;
        }
        
        File[] files = baseDir.listFiles();
        if (files == null) {
            return;
        }
        
        String fileName = "";
        for (File f : files) {
            if (f.getName().contains(flag)) {
                fileName = f.getName();
                break;
            }
        }
        
        try {
            if (StringUtils.isNotEmpty(fileName)) {
                response.addHeader("Content-Disposition", "attachment;filename=" + URLEncoder.encode(fileName, "UTF-8"));
                response.setContentType("application/octet-stream");
                byte[] bytes = Files.readAllBytes(new File(basePath + fileName).toPath());
                os = response.getOutputStream();
                os.write(bytes);
                os.flush();
                os.close();
            }
        } catch (Exception e) {
            System.out.println("文件下载失败");
        }
    }
}

