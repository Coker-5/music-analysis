# 音乐榜单可视化平台 - 操作文档

## 📋 项目概述

**音乐榜单可视化平台**是一个基于音乐榜单数据的大屏可视化系统，用于展示腾讯音乐由你榜的历史数据和实时数据。系统采用前后端分离架构，支持多维度数据分析和可视化展示。

### 主要功能

- **大屏可视化展示**：基于 Vue 2 + ECharts 的实时数据大屏
- **历史数据分析**：2018-2025年歌手上榜演化趋势
- **实时榜单追踪**：每日自动抓取最新榜单数据
- **多维度统计**：歌手、歌曲、得分等多维度分析

### 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| 大屏前端 | Vue 2 + ECharts 4 + Highcharts 8 | ^2.6.11 |
| 管理后台前端 | Vue 3 + Fast-CRUD + Element Plus | ^3.3.4 |
| 大屏后端 | Django + MySQL | 4.2.20 |
| 管理后台后端 | Django + Django REST Framework | 4.2.20 |
| 爬虫 | Python + DrissionPage + APScheduler | 3.10+ |
| 数据库 | MySQL | 8.0+ |

---

## 🏗️ 系统架构

```
music-analysis/
├── 📁 frontend/                    # Vue 2 大屏前端项目
│   ├── src/
│   │   ├── views/                  # 页面组件
│   │   ├── components/             # 图表组件
│   │   └── api/                    # API 请求封装
│   └── public/
│
├── 📁 admin/                       # Vue 3 管理后台项目
│   ├── web/                        # 前端项目
│   │   ├── src/views/music/        # 音乐管理模块
│   │   │   ├── dailyChart/         # 日榜数据管理
│   │   │   ├── weeklyChart/        # 周榜数据管理
│   │   │   ├── singer/             # 歌手信息管理
│   │   │   ├── singerStat/         # 歌手统计管理
│   │   │   ├── songLongevity/      # 歌曲留榜时长管理
│   │   │   └── weekIssue/          # 周度期数管理
│   │   └── src/router/             # 路由配置
│   └── backend/                    # Django 后端项目
│       ├── apps/music/             # 音乐应用
│       │   ├── models.py           # 数据模型
│       │   ├── views.py            # API 视图
│       │   ├── serializers.py      # 序列化器
│       │   └── urls.py             # 路由配置
│       └── dvadmin/                # 基础框架
│
├── 📁 backend/                     # Django 大屏后端项目
│   └── music_backend/
│       ├── datashow/               # 数据展示应用
│       │   ├── db_query.py         # SQL 查询封装
│       │   ├── views.py            # API 视图
│       │   └── urls.py             # 路由配置
│       └── music_backend/          # 项目配置
│
├── 📁 crawler/                     # 数据爬虫模块
│   ├── spider.py                   # 爬虫核心
│   ├── cleaner.py                  # 数据清洗
│   ├── db.py                       # 数据库操作
│   ├── pipeline.py                 # 数据流水线
│   ├── scheduler.py                # 定时任务
│   └── main.py                     # 入口文件
│
├── 📁 docs/                        # 项目文档
│   ├── 前端改造文档.md
│   ├── 后端改造文档.md
│   └── 操作实现文档-爬虫.md
│
└── 📄 README.md                    # 本文档
```

---

## 💻 环境要求

### 基础环境

| 软件 | 版本要求 | 说明 |
|------|---------|------|
| Python | 3.10+ | 后端和爬虫运行环境 |
| Node.js | 14.x - 18.x | 前端构建环境 |
| MySQL | 8.0+ | 数据存储 |
| Chrome/Chromium | 最新版 | 爬虫浏览器驱动 |

### 硬件要求

- **最低配置**：4核CPU / 8GB内存 / 20GB磁盘
- **推荐配置**：8核CPU / 16GB内存 / 50GB磁盘

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/Coker-5/music-analysis.git
cd music-analysis
```

### 2. 数据库初始化

```bash
# 登录 MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE music_chart DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 执行建表脚本（详见 docs/操作实现文档-爬虫.md 第一步）
# 复制其中的 SQL 语句在 MySQL 中执行
```

### 3. 大屏后端启动

```bash
cd backend/music_backend

# 安装依赖
pip install -r requirements.txt

# 修改数据库配置
# 编辑 music_backend/settings.py，修改 DB_CONFIG 中的密码

# 执行迁移
python manage.py migrate

# 启动服务
python manage.py runserver 0.0.0.0:8000
```

服务启动后访问：http://localhost:8000/music/head/ 测试接口

### 4. 大屏前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run serve
```

访问 http://localhost:8080 查看大屏

### 5. 管理后台启动

#### 管理后台后端

```bash
cd admin/backend

# 安装依赖
pip install -r requirements.txt

# 修改数据库配置
# 编辑 application/settings.py，修改 DATABASES 配置

# 执行迁移
python manage.py migrate

# 初始化数据
python manage.py init

# 启动服务
python manage.py runserver 0.0.0.0:8001
```

#### 管理后台前端

```bash
cd admin/web

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问 http://localhost:8888 进入管理后台登录页面
- 默认账号：`admin`
- 默认密码：`admin123456`

### 5. 爬虫初始化（历史数据导入）

```bash
cd crawler

# 安装依赖
pip install pymysql apscheduler DrissionPage

# 修改配置文件
# 编辑 config.py，设置数据库密码

# 执行历史数据全量导入（仅需执行一次）
python main.py history
```

---

## 📖 详细配置

### 后端配置 (backend/music_backend/music_backend/settings.py)

```python
# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'music_chart',
        'USER': 'root',
        'PASSWORD': 'your_password',  # ← 修改为你的密码
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# CORS 配置（开发环境允许所有域名）
CORS_ALLOW_ALL_ORIGINS = True
```

### 前端配置 (frontend/src/api/request.js)

```javascript
const request = axios.create({
    baseURL: "http://localhost:8000",  // ← 修改为后端实际地址
    timeout: 8000,
})
```

### 爬虫配置 (crawler/config.py)

```python
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "your_password",   # ← 修改为你的密码
    "database": "music_chart",
    "charset": "utf8mb4",
}

# 定时任务配置（每天8:00执行）
DAILY_CRAWL_HOUR = 8
DAILY_CRAWL_MINUTE = 0
```

---

## 🎯 使用指南

### 日常运行流程

#### 1. 启动后端服务

```bash
cd backend/music_backend
python manage.py runserver 0.0.0.0:8000
```

#### 2. 启动前端服务

```bash
cd frontend
npm run serve
```

#### 3. 启动定时爬虫（生产环境）

```bash
cd crawler
python main.py schedule
```

爬虫会在每天 8:00 自动抓取最新榜单数据并入库。

### 手动触发日榜抓取

```bash
cd crawler
python main.py daily
```

### 大屏访问

- 开发环境：http://localhost:8080
- 局域网访问：http://<本机IP>:8080

---

## 📊 数据说明

### 数据库表结构

| 表名 | 类型 | 说明 |
|------|------|------|
| dim_singer | 维度表 | 歌手信息 |
| dim_week_issue | 维度表 | 周榜期数元数据 |
| fact_weekly_chart | 事实表 | 历史周榜明细（2018-2025） |
| fact_weekly_classify_index | 事实表 | 周榜五维分项指数 |
| fact_daily_chart | 事实表 | 日榜明细（每日更新） |
| agg_singer_yearly | 聚合表 | 歌手历年上榜统计 |
| agg_song_longevity | 聚合表 | 歌曲留榜生命力统计 |
| agg_singer_total | 聚合表 | 歌手全量上榜统计 |

### 大屏图表对应

| 区域 | 图表 | 数据源 | 接口 |
|------|------|--------|------|
| 左上1 | 歌手占比饼图 | agg_singer_total | /music/centerLeft1/ |
| 左上2 | 歌手词云图 | agg_singer_total | /music/centerLeft2/ |
| 中上 | 数字卡片+歌手排行 | fact_daily_chart | /music/head/ + /music/centerData/ |
| 中右1 | Top1三维指数 | fact_daily_chart | /music/centerRight1/ |
| 右上1 | 得分区间分布 | fact_daily_chart | /music/centerRight2/ |
| 右上2 | 长红歌曲排行 | agg_song_longevity | /music/centerRight2/ |
| 左下 | 今日实时榜单 | fact_daily_chart | /music/bottomLeft/ |
| 右下 | 历年演化3D柱状图 | agg_singer_yearly | /music/bottomRight/ |

---

## 🔌 API 接口文档

### 接口列表

| 接口 | 方法 | 说明 | 返回格式 |
|------|------|------|---------|
| /music/head/ | GET | 今日核心指标 | JSON对象 |
| /music/centerLeft1/ | GET | 歌手占比饼图数据 | JSON数组 |
| /music/centerLeft2/ | GET | 歌手词云数据 | JSON数组 |
| /music/centerData/ | GET | 歌手排行条形图 | JSON对象 |
| /music/centerRight1/ | GET | Top1三维指数 | JSON对象 |
| /music/centerRight2/ | GET | 得分分布+留榜排行 | JSON对象 |
| /music/bottomLeft/ | GET | 今日实时榜单 | JSON数组 |
| /music/bottomRight/ | GET | 历年演化数据 | JSON对象 |

### 接口示例

#### 获取今日核心指标

```bash
curl http://localhost:8000/music/head/
```

返回：
```json
{
  "chart_date": "2026-03-09",
  "champion_song": "吉量",
  "champion_singer": "周深",
  "champion_cover": "https://...",
  "avg_score": 77.35,
  "top10_new_count": 2,
  "max_incr_song": "某歌曲",
  "max_incr_value": 5
}
```

---

## 🛠️ 开发指南

### 前端开发

```bash
cd frontend

# 开发模式（热更新）
npm run serve

# 构建生产环境
npm run build

# 代码检查
npm run lint
```

### 后端开发

```bash
cd backend/music_backend

# 启动开发服务器
python manage.py runserver

# 创建超级用户
python manage.py createsuperuser

# 进入 Django shell
python manage.py shell
```

### 爬虫开发

```bash
cd crawler

# 运行历史数据导入
python main.py history

# 运行单日数据抓取
python main.py daily

# 启动定时调度
python main.py schedule
```

---

## 🐛 故障排除

### 常见问题

#### 1. 前端无法连接后端

**现象**：页面空白，浏览器控制台显示 CORS 错误

**解决**：
```python
# 在 backend/music_backend/settings.py 中添加
CORS_ALLOW_ALL_ORIGINS = True
```

#### 2. 数据库连接失败

**现象**：后端报错 `Can't connect to MySQL server`

**检查**：
```bash
# 1. 确认 MySQL 服务运行
mysql -u root -p

# 2. 确认数据库存在
SHOW DATABASES;

# 3. 确认用户权限
GRANT ALL PRIVILEGES ON music_chart.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

#### 3. 爬虫无法启动浏览器

**现象**：报错 `Chrome not found` 或浏览器启动失败

**解决**：
```bash
# 安装 Chromium 或配置 Chrome 路径
# 在 crawler/spider.py 中修改浏览器配置
```

#### 4. 缺少 @jiaminghi/data-view 依赖

**现象**：报错 `Module not found: Can't resolve '@jiaminghi/data-view'`

**解决**：
```bash
cd frontend
npm install @jiaminghi/data-view
```

#### 5. 历史数据导入失败

**现象**：执行 `python main.py history` 时报错

**检查**：
```bash
# 1. 确认 result_data.json 和 years_issue_data.json 在 crawler/statics/ 目录
ls crawler/statics/

# 2. 确认 MySQL 表结构已创建
USE music_chart;
SHOW TABLES;

# 3. 检查数据库编码
SHOW VARIABLES LIKE 'character_set%';
```

---

## 📁 项目文件说明

### 关键文件清单

| 文件路径 | 说明 |
|---------|------|
| frontend/src/views/index.vue | 大屏主页面 |
| frontend/src/api/request.js | API 请求配置 |
| backend/music_backend/settings.py | Django 配置 |
| backend/music_backend/urls.py | URL 路由 |
| backend/datashow/db_query.py | SQL 查询封装 |
| backend/datashow/views.py | API 视图 |
| crawler/config.py | 爬虫配置 |
| crawler/db.py | 数据库操作 |
| crawler/pipeline.py | 数据流水线 |
| crawler/scheduler.py | 定时任务 |

---

## 📝 更新日志

### v1.1.0 (2026-03-11)

- ✅ 新增管理后台模块（Vue 3 + Fast-CRUD）
- ✅ 修复音乐管理模块 Fast-CRUD 配置问题
- ✅ 支持日榜数据、周榜数据、歌手信息、歌手统计、歌曲留榜时长、周度期数管理
- ✅ 实现数据增删改查和搜索功能

### v1.0.0 (2026-03-09)

- ✅ 完成前端大屏改造（Vue 2 + ECharts）
- ✅ 完成后端 API 开发（Django + MySQL）
- ✅ 完成数据爬虫模块（DrissionPage）
- ✅ 完成历史数据全量导入
- ✅ 实现每日定时数据更新

---

## 🤝 贡献指南

### 提交代码

```bash
# 1. 创建新分支
git checkout -b feature/your-feature

# 2. 提交修改
git add .
git commit -m "feat: 你的修改说明"

# 3. 推送到远程
git push origin feature/your-feature

# 4. 创建 Pull Request
```

### 代码规范

- **前端**：遵循 Vue 官方风格指南
- **后端**：遵循 PEP 8 规范
- **提交信息**：使用 Conventional Commits 规范

---

## 📧 联系方式

如有问题或建议，请通过以下方式联系：

- **GitHub Issues**: [提交问题](https://github.com/Coker-5/music-analysis/issues)
- **Email**: your-email@example.com

---

## 📄 许可证

本项目基于 MIT 许可证开源。

---

**最后更新**: 2026-03-09
