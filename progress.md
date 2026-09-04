# 西行计划 · 丝路自驾路书 · 项目全局开发与进度手册 (progress.md)

> **项目定位**：专为 9 天西北大环线（济南往返 9.24 - 10.02 · 兰州/张掖/酒泉/鼎新/额济纳/嘉峪关/瓜州/敦煌/当金山/柴达木/茶卡/西宁）考斯特 10 人+团队自驾深度定制的高颜值移动端 Web App。  
> **核心原则**：纯静态单文件免构建打包、零后端、全套苹果液态玻璃（Liquid Glass）视觉系统、移动端优先（响应式兼顾桌面浏览器）、Cloudflare Pages 静态边缘秒开。  
> 📌 **项目阶段记忆规范**：**在每一次对话或开发阶段完成后，必须在此文件中更新当前最新状态与技术决策，以便在新的对话中实现秒级上下文恢复并无缝衔接后续开发！**

---

## 一、新对话快速唤醒指南 (AI Agent Onboarding)

当在新的对话窗口中开启工作时，AI 助手只需按顺序执行以下 3 步即可完整接管项目：
1. **查阅本文档 (`progress.md`)**：掌握最新已完成功能、底层数据结构与未尽待办；
2. **确认文件对应关系**：
   - 核心开发文件：`d:\Document\Project\Pilgrimage to the West\trip-map\index.html`
   - 根目录镜像文件：`d:\Document\Project\Pilgrimage to the West\index.html`
   - 二级探索知识库：`d:\Document\Project\Pilgrimage to the West\路书第二层级规划.md`
3. **验证与部署规范**：
   - 桌面/移动端预览：使用 Chrome DevTools MCP（移动端建议模拟 `390×844`, `deviceScaleFactor: 3`, `hasTouch: true`）；
   - 代码同步铁律：修改 `trip-map/index.html` 后，**必须执行命令强制同步至根目录 `index.html`**，保持字节大小 100% 一致：
     ```powershell
     Copy-Item -Path "trip-map\index.html" -Destination "index.html" -Force
     ```
   - 自动化部署铁律：自动执行 Git 提交并推送到远端 `origin main`，触发 Cloudflare Pages (`https://trip-cts.pages.dev`) 自动化构建与秒级全球上线：
     ```powershell
     git add .
     git commit -m "feat/fix: <简要改动说明>"
     git push origin main
     ```

---

## 二、高德开放平台凭证与地图配置 (Official Credentials)

本项目已正式接入高德开放平台 Web 端 JS API v2.0，所有凭据已完成实机联动测试：

| 配置项 | 官方参数值 | 说明与代码嵌入位置 |
| :--- | :--- | :--- |
| **服务平台** | `Web端 (JS API)` | 支持 `AMap.Map`、`AMap.Driving`、`AMap.TileLayer` 与 `AMap.Geolocation` |
| **Web端 Key** | `15d8ab014e31b56f285e8425bf05e78f` | `<script src="https://webapi.amap.com/maps?v=2.0&key=..."></script>` |
| **安全密钥 securityJsCode** | `bbeb02ef5fd2ffb3079e5c8cdbbdb165` | **必须在加载高德地图脚本前注入**，挂载于 `window._AMapSecurityConfig` |
| **搭载插件** | `AMap.Driving, AMap.Scale, AMap.ToolBar, AMap.Geolocation` | 作为 URL 参数一次性引入 |
| **生产白名单** | 留空（全域免鉴权直开） | 允许本地 `file://`、`localhost`、局域网及 `trip-cts.pages.dev` 访问 |

### 代码标准注入代码段
```html
<script>
  window._AMapSecurityConfig = {
    securityJsCode: 'bbeb02ef5fd2ffb3079e5c8cdbbdb165'
  };
</script>
<script src="https://webapi.amap.com/maps?v=2.0&key=15d8ab014e31b56f285e8425bf05e78f&plugin=AMap.Driving,AMap.Scale,AMap.ToolBar,AMap.Geolocation"></script>
```

---

## 三、文件组织体系与双向同步原则

```text
Pilgrimage to the West/
├── trip-map/
│   ├── assets/             ← 本地静态图标与媒体资源
│   └── index.html          ← 【主生产文件】包含完整 HTML/CSS/JS/数据源，部署时上传此文件夹
├── index.html              ← 【根目录镜像】与 trip-map/index.html 字节级 100% 相同，双击直开
├── progress.md             ← 【阶段记忆与开发手册】唯一进度基准文档（本文档）
└── 路书第二层级规划.md     ← 【知识库】Day 0 ~ Day 8 苍蝇馆/公路观景台/机位/高德导航数据集
```

> ⚠️ **双向同步命令（PowerShell）**：
> ```powershell
> Copy-Item -Path "trip-map\index.html" -Destination "index.html" -Force
> ```

---

## 四、全量功能与最新架构解析

### 4.1 苹果液态玻璃（Liquid Glass）视觉系统与五层层级架构
整个应用采用全屏满铺地图，界面控件悬浮于上层，形成清透的景深与层级：
- **Layer 0（底图层）**：全屏尺寸 `amap-container`，地图 100% 满铺，下潜于所有控件之下；
- **Layer 1（悬浮控制层）**：
  - 顶部 Header 悬浮岛（`rgba(20, 13, 7, 0.58)` + `blur(24px)`）
  - 日程切换药丸横向滑动条（`rgba(255, 255, 255, 0.08)`）
  - 右侧悬浮垂直玻璃 Dock（`✨`二级图钉开关、`📍`自驾轨迹开关、`🛰️`卫星图层切换、`🎯`视野居中）
  - 底部路线信息胶囊条（`rgba(30, 20, 10, 0.55)` + `blur(20px)`）
- **Layer 2（底部 Dock 导航栏）**：iOS 悬浮磨砂玻璃 Dock，实现路书、地图、贴士三 Tab 平滑切换；
- **Layer 3（二级点位定制玻璃信息窗 `l2-map-infowindow`）**：暗曜石液态玻璃微气泡，带分类标签、考斯特通达性标识、高德导航与深度攻略跳转按钮；
- **Layer 4（半屏深度攻略抽屉 `bottom-sheet-modal`）**：48%~68% 渐变高透磨砂玻璃，顶部区域 100% 透明展示地图，下方展示完整攻略长图文。

---

### 4.2 标签一：【📅 行程路书 (Schedule)】
1. **9 天时间轴全览 (Day 0 ~ Day 8)**：
   - 兰州集结 ➔ 七彩丹霞 ➔ 鼎新基地 ➔ 东风航天城 ➔ 额济纳怪树林 ➔ 嘉峪关 ➔ 瓜州 ➔ 敦煌莫高窟 ➔ 翻越当金山 ➔ 柴达木盆地翡翠湖 ➔ 茶卡盐湖 ➔ 青海湖 ➔ 塔尔寺/西宁；
2. **打卡状态持久化**：
   - 卡片右上角打卡按钮，点击后保存至 `localStorage("xy_trip_checkins")`，顶部动态展示打卡进度条百分比；
3. **路书与地图一键联动**：
   - 卡片底部【🗺️ 地图查看路线】按钮，点击后自动切换至地图 Tab 并定位到对应天数的专属路线。

---

### 4.3 标签二：【🗺 路线地图 (Trip Map)】

#### 1. 默认底图与卫星切换
- **默认底图**：高德浅色标准矢量地图（`amap://styles/normal`，白底白天公路网），省市行政区划与国道高速脉络最清晰；
- **卫星图按需切换**：右侧第 3 个按钮 `🛰️` 挂载 `AMap.TileLayer.Satellite` 与 `AMap.TileLayer.RoadNet`，一键在大漠卫星实景与浅色公路图之间无缝切换。

#### 2. 真实公路轨迹绘制（Apple Maps 电光蓝导航设计）
- **告别生硬粗折线**：调用 `AMap.Driving` 沿真实 G30 连霍高速、敦当高速、德小高速贴地拟合；
- **双层光晕高对比度**：
  - 底层：液态玻璃电光蓝柔和光晕（`#0284c7`，线宽 9~12px，透明度 0.32~0.42）；
  - 表层：高对比电光天蓝实线（`#0091ff`，线宽 4.5~6px，带 1.5~2px 纯白晶体描边 `#ffffff`）；
  - **彻底解决与国道黄色背景线撞色的问题**，无论在浅色矢量图还是深色卫星图上均极度醒目。
- **全览尺度防文字堆叠**：
  - 全览仅展示 12 大地理枢纽城市药丸（`hub-marker-pill`：兰州、张掖、酒泉、航天城、额济纳等）；
  - 细分景点以星芒微光点（`starlight-marker-dot`）精致呈现，单天模式展开完整标签。

#### 3. 32 个二级探索点位（Level-2 Exploration Pins）
- 涵盖 Day 0 ~ Day 8 沿途 32 个实测点位：
  - 🥢 苍蝇馆美食（正宁路老马爷醪糟、大胡子烤肉、磨沟沿牛肉面、张掖炒炮、大柴旦炕锅羊肉等）
  - 🔭 绝美公路观景点（乌鞘岭垭口、当金山 3648m 垭口等）
  - 🚀 航天城机位（东风礼堂、问天阁出征机位）
  - 📸 摄影打卡点（瓜州大地之子、汉武雄风、怪树林枯木日落）
  - 💡 秘籍与行前避坑（大柴旦翡翠湖小火车动线、青海湖二郎剑等）
- **状态控制**：右侧第 1 个按钮 `✨` 一键展开/隐藏，默认精简隐藏保持地图清爽。

#### 4. 二级图钉防闪退四维架构（关键 Bug 根治）
- **现象**：之前版本点击二级图钉后，信息窗一闪而过瞬间消失；
- **根因**：AMap 2.0 点击 Marker 时触发 `marker.on('click')` 后，原生点击事件与内部手势在 0~5ms 内冒泡触发了 `mapInstance.on('click')` 与容器点击，无条件触发 `closeL2InfoWindow()`；
- **四维防护措施**：
  1. **时间戳保护阀**：打开信息窗时记录 `lastInfoWindowOpenTime = Date.now()`，400ms 内的关闭调用一律拦截；
  2. **事件传播阻断**：Marker 点击执行 `e.originEvent.stopPropagation()`，卡片容器绑定 `onclick="event.stopPropagation()"`；
  3. **InfoWindow 原生解耦**：配置 `autoMove: false`（防止地图微调触发移动）与 `closeWhenClickMap: false`；
  4. **受控关闭**：点击右上角 `✕` 传 `force: true` 立即关闭；400ms 后点击地图纯空白区域自然平滑关闭。

#### 5. 实时定位我在哪（极简单行胶囊）
- 接入 `AMap.Geolocation`，高精度雷达呼吸蓝点；
- 自动计算并显示距离最近行程景点的公路距离（`📍 当前位置 | 距「XXX」约 XX km`）；
- 单行防折行排版，手指触摸或拖动地图时立即自动消失，3.5 秒自动淡出。

---

### 4.4 标签三：【⚠️ 贴士备忘与团队工具】
1. **重要纪律与安全警示**：航天城与鼎新基地身份证随身携带、军工禁区严禁航拍无人机、莫高窟 A 类票预约政策、柴达木无人区满油备水与高反防晒；
2. **行前行李打勾清单**：证件资金、户外穿戴、医疗防干燥 3 大类，点击状态持久化存储；
3. **考斯特团队公共 AA 记账器**：
   - 支持新增/删除公共账目（加油、餐饮、景区门票、过路费等）；
   - 自定义同行分摊人数（默认 10 人，`+/-` 实时计算每人人均应摊金额）；
   - **一键复制微信群格式文本**：格式化生成团队 AA 公示文本，直接粘贴至微信群。

---

### 4.5 深度攻略半屏悬浮抽屉 (Bottom Sheet Modal)
- **触发方式**：在路书节点点击胶囊，或在地图二级图钉信息窗中点击【📖 深度攻略 ➔】；
- **内容呈现**：
  - 深度文化风味导读背景；
  - 招牌必吃 / 必打卡体验清单；
  - 参考价格标准；
  - **🚌 考斯特通达性真实指南**（明确标注是大巴直达停靠还是深巷建议打车分乘）；
  - **🧭 高德地图一键导航 Universal Link**：
    `https://uri.amap.com/marker?position={lng},{lat}&name={name}&coordinate=gaode&callnative=1`
    手机浏览器点击后可直接唤起已安装的高德地图 App 开启自驾导航。

---

## 五、发布与持续部署实战 (CI/CD Deployment Runbook)

### 5.1 正式生产环境配置
- **托管与边缘网络**：Cloudflare Pages
- **正式生产发布地址**：👉 **`https://trip-cts.pages.dev`**
- **关联 GitHub 仓库**：`JohnMaxwell0123/Trip` (分支: `main`)
- **技术优势**：纯静态全球 CDN 边缘节点直连，彻底规避大陆境内访问未备案域名的 `401 Unauthorized` 拦截，秒级加载无任何白屏等待。

### 5.2 全自动 CI/CD 发布规程
本项目已彻底告别手动打包与拖拽上传：
1. 本地代码修改自测完成后，Agent 自动执行镜像同步：`Copy-Item trip-map\index.html -> index.html`；
2. 自动提交并推送到远端：`git push origin main`；
3. Cloudflare Pages 自动接收 Webhook 并在 15 秒内构建部署生效至全球边缘节点；
4. 构建参数规范：
   - 框架预设：`None`
   - 构建命令：留空（无需打包）
   - 构建输出目录：`trip-map`
   - 生产分支：`main`

---

## 六、阶段开发记录与未来规划 (Stage Log & Roadmap)

### 6.1 阶段里程碑记录 (Changelog)
- **v1.0 (初始版本)**：
  - 搭建 9 天行程路书与基础自驾轨迹；
  - 引入苹果液态玻璃 UI 规范。
- **v2.0 (高德原生引擎升级与 EdgeOne 踩坑迁移)**：
  - 申请并规范接入高德开放平台 JS API 2.0 与安全密钥；
  - 废弃腾讯云 EdgeOne（解决 401 报错），正式上线 Cloudflare Pages (`journeytothewest.pages.dev`)；
  - 落地行前行李清单与考斯特团队公共 AA 记账器。
- **v2.5 (大环线视觉与二级探索全面重构)**：
  - **真实公路轨迹革新**：摒弃粗黄线，升级为苹果地图电光蓝高对比导航流光线（`#0091ff` + `#ffffff` 描边）；
  - **全览防堆叠体系**：12 大核心枢纽城市药丸徽章 + 细分景点星芒微光点；
  - **32 个二级点位上图**：美食、观景台、航天城机位全要素挂载，支持浮动按钮 `✨` 展开/隐藏；
  - **底图偏好调优**：默认采用高德浅色标准公路矢量图，高清卫星实景图（`AMap.TileLayer.Satellite`）作为悬浮按钮 `🛰️` 随时切换；
  - **五层液态玻璃透明度重塑**：地图满铺，顶部全透悬浮，底部抽屉半透磨砂，视觉层次更通透；
  - **二级图钉闪退彻底根治**：建立时间戳防抖（400ms）、事件传播阻断、InfoWindow 配置解耦与受控关闭体系。
- **v2.6 (二级探索知识库与元数据库重构)**：
  - 全面重构并升级 [`路书第二层级规划.md`](file:///d:/Document/Project/Pilgrimage%20to%20the%20West/路书第二层级规划.md)；
  - 角色由纯文本指南升级为【路书半屏抽屉长图文 + 路线地图二级图钉（Level-2 Exploration Pins）的统一元数据库】；
  - 梳理并建立全量 32 个二级点位（包含代码 Key、分类 Emoji、GCJ-02 经纬度坐标、考斯特通达性、高德导航直达链接）速查总表；
  - 数据与 `trip-map/index.html` 中的 `DAY_DETAILS` 达成 100% 精确映射，规范后续增删改点位操作规程。
- **v2.7 (从路书跳转地图卡死与悬浮按钮失效根治)**：
  - **根因深度溯源**：
    1. **CSS `transform` 破坏 `position: fixed`**：`.tab-view` 包含 `animation: viewFadeIn ... forwards`，保留了 `transform: translateY(0)`。CSS 规范规定带 `transform` 的元素会沦为包含块，使子级 `#view-map` 失去视口固定定位，在路书页面滚动（如滚至 Day 1）后跳转导致其点击/触摸命中盒（Hit-testing Box）严重脱节偏离；
    2. **滚动冲突与触摸挂起**：切换 Tab 原使用 `behavior: "smooth"` 平滑滚动，在移动端触摸屏上会挂起并拦截所有点击/拖拽手势，且地图模式下未锁定 `body` 滚动导致拖拽被页面捕获；
    3. **初始化并发覆盖竞态 (Race Condition)**：`viewDayOnMap` 触发地图首次加载时，`initMap` 内部异步完成 `AMap.Driving` 插件加载后无条件执行 `renderMapDayView(-1)`，强行把请求的单日视图重置覆盖为全程总览，导致路线、高斯模糊覆盖物与图层状态错乱；
    4. **单日视野自适应污染**：`fitMapFullView` 在单天模式下将包含全程 8 天的底线 `bgLine` 一并传入 `setFitView`，导致镜头异常缩放至全局大尺度。
  - **核心技术重构决策**：
    1. **层级与动画解耦**：`#view-map` 显式声明 `animation: none !important; transform: none !important; touch-action: none;`，恢复纯净的视口固定定位；
    2. **地图模式锁定与瞬间滚回**：切入地图时为 `body` 注入 `map-mode`（`overflow: hidden !important; touch-action: none;`），且使用 `window.scrollTo(0, 0)` 瞬间归位，杜绝手势被平滑滚动挂起；
    3. **初始化队列与优先单天渲染**：重构 `ensureMapInit` 与 `initMap`，支持排队回调机制，优先保障单日渲染指令，并在异步插件就绪时杜绝无脑覆盖；
    4. **单日高光轨迹聚焦**：引入 `currentDayActiveLine` 独立引用，单天模式下仅自适应单日公路高光线与对应景点，视野精准居中，操作行云流水。

- **v2.8 (CI/CD 自动化构建与 GitHub 仓库全链路打通)**：
  - **集中式旅行路书仓库确立 (Monorepo)**：正式绑定 GitHub 远端仓库 `JohnMaxwell0123/Trip`（主分支 `main`），规划全集旅行自驾路书宇宙，首发核心项目为西行丝路；
  - **根目录导航与防混淆规范**：建立工程级 `README.md` 与 `.gitignore`，全面厘清单文件 SPA 架构、资源镜像关系与未来多项目子目录演进标准；
  - **Cloudflare Pages Git 持续集成流水线**：打通 GitHub ➔ Cloudflare Pages 自动构建 Webhook，免去手动拖拽文件夹上传的旧模式（正式站点：`https://trip-cts.pages.dev`，零构建配置：Build command 留空，输出目录 `trip-map`，构建耗时仅约 15 秒）；
  - **Agent 自动提交与远端推送铁律**：在 `GEMINI.md` 固化「代码改动 ➔ 镜像同步 ➔ progress.md 记录 ➔ git push 触发上线」四步一体自动化闭环。
- **v2.9 (全机型/触摸屏手势与横向胶囊滚动彻底解耦，根治地图无法拖动)**：
  - **线上环境诊断**：确认 `journeytothewest.pages.dev` 此前仍停留在手动拖拽部署的旧包，未生效 v2.7 补丁，导致用户访问线上旧版时依旧触发 Bug；
  - **CSS 触摸手势阻断清除**：移除了 `#view-map`、`#amap-container` 与 `body.map-mode` 上的 `touch-action: none` 与 `height: 100vh !important`，交还高德原生引擎的触摸与双指缩放手势判定，解决 WebKit/移动浏览器下全局手势被吃掉的问题；
  - **横向胶囊容器滚动隔离**：将原 `targetBtn.scrollIntoView()` 彻底重构为独立容器位移 `pillsContainer.scrollTo({ left: ... })`，根除 `scrollIntoView` 冒泡导致外层祖先视口产生隐式偏移的顽疾；
  - **Tab 与单日模式单一数据流**：重构 `switchTab(1, btn, dayIndex)`，切入地图前优先彻底重置 `window.scrollTo(0, 0)`、`document.documentElement.scrollTop = 0`、`document.body.scrollTop = 0`，并将单日索引直通传递，彻底消灭初始化竞态。
- **v3.0 (二次切入地图卡死与 Pixel NaN 致命异常根治)**：
  - **现象溯源**：用户从行程路书首次点击“地图查看路线”时正常，但切换回行程路书、再次返回路线地图（无论通过底部 Dock 还是再次点击其他天查看路线）后，地图彻底卡死无法拖拽、缩放；
  - **深层根因定位 (Stack Trace 铁证)**：
    1. **`display: none` 摧毁地图几何尺寸**：`#view-map` 原隶属于 `.tab-view`，离开地图 Tab 时无条件被赋予 `display: none`，导致内部 `#amap-container` 的宽和高瞬间塌陷为 `0×0`（`getBoundingClientRect` 均为 0）；
    2. **滚动监听触发致命投射异常**：高德地图 AMap 2.0 在 `window` 上挂载了全局 `scroll` 监听以便联动更新覆盖物坐标。当用户在行程路书页面滚动长列表时，AMap 内部触发 `updateOverlay` ➔ `lngLatToContainer`；
    3. **`Pixel(NaN, NaN)` 抛出未捕获异常**：因地图容器长宽为 0，高德相机投影矩阵计算得出 `0/0 = NaN`，执行 `new AMap.Pixel(NaN, NaN)` 触发源码防御检测，直接抛出 `Uncaught Error: Invalid Object: Pixel(NaN, NaN)`；
    4. **事件与渲染循环永久阵亡**：该未捕获异常发生在高德地图的 `requestAnimationFrame` 核心帧循环中，导致整个 AMap 渲染与手势交互流水线彻底崩溃，第二次返回地图时即使容器恢复显示，底层事件循环早已死亡。
  - **四重系统化根治措施**：
    1. **CSS 维度彻底解耦 `display: none`**：为 `#view-map` 声明 `display: block !important; visibility: hidden; opacity: 0; pointer-events: none; z-index: -10;`，激活时赋予 `visibility: visible; opacity: 1; pointer-events: auto; z-index: 10;`。使地图容器几何物理尺寸全时保持 `100vw × 100vh`，从物理根源上彻底消灭投影矩阵除以 0 产生 `NaN` 的条件；
    2. **行程路书浏览位置记忆恢复**：切出路书时记录当前阅读滚动深度 `scheduleScrollY`，切回路书时通过 `requestAnimationFrame` 自动平滑恢复，避免每次返回路书都被强制踢回顶部；
    3. **手势挂起清除与状态重置强保障**：在 `renderMapDayView` 与 `switchTab(1)` 入口处显式注入 `mapInstance.setStatus({ dragEnable: true, zoomEnable: true })`，并调用 `fitMapFullView()` 确保镜头自动居中；
    4. **胶囊滑块横向位移优化**：将 `viewDayOnMap` 联动胶囊栏的滑动行为由容易在切页瞬间挂起手势的 `behavior: 'smooth'` 改为即时到位的 `behavior: 'auto'`，杜绝移动端事件拦截。

### 6.2 阶段记忆更新机制 (Stage Memory Rule)
**【开发纪律铁律】**：
在未来的每次开发会话中，每当完成一个功能点、Bug 修复或设计迭代：
1. 立即在此 `progress.md` 对应的章节（如“阶段里程碑记录”或相应功能点）追加技术记录与决策；
2. 确保随后的新会话通过直接阅读此文件，即刻无缝衔接最新状态。

### 6.3 后续潜在迭代方向 (Roadmap)
1. **PWA 离线支持 (Service Worker)**：为青海湖及柴达木部分弱网路段增加离线地图切片与离线路书缓存；
2. **多日天气/风沙预警联动**：接入甘肃/青海沿途城市降水与大风降温实时天气 API；
3. **团队位置共享预留**：预留多人位置信标接口或微信小程序桥接；
4. **多旅行项目 Portal 门户页**：未来新增旅行计划时，在根目录上线精美自驾足迹卡片总览大厅。

