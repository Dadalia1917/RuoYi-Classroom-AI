package com.ruoyi.system.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

/**
 * 图片检测记录实体
 * 
 * @author ruoyi
 */
@TableName("imgrecords")
public class ImgRecords {
    
    /** 主键ID */
    @TableId(type = IdType.AUTO)
    private Integer id;
    
    /** 模型权重 */
    private String weight;
    
    /** 输入图片 */
    private String inputImg;
    
    /** 输出图片 */
    private String outImg;
    
    /** 置信度详情 */
    private String confidence;
    
    /** 总耗时 */
    private String allTime;
    
    /** 置信度阈值 */
    private String conf;
    
    /** 检测标签 */
    private String label;
    
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

    public String getInputImg() {
        return inputImg;
    }

    public void setInputImg(String inputImg) {
        this.inputImg = inputImg;
    }

    public String getOutImg() {
        return outImg;
    }

    public void setOutImg(String outImg) {
        this.outImg = outImg;
    }

    public String getConfidence() {
        return confidence;
    }

    public void setConfidence(String confidence) {
        this.confidence = confidence;
    }

    public String getAllTime() {
        return allTime;
    }

    public void setAllTime(String allTime) {
        this.allTime = allTime;
    }

    public String getConf() {
        return conf;
    }

    public void setConf(String conf) {
        this.conf = conf;
    }

    public String getLabel() {
        return label;
    }

    public void setLabel(String label) {
        this.label = label;
    }

    public String getLable() {
        return label;
    }

    public void setLable(String lable) {
        this.label = lable;
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

