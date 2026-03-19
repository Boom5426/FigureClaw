# Generated from a source notebook for audit and review purposes.

# --- cell 1: code ---
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

# Methods and their corresponding metrics
methods = ['PhenoProfiler', 'DeepProfiler*', 'ResNet50', 'ViT', 'OpenPhenom']
folds_of_enrichment = [48.0, 29.2, 28.9, 27.0, 10.3]  # Example values for FoE
mean_average_precision = [0.092, 0.075, 0.073, 0.072, 0.054]  # Example values for MAP

colors = ['#E64B35B2', '#3C5488B2', '#00A087B2', '#91D1C2B2', '#D4B9DA']

# Plotting the data
plt.figure(figsize=(10, 6))
for method, fe, MAP, color in zip(methods, folds_of_enrichment, mean_average_precision, colors):
    plt.scatter(MAP, fe, label=method, color=color, s=200)  # Adjust the size of the dots with the 's' parameter
    # Ensure the text labels do not go outside the plot area
    if MAP > 0.09:
        plt.text(MAP - 0.0003, fe-0.96, method, fontsize=28, ha='right', color=color)
    elif method=='ResNet50':
        plt.text(MAP - 0.009, fe + 0.9, method, fontsize=28, ha='left', color=color)
    elif method=='ViT':
        plt.text(MAP - 0.0006, fe - 3.8, method, fontsize=28, ha='left', color=color)
    else:
        plt.text(MAP + 0.0005, fe - 0.6, method, fontsize=28, ha='left', color=color)
    # else:
    #     plt.text(MAP, fe, method, fontsize=22, ha='left', color=color)

# Adding labels and title
plt.xlabel('MAP', fontsize=24)
plt.ylabel('FoE', fontsize=24)
plt.title('BBBC022', fontsize=26)
# "TAORF-BBBC037" , "CDRP-BIO-BBBC036"

# Adjusting the font size of the tick labels on both axes
plt.xticks(fontsize=20)
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.3f'))  # Format x-axis labels to 3 decimal places
plt.yticks(fontsize=20)

# Customizing grid appearance (modified part)
plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)  # Dashed lines, thinner and semi-transparent
plt.gca().set_axisbelow(True)  # Place grid lines behind the data points

# Adjust x-axis grid spacing (every 0.005)
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(0.01))
# Adjust y-axis grid spacing (every 5 units)
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(10))

plt.tight_layout()
# Save the plot as a PDF file
# plt.savefig("2a_022.pdf", dpi=300) 

plt.show()
