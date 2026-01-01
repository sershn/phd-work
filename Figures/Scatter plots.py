import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import seaborn as sns

# Load your dataset (replace with your own data)
#data = pd.read_csv('../data.csv')
data = pd.read_csv('../Figures/averaged_data1.csv')
#data = pd.read_csv('../Averaged_Data.csv')
#data = data.sample(frac=0.05, random_state=42)
time_window = 'total_t'
# Perform kernel density estimation for the scatter plot (heatmap)
total_cost_clean = data['total_$']
xy = np.vstack([data[time_window], total_cost_clean])
z = gaussian_kde(xy)(xy)
font = 12
# Create the scatter plot with density (heatmap overlay)
plt.figure(figsize=(7, 5))
plt.scatter(data[time_window], total_cost_clean, c=z, s=20, cmap='inferno', alpha=1, marker='x')
x1 = [599,607]
y1 = [29012352,29012352]
x2 = [603,603]
y2 = [28700000,29300000]
plt.plot(x1,y1, c='red', label='Deterministic TW')
plt.plot(x2,y2, c='red')
plt.legend(loc='upper right', fontsize=font)
#c='dodgerblue'
#cmap='viridis'
#cmap='plasma'
#cmap='hot'
# Set titles and labels
plt.title('Total project cost vs time', fontsize=font)
plt.xlabel('Duration, days', fontsize=font)
plt.ylabel('Total project cost, $', fontsize=font)
plt.xticks(fontsize=font)
plt.yticks(fontsize=font)

# Adjust the y-axis to display values in millions
plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e6:.0f}m'))

# Add a colorbar for density
cbar = plt.colorbar()
cbar.set_label('Density', fontsize=font)
cbar.ax.tick_params(labelsize=font)


# Display the grid and show the plot
#plt.grid(True)

plt.show()

plt.hexbin(data[time_window], total_cost_clean, gridsize=30, cmap='plasma', mincnt=1)
plt.colorbar(label="Point Count")
plt.xlabel("Duration, days")
plt.ylabel("Total project cost, $")
plt.show()