# 吉隆坡漫行 · 城市旅行互动路书 · 全局开发与进度手册 (progress-kl.md)

> **项目定位**：专为马来西亚吉隆坡（KLCC / 武吉免登 / 茨厂街 / 黑风洞 / 布城粉红清真寺 / 独立广场）深度漫行定制的高颜值移动端 Web App。  
> **核心原则**：纯静态单文件免构建打包、零后端、全套苹果液态玻璃（Liquid Glass）视觉系统、移动端优先、Google Maps JavaScript API 深度驱动。  
> **当前生产版本**：`RELEASE v1.2.0 · 2026.09 (Apple Liquid Glass)` ｜ **全球直达**：[trip-kl.pages.dev](https://trip-kl.pages.dev) ｜ **坐标基准**：国际标准 WGS-84（原生零偏差）  
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
  - 迁移苹果液态玻璃视觉系统，落地行程路书、路线地图与工具。
- **v1.1.0 (两人同行极简实用版全面重塑 · 2026.09)**：
  - **定位精准下沉**：彻底剥离花哨冗余的视觉过载，重塑为专为两人自由行（用户与同学）量身定制的「高清晰度、极度实用、单手即开」移动端路书；
  - **真实行程与航班全量接入**：
    1. 真实航班：9/18 济南往返经深圳/广州（ZH9930/ZH333 ➔ CZ350/CZ3663）；
    2. 核心大本营锁定：甘榜峇鲁·拉惹乌达站旁「阿玛尼公寓 (Armani Residence and Hotel)」，39F 无边泳池正对双子塔全貌；
  - **4 大硬约束 100% 闭环落地**：
    1. **9/21 周一 14:00–15:00 面试锁定**：上午限吉隆坡塔（15分钟车程），12:30 准时回房，房间内双网热点+测速+防噪预案；
    2. **双子塔周一闭馆避坑**：登塔锁定 9/20 周日 17:30 黄昏场（41F 连桥 + 86F 观景台）；
    3. **黄亚华烤鸡翅周一公休**：9/19 周六夜市品尝，9/21 晚餐平滑切换为明记魔鬼鱼；
    4. **马六甲一日游锚定 9/22 周二**：TBS 大巴直达，荷兰红屋、圣保罗山、娘惹菜、河游船与海峡水上清真寺闭环；
  - **极简实用三大刚需功能上线**：
    1. **Google 搜索词一键复制（带 Toast 弹窗）**：每个节点配备复制按钮与 Google Maps / Grab 一键直达，告别输入法手动打马来文地名；
    2. **两人 50/50 AA 记账器**：专为 2 人出行设计，实时将马币支出一键对半折算为人民币 CNY，带常用场景快捷输入；
    3. **7 大出行防雷避坑手册**：凌晨自助入住、榴莲禁带、防雷雨时段、广州国际转机行李提取等要项置顶。
- **v1.1.1 (地道老饕美食与悦榕庄 59F 高空 Bar 深度闭环 · 2026.09)**：
  - **美食精准排雷与筛选**：
    1. **果断剔除「朱光玉火锅馆」**：避免在 5 天异国行程中浪费胃容量吃国内随处可见且溢价高昂的连锁火锅；
    2. **权衡「Village Park 椰浆饭」**：其距离市区 15+ 公里往返极易堵塞近 2 小时，保留酒店楼下同等级「万娇椰浆饭 (Wanjo)」，Village Park 作为机动备选；
    3. **全面升级 D2 早午餐为「ICC PUDU 美食广场」**：黑风洞下山直达本地人早餐圣地，集成【宽记三合一炸年糕】、【丰扬咖喱面】、【阿福客家酿豆腐】与妹记瓦煲海南茶；
    4. **茨厂街老字号「亚三叻沙 (Asam Laksa)」**：9 RM 纯正酸辣开胃，两人分食尝鲜；
    5. **歇脚中转「Kafe Kleptokrat」**：老洋房中庭泳池秋千咖啡馆，老城徒步避暑吹冷气；
    6. **夜景高空 Bar 迭代为「悦榕庄 Vertigo 59F Sky Bar」**：替换老旧 Heli Lounge，59 楼露天直面通体银白双子塔，无生硬强制低消；
    7. **D3 午餐替换为「亦是好肉骨茶 (Yik See Ho)」**：Ella 同款平价老饕店，替换商业化且昂贵的游客店新峰；
  - **交互与快捷工具升级**：
    1. 增加 ICC Pudu、宽记年糕、丰扬咖喱、亚三叻沙、Kleptokrat、悦榕庄 Vertigo、亦是好肉骨茶的 Google 英文搜索词与一键直通链接；
    2. 记账器快捷标签同步扩充；
    3. 路线地图 `KL_MAP_POINTS` 挂载对应真实 WGS-84 经纬度。
- **v1.1.2 (核心景点门票与预订速查中枢上线 · 2026.09)**：
  - **门票急迫度四级梯度分流**：
    1. 🔴 **必提前抢票（锁死日落）**：国油双峰塔 (Petronas Twin Towers)，9/20 周日 17:30 黄金场次，集成官方预约入口 (`eticket2.petronastwintowers.com.my`) 与飞猪余位直达通道；
    2. 🟡 **提前 1-2 天线上买（比现场省 10-15%）**：吉隆坡塔 KL Tower（飞猪户外露天+SkyBox透明天桥、室内观景台电子票即买即出）；TBS ⇄ 马六甲长途大巴（redBus 提前选座）；
    3. 🟢 **现场买 / 随到随用**：马六甲河游船 (Melaka River Cruise，RM30)、伊斯兰艺术博物馆 (RM20)、峇峇娘惹祖屋博物馆 (RM16-20)；
    4. ⚪ **免费开放景点 & 礼仪守则**：黑风洞 (272级彩虹阶梯过膝装要求)、国家清真寺 (免费借袍脱鞋)、独立广场、荷兰红屋、悦榕庄 Vertigo 59F (无门票低消，Smart Casual 着装)；
    5. 🛂 **必办申报**：马来西亚电子入境卡 (MDAC) 官方入口直达 (`imigresen-online.imi.gov.my/mdac/main`)，行前 3 天免费申报提醒；
  - **行程节点行动按钮深度闭环**：
    1. D2 双子塔增加【🌐 官网抢票】+【🎟️ 飞猪查位】；
    2. D3 吉隆坡塔增加【🎟️ 飞猪露天+天桥】+【🎟️ 飞猪室内票】；
    3. D4 TBS 总站增加【🚌 redBus订票】、马六甲河游船增加【🎟️ 飞猪查票】；
  - **功能 Tab 交互增强**：
    1. Tab 3 专属嵌入高对比度「🎫 核心景点门票与预订速查 (Ticket & Booking Hub)」模块；
    2. 底部 Dock 菜单第三项升级为 `[🎫 门票/AA/避坑]`，实现一键穿透直达。
- **v1.2.0 (苹果液态玻璃 Apple Liquid Glass 视觉重塑全面落地 · 2026.09)**：
  - **多层级折射与高斯模糊系统 (Glassmorphism & Optical Refraction)**：
    1. **深邃环境基底与弥散光晕 (Ambient Glow Mesh)**：采用 `#060911` 黑曜石深色底，叠加固定视口四焦点微光晕径向渐变（天蓝、紫罗兰、薄荷绿、玫瑰红），卡片滑动时呈现真实光学折射与色散通透感；
    2. **液态玻璃全域材质升级**：全面接入 `backdrop-filter: blur(24px) saturate(180%)`（及 `-webkit-` 前缀）；卡片采用 `rgba(255, 255, 255, 0.055)` 高透磨砂层，配合 `border: 1px solid rgba(255, 255, 255, 0.14)` 拟真高光边缘与双层镜面倒角；
    3. **微内阴影与悬浮深沉阴影**：加入 `box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.15), 0 8px 32px rgba(0, 0, 0, 0.38)`，边缘立体光效显著；
    4. **主题液态玻璃衍生**：D3 面试日尊享 Rose Liquid Glass（红宝石微光）；大本营住宿条 Emerald Liquid Glass；避雨与面试警示框高透警示玻璃；
    5. **悬浮灵动岛 Dock**：升级为浮空液态玻璃胶囊，`blur(28px) saturate(200%)`，高光镜面边缘与悬空阴影 `0 16px 40px rgba(0, 0, 0, 0.6)`。
  - **iOS 触觉反馈与动效 (Micro-Interactions)**：
    1. 全局按钮（操作按钮、复制、快捷标签、记账添加、地图 Pill、Dock 项）统一配备 `:active { transform: scale(0.97); }` 触控微缩回弹；
    2. 全局贝塞尔弹簧缓动：`transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`；
    3. 强化日光下易读性：SF Pro 字体阶层搭配纯白与高级冷灰高对比度排版，彻底杜绝毛玻璃泛虚现象。
  - **业务功能与数据 100% 完整无损保全**：
    1. D0~D5 完整行程、4 大硬约束（9/21 面试、9/20 双子塔黄昏、黄亚华周六/周一明记、9/22 马六甲）无损闭环；
    2. 全部操作链接（Google Maps 直达、Grab 唤起、官网抢票、飞猪比价、redBus、MDAC）及 Toast 复制逻辑完好；
    3. Tab 2 Google Maps WGS-84 地图网络与 Tab 3 门票速查/两人 AA 记账器/避坑清单持久化逻辑全量保留。


