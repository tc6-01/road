# GitHub Actions工作流说明

本项目包含两个自动化工作流。

## auto-deploy.yml - 自动部署

**触发条件**:
- 推送到main/master分支
- 修改了`data/places.json`或`frontend/`目录
- 手动触发

**功能**:
1. 检出代码
2. 安装Node.js依赖
3. 构建前端应用
4. 部署到Vercel/Netlify

**环境变量** (在GitHub Secrets中配置):
- `VITE_AMAP_KEY`: 高德地图JavaScript API Key (必需)
- `VERCEL_TOKEN`: Vercel部署令牌 (可选)
- `NETLIFY_AUTH_TOKEN`: Netlify认证令牌 (可选)
- `NETLIFY_SITE_ID`: Netlify站点ID (可选)

## extract-video.yml - 提取视频信息

**触发方式**: 手动触发

**使用步骤**:
1. 进入GitHub仓库的Actions标签
2. 选择"Extract Video Info"工作流
3. 点击"Run workflow"
4. 输入抖音视频链接
5. 点击"Run workflow"开始执行

**功能**:
1. 检出代码
2. 安装Python依赖
3. 运行提取脚本
4. 自动提交更新的数据文件
5. 推送到仓库（触发自动部署）

**环境变量** (在GitHub Secrets中配置):
- `AMAP_WEB_SERVICE_KEY`: 高德地图Web服务API Key (必需)
- `DEEPSEEK_API_KEY`: DeepSeek API Key (推荐)
- `TIKHUB_API_KEY`: TikHub API Key (可选)

## 配置GitHub Secrets

1. 进入仓库Settings
2. 点击Secrets and variables → Actions
3. 点击New repository secret
4. 添加以上环境变量

## 注意事项

- 确保所有必需的API密钥已配置
- extract-video.yml会自动提交代码，确保有写入权限
- 如果使用Vercel CLI部署，需要取消注释相关代码并配置VERCEL_TOKEN

