# Chart Source Audit

This audit compares the notebooks backing the current registry against the shipped templates.

| Chart ID | Decision | Visual Grammar | Notes |
|---|---|---|---|
| `contrast_dot` | `rename` | labeled two-metric comparison scatter | The notebook called 对比点图 behaves like a labeled benchmark scatter, not a grouped category contrast-dot chart with mean and SEM overlays. |
| `stacked_bar` | `keep` | stacked categorical bar chart | The current template is a reasonable simplified version of the notebook. |
| `raincloud` | `keep` | distribution plot combining density and points | The current raincloud template preserves the core distribution-comparison semantics. |
| `line` | `keep` | ordered line chart | The template matches the source chart family closely. |
| `multi_trend` | `keep` | multi-series time trend comparison | The notebook uses heavier styling than the template, but the simplified template preserves the same broad multi-series trend story. |
| `heatmap` | `keep` | matrix heatmap | The shipped heatmap template is semantically aligned with the source notebook. |
| `benchmark_scatter_error` | `keep` | two-metric scatter with x/y error bars | The template preserves the notebook's core benchmark comparison structure. |
| `correlation_network` | `keep` | network-like relation map for weighted pairwise associations | The notebook is heavily styled, but the template still represents the same weighted relationship story. |
| `sunburst` | `demote` | hierarchical radial partition chart | The chart is conceptually valid but should remain non-default because it is not executable in the Tier 1 path. |
| `chord` | `demote` | circular flow/relation chord diagram | The chart is too style-heavy and backend-specific for the default executable-first path. |

## Extra Notebook

- `配色`: retained as a palette reference notebook for future palette reconciliation.
