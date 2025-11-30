#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音视频内容提取脚本
从抖音视频链接中提取地点和美食信息,并保存到JSON文件
"""

import os
import sys
import json
import argparse
import requests
import uuid
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
IMAGE_DIR = ROOT_DIR / "frontend" / "public" / "images"

# 确保目录存在
DATA_DIR.mkdir(exist_ok=True)
IMAGE_DIR.mkdir(parents=True, exist_ok=True)


class DouyinExtractor:
    """抖音内容提取器"""
    
    def __init__(self):
        self.amap_key = os.getenv('AMAP_WEB_SERVICE_KEY')
        self.deepseek_key = os.getenv('DEEPSEEK_API_KEY')
        self.tikhub_key = os.getenv('TIKHUB_API_KEY')
        
        if not self.amap_key:
            print("警告: 未配置高德地图API密钥,将无法获取精确坐标")
        
        if not self.deepseek_key:
            print("警告: 未配置AI API密钥,将使用手动输入模式")
    
    def get_video_info(self, url):
        """
        获取抖音视频信息
        由于抖音API限制,这里提供两种模式:
        1. 使用第三方API (如TikHub)
        2. 手动输入模式
        """
        print("\n正在获取视频信息...")
        
        # 如果配置了TikHub API,尝试自动获取
        if self.tikhub_key:
            try:
                return self._fetch_via_tikhub(url)
            except Exception as e:
                print(f"自动获取失败: {e}")
                print("切换到手动输入模式...")
        
        # 手动输入模式
        return self._manual_input(url)
    
    def _fetch_via_tikhub(self, url):
        """通过TikHub API获取视频信息"""
        # 这是示例实现,实际需要根据TikHub API文档调整
        api_url = "https://api.tikhub.io/api/v1/douyin/video/info"
        headers = {
            "Authorization": f"Bearer {self.tikhub_key}"
        }
        params = {"url": url}
        
        response = requests.get(api_url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        return {
            "title": data.get("title", ""),
            "description": data.get("desc", ""),
            "cover_url": data.get("cover", ""),
            "video_url": url
        }
    
    def _manual_input(self, url):
        """手动输入模式"""
        print("\n=== 手动输入模式 ===")
        print("请根据抖音视频内容填写以下信息:\n")
        
        title = input("视频标题: ").strip()
        description = input("视频描述 (可选): ").strip()
        cover_url = input("封面图片URL (可选,直接回车跳过): ").strip()
        
        return {
            "title": title,
            "description": description,
            "cover_url": cover_url,
            "video_url": url
        }
    
    def extract_info_with_ai(self, video_info):
        """使用AI提取地点和美食信息"""
        if not self.deepseek_key:
            return self._manual_extract()
        
        print("\n使用AI分析视频内容...")
        
        client = OpenAI(
            api_key=self.deepseek_key,
            base_url="https://api.deepseek.com"
        )
        
        prompt = f"""
请从以下抖音视频信息中提取地点和美食信息:

标题: {video_info['title']}
描述: {video_info['description']}

请以JSON格式返回,包含以下字段:
{{
    "place_name": "地点名称",
    "address": "详细地址 (如果有)",
    "city": "城市",
    "province": "省份",
    "foods": [
        {{
            "name": "美食名称",
            "description": "美食描述",
            "tags": ["标签1", "标签2"]
        }}
    ]
}}

如果无法提取某些信息,请留空字符串或空数组。
只返回JSON,不要其他说明文字。
"""
        
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个专业的信息提取助手,擅长从文本中提取地点和美食相关信息。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content.strip()
            # 移除可能的markdown代码块标记
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            
            extracted = json.loads(result_text.strip())
            
            print(f"✓ AI提取完成")
            print(f"  地点: {extracted.get('place_name', '未知')}")
            print(f"  城市: {extracted.get('city', '未知')}")
            print(f"  美食数量: {len(extracted.get('foods', []))}")
            
            return extracted
            
        except Exception as e:
            print(f"AI提取失败: {e}")
            print("切换到手动输入模式...")
            return self._manual_extract()
    
    def _manual_extract(self):
        """手动提取信息"""
        print("\n=== 手动输入地点和美食信息 ===\n")
        
        place_name = input("地点名称: ").strip()
        address = input("详细地址 (可选): ").strip()
        city = input("城市: ").strip()
        province = input("省份: ").strip()
        
        foods = []
        while True:
            print(f"\n--- 美食 #{len(foods) + 1} ---")
            food_name = input("美食名称 (直接回车结束添加): ").strip()
            if not food_name:
                break
            
            food_desc = input("美食描述 (可选): ").strip()
            tags_input = input("标签 (用逗号分隔,可选): ").strip()
            tags = [t.strip() for t in tags_input.split(",") if t.strip()]
            
            foods.append({
                "name": food_name,
                "description": food_desc,
                "tags": tags
            })
        
        return {
            "place_name": place_name,
            "address": address,
            "city": city,
            "province": province,
            "foods": foods
        }
    
    def get_coordinates(self, address, city):
        """使用高德地图API获取坐标"""
        if not self.amap_key:
            print("未配置高德地图API,跳过坐标获取")
            return None
        
        print(f"\n正在获取坐标: {address or city}...")
        
        api_url = "https://restapi.amap.com/v3/geocode/geo"
        params = {
            "key": self.amap_key,
            "address": f"{city} {address}" if address else city,
            "city": city
        }
        
        try:
            response = requests.get(api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == '1' and data['geocodes']:
                location = data['geocodes'][0]['location']
                lng, lat = map(float, location.split(','))
                print(f"✓ 坐标获取成功: ({lng}, {lat})")
                return {"lng": lng, "lat": lat}
            else:
                print("坐标获取失败,请手动输入")
                return self._manual_coordinates()
                
        except Exception as e:
            print(f"坐标获取失败: {e}")
            return self._manual_coordinates()
    
    def _manual_coordinates(self):
        """手动输入坐标"""
        print("\n请手动输入坐标 (可在高德地图上查询)")
        lng = input("经度 (可选,直接回车跳过): ").strip()
        lat = input("纬度 (可选,直接回车跳过): ").strip()
        
        if lng and lat:
            try:
                return {"lng": float(lng), "lat": float(lat)}
            except ValueError:
                print("坐标格式错误,已跳过")
        
        return None
    
    def download_cover(self, cover_url):
        """下载封面图片"""
        if not cover_url:
            return None
        
        print("\n正在下载封面图片...")
        
        try:
            response = requests.get(cover_url, timeout=15)
            response.raise_for_status()
            
            # 生成唯一文件名
            ext = ".jpg"
            if "image/png" in response.headers.get('Content-Type', ''):
                ext = ".png"
            
            filename = f"{uuid.uuid4()}{ext}"
            filepath = IMAGE_DIR / filename
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ 封面图片已保存: {filename}")
            return f"/images/{filename}"
            
        except Exception as e:
            print(f"封面下载失败: {e}")
            return None
    
    def save_to_json(self, place_data):
        """保存到JSON文件"""
        json_file = DATA_DIR / "places.json"
        
        # 读取现有数据
        if json_file.exists():
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {"places": []}
        
        # 添加新地点
        data["places"].append(place_data)
        
        # 保存
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 数据已保存到: {json_file}")
        print(f"✓ 当前共有 {len(data['places'])} 个地点")
    
    def process(self, url):
        """处理抖音视频链接"""
        print(f"\n{'='*60}")
        print("抖音视频内容提取")
        print(f"{'='*60}")
        
        # 1. 获取视频信息
        video_info = self.get_video_info(url)
        
        # 2. 提取地点和美食信息
        extracted = self.extract_info_with_ai(video_info)
        
        # 3. 获取坐标
        location = self.get_coordinates(
            extracted.get('address', ''),
            extracted.get('city', '')
        )
        
        # 4. 下载封面
        thumbnail = self.download_cover(video_info.get('cover_url'))
        
        # 5. 组装数据
        place_data = {
            "id": str(uuid.uuid4()),
            "name": extracted.get('place_name', '未命名地点'),
            "address": extracted.get('address', ''),
            "city": extracted.get('city', ''),
            "province": extracted.get('province', ''),
            "location": location,
            "foods": extracted.get('foods', []),
            "thumbnail": thumbnail,
            "videoUrl": video_info['video_url'],
            "addedDate": datetime.utcnow().isoformat() + 'Z'
        }
        
        # 6. 保存到JSON
        self.save_to_json(place_data)
        
        print(f"\n{'='*60}")
        print("✓ 提取完成!")
        print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description='从抖音视频链接提取地点和美食信息'
    )
    parser.add_argument(
        '--url',
        type=str,
        required=True,
        help='抖音视频链接'
    )
    
    args = parser.parse_args()
    
    extractor = DouyinExtractor()
    extractor.process(args.url)


if __name__ == '__main__':
    main()

