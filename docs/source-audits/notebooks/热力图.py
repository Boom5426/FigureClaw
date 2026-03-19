# Generated from a source notebook for audit and review purposes.

# --- cell 1: code ---
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# 示例数据框: MAP 
data = {
    'λ_2': [1, 1, 1, 1, 1, 10, 10, 10, 10, 10, 100, 100, 100, 100, 100, 1000, 1000, 1000, 1000, 1000, 10000, 10000, 10000, 10000, 10000],
    'λ_3': [1, 10, 100, 1000, 10000, 1, 10, 100, 1000, 10000, 1, 10, 100, 1000, 10000, 1, 10, 100, 1000, 10000, 1, 10, 100, 1000, 10000],
    'performance': [0.082, 0.086, 0.084, 0.085, 0.081, 
                    0.085, 0.087, 0.088, 0.085, 0.088, 
                    0.09, 0.091, 0.089, 0.09, 0.088, 
                    0.092, 0.093, 0.091, 0.09, 0.091,
                    0.091, 0.092, 0.089, 0.084, 0.085
                    ]
}

df = pd.DataFrame(data)

# 使用 pivot_table 创建透视表
pivot_df = df.pivot_table(values='performance', index='λ_2', columns='λ_3')

# 自定义颜色映射
# custom_cmap = sns.color_palette("Paired", as_cmap=True)
custom_cmap = sns.cubehelix_palette(start=0.5, rot=-0.75, light=0.85, dark=0.35, as_cmap=True)
# 颜色候选：
# sns.set_palette("colorblind")
# sns.set_palette("Set2")
# sns.set_palette("Paired")
# custom_cmap = sns.cubehelix_palette(start=0.5, rot=-0.75, light=0.85, dark=0.15, as_cmap=True)

# 绘制热力图
plt.figure(figsize=(10, 8))
heatmap = sns.heatmap(pivot_df, annot=True, cmap=custom_cmap, annot_kws={"size": 20})
# sns.heatmap(pivot_df, annot=True, cmap=custom_cmap, annot_kws={"size": 20})

# 设置标题和标签的字体大小
plt.title('Mean Average Precision (MAP)', fontsize=24) # values while Keeping λ₁ constant varying λ₃ and λ₂
plt.xlabel('λ₃', fontsize=26)
plt.ylabel('λ₂', fontsize=26)

# 设置刻度标签的字体大小
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

# 设置颜色棒的字体大小
cbar = heatmap.collections[0].colorbar
cbar.ax.tick_params(labelsize=20)

plt.tight_layout()
# plt.savefig("2e_MAP.pdf", dpi=300)
plt.show()
