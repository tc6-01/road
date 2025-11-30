# 美食地点记录系统 🗺️🍴

一个温馨的项目，用于记录和展示想要一起去的美食地点。通过Python脚本从抖音视频中提取地点和美食信息，在Vue.js静态网站上用高德地图展示。

## ✨ 功能特点

- 🤖 **智能提取**: 使用AI大模型自动从抖音视频中提取地点和美食信息
- 🗺️ **地图展示**: 在高德地图上可视化展示所有标记的地点
- 📱 **响应式设计**: 完美支持PC端和移动端访问
- 🎨 **精美界面**: 使用Tailwind CSS打造现代化UI
- 🚀 **自动部署**: 数据更新后自动触发网站重新部署
- 💾 **简单存储**: 数据存储在JSON文件，易于管理和备份

## 📁 项目结构

```
road/
├── backend/                  # Python脚本
│   ├── extractor.py         # 抖音内容提取脚本
│   ├── requirements.txt     # Python依赖
│   └── README.md           # 脚本使用文档
├── frontend/                # Vue.js网站
│   ├── src/
│   │   ├── components/     # Vue组件
│   │   ├── App.vue         # 主应用
│   │   └── main.js
│   ├── public/
│   │   └── images/         # 缩略图存储
│   ├── package.json
│   └── vite.config.js
├── data/
│   └── places.json         # 地点数据
├── .github/
│   └── workflows/          # 自动化工作流
├── vercel.json             # Vercel部署配置
└── netlify.toml            # Netlify部署配置
```

## 🚀 快速开始

### 1. 安装Python依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 安装前端依赖

```bash
cd frontend
npm install
```

### 3. 配置API密钥

创建 `.env` 文件（参考 `.env.example`），填入你的API密钥：

```env
# 必需: 高德地图API
AMAP_WEB_SERVICE_KEY=你的高德地图Web服务API密钥
VITE_AMAP_KEY=你的高德地图JavaScript API密钥

# 推荐: AI大模型API
DEEPSEEK_API_KEY=你的DeepSeek API密钥

# 可选: 抖音内容获取
TIKHUB_API_KEY=你的TikHub API密钥
```

### 4. 运行前端开发服务器

```bash
cd frontend
npm run dev
```

访问 http://localhost:3000 查看网站。

## 📖 使用指南

### 添加新地点

#### 方式一: 本地运行脚本

```bash
cd backend
python extractor.py --url "抖音视频链接"
```

脚本会自动：
1. 获取视频信息（自动或手动）
2. 使用AI提取地点和美食信息
3. 调用高德地图API获取坐标
4. 下载封面图片
5. 保存到 `data/places.json`

详细使用说明请查看 [backend/README.md](backend/README.md)

#### 方式二: GitHub Actions（推荐）

1. 在GitHub仓库的Settings → Secrets中配置API密钥
2. 前往Actions标签页
3. 选择"Extract Video Info"工作流
4. 点击"Run workflow"，输入抖音视频链接
5. 等待自动提取并提交数据

### 查看效果

数据添加后：
- 本地开发：刷新页面即可看到新地点
- 线上部署：GitHub Actions会自动重新部署网站

## 🌐 部署到线上

### 部署到Vercel

1. 在 [Vercel](https://vercel.com) 创建新项目
2. 导入此GitHub仓库
3. Vercel会自动检测配置（`vercel.json`）
4. 在项目设置中添加环境变量：
   - `VITE_AMAP_KEY`: 高德地图JavaScript API Key
5. 部署完成！

### 部署到Netlify

1. 在 [Netlify](https://netlify.com) 创建新站点
2. 连接GitHub仓库
3. Netlify会自动检测配置（`netlify.toml`）
4. 在站点设置中添加环境变量：
   - `VITE_AMAP_KEY`: 高德地图JavaScript API Key
5. 部署完成！

### 配置GitHub Actions自动部署

在GitHub仓库的Settings → Secrets中添加以下密钥：

**必需**:
- `AMAP_WEB_SERVICE_KEY`: 高德地图Web服务API Key
- `VITE_AMAP_KEY`: 高德地图JavaScript API Key

**推荐**:
- `DEEPSEEK_API_KEY`: DeepSeek AI API Key

**可选**:
- `TIKHUB_API_KEY`: TikHub API Key
- `VERCEL_TOKEN`: Vercel部署令牌（如使用Vercel CLI部署）
- `NETLIFY_AUTH_TOKEN`: Netlify认证令牌（如使用Netlify CLI部署）
- `NETLIFY_SITE_ID`: Netlify站点ID

## 🔑 API密钥获取

### 1. 高德地图API（必需）

用于地图展示和地址解析。

1. 访问 [高德开放平台](https://console.amap.com/)
2. 注册/登录账号
3. 进入"应用管理" → "我的应用" → "创建新应用"
4. 添加Key:
   - **Web服务**: 用于地址解析（`AMAP_WEB_SERVICE_KEY`）
   - **Web端（JS API）**: 用于地图展示（`VITE_AMAP_KEY`）
5. 复制Key到 `.env` 文件

**注意**: 需要同时申请两个Key（Web服务 + JavaScript API）

### 2. DeepSeek API（推荐）

用于AI智能提取地点和美食信息。

1. 访问 [DeepSeek开放平台](https://platform.deepseek.com/)
2. 注册账号并登录
3. 进入"API密钥"页面
4. 创建新的API密钥
5. 复制密钥到 `.env` 文件中的 `DEEPSEEK_API_KEY`

**优势**: 
- 价格实惠（仅几分钱/千次调用）
- 中文理解能力强
- 响应速度快

**替代方案**: 也可以使用通义千问、文心一言等其他AI API，需要修改 `backend/extractor.py` 中的API调用代码。

### 3. TikHub API（可选）

用于自动获取抖音视频元数据。

1. 访问 [TikHub官网](https://api.tikhub.io/)
2. 注册账号
3. 获取API密钥
4. 填入 `.env` 文件中的 `TIKHUB_API_KEY`

**注意**: 
- 这是第三方服务，可能需要付费
- 如果不配置，脚本会自动切换到手动输入模式
- 手动输入模式同样好用，只是需要你手动填写视频信息

## 💡 使用场景

- 📹 看到美食视频想记录下来
- 🗺️ 规划旅行路线，查看想去的地方
- 👫 和对象一起收集美食打卡清单
- 📊 统计去过/想去的城市和美食数量
- 🔗 保存视频链接，随时回看

## 🛠️ 技术栈

**后端**:
- Python 3.11+
- requests (HTTP请求)
- openai (DeepSeek API调用)
- python-dotenv (环境变量管理)

**前端**:
- Vue 3 (渐进式框架)
- Vite (构建工具)
- Tailwind CSS (样式框架)
- 高德地图JavaScript API

**部署**:
- Vercel / Netlify (静态托管)
- GitHub Actions (自动化CI/CD)

## 📝 数据格式

`data/places.json` 文件格式：

```json
{
  "places": [
    {
      "id": "唯一ID",
      "name": "地点名称",
      "address": "详细地址",
      "city": "城市",
      "province": "省份",
      "location": {
        "lng": 经度,
        "lat": 纬度
      },
      "foods": [
        {
          "name": "美食名称",
          "description": "美食描述",
          "tags": ["标签1", "标签2"]
        }
      ],
      "thumbnail": "/images/xxx.jpg",
      "videoUrl": "抖音视频链接",
      "addedDate": "2025-11-30T12:00:00Z"
    }
  ]
}
```

## ❓ 常见问题

### Q: 不想配置那么多API怎么办？

A: 只需配置**高德地图API**即可使用！其他API都可以用手动输入替代：
- 没有AI API？手动输入地点和美食信息
- 没有TikHub API？手动输入视频标题和描述

### Q: 如何批量添加多个视频？

A: 创建一个简单的bash脚本：

```bash
#!/bin/bash
urls=(
  "视频链接1"
  "视频链接2"
  "视频链接3"
)

for url in "${urls[@]}"; do
  python backend/extractor.py --url "$url"
done
```

### Q: 数据文件丢失了怎么办？

A: 
- 如果推送到GitHub，从仓库恢复
- 建议定期备份 `data/places.json` 文件
- 图片文件备份 `frontend/public/images/` 目录

### Q: 如何修改或删除已添加的地点？

A: 直接编辑 `data/places.json` 文件：
- 修改：找到对应的地点对象，修改字段值
- 删除：从 `places` 数组中移除对应对象
- 保存后推送到GitHub，会自动重新部署

### Q: 地图显示不出来？

A: 检查：
1. 是否配置了 `VITE_AMAP_KEY`
2. 高德地图API Key是否正确
3. 浏览器控制台是否有错误信息
4. 检查 `frontend/index.html` 中的API Key是否正确

### Q: 能否使用百度地图或Google地图？

A: 可以，但需要修改代码：
- 百度地图：修改 `MapView.vue`，使用百度地图JavaScript API
- Google地图：修改 `MapView.vue`，使用Google Maps API
- 需要相应修改 `extractor.py` 中的坐标获取逻辑

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 💖 致谢

感谢对象给我分享那么多美食视频 ❤️

---

**开始记录你们的美食地图吧！** 🎉

