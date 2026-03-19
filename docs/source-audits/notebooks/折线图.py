# Generated from a source notebook for audit and review purposes.

# --- cell 1: code ---
import matplotlib.pyplot as plt
import numpy as np

# 数据
positions = ['Recall@1', 'Recall@3', 'Recall@5', 'Recall@10']
method1 = [0.041, 0.087, 0.121, 0.182]  # PhenoProfiler
method2 = [0.032, 0.071, 0.108, 0.155]  # DeepProfiler
method3 = [0.032, 0.062, 0.093, 0.134]  # ResNet50
method4 = [0.021, 0.053, 0.080, 0.119]  # ViT
method5 = [0.018, 0.050, 0.072, 0.117]  # OpenPhenom
method6 = [0.009, 0.029, 0.049, 0.099]  # Baseline

methods = ['PhenoProfiler', 'DeepProfiler', 'ResNet50', 'ViT', 'OpenPhenom', 'Baseline']

#  colors = ['#E64B35B2', '#3C5488B2', '#00A087B2', '#91D1C2B2', '#D4B9DA', "#78617E"]
colors = ['#E64B35B2', '#3C5488B2', '#00A087B2', '#91D1C2B2', '#D4B9DA', "#78617E"]
# colors = ['red', 'purple', 'mediumseagreen', 'cornflowerblue']

# 绘制图表
plt.figure(figsize=(10, 6))

plt.plot(positions, method1, marker='s', linestyle='-', color=colors[0], label=methods[0], markersize=12)
plt.plot(positions, method2, marker='o', linestyle='-', color=colors[1], label=methods[1], markersize=12)
plt.plot(positions, method3, marker='^', linestyle='-', color=colors[2], label=methods[2], markersize=12)
plt.plot(positions, method4, marker='d', linestyle='-', color=colors[3], label=methods[3], markersize=12)
plt.plot(positions, method5, marker='v', linestyle='-', color=colors[4], label=methods[4], markersize=12)
plt.plot(positions, method6, marker='+', linestyle='-', color=colors[5], label=methods[5], markersize=12)

# 添加标题和标签
plt.title('BBBC022', fontsize=26)
plt.xlabel('Top Percentage (%)', fontsize=24)
plt.ylabel('Average Recallall', fontsize=24)

# 添加网格
plt.grid(True, linestyle='--', alpha=0.7)

# 添加图例，并设置字体大小为20
legend = plt.legend(fontsize=18)

# 为图例中的每个文本设置对应的颜色
for text, color in zip(legend.get_texts(), colors):
    text.set_color(color)

# 自定义刻度
plt.xticks(positions, fontsize=20)
plt.yticks(np.linspace(0, 0.2, 5), fontsize=20)

# 保存高分辨率图像
plt.tight_layout()
# plt.savefig('2b_022_pert.pdf', dpi=300)

# 显示图表
plt.show()
