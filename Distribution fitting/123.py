import matplotlib.pyplot as plt
import pandas as pd

# Loading data from CSV files
wr_data = pd.read_csv('wr.csv')
th_data = pd.read_csv('th.csv')

# Extracting columns
wr_start = wr_data['wr_start']
wr_stop = wr_data['wr_stop']
th_start = th_data['th_start']
th_stop = th_data['th_stop']

# Creating a figure with 2x2 subplot grid
fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=True, sharey=True)

# Defining histogram parameters
bins = 20
alpha = 0.7

# Plotting histograms
axes[0, 0].hist(wr_start, bins=bins, alpha=alpha, color='blue', edgecolor='black')
axes[0, 0].set_title('Winter Road Opening Dates')
axes[0, 0].set_xlabel('Day of Year')
axes[0, 0].set_ylabel('Frequency')

axes[0, 1].hist(wr_stop, bins=bins, alpha=alpha, color='green', edgecolor='black')
axes[0, 1].set_title('Winter Road Closing Dates')
axes[0, 1].set_xlabel('Day of Year')
axes[0, 1].set_ylabel('Frequency')

axes[1, 0].hist(th_start, bins=bins, alpha=alpha, color='red', edgecolor='black')
axes[1, 0].set_title('Thawing Window Opening Dates')
axes[1, 0].set_xlabel('Day of Year')
axes[1, 0].set_ylabel('Frequency')

axes[1, 1].hist(th_stop, bins=bins, alpha=alpha, color='purple', edgecolor='black')
axes[1, 1].set_title('Thawing Window Closing Dates')
axes[1, 1].set_xlabel('Day of Year')
axes[1, 1].set_ylabel('Frequency')

# Adjusting layout for clarity
plt.tight_layout()

# Saving the plot for publication
plt.savefig('time_window_distributions.png', dpi=300, bbox_inches='tight')

# Displaying the plot
plt.show()