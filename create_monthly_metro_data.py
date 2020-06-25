import pandas as pd
import json

df = pd.read_csv("data/대구도시철도공사_월별승차인원_20200430.csv", encoding="euc-kr")
for i in range(1, 13):
    df.replace("0" + str(i)+"월", i, inplace=True)
    df.replace(to_replace= str(i)+"월", value=i, inplace=True)

for i in range(1997, 2021):
    df.replace(str(i) + "년", i, inplace=True)

df.rename(columns={"년": "year", "월": "month", "전호선": "total"}, inplace=True)

for i in range(1, 4):
    df.rename(columns={str(i)+"호선": "line_" + str(i)}, inplace=True)

with open("data/ios_subwaydata.json") as j:
    subway_coordinates = json.load(j)

# def get_station_coordinates(row):
#     coords = subway_coordinates[row['station'][:-1]]
#     return coords['lat']

# subway_coordinates = {station['station']: {'lat': station['lat'], 'long': station['long']} for station in subway_coordinates}
# a = df.apply(lambda row: get_station_coordinates(row), axis=1)

print(df.tail())

df.to_csv("data/metro_data_monthly_199701_202004.csv", encoding="utf-8")
df_part1 = df[['year', 'month', 'total']].rename(columns={"total": "passengers"})
df_part1["percent_change"] = df_part1["passengers"].pct_change(periods=12).round(6) * 100
df_part1["passengers_last_year"] = df_part1["passengers"].shift(periods=12, fill_value=-1).astype("int64")
# df_part1["passengers_last_year"] = df_part1["passengers"].shift(periods=12)


df_part1[253:].to_csv("data/part1/part1_metro_data_monthly_201901_202004.csv", encoding="utf-8", index=False)
