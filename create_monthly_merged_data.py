import pandas as pd

df_corona = pd.read_csv("data/part1/part1_monthly_corona_data.csv")
df_bus = pd.read_csv("data/part1/part1_monthly_bus_data.csv")
df_metro = pd.read_csv("data/part1/part1_metro_data_monthly_201901_202004.csv")

df_bus.columns = ["bus_" + str(c) for c in df_bus.columns]
df_bus.rename(columns={"bus_year": "year", "bus_month": "month"}, inplace=True)
df_metro.columns = ["metro_" + str(c) for c in df_metro.columns]
df_metro.rename(columns={"metro_year": "year", "metro_month": "month"}, inplace=True)


df_merged = pd.merge(df_bus, df_metro, how='left').fillna(0)
df_merged = pd.merge(df_merged, df_corona, how='left').fillna(0)

nr_columns = [c for c in df_merged.columns]
nr_columns.remove("bus_percent_change")
nr_columns.remove("metro_percent_change")
nr_columns.remove("region")
df_merged[nr_columns] = df_merged[nr_columns].astype(int)
df_merged["region"] = "대구"

df_merged = df_merged.reindex(index=df_merged.index[::-1])
df_merged.to_csv("data/part1/part1_monthly.csv", index=False)