# Figure Recommender Reference

This skill now targets a structured `figure_brief -> chart registry -> palette registry -> Python template` workflow.

## `figure_brief` Contract

Required fields:

- `id`
- `story_goal`
- `data_shape`
- `field_mapping`
- `figure_role`
- `style_mode`
- `palette_mode`

Optional fields:

- `candidate_chart_types`
- `notes`

Example:

```json
{
  "id": "fig-01",
  "story_goal": "compare_group_difference",
  "data_shape": "grouped_metric",
  "field_mapping": {
    "category": "condition",
    "value": "score"
  },
  "figure_role": "paper-main",
  "style_mode": "readable",
  "palette_mode": "paper-neutral"
}
```

## Selection Policy

- Prefer Tier 1 charts when they match the story goal.
- If `candidate_chart_types` names a known chart, respect it as the primary recommendation.
- If the primary chart is Tier 2 or Tier 3, keep it as the conceptual recommendation but emit fallback code from `fallback_chart`.
- If two options are equally valid, choose the simpler chart first.
- For `paper-main`, bias toward readability.
- For `slides` or `style-forward`, style-heavy options are acceptable as the primary recommendation, but only Tier 1 fallbacks get code in v1.

## Tiering

- Tier 1: direct codegen from shipped templates
  - `contrast_dot`
  - `stacked_bar`
  - `raincloud`
  - `line`
  - `multi_trend`
  - `heatmap`
  - `benchmark_scatter_error`
  - `correlation_network`
- Tier 2: recommendable, no direct codegen in v1
  - `sunburst`
- Tier 3: high-complexity or style-heavy, no direct codegen in v1
  - `chord`

## Goal-to-Chart Defaults

| Story goal | Default chart | Notebook source |
|---|---|---|
| `compare_group_difference` | `contrast_dot` | `Awesome-Scientific-Figures/对比点图.ipynb` |
| `compare_composition` | `stacked_bar` | `Awesome-Scientific-Figures/堆叠柱状图.ipynb` |
| `show_distribution` | `raincloud` | `Awesome-Scientific-Figures/云雨图.ipynb` |
| `show_trend` | `line` | `Awesome-Scientific-Figures/折线图.ipynb` |
| `show_multi_trend` | `multi_trend` | `Awesome-Scientific-Figures/多变量变化趋势图.ipynb` |
| `show_matrix_pattern` | `heatmap` | `Awesome-Scientific-Figures/热力图.ipynb` |
| `benchmark_tradeoff_with_uncertainty` | `benchmark_scatter_error` | `Awesome-Scientific-Figures/散点图_误差棒组合图.ipynb` |
| `show_network_relations` | `correlation_network` | `Awesome-Scientific-Figures/相关性网络热图.ipynb` |
| `show_hierarchy` | `sunburst` | `Awesome-Scientific-Figures/旭日图.ipynb` |
| `show_flow_relationship` | `chord` | `Awesome-Scientific-Figures/弦图.ipynb` |

## Common “Not Recommended” Cases

- Do not recommend hierarchy charts when there is no real hierarchy.
- Do not recommend circular charts when the user needs precise comparison.
- Do not recommend network charts when the graph is dense and the story lacks a focal module.
- Do not recommend bubble charts when size is decorative.
- Do not pretend unsupported charts have shipped codegen.

## Runtime Files

- `references/chart-registry.json`: chart metadata and fallback mapping
- `references/palette-registry.json`: palette metadata
- `templates/*.py.tmpl`: Tier 1 Python templates
- `scripts/generate_figure_response.py`: selector and renderer
