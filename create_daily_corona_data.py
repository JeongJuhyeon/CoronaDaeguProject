import pandas as pd

df = pd.read_csv("data/coronaboard_kr-master/kr_regional_daily.csv")
df = df[df['region'] == '대구']
df2 = pd.read_csv("data/coronaboard_kr-master/kr_daily.csv", usecols=["date", "confirmed","death","released"])
df2['region'] = "전국"
df2 = df2.append(df)

df2['new'] = df2['confirmed'].diff().fillna(0).astype(int)
df2['active'] = df2['confirmed'] - df2['death'] - df2['released']

mask = df2['region'] == "대구"
df2.loc[mask.idxmax(), 'new'] = 0
df2.to_csv("data/part1/part1_daily_corona_data.csv", index=False)
