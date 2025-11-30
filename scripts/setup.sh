#!/bin/bash

echo "================================"
echo "美食地点记录系统 - 初始化脚本"
echo "================================"
echo ""

# 检查是否在正确的目录
if [ ! -f "README.md" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 1. 检查Python
echo "📦 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python 3.11+"
    exit 1
fi
echo "✅ Python版本: $(python3 --version)"
echo ""

# 2. 检查Node.js
echo "📦 检查Node.js环境..."
if ! command -v node &> /dev/null; then
    echo "❌ 未找到Node.js，请先安装Node.js 20+"
    exit 1
fi
echo "✅ Node.js版本: $(node --version)"
echo "✅ npm版本: $(npm --version)"
echo ""

# 3. 安装Python依赖
echo "📦 安装Python依赖..."
cd backend
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Python依赖安装失败"
    exit 1
fi
cd ..
echo "✅ Python依赖安装成功"
echo ""

# 4. 安装前端依赖
echo "📦 安装前端依赖..."
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "❌ 前端依赖安装失败"
    exit 1
fi
cd ..
echo "✅ 前端依赖安装成功"
echo ""

# 5. 检查环境变量文件
echo "📝 检查环境变量配置..."
if [ ! -f ".env" ]; then
    echo "⚠️  未找到.env文件"
    read -p "是否创建.env模板文件? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp .env.example .env 2>/dev/null || echo "未找到.env.example文件"
        echo "✅ 已创建.env文件，请编辑并填入你的API密钥"
        echo ""
        echo "需要配置的API密钥："
        echo "  1. AMAP_WEB_SERVICE_KEY - 高德地图Web服务API (必需)"
        echo "  2. VITE_AMAP_KEY - 高德地图JavaScript API (必需)"
        echo "  3. DEEPSEEK_API_KEY - DeepSeek AI API (推荐)"
        echo "  4. TIKHUB_API_KEY - TikHub API (可选)"
    fi
else
    echo "✅ 已存在.env文件"
fi
echo ""

# 6. 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p frontend/public/images
mkdir -p data
echo "✅ 目录创建完成"
echo ""

# 7. 检查数据文件
if [ ! -f "data/places.json" ]; then
    echo "📄 创建初始数据文件..."
    echo '{"places":[]}' > data/places.json
    echo "✅ 已创建空的places.json"
    echo ""
    echo "💡 提示: 可以复制data/places.example.json作为示例数据"
fi

echo "================================"
echo "✨ 初始化完成！"
echo "================================"
echo ""
echo "下一步操作："
echo "  1. 编辑.env文件，填入API密钥"
echo "  2. 运行前端开发服务器:"
echo "     cd frontend && npm run dev"
echo "  3. 添加第一个地点:"
echo "     cd backend && python extractor.py --url \"抖音视频链接\""
echo ""
echo "详细文档请查看: README.md"
echo ""

