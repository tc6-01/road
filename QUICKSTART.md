# 快速开始指南 🚀

5分钟快速上手美食地点记录系统！

## 第一步：安装依赖

### 自动安装（推荐）

```bash
./scripts/setup.sh
```

### 手动安装

```bash
# 1. 安装Python依赖
cd backend
pip install -r requirements.txt

# 2. 安装前端依赖
cd ../frontend
npm install
```

## 第二步：配置API密钥

### 1. 创建环境变量文件

复制示例文件：
```bash
cp .env.example .env
```

### 2. 填写API密钥

编辑 `.env` 文件：

```env
# 必需 - 高德地图API
AMAP_WEB_SERVICE_KEY=你的密钥
VITE_AMAP_KEY=你的密钥

# 推荐 - AI提取
DEEPSEEK_API_KEY=你的密钥

# 可选 - 自动获取视频
TIKHUB_API_KEY=你的密钥
```

### 3. 获取高德地图API密钥（必需）

1. 访问：https://console.amap.com/
2. 注册并登录
3. 创建应用 → 添加Key
4. 需要两个Key：
   - **Web服务** → `AMAP_WEB_SERVICE_KEY`
   - **Web端(JS API)** → `VITE_AMAP_KEY`

### 4. 获取DeepSeek API（推荐）

1. 访问：https://platform.deepseek.com/
2. 注册并创建API密钥
3. 复制到 `DEEPSEEK_API_KEY`

> 💡 提示：如果不配置DeepSeek，可以使用手动输入模式

## 第三步：运行项目

### 启动开发服务器

```bash
cd frontend
npm run dev
```

访问：http://localhost:3000

## 第四步：添加第一个地点

### 方式一：使用脚本（推荐）

```bash
cd backend
python extractor.py --url "抖音视频链接"
```

按照提示输入信息即可。

### 方式二：使用示例数据

```bash
cp data/places.example.json data/places.json
```

刷新浏览器即可看到示例地点。

## 第五步：部署到线上（可选）

### 部署到Vercel

1. 推送代码到GitHub
2. 访问 https://vercel.com
3. 导入GitHub仓库
4. 在项目设置中添加环境变量 `VITE_AMAP_KEY`
5. 部署完成！

### 部署到Netlify

1. 推送代码到GitHub
2. 访问 https://netlify.com
3. 连接GitHub仓库
4. 在站点设置中添加环境变量 `VITE_AMAP_KEY`
5. 部署完成！

## 常用命令

```bash
# 前端开发
cd frontend && npm run dev

# 前端构建
cd frontend && npm run build

# 添加地点
cd backend && python extractor.py --url "视频链接"

# 批量添加（需要先编辑脚本）
./scripts/add-place.sh

# 查看项目结构
tree -L 2 -I 'node_modules|dist|__pycache__'
```

## 使用流程

```
1. 看到美食视频 → 复制链接
2. 运行提取脚本 → 自动/手动填写信息
3. 数据保存到JSON → 刷新网页即可看到
4. 推送到GitHub → 自动部署更新
```

## 故障排除

### 问题：地图显示不出来

**解决**：
1. 检查 `.env` 中的 `VITE_AMAP_KEY` 是否配置
2. 检查浏览器控制台是否有错误
3. 确认高德地图API密钥是否正确

### 问题：数据不显示

**解决**：
1. 检查 `data/places.json` 文件是否存在
2. 检查JSON格式是否正确
3. 刷新浏览器缓存（Ctrl+F5）

### 问题：脚本运行失败

**解决**：
1. 检查Python版本（需要3.11+）
2. 重新安装依赖：`pip install -r requirements.txt`
3. 检查 `.env` 文件中的API密钥

### 问题：前端构建失败

**解决**：
1. 删除 `node_modules` 和 `package-lock.json`
2. 重新安装：`npm install`
3. 检查Node.js版本（需要20+）

## 进阶使用

### 批量添加视频

编辑 `scripts/add-place.sh`，添加视频链接：

```bash
urls=(
  "https://v.douyin.com/xxxxx/"
  "https://v.douyin.com/yyyyy/"
  "https://v.douyin.com/zzzzz/"
)
```

然后运行：
```bash
./scripts/add-place.sh
```

### 自定义地图样式

编辑 `frontend/src/components/MapView.vue`，修改：

```javascript
mapStyle: 'amap://styles/normal'  // 标准
// 'amap://styles/dark'           // 暗黑
// 'amap://styles/light'          // 月光银
// 'amap://styles/whitesmoke'     // 远山黛
```

### 修改主题色

编辑 `frontend/tailwind.config.js`，修改 `primary` 颜色。

## 需要帮助？

- 📖 查看详细文档：[README.md](README.md)
- 🐛 提交问题：GitHub Issues
- 💬 讨论交流：GitHub Discussions

---

**祝你使用愉快！开始记录美食之旅吧！** 🎉

