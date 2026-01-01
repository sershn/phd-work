import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# Beta distribution parameters
a = 0.968
b = 0.806
loc = 11.759
scale = 29.240

# Create figure
plt.figure(figsize=(7, 6))

# Plot beta distribution PDF
x_fit = np.linspace(10, 57, 100)  # Range covering wr_stop (13 to 49)
pdf = stats.logistic.pdf(x_fit, loc=35.392, scale=3.989)

#Plot histogram of wr_stop data (uncomment to include)
dataset = pd.read_csv("th.csv")
x = dataset["th_stop"].values
bins = np.arange(int(min(x)) - 0.5, int(max(x)) + 1.5, 1)  # 1-day bins
counts, bins, _ = plt.hist(x, bins=bins, alpha=0.6, label='Histogram (thawing data)', color='paleturquoise', edgecolor='black')
# Scale PDF to match histogram counts
bin_width = bins[1] - bins[0]  # Should be 1.0
pdf_scaled = pdf * len(x) * bin_width
plt.plot(x_fit, pdf_scaled, label='Logistic (scaled to data frequency)', color='red', linewidth=2)


# Customize plot
plt.title('Closing day of the month for thawing time window', fontsize=12)
plt.xlabel('Day of the month (day 1 = Sep 1)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save and show
plt.savefig('beta_distribution.png', dpi=300, bbox_inches='tight')
plt.show()