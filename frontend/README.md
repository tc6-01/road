# 美食地点地图 - 前端

基于Vue 3 + Vite + Tailwind CSS的现代化Web应用。

## 开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

## 环境变量

创建 `.env` 文件并配置：

```env
VITE_AMAP_KEY=你的高德地图JavaScript_API_Key
```

## 目录结构

```
src/
├── components/
│   ├── MapView.vue        # 地图组件
│   ├── PlaceList.vue      # 地点列表
│   └── PlaceDetail.vue    # 地点详情
├── data/                  # 数据文件
├── App.vue                # 根组件
├── main.js                # 入口文件
└── style.css              # 全局样式
```

## 组件说明

### MapView.vue
- 集成高德地图API
- 渲染地点标记
- 支持标记点击交互
- 自适应地图视野

### PlaceList.vue
- 显示所有地点列表
- 支持搜索和筛选
- 按省份分组展示
- 显示统计信息

### PlaceDetail.vue
- 展示地点详细信息
- 美食列表展示
- 支持导航和查看原视频
- 响应式弹窗设计

## 数据加载

数据从 `/data/places.json` 加载，确保：
1. JSON文件格式正确
2. 图片路径正确（相对于public目录）
3. 坐标数据有效

