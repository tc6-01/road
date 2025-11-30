# 项目文件结构说明

```
road/
│
├── .github/                          # GitHub配置
│   └── workflows/                    # GitHub Actions工作流
│       ├── auto-deploy.yml          # 自动部署工作流
│       ├── extract-video.yml        # 视频提取工作流
│       └── README.md                # 工作流说明文档
│
├── .vscode/                          # VSCode编辑器配置
│   └── settings.json                # 编辑器设置
│
├── backend/                          # Python后端脚本
│   ├── extractor.py                 # 核心提取脚本（主要文件）
│   ├── requirements.txt             # Python依赖列表
│   └── README.md                    # 后端使用文档
│
├── data/                             # 数据存储目录
│   ├── places.json                  # 地点数据文件（核心数据）
│   └── places.example.json          # 示例数据文件
│
├── frontend/                         # Vue.js前端应用
│   ├── public/                      # 静态资源目录
│   │   └── images/                  # 图片存储（封面图片）
│   │       └── .gitkeep
│   │
│   ├── src/                         # 源代码目录
│   │   ├── components/              # Vue组件
│   │   │   ├── MapView.vue         # 地图展示组件
│   │   │   ├── PlaceList.vue       # 地点列表组件
│   │   │   └── PlaceDetail.vue     # 地点详情组件
│   │   │
│   │   ├── App.vue                  # 根组件
│   │   ├── main.js                  # 入口文件
│   │   └── style.css                # 全局样式
│   │
│   ├── index.html                   # HTML模板
│   ├── package.json                 # Node.js项目配置
│   ├── vite.config.js              # Vite构建配置
│   ├── tailwind.config.js          # Tailwind CSS配置
│   ├── postcss.config.js           # PostCSS配置
│   └── README.md                    # 前端开发文档
│
├── scripts/                          # 辅助脚本
│   ├── setup.sh                     # 一键初始化脚本
│   └── add-place.sh                 # 批量添加脚本
│
├── .gitignore                        # Git忽略配置
├── vercel.json                       # Vercel部署配置
├── netlify.toml                      # Netlify部署配置
│
├── README.md                         # 主项目文档（完整说明）
├── QUICKSTART.md                     # 快速开始指南
├── PROJECT_SUMMARY.md                # 项目实施总结
├── STRUCTURE.md                      # 本文件 - 结构说明
└── LICENSE                           # MIT开源许可证
```

## 核心文件说明

### 后端相关

#### `backend/extractor.py` ⭐
**最重要的脚本文件**
- 从抖音视频提取信息
- 调用AI分析地点和美食
- 获取地理坐标
- 下载封面图片
- 保存到JSON文件

#### `backend/requirements.txt`
Python依赖包列表：
- `requests`: HTTP请求库
- `python-dotenv`: 环境变量管理
- `openai`: DeepSeek API调用
- `Pillow`: 图片处理

### 前端相关

#### `frontend/src/App.vue` ⭐
**主应用组件**
- 管理整体布局
- 协调各个子组件
- 加载数据
- 处理状态

#### `frontend/src/components/MapView.vue` ⭐
**地图组件**
- 集成高德地图
- 渲染地点标记
- 处理地图交互

#### `frontend/src/components/PlaceList.vue`
**列表组件**
- 显示地点列表
- 搜索和筛选
- 统计信息

#### `frontend/src/components/PlaceDetail.vue`
**详情组件**
- 弹窗展示详情
- 美食列表
- 导航功能

#### `frontend/vite.config.js`
**构建配置**
- Vite构建设置
- 自动复制数据文件
- 路径别名配置

### 数据相关

#### `data/places.json` ⭐
**核心数据文件**
- 存储所有地点信息
- JSON格式
- 易于编辑和版本控制

#### `frontend/public/images/`
**图片存储目录**
- 存储视频封面图
- 提取脚本自动下载
- Web访问路径: `/images/xxx.jpg`

### 部署相关

#### `vercel.json`
Vercel部署配置：
- 构建命令
- 输出目录
- 路由规则

#### `netlify.toml`
Netlify部署配置：
- 构建设置
- 发布目录
- 重定向规则

#### `.github/workflows/auto-deploy.yml`
自动部署工作流：
- 监听文件变更
- 自动构建
- 部署到托管平台

#### `.github/workflows/extract-video.yml`
视频提取工作流：
- 手动触发
- 在线运行脚本
- 自动提交数据

### 文档相关

#### `README.md` ⭐
**主文档**
- 完整的项目介绍
- 安装和使用说明
- API密钥获取指南
- 常见问题解答

#### `QUICKSTART.md`
**快速上手**
- 5分钟快速开始
- 简化的步骤说明
- 常用命令参考

#### `PROJECT_SUMMARY.md`
**项目总结**
- 功能完成度
- 技术架构
- 扩展建议

## 工作流程图

```
1. 开发者操作
   ↓
   运行 extractor.py --url "视频链接"
   ↓
2. 数据提取
   ↓
   保存到 data/places.json
   ↓
3. Git操作
   ↓
   git add . && git commit && git push
   ↓
4. GitHub Actions
   ↓
   触发 auto-deploy.yml
   ↓
5. 构建部署
   ↓
   前端构建 (npm run build)
   ↓
   复制 data/places.json 到 dist/
   ↓
   部署到 Vercel/Netlify
   ↓
6. 用户访问
   ↓
   浏览器加载网站
   ↓
   读取 /data/places.json
   ↓
   在地图上展示
```

## 数据流向

```
抖音视频
   ↓
[Python脚本提取]
   ↓
AI分析 + 高德API
   ↓
data/places.json ← 手动编辑也可以
   ↓
[Vite构建]
   ↓
dist/data/places.json
   ↓
[前端应用]
   ↓
Vue组件读取
   ↓
地图展示
```

## 开发vs生产

### 开发环境
- 前端: `npm run dev` (localhost:3000)
- 数据: 读取 `../data/places.json`
- 图片: `public/images/`

### 生产环境
- 前端: 静态文件在 `dist/`
- 数据: `dist/data/places.json`
- 图片: `dist/images/`
- 托管: Vercel/Netlify

## 关键技术点

### Python脚本
- **异步API调用**: requests库
- **AI集成**: OpenAI兼容接口
- **地理编码**: 高德地图Geocoding API
- **错误处理**: try-except + 降级机制

### Vue前端
- **响应式**: Composition API
- **状态管理**: ref + computed
- **组件通信**: props + emit
- **生命周期**: onMounted

### 地图集成
- **API加载**: script标签 + window.AMap
- **标记渲染**: AMap.Marker + 自定义HTML
- **事件处理**: marker.on('click')
- **视野调整**: map.setFitView()

### 样式方案
- **工具类**: Tailwind CSS
- **组件样式**: scoped style
- **响应式**: @media queries
- **动画**: transition + transform

## 最佳实践

### 代码组织
- ✅ 单一职责原则（每个组件专注一件事）
- ✅ 组件化开发（可复用的小组件）
- ✅ 配置分离（环境变量独立）

### 数据管理
- ✅ 版本控制（Git跟踪数据变更）
- ✅ 备份策略（示例文件作为参考）
- ✅ 数据验证（JSON格式检查）

### 部署策略
- ✅ 自动化CI/CD（GitHub Actions）
- ✅ 零停机部署（静态站点）
- ✅ 环境变量分离（敏感信息保护）

## 扩展指南

### 添加新功能
1. 修改数据结构（`data/places.json`）
2. 更新提取脚本（`backend/extractor.py`）
3. 修改前端组件（`frontend/src/components/`）
4. 更新文档（`README.md`）

### 更换服务
- **地图服务**: 修改 `MapView.vue`
- **AI服务**: 修改 `extractor.py` 中的API调用
- **托管平台**: 添加新的部署配置文件

### 自定义样式
- **主题色**: 修改 `tailwind.config.js`
- **组件样式**: 修改各组件的 `<style>` 部分
- **全局样式**: 修改 `src/style.css`

