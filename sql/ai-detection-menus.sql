-- ----------------------------
-- AI检测菜单SQL脚本
-- 基于计算机图像检测与大模型反馈的课堂行为系统
-- ----------------------------

-- 先删除已存在的AI检测相关菜单（如果存在）
DELETE FROM sys_role_menu WHERE menu_id >= 1500 AND menu_id <= 2999;
DELETE FROM sys_menu WHERE menu_id >= 1500 AND menu_id <= 2999;

-- 数据总览菜单（一级菜单，order_num=1）
INSERT INTO sys_menu VALUES(1500, '数据总览', '0', '1', 'data-overview', 'ai/data-overview/index', '', '', 1, 0, 'C', '0', '0', 'ai:data:overview', 'chart', 'admin', sysdate(), '', null, '数据总览页面');

-- AI检测主菜单（一级菜单，order_num=2）
INSERT INTO sys_menu VALUES(2000, 'AI检测', '0', '2', 'ai-detection', null, '', '', 1, 0, 'M', '0', '0', '', 'robot', 'admin', sysdate(), '', null, 'AI检测目录');

-- AI检测子菜单
INSERT INTO sys_menu VALUES(2001, '图像检测', '2000', '1', 'img-predict', 'ai/img-predict/index', '', '', 1, 0, 'C', '0', '0', 'ai:img:predict', 'camera', 'admin', sysdate(), '', null, '图像检测菜单');
INSERT INTO sys_menu VALUES(2002, '视频检测', '2000', '2', 'video-predict', 'ai/video-predict/index', '', '', 1, 0, 'C', '0', '0', 'ai:video:predict', 'video', 'admin', sysdate(), '', null, '视频检测菜单');
INSERT INTO sys_menu VALUES(2003, '摄像检测', '2000', '3', 'camera-predict', 'ai/camera-predict/index', '', '', 1, 0, 'C', '0', '0', 'ai:camera:predict', 'camera-live', 'admin', sysdate(), '', null, '摄像检测菜单');

-- 检测记录主菜单（一级菜单，order_num=3）
INSERT INTO sys_menu VALUES(2010, '检测记录', '0', '3', 'detection-records', null, '', '', 1, 0, 'M', '0', '0', '', 'list', 'admin', sysdate(), '', null, '检测记录目录');

-- 检测记录子菜单
INSERT INTO sys_menu VALUES(2011, '图片记录', '2010', '1', 'img-records', 'ai/img-records/index', '', '', 1, 0, 'C', '0', '0', 'ai:imgRecords:list', 'picture', 'admin', sysdate(), '', null, '图片记录菜单');
INSERT INTO sys_menu VALUES(2012, '视频记录', '2010', '2', 'video-records', 'ai/video-records/index', '', '', 1, 0, 'C', '0', '0', 'ai:videoRecords:list', 'video-record', 'admin', sysdate(), '', null, '视频记录菜单');
INSERT INTO sys_menu VALUES(2013, '摄像记录', '2010', '3', 'camera-records', 'ai/camera-records/index', '', '', 1, 0, 'C', '0', '0', 'ai:cameraRecords:list', 'camera-live', 'admin', sysdate(), '', null, '摄像记录菜单');

-- 图片记录管理按钮
INSERT INTO sys_menu VALUES(2101, '图片记录查询', '2011', '1', '', '', '', '', 1, 0, 'F', '0', '0', 'ai:imgRecords:query', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu VALUES(2102, '图片记录新增', '2011', '2', '', '', '', '', 1, 0, 'F', '0', '0', 'ai:imgRecords:add', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu VALUES(2103, '图片记录修改', '2011', '3', '', '', '', '', 1, 0, 'F', '0', '0', 'ai:imgRecords:edit', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu VALUES(2104, '图片记录删除', '2011', '4', '', '', '', '', 1, 0, 'F', '0', '0', 'ai:imgRecords:remove', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu VALUES(2105, '图片记录导出', '2011', '5', '', '', '', '', 1, 0, 'F', '0', '0', 'ai:imgRecords:export', '#', 'admin', sysdate(), '', null, '');

-- 视频记录管理按钮  
INSERT INTO sys_menu VALUES(2111, '视频记录查询', '2012', '1', '', '', '', '', 1, 0, 'F', '0', '0', 'ai:videoRecords:query', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu VALUES(2112, '视频记录新增', '2012', '2', '', '', '', '', 1, 0, 'F', '0', '0', 'ai:videoRecords:add', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu VALUES(2113, '视频记录修改', '2012', '3', '', '', '', '', 1, 0, 'F', '0', '0', 'ai:videoRecords:edit', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu VALUES(2114, '视频记录删除', '2012', '4', '', '', '', '', 1, 0, 'F', '0', '0', 'ai:videoRecords:remove', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu VALUES(2115, '视频记录导出', '2012', '5', '', '', '', '', 1, 0, 'F', '0', '0', 'ai:videoRecords:export', '#', 'admin', sysdate(), '', null, '');

-- 摄像记录管理按钮
INSERT INTO sys_menu VALUES(2121, '摄像记录查询', '2013', '1', '', '', '', '', 1, 0, 'F', '0', '0', 'ai:cameraRecords:query', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu VALUES(2122, '摄像记录新增', '2013', '2', '', '', '', '', 1, 0, 'F', '0', '0', 'ai:cameraRecords:add', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu VALUES(2123, '摄像记录修改', '2013', '3', '', '', '', '', 1, 0, 'F', '0', '0', 'ai:cameraRecords:edit', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu VALUES(2124, '摄像记录删除', '2013', '4', '', '', '', '', 1, 0, 'F', '0', '0', 'ai:cameraRecords:remove', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu VALUES(2125, '摄像记录导出', '2013', '5', '', '', '', '', 1, 0, 'F', '0', '0', 'ai:cameraRecords:export', '#', 'admin', sysdate(), '', null, '');

-- 更新系统管理等菜单的order_num
-- 首页(0) -> 数据总览(1) -> AI检测(2) -> 检测记录(3) -> 系统管理(4) -> 系统监控(5) -> 系统工具(6) -> 若依官网(7)
UPDATE sys_menu SET order_num = 4 WHERE menu_id = 1 AND menu_name = '系统管理';
UPDATE sys_menu SET order_num = 5 WHERE menu_id = 2 AND menu_name = '系统监控';  
UPDATE sys_menu SET order_num = 6 WHERE menu_id = 3 AND menu_name = '系统工具';
UPDATE sys_menu SET order_num = 7 WHERE menu_id = 4 AND menu_name = '若依官网';

-- 为超级管理员分配数据总览、AI检测和检测记录菜单权限
INSERT INTO sys_role_menu VALUES ('1', '1500');
INSERT INTO sys_role_menu VALUES ('1', '2000');
INSERT INTO sys_role_menu VALUES ('1', '2001');
INSERT INTO sys_role_menu VALUES ('1', '2002');
INSERT INTO sys_role_menu VALUES ('1', '2003');
INSERT INTO sys_role_menu VALUES ('1', '2010');
INSERT INTO sys_role_menu VALUES ('1', '2011');
INSERT INTO sys_role_menu VALUES ('1', '2012');
INSERT INTO sys_role_menu VALUES ('1', '2013');
INSERT INTO sys_role_menu VALUES ('1', '2101');
INSERT INTO sys_role_menu VALUES ('1', '2102');
INSERT INTO sys_role_menu VALUES ('1', '2103');
INSERT INTO sys_role_menu VALUES ('1', '2104');
INSERT INTO sys_role_menu VALUES ('1', '2105');
INSERT INTO sys_role_menu VALUES ('1', '2111');
INSERT INTO sys_role_menu VALUES ('1', '2112');
INSERT INTO sys_role_menu VALUES ('1', '2113');
INSERT INTO sys_role_menu VALUES ('1', '2114');
INSERT INTO sys_role_menu VALUES ('1', '2115');
INSERT INTO sys_role_menu VALUES ('1', '2121');
INSERT INTO sys_role_menu VALUES ('1', '2122');
INSERT INTO sys_role_menu VALUES ('1', '2123');
INSERT INTO sys_role_menu VALUES ('1', '2124');
INSERT INTO sys_role_menu VALUES ('1', '2125');

-- 为普通角色分配数据总览、AI检测菜单权限
INSERT INTO sys_role_menu VALUES ('2', '1500');
INSERT INTO sys_role_menu VALUES ('2', '2000');
INSERT INTO sys_role_menu VALUES ('2', '2001');
INSERT INTO sys_role_menu VALUES ('2', '2002');
INSERT INTO sys_role_menu VALUES ('2', '2003');
INSERT INTO sys_role_menu VALUES ('2', '2010');
INSERT INTO sys_role_menu VALUES ('2', '2011');
INSERT INTO sys_role_menu VALUES ('2', '2012');
INSERT INTO sys_role_menu VALUES ('2', '2013');
INSERT INTO sys_role_menu VALUES ('2', '2101');
INSERT INTO sys_role_menu VALUES ('2', '2102');
INSERT INTO sys_role_menu VALUES ('2', '2103');
INSERT INTO sys_role_menu VALUES ('2', '2104');
INSERT INTO sys_role_menu VALUES ('2', '2105');
INSERT INTO sys_role_menu VALUES ('2', '2111');
INSERT INTO sys_role_menu VALUES ('2', '2112');
INSERT INTO sys_role_menu VALUES ('2', '2113');
INSERT INTO sys_role_menu VALUES ('2', '2114');
INSERT INTO sys_role_menu VALUES ('2', '2115');
INSERT INTO sys_role_menu VALUES ('2', '2121');
INSERT INTO sys_role_menu VALUES ('2', '2122');
INSERT INTO sys_role_menu VALUES ('2', '2123');
INSERT INTO sys_role_menu VALUES ('2', '2124');
INSERT INTO sys_role_menu VALUES ('2', '2125');
