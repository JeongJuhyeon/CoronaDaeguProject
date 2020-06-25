import pandas as pd

df_corona = pd.read_csv("data/part1/part1_daily_corona_data.csv")

datetime = pd.to_datetime(df_corona['date'], yearfirst=True, format="%Y%m%d")
dti = pd.DatetimeIndex(datetime)
df_corona["year"] = dti.year
df_corona["month"] = dti.month
# df_corona["day"] = dti.day

df_corona_last_day = df_corona.groupby("month").tail(1).copy()
df_corona_last_day['new'] = df_corona_last_day['confirmed'].diff().fillna(2236).astype(int)
rearrange_columns = list(df_corona_last_day.columns[-2:]) + list(df_corona_last_day.columns[1:-2]) + ['date']
df_corona_last_day = df_corona_last_day[rearrange_columns]

df_missing_months = pd.DataFrame(2*[[0]*df_corona_last_day.shape[1]], columns=df_corona_last_day.columns)
df_corona_last_day = pd.concat([df_missing_months, df_corona_last_day], ignore_index=True)
df_corona_last_day.at[0, 'year'] = 2019
df_corona_last_day.at[0, 'month'] = 12
df_corona_last_day.at[0, 'date'] = 20191231

df_corona_last_day.at[1, 'year'] = 2020
df_corona_last_day.at[1, 'month'] = 1
df_corona_last_day.at[1, 'date'] = 20200131

df_corona_last_day['region'] = '대구'

df_corona_last_day.to_csv("data/part1/part1_monthly_corona_data.csv", index=False)
