# 🎓 RuoYi-AI-Classroom

## 基于RuoYi框架的智能课堂行为分析系统

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Java](https://img.shields.io/badge/Java-25-orange.svg)](https://openjdk.java.net/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.5.6-brightgreen.svg)](https://spring.io/projects/spring-boot)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.5.13-4FC08D.svg)](https://vuejs.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![RuoYi](https://img.shields.io/badge/RuoYi-Vue3-red.svg)](http://ruoyi.vip/)

---

## 📋 目录

- [📖 项目简介](#-项目简介)
- [💻 技术栈](#-技术栈)
- [🏗️ 系统架构](#️-系统架构)
  - [📋 架构概览](#-架构概览)
  - [🔧 核心组件说明](#-核心组件说明)
  - [📁 项目目录结构](#-项目目录结构)
- [🔄 系统流程设计](#-系统流程设计)
  - [⏱️ 图片检测流程时序图](#️-图片检测流程时序图)
  - [📊 数据流图](#-数据流图)
- [🗄️ 数据模型设计](#️-数据模型设计)
  - [📊 实体关系图](#-实体关系图)
- [🚀 部署架构](#-部署架构)
  - [🖥️ 部署架构图](#️-部署架构图)
  - [🌐 网络拓扑说明](#-网络拓扑说明)
- [🚀 快速开始](#-快速开始)
- [🎯 主要功能](#-主要功能)
- [🔑 默认账号](#-默认账号)
- [📡 API接口](#-api接口)
- [🔧 配置说明](#-配置说明)
- [🐛 常见问题](#-常见问题)
- [🎨 界面预览](#-界面预览)
- [🚀 部署建议](#-部署建议)
- [📝 更新日志](#-更新日志)
- [🤝 贡献指南](#-贡献指南)
- [🙏 致谢](#-致谢)

---

## 📖 项目简介

> **本项目是基于原"计算机图像检测与大模型反馈的课堂行为系统"深度改装而来**，完整集成了 **RuoYi-Vue3** 前后端分离框架，升级至 **Spring Boot 3.5.6** 和 **Vue 3** 最新版本。

系统结合 **计算机视觉（YOLO/RT-DETR）** 与 **大语言模型（Deepseek/通义千问）**，在 RuoYi 企业级框架基础上，实现课堂行为自动识别、智能分析与反馈。

### 🌟 核心特性

- 🏢 **企业级RuoYi框架**：完善的权限管理、菜单配置、系统监控
- 🤖 **AI智能检测**：YOLO/RT-DETR目标检测 + 大模型智能分析
- 🎯 **前后端分离**：Spring Boot 3.5.6 + Vue 3 + Element Plus
- 📊 **数据可视化**：ECharts实时展示学生行为统计
- 🔐 **安全认证**：Spring Security + JWT + Redis
- 📹 **多模态检测**：图片、视频、实时摄像头三种检测方式

### ✨ 项目亮点

| 特性 | 说明 |
|------|------|
| 🎯 高精度检测 | 基于YOLOv8和RT-DETR先进算法，识别9种课堂行为，准确率高 |
| 🧠 智能AI分析 | 集成DeepSeek、通义千问等大模型，提供专业教学建议 |
| ⚡ 实时处理 | WebSocket实时推送检测进度，毫秒级响应 |
| 🔧 灵活部署 | 支持云端API、本地LM-Studio、局域网三种AI部署方式 |
| 📊 可视化报告 | 直观的检测结果展示，支持PDF报告导出 |
| 🚀 现代技术栈 | Spring Boot 3.5.6 + Vue 3.5.13，性能卓越 |
| 🎨 美观界面 | Element Plus现代化UI，交互流畅 |
| 🔐 企业级安全 | Spring Security + JWT双重认证，数据安全可靠 |

---

## 💻 技术栈

### 后端技术

| 技术 | 版本 | 说明 |
|------|------|------|
| Spring Boot | 3.5.6 | 核心框架 |
| Spring Security | 6.5.5 | 安全框架 |
| MyBatis-Plus | 3.5.9 | ORM框架 |
| MySQL | 8.0+ | 关系型数据库 |
| Redis | Latest | 缓存 |
| Druid | 1.2.23 | 数据库连接池 |
| JWT | 0.9.1 | Token认证 |
| Quartz | 2.5.0 | 定时任务 |
| Flask | 3.1.0 | AI推理服务 |

### 前端技术

| 技术 | 版本 | 说明 |
|------|------|------|
| Vue.js | 3.5.13 | 渐进式框架 |
| Element Plus | Latest | UI组件库 |
| Vite | Latest | 构建工具 |
| Axios | 1.7.9 | HTTP客户端 |
| Pinia | Latest | 状态管理 |
| ECharts | Latest | 数据可视化 |
| Socket.IO | Latest | 实时通信 |

### AI推理

| 技术 | 版本 | 说明 |
|------|------|------|
| Ultralytics | 8.3.53 | YOLO框架 |
| OpenCV | 4.10.0 | 计算机视觉 |
| FFmpeg | 8.0 | 视频处理 |
| Flask-SocketIO | 5.4.1 | WebSocket |

---

## 🏗️ 系统架构

### 📋 架构概览

本项目采用现代化的微服务架构设计，基于RuoYi-Vue3框架，集成AI检测与大模型分析能力。

```mermaid
graph TD
    %% 前端层
    subgraph Frontend["🖥️ 前端层 (Vue 3.5.13)"]
        direction TB
        UI[用户界面]
        
        subgraph RuoYiPages["RuoYi系统页面"]
            UserMgmt[用户管理]
            RoleMgmt[角色管理]
            MenuMgmt[菜单管理]
            SysMon[系统监控]
        end
        
        subgraph AIPages["AI检测页面"]
            DataOverview[数据总览]
            ImgPage[图片检测]
            VideoPage[视频检测]
            CameraPage[摄像头检测]
            RecordPages[检测记录管理]
        end
        
        UI --- RuoYiPages
        UI --- AIPages
    end

    %% 业务逻辑层
    subgraph Backend["⚙️ 业务逻辑层 (Spring Boot 3.5.6)"]
        direction TB
        
        subgraph Security["安全框架"]
            SpringSec[Spring Security 6.5.5]
            JWT[JWT Token认证]
            Redis[Redis缓存]
        end
        
        subgraph Controllers["控制器层"]
            UserController[用户控制器]
            PredController[检测控制器]
            FileController[文件控制器]
            RecordControllers[记录控制器]
        end
        
        subgraph Services["服务层"]
            UserService[用户服务]
            FileService[文件服务]
            RecordService[记录服务]
            CacheService[缓存服务]
        end
        
        subgraph Mappers["数据访问层"]
            MyBatisPlus[MyBatis-Plus 3.5.9]
            UserMapper[用户Mapper]
            ImgMapper[图片记录Mapper]
            VideoMapper[视频记录Mapper]
            CameraMapper[摄像头记录Mapper]
        end
        
        Security --- Controllers
        Controllers --- Services
        Services --- Mappers
    end

    %% AI推理层
    subgraph AILayer["🤖 AI推理层 (Flask 3.1.0)"]
        direction TB
        FlaskApp[Flask应用]
        SocketIO[SocketIO实时通信]
        
        subgraph ModelEngine["模型引擎"]
            YOLOModel[YOLO v8模型]
            DETRModel[RT-DETR模型]
            ImagePredictor[图片预测器]
            VideoProcessor[视频处理器]
            CameraHandler[摄像头处理器]
        end
        
        subgraph AIAssistant["AI助手服务"]
            ChatAPI[ChatAPI]
            DeepSeek[DeepSeek API]
            Qwen[通义千问 API]
            LocalModels[本地LM-Studio]
            LANModels[局域网AI服务]
        end
        
        FlaskApp --- SocketIO
        FlaskApp --- ModelEngine
        FlaskApp --- AIAssistant
    end

    %% 数据存储层
    subgraph Storage["💾 数据存储层"]
        direction TB
        MySQL[(MySQL 8.0+ 数据库)]
        FileStorage[(文件存储系统)]
        RedisCache[(Redis缓存)]
        
        subgraph Tables["核心数据表"]
            SysUser[sys_user 用户表]
            SysRole[sys_role 角色表]
            SysMenu[sys_menu 菜单表]
            ImgTable[img_records 图片记录]
            VideoTable[video_records 视频记录]
            CameraTable[camera_records 摄像记录]
        end
        
        MySQL --- Tables
    end

    %% 外部服务
    subgraph External["🌐 外部服务"]
        direction TB
        OnlineAI[在线AI服务<br/>DeepSeek/Qwen]
        LMStudio[本地LM-Studio<br/>端口:1234]
        LANAI[局域网AI服务]
        FFmpeg[FFmpeg 8.0<br/>视频处理]
    end

    %% 连接关系
    Frontend -.->|REST API| Backend
    Backend -.->|HTTP转发| AILayer
    Backend -.->|JDBC| Storage
    Backend -.->|Token验证| Redis
    AILayer -.->|API调用| External
    AILayer -.->|文件读写| Storage
    
    %% 样式
    classDef frontendStyle fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef backendStyle fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef aiStyle fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef storageStyle fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef externalStyle fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    
    class Frontend,UI,RuoYiPages,AIPages,UserMgmt,RoleMgmt,MenuMgmt,SysMon,DataOverview,ImgPage,VideoPage,CameraPage,RecordPages frontendStyle
    class Backend,Security,Controllers,Services,Mappers,SpringSec,JWT,Redis,UserController,PredController,FileController,RecordControllers,UserService,FileService,RecordService,CacheService,MyBatisPlus,UserMapper,ImgMapper,VideoMapper,CameraMapper backendStyle
    class AILayer,FlaskApp,SocketIO,ModelEngine,AIAssistant,YOLOModel,DETRModel,ImagePredictor,VideoProcessor,CameraHandler,ChatAPI,DeepSeek,Qwen,LocalModels,LANModels aiStyle
    class Storage,MySQL,FileStorage,RedisCache,Tables,SysUser,SysRole,SysMenu,ImgTable,VideoTable,CameraTable storageStyle
    class External,OnlineAI,LMStudio,LANAI,FFmpeg externalStyle
```

### 🔧 核心组件说明

1. **🖥️ 前端层 (Vue 3 + Element Plus)**
   - **RuoYi系统页面**：完整的权限管理、用户管理、系统监控等企业级功能
   - **AI检测页面**：图片/视频/摄像头检测、数据可视化、检测记录管理

2. **⚙️ 业务逻辑层 (Spring Boot 3.5.6)**
   - **安全框架**：Spring Security + JWT + Redis实现完整的认证授权体系
   - **分层架构**：Controller → Service → Mapper 清晰的三层架构
   - **MyBatis-Plus**：简化数据库操作，提供强大的CRUD能力

3. **🤖 AI推理层 (Flask + PyTorch)**
   - **模型引擎**：支持YOLO v8和RT-DETR两种检测模型
   - **AI助手**：集成多种大语言模型提供智能分析
   - **实时通信**：SocketIO支持实时检测进度推送

4. **💾 数据存储层**
   - **MySQL**：存储用户数据、检测记录、系统配置
   - **Redis**：缓存用户会话、Token、频繁访问数据
   - **文件存储**：保存上传的图片、视频及检测结果

### 📁 项目目录结构

```
RuoYi-Vue3-springboot3/
├── ruoyi-admin/          # Spring Boot主应用
├── ruoyi-system/         # 系统核心模块
├── ruoyi-common/         # 公共工具类
├── ruoyi-framework/      # 框架核心（Security配置）
├── ruoyi-quartz/         # 定时任务模块
├── ruoyi-generator/      # 代码生成器
├── ruoyi-flask/          # Flask AI推理服务
│   ├── main(DETR).py     # RT-DETR检测服务
│   ├── main(YOLO).py     # YOLO检测服务
│   ├── utils/            # 工具类（chatApi.py等）
│   └── weights/          # 模型权重文件
├── ruoyi-ui/             # Vue3前端项目
│   ├── src/
│   │   ├── views/ai/     # AI检测页面
│   │   │   ├── data-overview/     # 数据总览
│   │   │   ├── img-predict/       # 图片检测
│   │   │   ├── video-predict/     # 视频检测
│   │   │   ├── camera-predict/    # 摄像头检测
│   │   │   ├── img-records/       # 图片记录
│   │   │   ├── video-records/     # 视频记录
│   │   │   └── camera-records/    # 摄像记录
│   │   └── ...
│   └── package.json
├── sql/                  # 数据库脚本
│   ├── ry_20250522.sql   # RuoYi基础表结构
│   ├── quartz.sql        # Quartz定时任务表
│   └── ai-detection-menus.sql  # AI检测菜单和权限
├── ffmpeg-8.0-full_build/  # FFmpeg工具（视频处理）
└── pom.xml               # Maven父项目配置
```

---

## 🔄 系统流程设计

### ⏱️ 图片检测流程时序图

```mermaid
sequenceDiagram
    participant U as 🧑‍🏫 教师用户
    participant V as 💻 Vue前端
    participant S as ⚙️ Spring Boot
    participant R as 🔴 Redis
    participant F as 🤖 Flask AI服务
    participant Y as 🎯 YOLO/DETR模型
    participant A as 🧠 AI助手
    participant D as 💾 MySQL数据库
    participant FS as 📁 文件存储
    
    %% 用户登录认证
    Note over U,R: 🔐 用户认证阶段
    U->>V: 1. 输入账号密码登录
    V->>S: 2. POST /login
    S->>D: 3. 验证用户信息
    D-->>S: 4. 返回用户数据
    S->>R: 5. 生成并缓存JWT Token
    S-->>V: 6. 返回Token和用户信息
    V-->>U: 7. 登录成功，跳转主页
    
    %% 图片上传阶段
    Note over U,FS: 📤 图片上传阶段
    U->>V: 8. 选择并上传图片文件
    V->>S: 9. POST /uploadFile (带Token)
    S->>R: 10. 验证Token有效性
    S->>FS: 11. 保存图片到文件系统
    FS-->>S: 12. 返回图片访问URL
    S-->>V: 13. 返回上传成功信息
    
    %% 配置参数阶段
    Note over U,V: ⚙️ 参数配置阶段
    U->>V: 14. 选择检测模型(YOLO/DETR)
    U->>V: 15. 设置置信度阈值
    U->>V: 16. 选择AI助手类型
    U->>V: 17. 启用思考模式(可选)
    
    %% 检测请求阶段
    Note over U,A: 🔍 AI检测阶段
    U->>V: 18. 点击开始检测
    V->>S: 19. POST /predict (带Token)
    S->>R: 20. 验证Token
    S->>F: 21. 转发请求到Flask
    F->>Y: 22. 加载模型并预测
    Y-->>F: 23. 返回检测结果<br/>(标签、置信度、坐标)
    
    F->>FS: 24. 保存标注图片
    FS-->>F: 25. 返回图片URL
    
    %% AI分析阶段
    Note over F,A: 🧠 AI智能分析阶段
    alt 用户选择了AI助手
        F->>A: 26. 发送检测结果请求分析
        Note right of F: 根据选择调用对应AI服务<br/>DeepSeek/Qwen/本地/局域网
        A-->>F: 27. 返回教学建议和分析
    end
    
    %% 数据保存阶段
    Note over S,D: 💾 数据持久化阶段
    F-->>S: 28. 返回完整结果
    S->>D: 29. 保存检测记录到数据库
    D-->>S: 30. 确认保存成功
    S->>R: 31. 更新统计缓存
    
    %% 结果展示阶段
    Note over U,V: 📊 结果展示阶段
    S-->>V: 32. 返回处理结果
    V-->>U: 33. 展示原图和标注图对比
    V-->>U: 34. 显示检测标签和置信度
    V-->>U: 35. 展示AI教学建议
    
    %% 可选导出阶段
    Note over U,V: 📄 报告导出(可选)
    U->>V: 36. 导出检测报告
    V-->>U: 37. 生成并下载PDF报告
```

### 📊 数据流图

```mermaid
graph LR
    %% 输入层
    subgraph Input["📥 数据输入层"]
        direction TB
        A[📷 图片/视频上传]
        B[🎯 模型选择<br/>YOLO/RT-DETR]
        C[⚙️ 置信度设置<br/>0.0-1.0]
        D[🤖 AI助手选择<br/>Deepseek/Qwen等]
        E[🧠 思考模式开关]
        F[🔑 用户认证Token]
    end
    
    %% 处理层
    subgraph Process["⚡ 数据处理层"]
        direction TB
        G[🔐 Token验证]
        H[🔄 图片预处理<br/>格式转换/尺寸调整]
        I[🎯 模型推理<br/>目标检测]
        J[📊 结果后处理<br/>NMS/阈值过滤]
        K[🧠 AI建议生成<br/>LLM分析]
        L[🎨 结果可视化<br/>边框绘制]
    end
    
    %% 存储层
    subgraph Storage["💾 数据存储层"]
        direction TB
        M[📁 原始文件存储]
        N[🖼️ 处理结果存储]
        O[📋 检测记录入库<br/>MySQL]
        P[💭 AI建议存储]
        Q[🔴 缓存统计数据<br/>Redis]
    end
    
    %% 输出层
    subgraph Output["📤 结果输出层"]
        direction TB
        R[🏷️ 检测标签列表]
        S[📈 置信度分数]
        T[🖼️ 标注图片URL]
        U[💡 AI教学建议]
        V[📄 检测报告]
        W[📊 统计图表数据]
    end
    
    %% 数据流连接
    F --> G
    A --> H
    B --> I
    C --> I
    D --> K
    E --> K
    
    G --> H
    H --> I
    I --> J
    J --> L
    J --> K
    
    A --> M
    J --> N
    I --> O
    K --> P
    O --> Q
    
    J --> R
    J --> S
    L --> T
    K --> U
    R --> V
    S --> V
    T --> V
    U --> V
    O --> W
    
    %% 样式定义
    classDef inputStyle fill:#e3f2fd,stroke:#1976d2,stroke-width:2px,color:#000
    classDef processStyle fill:#e8f5e8,stroke:#388e3c,stroke-width:2px,color:#000
    classDef storageStyle fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#000
    classDef outputStyle fill:#fff3e0,stroke:#f57c00,stroke-width:2px,color:#000
    
    class A,B,C,D,E,F inputStyle
    class G,H,I,J,K,L processStyle
    class M,N,O,P,Q storageStyle
    class R,S,T,U,V,W outputStyle
```

---

## 🗄️ 数据模型设计

### 📊 实体关系图

```mermaid
classDiagram
    %% RuoYi核心实体
    class SysUser {
        +Long userId
        +String userName
        +String nickName
        +String email
        +String phonenumber
        +String sex
        +String avatar
        +String password
        +String status
        +Date createTime
        +Date updateTime
    }
    
    class SysRole {
        +Long roleId
        +String roleName
        +String roleKey
        +String status
        +Integer roleSort
        +Date createTime
    }
    
    class SysMenu {
        +Long menuId
        +String menuName
        +String parentId
        +String path
        +String component
        +String perms
        +String icon
        +Integer orderNum
    }
    
    %% AI检测记录实体
    class ImgRecords {
        +Long id
        +String weight
        +String inputImg
        +String outImg
        +String confidence
        +String allTime
        +String conf
        +String label
        +String username
        +Date startTime
        +String ai
        +String suggestion
        +Date createTime
    }
    
    class VideoRecords {
        +Long id
        +String weight
        +String inputVideo
        +String outVideo
        +String conf
        +String username
        +Date startTime
        +String ai
        +String suggestion
        +Date createTime
    }
    
    class CameraRecords {
        +Long id
        +String weight
        +String outVideo
        +String conf
        +String username
        +Date startTime
        +Date createTime
    }
    
    %% 控制器类
    class PredictionController {
        -ImgRecordsMapper imgRecordsMapper
        -RestTemplate restTemplate
        +predict() AjaxResult
        +getFileNames() AjaxResult
    }
    
    class SysLoginController {
        -SysLoginService loginService
        +login() AjaxResult
        +getInfo() AjaxResult
        +logout() AjaxResult
    }
    
    %% 服务类
    class FlaskAIService {
        -Flask app
        -SocketIO socketio
        +predictImg() Dict
        +predictVideo() Response
        +predictCamera() Response
        +stopCamera() String
    }
    
    class ChatAPIService {
        -OpenAI deepseek_client
        -String qwen_headers
        +deepseek_request() String
        +qwen_request() String
        +local_request() String
        +lan_request() String
    }
    
    %% 请求DTO
    class PredictRequest {
        +Date startTime
        +String weight
        +String username
        +String inputImg
        +String conf
        +String ai
        +Boolean thinkMode
    }
    
    %% 关系定义
    SysUser "1" --> "*" SysRole : has
    SysUser "1" --> "*" SysMenu : access
    
    SysUser "1" --> "*" ImgRecords : creates
    SysUser "1" --> "*" VideoRecords : creates
    SysUser "1" --> "*" CameraRecords : creates
    
    PredictionController --> PredictRequest : uses
    PredictionController --> ImgRecords : manages
    PredictionController --> FlaskAIService : calls
    
    SysLoginController --> SysUser : authenticates
    
    FlaskAIService --> ChatAPIService : uses
    FlaskAIService --> ImgRecords : saves
    FlaskAIService --> VideoRecords : saves
    FlaskAIService --> CameraRecords : saves
```

---

## 🚀 部署架构

### 🖥️ 部署架构图

```mermaid
graph TB
    %% 客户端层
    subgraph Client["👥 客户端层"]
        direction LR
        WebBrowser[🌐 Web浏览器<br/>Chrome/Firefox/Edge]
        MobileBrowser[📱 移动端浏览器<br/>响应式设计]
    end
    
    %% 负载均衡层
    subgraph LoadBalancer["⚖️ 负载均衡层 (可选)"]
        Nginx[🔄 Nginx反向代理<br/>端口: 80/443<br/>SSL证书配置]
    end
    
    %% 应用服务层
    subgraph AppServer["🖥️ 应用服务层"]
        direction TB
        
        subgraph Frontend["🎨 前端服务"]
            Vue[Vue 3.5.13<br/>📦 Node.js 18+<br/>🔗 端口: 8081]
        end
        
        subgraph Backend["⚙️ 后端服务"]
            SpringBoot[Spring Boot 3.5.6<br/>☕ JDK 21<br/>🔗 端口: 9999]
        end
        
        subgraph AIService["🤖 AI推理服务"]
            Flask[Flask 3.1.0<br/>🐍 Python 3.8+<br/>🔗 端口: 5000]
            YOLO[🎯 YOLO/DETR引擎<br/>🔥 PyTorch + CUDA]
        end
    end
    
    %% AI模型服务层
    subgraph ModelService["🧠 AI模型服务层"]
        direction TB
        
        subgraph Local["💻 本地服务"]
            LMStudio[🏠 LM-Studio<br/>🔗 端口: 1234<br/>支持多种开源模型]
        end
        
        subgraph Cloud["☁️ 云端服务"]
            DeepSeek[🌊 DeepSeek API<br/>🔑 API Key认证<br/>DeepSeek-R1模型]
            Qwen[🔮 通义千问 API<br/>🔑 API Key认证<br/>Qwen系列模型]
        end
        
        subgraph LAN["🏢 局域网服务"]
            LANModels[🌐 局域网AI服务<br/>🔗 192.168.x.x:1234<br/>私有部署大模型]
        end
    end
    
    %% 数据存储层
    subgraph DataLayer["💾 数据存储层"]
        direction TB
        MySQL[🗄️ MySQL 8.0+<br/>🔗 端口: 3306<br/>📊 用户/角色/检测记录]
        Redis[🔴 Redis 6.0+<br/>🔗 端口: 6379<br/>⚡ Token/缓存/会话]
        FileStorage[📁 文件存储系统<br/>🖼️ 图片/视频文件<br/>📦 检测结果文件]
    end
    
    %% 外部工具层
    subgraph Tools["🛠️ 外部工具层"]
        FFmpeg[🎬 FFmpeg 8.0<br/>📹 视频格式转换<br/>🎥 摄像头捕获]
        CUDA[⚡ CUDA Runtime<br/>🚀 GPU加速计算<br/>🎯 模型推理加速]
    end
    
    %% 监控与日志
    subgraph Monitor["📊 监控与日志 (可选)"]
        direction LR
        Actuator[Spring Boot Actuator<br/>系统健康检查]
        Logback[Logback日志系统<br/>日志收集分析]
    end
    
    %% 连接关系
    Client -.->|HTTPS/HTTP| LoadBalancer
    LoadBalancer -.->|反向代理| Frontend
    LoadBalancer -.->|API转发| Backend
    
    Frontend -.->|REST API<br/>Axios请求| Backend
    Backend -.->|HTTP转发<br/>检测请求| AIService
    Backend -.->|JDBC<br/>数据操作| MySQL
    Backend -.->|Jedis<br/>缓存操作| Redis
    
    AIService -.->|HTTP请求<br/>AI分析| ModelService
    AIService -.->|文件读写| FileStorage
    AIService -.->|调用| Tools
    
    Backend -.->|监控数据| Monitor
    
    %% 样式定义
    classDef clientStyle fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef proxyStyle fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef appStyle fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef modelStyle fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef dataStyle fill:#fff8e1,stroke:#f9a825,stroke-width:2px
    classDef toolStyle fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef monitorStyle fill:#e0f2f1,stroke:#00897b,stroke-width:2px
    
    class WebBrowser,MobileBrowser clientStyle
    class Nginx proxyStyle
    class Vue,SpringBoot,Flask,YOLO appStyle
    class LMStudio,DeepSeek,Qwen,LANModels modelStyle
    class MySQL,Redis,FileStorage dataStyle
    class FFmpeg,CUDA toolStyle
    class Actuator,Logback monitorStyle
```

### 🌐 网络拓扑说明

1. **客户端访问**：用户通过浏览器访问系统（可选配置Nginx进行负载均衡和SSL加密）
2. **前后端分离**：Vue前端（8081端口）与Spring Boot后端（9999端口）独立部署
3. **AI服务独立**：Flask AI服务（5000端口）作为独立微服务运行
4. **数据库集群**：MySQL存储持久化数据，Redis提供高速缓存
5. **AI模型灵活部署**：支持云端API、本地LM-Studio、局域网私有部署三种方式
6. **监控体系**：Spring Boot Actuator提供健康检查，Logback记录系统日志

---

## 🚀 快速开始

### 📋 环境要求

| 软件 | 版本 | 必需 |
|------|------|------|
| JDK | 21+ | ✅ |
| Node.js | 18+ | ✅ |
| Python | 3.8+ | ✅ |
| MySQL | 8.0+ | ✅ |
| Redis | 6.0+ | ✅ |
| Maven | 3.6+ | ✅ |

### 1️⃣ 数据库初始化

```sql
-- 1. 创建数据库
CREATE DATABASE ry_vue CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2. 导入RuoYi基础表结构（约24张表）
source sql/ry_20250522.sql;

-- 3. 导入Quartz定时任务表
source sql/quartz.sql;

-- 4. 初始化AI检测菜单和权限
source sql/ai-detection-menus.sql;
```

### 2️⃣ 后端配置

修改 `ruoyi-admin/src/main/resources/application-druid.yml`：

```yaml
spring:
  datasource:
    druid:
      master:
        url: jdbc:mysql://localhost:3306/ry_vue?useUnicode=true&characterEncoding=utf8&zeroDateTimeBehavior=convertToNull&useSSL=true&serverTimezone=GMT%2B8
        username: root        # 修改数据库用户名
        password: password    # 修改数据库密码
```

修改 `application.yml`（Redis配置）：

```yaml
spring:
  data:
    redis:
      host: localhost
      port: 6379
      password:              # Redis密码（如有）
      database: 0
```

### 3️⃣ IntelliJ IDEA 配置（重要）

如果使用 **IntelliJ IDEA** 开发，请按以下步骤配置（解决 JDK 25 编译问题）：

1. 打开 `File` → `Settings`（或按 `Ctrl + Alt + S`）
2. 导航到：`Build, Execution, Deployment` → `Build Tools` → `Maven` → `Runner`
3. 勾选 ✅ **`Delegate IDE build/run actions to Maven`**（将 IDE 构建/运行操作委托给 Maven）
4. 点击 `Apply` 和 `OK`
5. 重新构建项目：`Build` → `Rebuild Project`

> 💡 **说明**：此配置让 IDEA 使用 Maven 进行编译，而不是自带的编译器。Maven 会自动应用 `pom.xml` 中配置的 JDK 25 兼容性参数，避免编译错误。

### 4️⃣ 启动后端服务

```bash
# 编译整个项目
mvn clean install

# 启动主应用
cd ruoyi-admin
mvn spring-boot:run

# 或在 IDEA 中直接运行 RuoYiApplication.java
```

访问：http://localhost:9999

### 5️⃣ Python环境配置

```bash
# 创建虚拟环境（推荐）
conda create -n yolo python=3.8
conda activate yolo

# 安装依赖
cd ruoyi-flask
pip install flask flask-socketio flask-cors
pip install ultralytics opencv-python numpy
pip install requests openai python-dotenv
```

### 6️⃣ 启动Flask AI服务

```bash
cd ruoyi-flask

# 启动RT-DETR服务
python main(DETR).py

# 或启动YOLO服务（二选一）
python main(YOLO).py
```

访问：http://localhost:5000

### 7️⃣ 前端配置与启动

```bash
cd ruoyi-ui

# 安装依赖
npm install
# 或 yarn install
# 或 pnpm install

# 启动开发服务器
npm run dev

# 生产环境打包
npm run build:prod
```

访问：http://localhost:8081

---

## 🎯 主要功能

### 📊 数据总览（新增）
- 学生行为统计图（柱状图）
- 用户使用率分析（饼图）
- 近期检测情况（表格）

### 🖼️ AI检测模块
- **图片检测**：单张图片上传检测
- **视频检测**：视频文件批量处理
- **摄像头检测**：实时流媒体处理

### 📝 检测记录管理
- **图片记录**：查看、修改、删除、导出
- **视频记录**：在线播放、记录管理
- **摄像记录**：完整录制过程管理
- **批量操作**：支持批量删除

### 🛠️ RuoYi系统功能
- 用户管理、角色管理、菜单管理
- 部门管理、岗位管理、字典管理
- 参数设置、通知公告、日志管理
- 定时任务、系统监控、代码生成

### 🤖 AI助手支持
- **Deepseek**：在线API / 本地部署 / 局域网部署
- **通义千问（Qwen）**：在线API / 本地qwen3-4b / 局域网部署
- **本地LLM**：支持LM-Studio等本地大模型

### 🎓 课堂行为识别（9种）
| 行为 | 标签 |
|------|------|
| 写作 | Writing |
| 阅读 | Reading |
| 听讲 | Listening |
| 睡觉 | Sleeping |
| 讨论 | Discussing |
| 举手 | Raising_hand |
| 低头 | Bowing |
| 玩手机 | Phone |
| 站立 | Stand |

---

## 🔑 默认账号

| 账号 | 密码 | 角色 |
|------|------|------|
| admin | admin123 | 超级管理员 |
| ry | admin123 | 普通用户 |

---

## 📡 API接口

### 后端API（Spring Boot）
- **文件上传**：`POST /uploadFile`
- **预测转发**：`POST /predict`
- **图片记录**：`/imgRecords/*`
- **视频记录**：`/videoRecords/*`
- **摄像记录**：`/cameraRecords/*`

### Flask AI API
- **图片检测**：`POST /predictImg`
- **视频检测**：`POST /predictVideo`
- **摄像头检测**：`GET /predictCamera`
- **停止录制**：`GET /stopCamera`
- **模型列表**：`GET /file_names`

### Swagger文档
访问：http://localhost:9999/doc.html

---

## 🔧 配置说明

### AI模型配置

在 `ruoyi-flask/utils/chatApi.py` 中配置：

```python
# Deepseek API Key
DEEPSEEK_API_KEY = "your_deepseek_api_key"

# 通义千问 API Key  
QWEN_API_KEY = "your_qwen_api_key"

# 本地LM-Studio地址
LOCAL_API_BASE = "http://localhost:1234/v1"

# 局域网服务器地址
LAN_API_BASE = "http://192.168.1.100:1234/v1"
```

### 模型权重文件

将YOLO/RT-DETR模型文件（`.pt`）放到 `ruoyi-flask/weights/` 目录：

```
weights/
└── RT-DETR.pt    # 推荐使用RT-DETR
```

### FFmpeg路径

项目已内置FFmpeg（相对路径）：
```
RuoYi-Vue3-springboot3/ffmpeg-8.0-full_build/bin/ffmpeg.exe
```

---

## 🐛 常见问题

### Q: IntelliJ IDEA 编译失败，提示 `java.lang.ExceptionInInitializerError`？
**A:** 这是因为 IDEA 使用自带编译器无法正确处理 JDK 25。请按以下步骤解决：
1. 打开 `Settings` → `Build Tools` → `Maven` → `Runner`
2. 勾选 ✅ `Delegate IDE build/run actions to Maven`
3. 重新构建项目

或者，在 `Settings` → `Compiler` → `Java Compiler` → `Additional command line parameters` 中添加：
```
--add-exports=jdk.compiler/com.sun.tools.javac.api=ALL-UNNAMED --add-exports=jdk.compiler/com.sun.tools.javac.file=ALL-UNNAMED --add-exports=jdk.compiler/com.sun.tools.javac.main=ALL-UNNAMED --add-exports=jdk.compiler/com.sun.tools.javac.model=ALL-UNNAMED --add-exports=jdk.compiler/com.sun.tools.javac.parser=ALL-UNNAMED --add-exports=jdk.compiler/com.sun.tools.javac.processing=ALL-UNNAMED --add-exports=jdk.compiler/com.sun.tools.javac.tree=ALL-UNNAMED --add-exports=jdk.compiler/com.sun.tools.javac.util=ALL-UNNAMED --add-opens=jdk.compiler/com.sun.tools.javac.code=ALL-UNNAMED --add-opens=jdk.compiler/com.sun.tools.javac.comp=ALL-UNNAMED
```

### Q: 摄像头无法打开？
**A:** 本项目使用FFmpeg直接捕获摄像头，解决了OpenCV在Windows 11上的兼容性问题。系统会自动检测可用摄像头。

### Q: 视频转换失败？
**A:** 确保FFmpeg路径正确，项目已内置FFmpeg，使用相对路径自动查找。

### Q: AI超时？
**A:** 已将前端超时时间设置为5分钟（300秒），如仍超时，请检查：
- AI服务是否启动（Flask）
- API Key是否配置正确
- 网络连接是否正常

### Q: 检测结果显示乱码？
**A:** 已修复Unicode转义字符问题，刷新页面即可正确显示中文标签。

### Q: 批量删除失败？
**A:** 已修复批量删除功能，后端支持逗号分隔的ID列表。

---

## 🎨 界面预览

### 数据总览
- 学生行为柱状图（今日统计）
- 用户使用饼图
- 近期检测记录表格

### AI检测
- 实时显示检测进度
- 可视化检测结果
- AI智能建议

### 检测记录
- 表格展示所有记录
- 详情弹窗查看
- 批量操作支持

---

## 🚀 部署建议

### 开发环境
- 后端：IDEA 直接运行 `RuoYiApplication`
- Flask：命令行运行 `python main(DETR).py`
- 前端：`npm run dev`

### 生产环境
- 后端：`mvn clean package` 打包为jar，`java -jar` 运行
- Flask：使用 `gunicorn` 或 `uwsgi` 部署
- 前端：`npm run build:prod` 打包，使用Nginx部署

### Nginx配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态资源
    location / {
        root /path/to/ruoyi-ui/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端API
    location /prod-api/ {
        proxy_pass http://localhost:9999/;
    }

    # Flask AI服务
    location /flask/ {
        proxy_pass http://localhost:5000/;
    }
}
```

---

## 📝 更新日志

### v2.0.0 (2025-10-17) - RuoYi集成版

#### 🎉 重大更新
- ✅ 完整集成RuoYi-Vue3框架
- ✅ 升级Spring Boot至3.5.6
- ✅ 升级Vue至3最新版
- ✅ 新增数据总览可视化页面
- ✅ 优化检测记录管理
- ✅ FFmpeg摄像头方案
- ✅ 统一视频处理流程

#### 🔧 技术改进
- MyBatis-Plus替代MyBatis
- Spring Security + JWT认证
- Redis缓存优化
- Druid数据库监控

#### 🐛 Bug修复
- 修复检测结果Unicode显示问题
- 修复摄像头无法打开问题
- 修复视频转换失败问题
- 修复批量删除功能
- 修复AI超时问题

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 开发规范
- 遵循Java/Python/JavaScript编码规范
- 提交信息清晰描述更改内容
- 重要功能请更新文档
- 确保新功能通过测试


## 🙏 致谢

感谢以下开源项目：

- [RuoYi-Vue3](http://ruoyi.vip/) - 若依管理系统
- [Spring Boot](https://spring.io/) - 企业级框架
- [Vue.js](https://vuejs.org/) - 前端框架
- [Ultralytics](https://ultralytics.com/) - YOLO模型
- [Deepseek](https://www.deepseek.com/) - 大语言模型
- [通义千问](https://tongyi.aliyun.com/) - 大语言模型


<div align="center">

**如果这个项目对你有帮助，请给个⭐Star支持一下！**

Made with ❤️ by RuoYi-AI-Classroom Team

</div>
