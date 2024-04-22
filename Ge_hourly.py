import pandas as pd
import matplotlib.pyplot as plt

results_file = "LEC_yaku-resampled_ERA5_track/Ge_level.csv"
df = pd.read_csv(results_file, index_col=0)
df.index = pd.to_datetime(df.index)
df_300 = df['3000.0']
df_300.index = pd.to_datetime(df_300.index)
plt.plot(df.index, df_300.values)
plt.show()

ge_mean = df_300.mean()

mean_hours1 = []
for time in (0,3,6,9,12,15,18,21):
    mean = df_300.loc[df_300.index.hour==time].mean()
    print(mean)
    mean_hours1.append(float(mean- ge_mean))

plt.axhline(y=ge_mean, color='r', linestyle='--')
plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
plt.plot([0,3,6,9,12,15,18,21], mean_hours1, linewidth=3)
plt.show()