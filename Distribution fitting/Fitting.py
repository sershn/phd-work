import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from fitter import Fitter, get_common_distributions, get_distributions

dataset = pd.read_csv("th.csv")

x = dataset["th_start"].values

f = Fitter(x)
f = Fitter(x,distributions=['beta', 'gamma', 'norm', 'lognorm', 'chi',
                            'laplace', 'rayleigh', 'pareto', 'logistic'])

f.fit()
print(f.summary(Nbest=9).to_string())
#f.summary(Nbest=10).to_csv("th_stop.csv")
f.summary(Nbest=3, plot=True)
print(f.get_best())
for dist_name, params in f.fitted_param.items():
    print(f"{dist_name}: {params}")

# plt.title('Closing day of the month for winter road time window')
# plt.xlabel('Day of the month, day 1 = Mar 1')
# plt.ylabel('Probability density')
# plt.savefig('wr_stop_density_distribution.png', dpi=300, bbox_inches='tight')
plt.show()