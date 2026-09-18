# 吉隆坡漫行 · 城市旅行互动路书 · 全局开发与进度手册 (progress-kl.md)

> **项目定位**：专为马来西亚吉隆坡（KLCC / 武吉免登 / 茨厂街 / 黑风洞 / 布城粉红清真寺 / 独立广场）深度漫行定制的高颜值移动端 Web App。  
> **核心原则**：纯静态单文件免构建打包、零后端、全套苹果液态玻璃（Liquid Glass）视觉系统、移动端优先、Google Maps JavaScript API 深度驱动。  
> **当前生产版本**：`RELEASE v1.0.0 · 2026.09` ｜ **坐标基准**：国际标准 WGS-84（原生零偏差）  
> 📌 **项目阶段记忆规范**：**在每一次对话或开发阶段完成后，必须在此文件中更新当前最新状态与技术决策，以便在新的对话中实现秒级上下文恢复并无缝衔接后续开发！**

---

## 一、新对话快速唤醒指南 (AI Agent Onboarding)

当在新的对话窗口中开启工作时，AI 助手只需按顺序执行以下 3 步即可完整接管项目：
1. **查阅本文档 (`progress-kl.md`)**：掌握最新已完成功能、底层数据结构与待办事项；
2. **确认文件对应关系**：
   - 核心开发文件：`d:\Document\Project\Pilgrimage to the West\kl-trip\index.html`
   - 二级探索知识库：`d:\Document\Project\Pilgrimage to the West\吉隆坡第二层级规划.md`
   - 西北丝路项目互不干扰：`trip-map/index.html`
3. **验证与部署规范**：
   - 移动端预览推荐模拟尺寸：`390×844`, `deviceScaleFactor: 3`, `hasTouch: true`；
   - 自动化部署：推送到 GitHub 远端 `JohnMaxwell0123/Trip` 的 `main` 分支，由 Cloudflare Pages 自动构建秒级上线。

---

## 二、Google Maps API 凭证与配置规范 (Official Credentials)

本项目正式接入 Google Maps Platform Web 端 JavaScript API：

| 配置项 | 官方参数值 / 规范 | 说明与代码嵌入位置 |
| :--- | :--- | :--- |
| **服务平台** | `Google Maps JavaScript API` | 支持 `Map`、`DirectionsService`、`marker.AdvancedMarkerElement` |
| **坐标系统** | `WGS-84` (GPS标准) | 吉隆坡经纬度无需任何 GCJ-02 火星加偏 |
| **搭载库 (Libraries)** | `routes, places, geometry, marker` | URL 参数：`&libraries=routes,places,geometry,marker` |
| **API Key 注入** | `<script src="https://maps.googleapis.com/maps/api/js?key=..."></script>` | 支持在代码内配置专属 Key，或缺省时优雅降级提示 |
| **城市基准中心** | `Lat: 3.1579, Lng: 101.7116` | 默认定位以吉隆坡市中心国油双峰塔（KLCC）为视觉锚点 |

---

## 三、文件组织体系 (Monorepo Architecture)

```text
Pilgrimage to the West (Trip)/
├── kl-trip/                  ← 【吉隆坡主项目目录】
│   ├── assets/images/        ← 城市背景图、景点素材
│   └── index.html            ← 【主生产文件】包含完整 HTML/CSS/JS/Google Maps
├── trip-map/                 ← 【丝路自驾项目】高德地图引擎独立运行
├── 吉隆坡第二层级规划.md     ← 【知识库】Day 0 ~ Day 4 美食/高空机位/Grab通达性
├── progress-kl.md            ← 【吉隆坡进度手册】唯一基准文档（本文档）
├── progress.md               ← 【丝路进度手册】
└── README.md                 ← 【多项目总览大厅】
```

---

## 四、核心技术决策与防踩坑规程

1. **容器全时保活与防 Collapse 铁律**：
   - 地图 Tab 隐藏时绝不使用 `display: none`，采用 `visibility: hidden; opacity: 0; pointer-events: none;`，从根本上防止 Google Maps 计算长宽为 0 导致相机投影崩溃。
2. **图钉弹窗防闪退四维架构**：
   - 点击 Marker 展开 InfoWindow 时，严格阻断冒泡并设立 400ms 时间戳防护，彻底根除移动端手势一闪而过的问题。
3. **Grab 与 Google Maps 深度直达**：
   - 每处景点与餐厅均内嵌 Google Maps Universal Links 及 Grab 唤起协议，手机端一键唤起打车与步行/地铁导航。
4. **热带气候与都市通勤弹性熔断（Cutoff）**：
   - 针对吉隆坡午后强对流雷阵雨设立 15:30 室内降级预案，晚高峰设立 17:30 避堵出行策略。

---

## 五、阶段开发记录 (Changelog)

- **v1.0.0 (初始奠基 · 2026.09)**：
  - 完成吉隆坡 Monorepo 子目录与知识库架构建立；
  - 接入 Google Maps JavaScript API 与国际标准 WGS-84 坐标系；
  - 迁移苹果液态玻璃（Liquid Glass）视觉系统，适配热带都市青柠/双子塔科技蓝流光；
  - 落地行程路书（Day 0 ~ Day 4）、全要素城市地图、双币种（MYR/CNY）AA 记账器与大马出行备忘录。
