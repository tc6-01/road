#!/bin/bash

# 批量添加地点的示例脚本

echo "================================"
echo "批量添加美食地点"
echo "================================"
echo ""

# 视频链接列表（替换为实际的抖音视频链接）
urls=(
  # "抖音视频链接1"
  # "抖音视频链接2"
  # "抖音视频链接3"
)

if [ ${#urls[@]} -eq 0 ]; then
    echo "⚠️  请先编辑此脚本，添加视频链接到urls数组"
    echo ""
    echo "示例："
    echo "urls=("
    echo "  \"https://v.douyin.com/xxxxx/\""
    echo "  \"https://v.douyin.com/yyyyy/\""
    echo ")"
    exit 1
fi

total=${#urls[@]}
success=0
failed=0

for i in "${!urls[@]}"; do
    url="${urls[$i]}"
    num=$((i + 1))
    
    echo "[$num/$total] 处理: $url"
    echo ""
    
    cd backend
    python extractor.py --url "$url"
    
    if [ $? -eq 0 ]; then
        ((success++))
        echo "✅ 成功"
    else
        ((failed++))
        echo "❌ 失败"
    fi
    
    cd ..
    echo ""
    echo "---"
    echo ""
done

echo "================================"
echo "批量处理完成！"
echo "================================"
echo "总计: $total"
echo "成功: $success"
echo "失败: $failed"
echo ""

