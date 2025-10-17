package com.ruoyi.system.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 摄像头检测记录实体
 * 
 * @author ruoyi
 */
@TableName("camerarecords")
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
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
}

