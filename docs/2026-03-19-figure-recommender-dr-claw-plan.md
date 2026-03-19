# Figure Recommender 升级为科研出图 Codegen Skill，并优先适配 Dr. Claw

## 摘要

- 保留单一 skill 形态，升级 `figure-recommender` 为“接收结构化 `figure_brief` -> 选图 -> 选配色 -> 生成 Python 绘图代码”的完整能力。
- 代码生成策略锁定为“模板驱动分层支持”：
  - Tier 1：高频图直接输出可运行代码
  - Tier 2：可推荐但不保证直接生成代码
  - Tier 3：高复杂或风格型图只做建议或明确不推荐
- Dr. Claw 只做轻量接入，不新增 stage，只挂到 experiment-analysis 和 publication-writing 的任务推荐中。
- 分发主轴是独立 zip skill 包，可被 Dr. Claw 一键导入，也能被普通用户手动安装。

## 关键变更

- skill 输入契约升级为结构化 `figure_brief`，最少包含：
  - `id`
  - `story_goal`
  - `data_shape`
  - `field_mapping`
  - `figure_role`
  - `style_mode`
  - `palette_mode`
  - 可选 `candidate_chart_types`
  - 可选 `notes`
- skill 输出契约固定为 6 段：
  - `Primary figure`
  - `Optional fallback`
  - `Palette`
  - `Dependencies`
  - `Python code`
  - `Adaptation notes`
- chart mapping 升级成 registry，记录：
  - `chart_id`
  - `support_level`
  - `source_notebook`
  - `backend`
  - `required_fields`
  - `template_file`
  - `palette_modes`
  - `fallback_chart`
- v1 只做 8 个 Tier 1 图种直接 codegen：
  - 对比点图
  - 堆叠柱状图
  - 云雨图
  - 折线图
  - 多变量变化趋势图
  - 热力图
  - 散点图 + 误差棒
  - 相关性网络热图
- backend 白名单：
  - 默认 `matplotlib + seaborn + pandas + numpy`
  - 网络图允许纯 `matplotlib` 实现
  - v1 不把 `plotly`、`pycirclize`、`shap` 作为直接 codegen 主路线
- notebook 资产处理：
  - 原始 `.ipynb` 保留为来源资产
  - 开发期抽取为 skill 内部 `.py` 模板
  - 运行期只依赖 skill 包内模板
  - 不依赖 `nbconvert`
- 配色固定 5 套：
  - `paper-neutral`
  - `paper-emphasis`
  - `sequential`
  - `diverging`
  - `presentation-bold`
- 分发包固定目录：
  - `SKILL.md`
  - `references/`
  - `templates/`
  - `examples/`
  - `scripts/`

## 测试方案

- 建立中英文兼容的 `figure_brief` fixtures，覆盖：
  - 组间差异
  - 组成占比
  - 分布
  - 趋势
  - 矩阵
  - benchmark
  - 网络
  - 主图与补充图
- 对每个 Tier 1 图种做 smoke test：
  - 输出代码语法可过
  - dummy dataframe 可跑通
  - import 完整
  - 占位字段全部替换
- fallback 逻辑验证：
  - 未支持复杂图要明确说明推荐成立但 codegen 未支持
  - 必须回退到最近的 Tier 1 模板或只给实现建议
  - 不允许编造不可运行代码
- 分发验证：
  - zip 结构可被 Dr. Claw 的 skill zip 规则接受
  - 导入后能被发现
  - publication 和 analysis 任务会推荐该 skill
