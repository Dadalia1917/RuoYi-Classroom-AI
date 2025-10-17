package com.ruoyi.system.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 图片检测记录实体
 * 
 * @author ruoyi
 */
@TableName("imgrecords")
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
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

    public String getLable() {
        return label;
    }

    public void setLable(String lable) {
        this.label = lable;
    }
}

