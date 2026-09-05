# BlenderGIS-CN（汉化增强版）

BlenderGIS 的**简体中文汉化版**，并新增了**高德地图、天地图**等国内地图源。

基于 [domlysz/BlenderGIS](https://github.com/domlysz/BlenderGIS)（GPL-3.0），感谢原作者 domlysz 的开源贡献。

> 原项目：<https://github.com/domlysz/BlenderGIS>

## 相比原版的改动

1. **界面汉化**：通过 Blender 官方翻译接口（`bpy.app.translations`）提供简体中文界面，只替换显示文字，不影响任何功能，可随时切回英文。
2. **高德地图源（AMap）**：新增高德「街道图 / 卫星影像」，并实现 **GCJ-02（火星坐标）↔ WGS84 坐标校正**，可与 WGS84 数据（Shapefile / GeoTIFF / OSM / GPS）精确对齐。
3. **天地图源（Tianditu）**：新增天地图「矢量底图 / 矢量注记 / 影像底图 / 影像注记 / 地形晕渲 / 地形注记」6 个图层（需自行申请密钥）。
4. **OSM 获取修复**：修复 Overpass API 的 406 / 504 报错（切换可靠镜像 + 规范 User-Agent + 更长超时）。

## 安装

1. 下载本仓库，将整个文件夹（重命名为任意名字，如 `BlenderGIS-CN`）放到 Blender 插件目录：
   - Windows：`C:\Users\<用户名>\AppData\Roaming\Blender Foundation\Blender\<版本>\scripts\addons\`
2. 打开 Blender → 编辑 → 偏好设置 → 插件 → 搜索 `BlenderGIS` → 勾选启用。
3. 将界面语言设为「简体中文」：编辑 → 偏好设置 → 界面 → 语言 → 简体中文。

## 使用国内地图源

### 高德地图（无需密钥）

GIS → Web geodata → Basemap → 源选择「高德地图」，图层选「街道图」或「卫星影像」。

### 天地图（需密钥）

1. 到 [天地图官网](https://www.tianditu.gov.cn) 注册并申请「地图服务」Key（个人开发者免费）；
2. 偏好设置 → 插件 → BlenderGIS → 填入「Tianditu API Key」；
3. 重启 Blender（或重新勾选插件），Basemap → 源选择「天地图」。

## OSM 获取

- 偏好设置 → BlenderGIS → 「Overpass 服务器」选择 `overpass.kumi.systems`；
- 放大地图、缩小范围（2~5 公里）后再点「获取 OSM」，避免服务器超时。

## 坐标系说明

- **高德地图**：瓦片为 GCJ-02（火星坐标），本版已内置 GCJ-02 ↔ WGS84 转换，可与 WGS84 数据对齐。
- **天地图**：使用 CGCS2000 坐标（≈WGS84，偏差亚米级），天然与 WGS84 数据对齐，无需额外校正。

## 版权

本项目基于 GPL-3.0 许可的 [BlenderGIS](https://github.com/domlysz/BlenderGIS)（作者 domlysz），遵循相同许可证。详见 [LICENSE](LICENSE)。
