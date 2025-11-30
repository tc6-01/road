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
    
    def __init__(self, non_interactive=False):
        self.amap_key = os.getenv('AMAP_WEB_SERVICE_KEY')
        self.deepseek_key = os.getenv('DEEPSEEK_API_KEY')
        self.openai_key = os.getenv('OPENAI_API_KEY')  # 用于视觉分析
        self.qwen_key = os.getenv('QWEN_API_KEY')  # 通义千问 VL（推荐，国内可用）
        self.non_interactive = non_interactive  # GitHub Actions 非交互模式
        
        if not self.amap_key:
            print("警告: 未配置高德地图API密钥,将无法获取精确坐标")
        
        if not self.deepseek_key and not self.openai_key and not self.qwen_key:
            if self.non_interactive:
                print("提示: 非交互模式下建议配置 AI API 密钥，否则需要手动提供所有信息")
            else:
                print("警告: 未配置AI API密钥,将使用手动输入模式")
        
        if self.qwen_key:
            print("✓ 已配置 Qwen VL API，支持视频智能分析")
    
    def _manual_input(self, url):
        """手动输入模式（仅用于交互式环境）"""
        if self.non_interactive:
            # 非交互模式下，返回空的视频信息
            return {
                "title": "",
                "description": "",
                "cover_url": "",
                "video_url": url
            }
        
        print("\n=== 手动输入模式 ===")
        print("💡 提示：请打开抖音视频，根据视频内容填写以下信息")
        print("   建议：观看视频，记录画面中出现的地点名称、美食名称等关键信息\n")
        
        title = input("视频标题（或视频中的关键文字）: ").strip()
        description = input("视频描述（包含地点、美食等详细信息，越详细越好）: ").strip()
        cover_url = input("封面图片URL (可选,直接回车跳过): ").strip()
        
        return {
            "title": title,
            "description": description,
            "cover_url": cover_url,
            "video_url": url
        }
    
    def _analyze_video_with_qwen(self, video_url, title, description):
        """使用通义千问 Qwen VL 分析视频内容（国内推荐）"""
        if not self.qwen_key:
            return None
        
        try:
            print("\n🎬 使用通义千问 Qwen VL 分析视频内容...")
            print("  ⚠️  注意：直接使用抖音链接可能无法分析，建议手动提供数据")
            
            # 直接使用抖音链接（可能不支持）
            actual_video_url = video_url
            
            # Qwen API 兼容 OpenAI 格式
            client = OpenAI(
                api_key=self.qwen_key,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
            
            # 创建提示词
            prompt = f"""
请仔细观看这个抖音短视频，提取其中的地点和美食信息。

视频标题: {title if title else '无'}
视频描述: {description if description else '无'}

请重点关注：
1. 视频中出现的店铺名称、招牌、logo、门头
2. 画面中的美食名称、菜品、食物
3. 视频中提到的地点、地址、城市、省份信息
4. 字幕、文字、语音中的关键信息
5. 视频旁白和对话内容

请以JSON格式返回（只返回JSON，不要其他文字）:
{{
    "place_name": "地点/店铺名称",
    "address": "详细地址",
    "city": "城市",
    "province": "省份",
    "foods": [
        {{
            "name": "美食名称",
            "description": "美食描述（口味、特色等）",
            "tags": ["特色标签", "口味标签"]
        }}
    ]
}}

如果某些信息无法从视频中获取，请留空字符串或空数组。
"""
            
            # 调用 Qwen VL API
            response = client.chat.completions.create(
                model="qwen-vl-max-latest",  # 或 qwen-vl-plus, qwen-vl-flash
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "video_url", "video_url": {"url": actual_video_url}}
                        ]
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # 移除 markdown 标记
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            
            extracted = json.loads(result_text.strip())
            
            # 检查结果
            if extracted.get('place_name') or extracted.get('city') or extracted.get('foods'):
                print(f"\n  ✅ Qwen VL 视频分析完成！")
                print(f"    地点: {extracted.get('place_name', '未知')}")
                print(f"    城市: {extracted.get('city', '未知')}")
                print(f"    美食数量: {len(extracted.get('foods', []))}")
                return extracted
            else:
                print("  ⚠️  视频中未找到有效信息")
                return None
                
        except Exception as e:
            print(f"  Qwen VL 分析失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _analyze_with_vision(self, cover_url, title, description):
        """使用视觉AI分析封面图片"""
        if not self.openai_key:
            return None
        
        try:
            print("  使用 GPT-4 Vision 分析封面图片...")
            
            client = OpenAI(api_key=self.openai_key)
            
            prompt = f"""
请分析这张抖音视频封面图片，提取其中的地点和美食信息。

视频标题: {title}
视频描述: {description}

请重点关注图片中的：
1. 店铺招牌、地点名称
2. 美食名称、菜品
3. 地址、城市信息
4. 任何文字信息

请以JSON格式返回:
{{
    "place_name": "地点名称",
    "address": "详细地址",
    "city": "城市",
    "province": "省份",
    "foods": [
        {{
            "name": "美食名称",
            "description": "美食描述",
            "tags": ["标签"]
        }}
    ]
}}

如果无法提取某些信息，请留空字符串或空数组。只返回JSON。
"""
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # 使用支持视觉的模型
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": cover_url}}
                        ]
                    }
                ],
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # 移除markdown标记
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            
            extracted = json.loads(result_text.strip())
            
            # 检查是否有有效信息
            if extracted.get('place_name') or extracted.get('city') or extracted.get('foods'):
                print(f"  ✓ 视觉AI提取完成")
                print(f"    地点: {extracted.get('place_name', '未知')}")
                print(f"    城市: {extracted.get('city', '未知')}")
                print(f"    美食数量: {len(extracted.get('foods', []))}")
                return extracted
            else:
                print("  ⚠️  图片中未找到有效信息")
                return None
                
        except Exception as e:
            print(f"  视觉分析失败: {e}")
            return None
    
    def extract_info_with_ai(self, video_info):
        """使用AI提取地点和美食信息"""
        if not self.deepseek_key:
            return self._manual_extract()
        
        # 检查输入内容是否有效
        title = video_info.get('title', '').strip()
        description = video_info.get('description', '').strip()
        cover_url = video_info.get('cover_url', '').strip()
        
        # 如果有封面图片，尝试使用视觉AI分析
        if cover_url and len(title) < 10 and len(description) < 10:
            print("\n📷 检测到封面图片，尝试使用视觉AI分析...")
            vision_result = self._analyze_with_vision(cover_url, title, description)
            if vision_result:
                return vision_result
        
        if len(title) < 3 and len(description) < 3:
            print("\n⚠️  视频标题和描述内容过少,无法使用AI分析")
            print("切换到手动输入模式...")
            return self._manual_extract()
        
        print("\n使用AI分析文本内容...")
        
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
            
            # 检查AI提取结果是否有效
            if not extracted.get('place_name') and not extracted.get('city'):
                print("\n⚠️  AI未能提取到有效信息")
                print("切换到手动输入模式...")
                return self._manual_extract()
            
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
        if self.non_interactive:
            raise ValueError("错误: 非交互模式下AI提取失败，请检查 API 配置或视频内容质量")
        
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
        if self.non_interactive:
            print("  ⚠️  非交互模式下跳过手动输入坐标")
            return None
        
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
    
    def process(self, url, manual_data=None):
        """处理抖音视频链接
        
        Args:
            url: 抖音视频链接
            manual_data: 手动提供的数据（用于非交互模式下的备选方案）
        """
        print(f"\n{'='*60}")
        print("抖音视频内容提取")
        print(f"{'='*60}")
        
        video_info = {"video_url": url, "title": "", "description": "", "cover_url": ""}
        extracted = None
        
        # 1. 优先使用手动提供的数据（如果有的话）
        if manual_data and manual_data.get('place_name') and manual_data.get('city'):
            print("\n✓ 使用手动提供的数据")
            extracted = manual_data
            print(f"  地点: {extracted.get('place_name', '未知')}")
            print(f"  城市: {extracted.get('city', '未知')}")
            print(f"  美食数量: {len(extracted.get('foods', []))}")
        
        # 2. 如果没有手动数据，尝试 Qwen VL 视频分析
        if not extracted and self.qwen_key:
            extracted = self._analyze_video_with_qwen(url, "", "")
            
            if not extracted:
                print("\n⚠️  Qwen VL 分析失败，尝试其他方式...")
        
        # 3. 如果 Qwen 失败，尝试其他 AI 方法（文本分析）
        if not extracted and (self.deepseek_key or self.openai_key):
            print("\n尝试文本分析方式...")
            video_info = self._manual_input(url)
            if video_info.get('title') or video_info.get('description'):
                extracted = self.extract_info_with_ai(video_info)
        
        # 4. 如果还是没有数据，且是非交互模式，则失败
        if not extracted:
            if self.non_interactive:
                raise ValueError("所有自动提取方法均失败，且未提供手动数据。请在运行 workflow 时填写地点名称和城市信息。")
            else:
                # 交互模式：手动输入
                video_info = self._manual_input(url)
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
    parser.add_argument(
        '--non-interactive',
        action='store_true',
        help='非交互模式（用于GitHub Actions等自动化环境）'
    )
    
    # 手动输入参数（用于非交互模式下的备选方案）
    parser.add_argument(
        '--place-name',
        type=str,
        help='地点名称（非交互模式下的备选输入）'
    )
    parser.add_argument(
        '--city',
        type=str,
        help='城市（非交互模式下的备选输入）'
    )
    parser.add_argument(
        '--province',
        type=str,
        help='省份（非交互模式下的备选输入）'
    )
    parser.add_argument(
        '--address',
        type=str,
        help='详细地址（非交互模式下的备选输入）'
    )
    parser.add_argument(
        '--foods',
        type=str,
        help='美食列表JSON（非交互模式下的备选输入），格式：[{"name":"火锅","description":"麻辣","tags":["辣"]}]'
    )
    
    args = parser.parse_args()
    
    # 准备手动输入数据（如果提供）
    manual_data = None
    if args.place_name or args.city:
        manual_data = {
            'place_name': args.place_name or '',
            'city': args.city or '',
            'province': args.province or '',
            'address': args.address or '',
            'foods': []
        }
        
        # 解析美食JSON
        if args.foods:
            try:
                manual_data['foods'] = json.loads(args.foods)
            except json.JSONDecodeError as e:
                print(f"⚠️  警告: 美食JSON格式错误: {e}")
                print(f"   使用空列表")
    
    try:
        extractor = DouyinExtractor(non_interactive=args.non_interactive)
        extractor.process(args.url, manual_data=manual_data)
    except ValueError as e:
        print(f"\n❌ {e}")
        print("\n💡 提示：")
        print("   方案1：配置 AI API 密钥（推荐）")
        print("      在 GitHub 仓库的 Settings > Secrets 中添加：")
        print("      - QWEN_API_KEY (推荐，国内可用)")
        print("      - AMAP_WEB_SERVICE_KEY (必需)")
        print("      - TIKHUB_API_KEY (可选，用于自动获取视频)")
        print("\n   方案2：手动提供信息")
        print("      在运行 workflow 时填写：")
        print("      - 地点名称")
        print("      - 城市")
        print("      - 美食列表（可选）\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 提取失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

