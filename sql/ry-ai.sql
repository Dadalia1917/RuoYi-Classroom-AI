/*
 Navicat Premium Dump SQL

 Source Server         : 基于计算机图像检测与大模型反馈的课堂行为系统
 Source Server Type    : MySQL
 Source Server Version : 80039 (8.0.39)
 Source Host           : localhost:3306
 Source Schema         : ry-ai

 Target Server Type    : MySQL
 Target Server Version : 80039 (8.0.39)
 File Encoding         : 65001

 Date: 24/10/2025 14:12:00
 
 说明：
 - 本脚本包含完整的表结构定义
 - 所有表都包含AI检测所需的完整字段（label, confidence, ai, suggestion, allTime等）
 - 如果表已存在，请使用底部的ALTER TABLE语句逐条添加缺失字段
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- 课堂行为系统相关表
-- ----------------------------

/*
 表字段说明：
 
 1. camerarecords（摄像头检测记录表）
    - id: 主键自增
    - weight: 检测模型权重 (RT-DETR.pt, best.pt, yolov8n.pt等)
    - conf: 置信度阈值 (0.25, 0.5等)
    - username: 用户名
    - start_time: 开始检测时间
    - out_video: 输出视频URL
    - ai: AI大模型类型 (不使用AI, Deepseek, Qwen等)
    - suggestion: AI教学建议
    - label: 检测标签JSON数组 (["阅读","写字",...])
    - confidence: 置信度JSON数组 (["85.2%","92.3%",...])
    - all_time: 总耗时 (12.3秒)
 
 2. imgrecords（图像检测记录表）
    - 字段同上，input_img/out_img替代input_video/out_video
 
 3. videorecords（视频检测记录表）
    - 字段同camerarecords
*/

-- ----------------------------
-- Table structure for camerarecords
-- ----------------------------
DROP TABLE IF EXISTS `camerarecords`;
CREATE TABLE `camerarecords`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `weight` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '模型权重',
  `conf` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '置信度阈值',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户名',
  `start_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '开始时间',
  `out_video` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '输出视频',
  `ai` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'AI模型类型',
  `suggestion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT 'AI建议',
  `label` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '检测标签',
  `confidence` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '置信度详情',
  `all_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '总耗时',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '摄像头检测记录表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for imgrecords
-- ----------------------------
DROP TABLE IF EXISTS `imgrecords`;
CREATE TABLE `imgrecords`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `input_img` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '输入图片',
  `out_img` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '输出图片',
  `confidence` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '置信度详情',
  `all_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '总耗时',
  `conf` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '置信度阈值',
  `weight` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '模型权重',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户名',
  `start_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '开始时间',
  `label` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '检测标签',
  `ai` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'AI模型类型',
  `suggestion` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT 'AI建议',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '图片检测记录表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for videorecords
-- ----------------------------
DROP TABLE IF EXISTS `videorecords`;
CREATE TABLE `videorecords`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `input_video` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '输入视频',
  `out_video` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '输出视频',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户名',
  `start_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '开始时间',
  `conf` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '置信度阈值',
  `weight` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '模型权重',
  `ai` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'AI模型类型',
  `suggestion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT 'AI建议',
  `label` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '检测标签',
  `confidence` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '置信度详情',
  `all_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '总耗时',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '视频检测记录表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- 【升级脚本】如果表已存在，使用以下语句添加缺失字段
-- 注意：
-- 1. 如果是全新安装，直接使用上面的CREATE TABLE语句，无需执行下面的ALTER TABLE
-- 2. 如果是从旧版本升级，逐条执行以下语句
-- 3. 如果某条SQL报错"Duplicate column name"（字段已存在），忽略该错误，继续执行下一条
-- 4. 执行完成后，重启SpringBoot应用使MyBatis Plus重新扫描表结构
-- ----------------------------

-- 为 videorecords 表添加字段（如果已有该字段会报错，忽略即可）
-- ALTER TABLE `videorecords` ADD COLUMN `label` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '检测标签' AFTER `suggestion`;
-- ALTER TABLE `videorecords` ADD COLUMN `confidence` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '置信度详情' AFTER `label`;
-- ALTER TABLE `videorecords` ADD COLUMN `all_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '总耗时' AFTER `confidence`;

-- 为 camerarecords 表添加字段（如果已有该字段会报错，忽略即可）
-- ALTER TABLE `camerarecords` ADD COLUMN `ai` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'AI模型类型' AFTER `out_video`;
-- ALTER TABLE `camerarecords` ADD COLUMN `suggestion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT 'AI建议' AFTER `ai`;
-- ALTER TABLE `camerarecords` ADD COLUMN `label` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '检测标签' AFTER `suggestion`;
-- ALTER TABLE `camerarecords` ADD COLUMN `confidence` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '置信度详情' AFTER `label`;
-- ALTER TABLE `camerarecords` ADD COLUMN `all_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '总耗时' AFTER `confidence`;

-- 验证表结构（执行完ALTER TABLE后，运行以下命令检查）
-- DESC camerarecords;
-- DESC videorecords;
-- DESC imgrecords;

SET FOREIGN_KEY_CHECKS = 1;

