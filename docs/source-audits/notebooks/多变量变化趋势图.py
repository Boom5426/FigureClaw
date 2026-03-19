# Generated from a source notebook for audit and review purposes.

# --- cell 1: markdown ---
# ## 经济体GDP趋势图: 该图展示了五个主要经济体自1960年以来的GDP变化趋势。通过重叠面积图，可以直观地比较各个国家的GDP如何随着时间的推移发生变化
# ## 可以用来展示不同变量随着某一因素的变化趋势

# --- cell 2: code ---
import matplotlib.pyplot as plt
import pandas as pd

# 设置样式
try:
    plt.style.use("scatter.mplstyle")
except:
    pass
# 使用Nature常用的无衬线字体，Ubuntu系统兼容
plt.rcParams["font.sans-serif"] = ["Liberation Sans", "Arial", "Helvetica", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

# --- cell 3: code ---

# 自定义样式
plt.rcParams["grid.color"] = "#fed2d2"
plt.rcParams["figure.facecolor"] = "#ffffff"
plt.rcParams["axes.facecolor"] = "#f1f5f9"
plt.rcParams["axes.edgecolor"] = "#ffffff"
plt.rcParams["axes.labelcolor"] = "#515a85"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["text.color"] = "#515a85"
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["xtick.color"] = "#515a85"
plt.rcParams["ytick.color"] = "#515a85"
plt.rcParams["legend.edgecolor"] = "#f1f5f9"

# --- cell 4: code ---
# # 读取 GDP 数据集(如果你有)
# file_path = "gdp_csv.csv"  # 替换为实际文件路径
# gdp_data = pd.read_csv(file_path)

# # 显示数据集的前几行，了解其结构（可选，运行时可注释）
# # print(gdp_data.head())

# # 手动选择 GDP 排名前五的国家
# top_5_actual_countries = ["United States", "China", "Japan", "Germany", "India"]

# # 筛选出这些国家的数据
# gdp_top_5_actual = gdp_data[gdp_data["Country Name"].isin(top_5_actual_countries)]

# # 将数据转置，年份作为行，国家作为列
# gdp_top_5_actual_pivoted = gdp_top_5_actual.pivot(
#     index="Year", 
#     columns="Country Name", 
#     values="Value"
# )

# # 绘制重叠区域图
# fig, ax = plt.subplots(figsize=(8, 5))

# # 定义颜色
# color = ["#c1e4dd", "#a1d2d4", "#85c3ca", "#64b2c3", "#4796b7"]

# zorder = 0
# # 绘制每个国家的 GDP 重叠区域图 + 折线
# for country in top_5_actual_countries:
#     # 绘制区域填充
#     ax.fill_between(
#         gdp_top_5_actual_pivoted.index,  # 年份
#         gdp_top_5_actual_pivoted[country] * 1e-12,  # GDP 转换为万亿美元
#         alpha=0.5,
#         zorder=zorder,
#         color=color[zorder],
#         label=country,
#     )
#     # 绘制折线
#     ax.plot(
#         gdp_top_5_actual_pivoted.index,
#         gdp_top_5_actual_pivoted[country] * 1e-12,
#         zorder=zorder,
#         color=color[zorder],
#         linewidth=0.5,
#     )
#     zorder += 1

# # 手动添加国家名称标注（需根据数据调整坐标）
# ax.text(2005, 11, top_5_actual_countries[0], ha="left", va="center", zorder=10)
# ax.text(2012, 7.5, top_5_actual_countries[1], ha="left", va="center", zorder=10)
# ax.text(2000, 2.8, top_5_actual_countries[2], ha="left", va="center", zorder=10)
# ax.text(2005, 2.0, top_5_actual_countries[3], ha="left", va="center", zorder=10)
# ax.text(2013, 0.5, top_5_actual_countries[4], ha="left", va="center", zorder=10)

# # 设置标签和标题
# ax.set_ylabel("GDP（万亿美元）")
# ax.set_title(
#     "五大经济体 GDP 变化趋势图", 
#     fontsize=24, 
#     x=0.065, 
#     y=0.85, 
#     ha="left", 
#     va="top"
# )

# # 设置 X 轴刻度和范围
# ax.set_xticks(range(1960, 2016, 5))
# ax.set_xlim(1960, 2016)

# # 设置 Y 轴范围
# ax.set_ylim(0, 20)

# # 设置图例
# ax.legend(
#     loc="upper left", 
#     bbox_to_anchor=(0.05, 0.80), 
#     ncols=3
# )

# # 优化布局并显示
# plt.tight_layout()
# plt.show()


# --- cell 5: code ---
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------
# 第一步：生成虚拟GDP数据集（保持不变）
# ------------------------------------------------------------------------------
countries = ["United States", "China", "Japan", "Germany", "India"]
years = np.arange(1960, 2016)
np.random.seed(42)

gdp_data_list = []
for country in countries:
    for year in years:
        year_diff = year - 1960
        
        if country == "United States":
            base_gdp = 5.4e11
            growth = 3.2e9 * year_diff + 1.2e7 * (year_diff ** 1.8)
            gdp = base_gdp + growth + np.random.normal(0, 5e10, 1)[0]
        
        elif country == "China":
            base_gdp = 1.45e11
            if year < 2000:
                growth = 8e8 * year_diff + 1e6 * (year_diff ** 1.5)
            else:
                growth = 8e8 * 40 + 1e6 * (40 ** 1.5) + 1.5e10 * (year - 2000)
            gdp = base_gdp + growth + np.random.normal(0, 8e10, 1)[0]
        
        elif country == "Japan":
            base_gdp = 4.4e10
            if year < 1990:
                growth = 1.8e9 * year_diff + 3e7 * (year_diff ** 1.6)
            else:
                growth = 1.8e9 * 30 + 3e7 * (30 ** 1.6) + 2.5e8 * (year - 1990)
            gdp = base_gdp + growth + np.random.normal(0, 3e10, 1)[0]
        
        elif country == "Germany":
            base_gdp = 8.3e10
            growth = 1.1e9 * year_diff + 5e6 * (year_diff ** 1.7)
            gdp = base_gdp + growth + np.random.normal(0, 2.5e10, 1)[0]
        
        elif country == "India":
            base_gdp = 3.7e10
            if year < 1990:
                growth = 3e8 * year_diff + 8e5 * (year_diff ** 1.4)
            else:
                growth = 3e8 * 30 + 8e5 * (30 ** 1.4) + 4.5e9 * (year - 1990)
            gdp = base_gdp + growth + np.random.normal(0, 2e10, 1)[0]
        
        gdp = max(gdp, 1e9)
        gdp_data_list.append({
            "Country Name": country,
            "Year": year,
            "Value": gdp
        })

gdp_data = pd.DataFrame(gdp_data_list)

# ------------------------------------------------------------------------------
# 第二步：字体配置+绘图（移除linejoin参数，修复AttributeError）
# ------------------------------------------------------------------------------
# 1. 全局字体配置：Ubuntu兼容+Nature常用字体，无中文字体
plt.rcParams["font.sans-serif"] = ["Liberation Sans", "Arial", "Helvetica", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.size"] = 10

# 2. 数据处理（保持不变）
top_5_actual_countries = ["United States", "China", "Japan", "Germany", "India"]
gdp_top_5_actual = gdp_data[gdp_data["Country Name"].isin(top_5_actual_countries)]
gdp_top_5_actual_pivoted = gdp_top_5_actual.pivot(
    index="Year", 
    columns="Country Name", 
    values="Value"
)

# 3. 绘图（核心：移除linejoin参数，保留折线清晰显示的关键设置）
fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
color = ["#2e86ab", "#a23b72", "#f18f01", "#c73e1d", "#6a994e"]

zorder = 1
for idx, country in enumerate(top_5_actual_countries):
    # 绘制区域填充（在折线下方）
    ax.fill_between(
        gdp_top_5_actual_pivoted.index,
        gdp_top_5_actual_pivoted[country] * 1e-12,
        alpha=0.3,
        zorder=zorder - 1,
        color=color[idx],
        label=country,
    )
    # 绘制折线（移除linejoin，保留线宽2和层级设置，确保清晰）
    ax.plot(
        gdp_top_5_actual_pivoted.index,
        gdp_top_5_actual_pivoted[country] * 1e-12,
        zorder=zorder,
        color=color[idx],
        linewidth=2,  # 核心：线宽足够粗，无需linejoin也能清晰显示
    )
    zorder += 2

# 4. 国家名称标注（英文粗体，位置优化）
ax.text(2008, 16, "United States", ha="left", va="center", fontweight="bold", fontsize=11, zorder=20)
ax.text(2010, 11, "China", ha="left", va="center", fontweight="bold", fontsize=11, zorder=20)
ax.text(2000, 5.2, "Japan", ha="left", va="center", fontweight="bold", fontsize=11, zorder=20)
ax.text(2005, 3.8, "Germany", ha="left", va="center", fontweight="bold", fontsize=11, zorder=20)
ax.text(2010, 2.2, "India", ha="left", va="center", fontweight="bold", fontsize=11, zorder=20)

# 5. 标签和标题（全英文学术风格）
ax.set_ylabel("GDP (Trillion USD)", fontsize=12, fontweight="bold")
ax.set_title(
    "GDP Growth Trends of the World's Top 5 Economies (1960-2015)", 
    fontsize=16, 
    fontweight="bold",
    x=0.02, 
    y=0.98, 
    ha="left", 
    va="top"
)

# 6. 坐标轴和图例优化
ax.set_xticks(range(1960, 2020, 10))
ax.set_xlim(1959, 2016)
ax.set_ylim(0, 22)
ax.legend(
    loc="upper left", 
    bbox_to_anchor=(0.02, 0.9), 
    ncols=3,
    frameon=True,
    fancybox=True
)
ax.grid(axis="y", alpha=0.3, linestyle="--")

# 7. 显示图表
plt.tight_layout()
plt.savefig('./Fig.pdf', dpi=300, bbox_inches='tight')
plt.show()

# --- cell 6: code ---
pass
