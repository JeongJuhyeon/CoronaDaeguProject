import pandas as pd

df_corona = pd.read_csv("data/part1/part1_daily_corona_data.csv")
df_bus = pd.read_csv("data/part1/part1_daily_bus_data.csv", usecols=["date", "total"])
df_bus['weekly_passengers'] = df_bus['total'].rolling(window=7).sum().fillna(0).astype(int)

df_merged = pd.merge(df_bus, df_corona, how='left').fillna(0)
df_merged.rename(columns={'total': 'passengers'}, inplace=True)
nr_columns = [c for c in df_merged.columns if c != "region"]
df_merged[nr_columns] = df_merged[nr_columns].astype(int)
# df_merged["region"] = "대구"

datetime = pd.to_datetime(df_merged['date'], yearfirst=True, format="%Y%m%d")
dti = pd.DatetimeIndex(datetime)
df_merged["year"] = dti.year
df_merged["month"] = dti.month
df_merged["day"] = dti.day

# df_bus_monthly = pd.read_csv("data/part1/part1_monthly_bus_data.csv")

def fan(row):
    day = row['day']
    if row['month'] == 2 and day == 29:
        day = 28
    last_year_row = df_merged[(df_merged['year'] == (row['year'] - 1)) & (df_merged['month'] == row['month']) & (df_merged['day'] == day)]
    if last_year_row.empty:
        return 0
    # months_days = {12: 31, 1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6:30}
    last_year_weekly = last_year_row['weekly_passengers']
    return last_year_weekly

last_year_weekly_passengers = df_merged.apply(lambda row: fan(row), axis=1)
last_year_weekly_passengers = last_year_weekly_passengers.astype(int)
df_merged['last_year_weekly_passengers'] = last_year_weekly_passengers
df_merged['weekly_passengers_1y_change'] = 100 * (df_merged['weekly_passengers'] - df_merged['last_year_weekly_passengers']) / df_merged['last_year_weekly_passengers']
rearrange_columns = list(df_merged.columns[:3]) + list(df_merged.columns[-5:]) + list(df_merged.columns[3:-5])
df_merged = df_merged[rearrange_columns]

df_merged['datetime'] = pd.to_datetime(df_merged['date'], yearfirst=True, format="%Y%m%d")
df_merged.to_csv("data/part1/part1_daily.csv", index=False)