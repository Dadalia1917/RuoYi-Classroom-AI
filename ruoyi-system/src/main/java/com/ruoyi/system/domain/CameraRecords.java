package com.ruoyi.system.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

/**
 * 摄像头检测记录实体
 * 
 * @author ruoyi
 */
@TableName("camerarecords")
public class CameraRecords {
    
    /** 主键ID */
    @TableId(type = IdType.AUTO)
    private Integer id;
    
    /** 模型权重 */
    private String weight;
    
    /** 输出视频 */
    private String outVideo;
    
    /** 置信度 */
    private String conf;
    
    /** 用户名 */
    private String username;
    
    /** 开始时间 */
    private String startTime;

    // Getter and Setter methods
    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getWeight() {
        return weight;
    }

    public void setWeight(String weight) {
        this.weight = weight;
    }

    public String getOutVideo() {
        return outVideo;
    }

    public void setOutVideo(String outVideo) {
        this.outVideo = outVideo;
    }

    public String getConf() {
        return conf;
    }

    public void setConf(String conf) {
        this.conf = conf;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getStartTime() {
        return startTime;
    }

    public void setStartTime(String startTime) {
        this.startTime = startTime;
    }
}

