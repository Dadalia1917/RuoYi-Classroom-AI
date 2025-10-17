package com.ruoyi.system.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 视频检测记录实体
 * 
 * @author ruoyi
 */
@TableName("videorecords")
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
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
}

