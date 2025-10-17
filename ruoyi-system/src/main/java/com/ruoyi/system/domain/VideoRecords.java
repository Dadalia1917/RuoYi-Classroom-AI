package com.ruoyi.system.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

/**
 * 视频检测记录实体
 * 
 * @author ruoyi
 */
@TableName("videorecords")
public class VideoRecords {
    
    /** 主键ID */
    @TableId(type = IdType.AUTO)
    private Integer id;
    
    /** 模型权重 */
    private String weight;
    
    /** 输入视频 */
    private String inputVideo;
    
    /** 输出视频 */
    private String outVideo;
    
    /** 置信度 */
    private String conf;
    
    /** 用户名 */
    private String username;
    
    /** 开始时间 */
    private String startTime;
    
    /** AI模型类型 */
    private String ai;
    
    /** AI建议 */
    private String suggestion;

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

    public String getInputVideo() {
        return inputVideo;
    }

    public void setInputVideo(String inputVideo) {
        this.inputVideo = inputVideo;
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
}

