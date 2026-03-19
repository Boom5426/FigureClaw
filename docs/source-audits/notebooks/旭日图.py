# Generated from a source notebook for audit and review purposes.

# --- cell 1: markdown ---
# ### 旭日图是一种用于展示层次结构数据的圆形可视化图表，因其形状类似太阳及其光芒而得名。它是树状图和饼图的结合体，能够直观地展示多层级数据的结构关系和数值分布~
# 	
# <!-- # 其主要优点包括：
# #  层次关系清晰：同时展示多个层级的数据结构
# #  高效利用空间：布局紧凑，适合仪表板应用
# #  交互性强：动态的旭日图支持点击展开和收缩 -->

# --- cell 2: code ---
import plotly.graph_objects as go
import pandas as pd

# --- cell 3: code ---
import pandas as pd
import plotly.graph_objects as go

### 用户配置
read_custom_data = False  # 是否读取自定义数据

if read_custom_data:
    # 读取CSV数据集
    data_df = pd.read_csv("data.csv")
else:
    # 创建随机数据集
    data = {
        'labels': [
            "A", "B", "C", "D", "E", "F", "B1", "B2", "B1-1",
            "B1-2", "B1-3", "C1", "C2", "D1", "D2", "E1",
            "E2", "E3", "E4", "E1-1", "E1-2", "E1-3", "E3-1",
            "E3-2", "F1", "F2", "F3", "F1-1", "F1-2", "F1-3"
        ],
        'parents': [
            "", "A", "A", "A", "A", "A", "B", "B", "B1", "B1",
            "B1", "C", "C", "D", "D", "E", "E", "E", "E",
            "E1", "E1", "E1", "E3", "E3", "F", "F", "F",
            "F1", "F1", "F1"
        ],
        'values': [
            0, 0, 0, 0, 0, 0, 8, 4, 2,
            2, 4, 4, 6, 6, 0, 7, 0, 3,
            7, 2, 2, 2, 0, 9, 8, 6, 5,
            6, 3, 4  # 补充了两个元素，使长度与其他列表一致
        ]
    }
    # 现在三个列表的长度都是30，可以正确创建DataFrame
    data_df = pd.DataFrame(data)
    data_df.to_csv('data.csv', index=False)

# 构建旭日图
fig = go.Figure(
    go.Sunburst(
        labels=data_df['labels'].tolist(),
        parents=data_df['parents'].tolist(),
        values=data_df['values'].tolist(),
        textinfo='label+percent root',  # 显示标签和占根节点的百分比
        textfont=dict(color='white', size=14),  # 文本样式
        marker=dict(
            colors=["#ffffff", "#f9b99e", "#f87f8c", 
                    "#e37e8e", "#a9758c", "#796b88"],  # 颜色映射
            line=dict(color='white', width=3)  # 分区边界样式
        )
    )
)

# 更新布局
fig.update_layout(
    margin=dict(t=0, l=0, r=0, b=0),  # 清除边距
    width=800,  # 图表宽度
    height=500  # 图表高度
)

# 显示图表
fig.show()

# --- cell 4: code ---
pass

# --- cell 5: code ---
pass
