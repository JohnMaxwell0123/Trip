# 西行计划 · 丝路自驾路书 · 项目全局引导规则 (GEMINI.md)

每次进入此工作区开启新会话或处理任务时，请严格遵守以下自动化准则：

## 1. 项目全局进度恢复与参照
- 必须优先查阅并严格遵循 [progress.md](file:///d:/Document/Project/Pilgrimage%20to%20the%20West/progress.md) 的最新开发进度、底层数据规范与设计原则；
- 核心生产代码位于 [trip-map/index.html](file:///d:/Document/Project/Pilgrimage%20to%20the%20West/trip-map/index.html)；
- 二级探索知识库位于 [路书第二层级规划.md](file:///d:/Document/Project/Pilgrimage%20to%20the%20West/路书第二层级规划.md)。

## 2. 阶段记忆与持续更新铁律 (Stage Memory Rule)
- **每一个阶段工作（包括新功能开发、UI样式重塑、交互改进或Bug修复）完成后，必须在 [progress.md](file:///d:/Document/Project/Pilgrimage%20to%20the%20West/progress.md) 对应章节中追加记录最新状态与技术决策**；
- 确保随后的新会话通过直接阅读 `progress.md` 即可实现秒级无缝衔接，绝不遗忘历史决策。

## 3. 文件双向同步铁律 (Code Sync Rule)
- 每次对 `trip-map/index.html` 进行任何代码变动后，必须执行命令保持根目录 `index.html` 100% 字节镜像一致：
  ```powershell
  Copy-Item -Path "trip-map\index.html" -Destination "index.html" -Force
  ```

## 4. 架构与设计铁律
- **免构建单文件**：坚持单文件 HTML/CSS/JS、零后端、免打包纯静态架构，直接拖入 Cloudflare Pages 部署上线；
- **苹果液态玻璃（Liquid Glass）**：视觉体系严格遵循高斯模糊、高透磨砂折射与五层层级架构（地图全屏满铺，控件高透悬浮）；
- **高德地图规范**：基于高德 JS API 2.0，默认采用高德浅色标准公路矢量图，卫星图作为悬浮按钮 `🛰️` 随时无缝切换。
