package com.ruoyi.framework.config;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.context.annotation.Configuration;

/**
 * MyBatis-Plus 配置类
 * 
 * @author ruoyi
 */
@Configuration
@MapperScan("com.ruoyi.**.mapper")
public class MyBatisPlusConfig
{
    // MyBatis-Plus 会自动加载所有继承 BaseMapper 的接口
    // 并提供通用的 CRUD 方法，无需编写 XML 配置
}

