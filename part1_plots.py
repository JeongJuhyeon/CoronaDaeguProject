import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

sns.set(style="whitegrid")

rs = np.random.RandomState(365)
values = rs.randn(365, 4).cumsum(axis=0)
dates = pd.date_range("1 1 2016", periods=365, freq="D")
data = pd.DataFrame(values, dates, columns=["A", "B", "C", "D"])
data = data.rolling(7).mean()

# sns.lineplot(data=data, palette="tab10", linewidth=2.5)

# Monthly


df = pd.read_csv("data/part1/part1_monthly.csv")

dates = pd.date_range(start="2019/11", periods=6, freq="M")
df_recent = df[6:]
df_recent = df_recent[["bus_percent_change", "metro_percent_change", "confirmed", "new", "active"]]
df_recent[["confirmed", "new", "active"]] = df_recent[["confirmed", "new", "active"]] / 100
df_recent.at[11, "metro_percent_change"] = np.NaN

df_recent.index = dates
sns.lineplot(data=df_recent, linewidth=2.5)

plt.show()

df_recent_transport = df_recent[["bus_percent_change", "metro_percent_change"]]
sns.lineplot(data=df_recent_transport, linewidth=2.5)

plt.savefig('plots/part1/monthly_transportation.png')
plt.show()

# Daily

df = pd.read_csv("data/part1/part1_daily.csv")
df['datetime'] = pd.to_datetime(df['datetime'], yearfirst=True)
df.set_index('datetime', inplace=True)
df_recent_daegu = df[(df.index >= '2019-12-07') & (df['region'] != '전국')]
df_recent_kr = df[(df.index >= '2019-12-07') & (df['region'] != '대구')]

# create figure and axis objects with subplots()
fig, ax = plt.subplots()
# make a plot
ax.plot(df_recent_daegu.index, df_recent_daegu['new'], color="red")
ax.plot(df_recent_daegu.index, df_recent_daegu['active'], color="orange")
# set x-axis label
ax.set_xlabel("date",fontsize=14)
ax.fmt_xdata = mdates.DateFormatter("%m")
# set y-axis label
ax.set_ylabel("new cases",color="red",fontsize=14)



#
# # twin object for two different y-axis on the sample plot
# ax2 = ax.twinx()
# # make a plot with different y-axis using second axis object
# ax2.plot(df_recent_daegu['datetime'].astype("O"), df_recent_daegu["weekly_passengers_1y_change"],color="blue")
# ax2.fmt_xdata = mdates.DateFormatter("%m")
# ax2.set_ylabel("wk passengers % change",color="blue",fontsize=14)
plt.show()
# save the plot as a file
# fig.savefig('two_different_y_axis_for_single_python_plot_with_twinx.jpg',
#             format='jpeg',
#             dpi=100,
#             bbox_inches='tight')

df_recent_daegu['new'].plot()
plt.show()