import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('thirty-bw2-wcsv-try4.csv', header=None)

plt.hist(data, bins='auto', density=True, histtype='step')

plt.show()

