import pandas as pd
import matplotlib.pyplot as plt
label_font = 16 #16 for double figure
tick_font = 14 #14 for double figure
#cmap='magma'
#cmap='viridis'
#cmap='plasma'
#cmap='cividis'
# Load  dataset
data0 = pd.read_csv('../averaged_data_crane.csv')
data1 = pd.read_csv('../averaged_data_launching.csv')
gridsize = 30
mincnt = 1
# Winter Road 1
time_window = 'tw0'
total_cost = data0['total_$']
plt.hexbin(data0[time_window], total_cost, gridsize=gridsize, cmap='viridis', mincnt=mincnt)
cbar = plt.colorbar()
cbar.set_label("Data point count", fontsize=label_font)
cbar.ax.tick_params(labelsize=tick_font)
plt.title('tw0 (winter road 2023)', fontsize=label_font)
plt.xlabel('Duration, days', fontsize=label_font)
plt.ylabel('Total project cost, $', fontsize=label_font)
plt.xticks(fontsize=tick_font), plt.yticks(fontsize=tick_font)
cross_x = 100
cross_y = 28499166
plt.scatter(cross_x, cross_y, color='r', marker='x', s=150, label="Deterministic TW")
plt.legend(loc='upper right', fontsize=tick_font)
# Adjust the y-axis to display values in millions
plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e6:.0f}m'))
plt.show()

# Winter Road 2
time_window = 'tw3'
total_cost = data0['total_$']
plt.hexbin(data0[time_window], total_cost, gridsize=gridsize, cmap='viridis', mincnt=mincnt)
cbar = plt.colorbar()
cbar.set_label("Data point count", fontsize=label_font)
cbar.ax.tick_params(labelsize=tick_font)
plt.title('tw3 (winter road 2024)', fontsize=label_font)
plt.xlabel('Duration, days', fontsize=label_font)
plt.ylabel('Total project cost, $', fontsize=label_font)
plt.xticks(fontsize=tick_font)
plt.yticks(fontsize=tick_font)
cross_x = 100
cross_y = 28499166
plt.scatter(cross_x, cross_y, color='r', marker='x', s=150, label="Deterministic TW")
plt.legend(loc='upper left', fontsize=tick_font)
# Adjust the y-axis to display values in millions
plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e6:.0f}m'))
plt.show()
""""""
# Thawing 1
time_window = 'tw1'
total_cost = data0['total_$']
plt.hexbin(data0[time_window], total_cost, gridsize=gridsize, cmap='cividis', mincnt=mincnt)
cbar = plt.colorbar()
cbar.set_label("Data point count", fontsize=label_font)
cbar.ax.tick_params(labelsize=tick_font)
plt.title('tw1 (thawing 2023)', fontsize=label_font)
plt.xlabel('Duration, days', fontsize=label_font)
plt.ylabel('Total project cost, $', fontsize=label_font)
plt.xticks(fontsize=tick_font)
plt.yticks(fontsize=tick_font)
cross_x = 160
cross_y = 28499166
plt.scatter(cross_x, cross_y, color='r', marker='x', s=150, label="Deterministic TW")
plt.legend(loc='upper left', fontsize=tick_font)
# Adjust the y-axis to display values in millions
plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e6:.0f}m'))
plt.show()
""""""
# Thawing 2
time_window = 'tw4'
total_cost = data0['total_$']
plt.hexbin(data0[time_window], total_cost, gridsize=gridsize, cmap='cividis', mincnt=mincnt)
cbar = plt.colorbar()
cbar.set_label("Data point count", fontsize=label_font)
cbar.ax.tick_params(labelsize=tick_font)
plt.title('tw4 (thawing 2024)', fontsize=label_font)
plt.xlabel('Duration, days', fontsize=label_font)
plt.ylabel('Total project cost, $', fontsize=label_font)
plt.xticks(fontsize=tick_font)
plt.yticks(fontsize=tick_font)
cross_x = 160
cross_y = 28499166
plt.scatter(cross_x, cross_y, color='r', marker='x', s=150, label="Deterministic TW")
plt.legend(loc='upper right', fontsize=tick_font)
# Adjust the y-axis to display values in millions
plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e6:.0f}m'))
plt.show()
""""""
label_font = 12
tick_font = 10
# Crane
time_window = 'total_t'
total_cost = data0['total_$']
plt.hexbin(data0[time_window], total_cost, gridsize=gridsize, cmap='plasma', mincnt=mincnt)
# plt.xlim(x_min, x_max)
# plt.ylim(y_min, y_max)
cbar = plt.colorbar()
cbar.set_label("Data point count", fontsize=label_font)
cbar.ax.tick_params(labelsize=tick_font)
plt.title('Crane method 2D hexbin plot', fontsize=label_font)
plt.xlabel('Total project duration, days', fontsize=label_font)
plt.ylabel('Total project cost, $', fontsize=label_font)
plt.xticks(fontsize=tick_font)
plt.yticks(fontsize=tick_font)
cross_x = 654
cross_y = 28499166
plt.scatter(cross_x, cross_y, color='lime', marker='x', s=150, label="Deterministic TW")
plt.legend(loc='upper right', fontsize=tick_font)
x1, y1 = [590,654], [28499166,28499166]
x2, y2 = [654,654], [28499166,27400000]
x3, y3 = [590,654], [27400000,27400000]
x4, y4 = [590,590], [28499166,27400000]
plt.plot(x1,y1, ls = '--', color = 'grey', label = 'On time & budget 20.72%')
plt.plot(x2,y2,x3,y3,x4,y4, ls = '--', color = 'grey',)
plt.legend(loc='upper right', fontsize=tick_font)
# Adjust the y-axis to display values in millions
plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e6:.0f}m'))
plt.show()
""""""
# Launching
time_window = 'total_t'
total_cost = data1['total_$']
plt.hexbin(data1[time_window], total_cost, gridsize=gridsize, cmap='magma', mincnt=mincnt)
# plt.xlim(x_min, x_max)
# plt.ylim(y_min, y_max)
cbar = plt.colorbar()
cbar.set_label("Data point count", fontsize=label_font)
cbar.ax.tick_params(labelsize=tick_font)
plt.title('Launching method 2D hexbin plot', fontsize=label_font)
plt.xlabel('Total project duration, days', fontsize=label_font)
plt.ylabel('Total project cost, $', fontsize=label_font)
plt.xticks(fontsize=tick_font)
plt.yticks(fontsize=tick_font)
cross_x = 603
cross_y = 29012352
plt.scatter(cross_x, cross_y, color='lime', marker='x', s=150, label="Deterministic TW")
plt.legend(loc='upper right', fontsize=tick_font)
x1, y1 = [540,603], [29012352,29012352]
x2, y2 = [603,603], [29012352,27700000]
x3, y3 = [540,603], [27700000,27700000]
x4, y4 = [540,540], [29012352,27700000]
plt.plot(x1,y1, ls = '--', color = 'grey', label = 'On time & budget 8.51%')
plt.plot(x2,y2,x3,y3,x4,y4, ls = '--', color = 'grey',)
plt.legend(loc='upper right', fontsize=tick_font)
# Adjust the y-axis to display values in millions
plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e6:.0f}m'))
plt.show()