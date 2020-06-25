import pandas as pd
import csv
import json



df = pd.read_excel("data/정류소이용현황(201812).xls", header=1)
station_names = df["구분"][1:]
df = df.drop('구분', axis=1)
print(df.head())
get_on = df.iloc[1:, ::2].astype(int)
get_off = df.iloc[1:, 1::2].astype(int)
get_off.columns = get_on.columns
total = (get_on + get_off).transpose()
total.columns = station_names

def append_file_data(y, m):
    global total
    path = "data/정류소이용현황(20" + str(y) + ("0" if m < 10 else "") + str(m) + ").xls"
    df = pd.read_excel(path, header=1)
    station_names = df["구분"][1:]
    df = df.drop('구분', axis=1)
    print(df.head())
    get_on = df.iloc[1:, ::2].astype(int)
    get_off = df.iloc[1:, 1::2].astype(int)
    get_off.columns = get_on.columns
    total2 = (get_on + get_off).transpose()
    total2.columns = station_names
    total = total.append(total2)

append_file_data(19, 12)

for y in range(19, 21):
    for m in range(1, 7):
        append_file_data(y, m)

total.dropna(axis=1, inplace=True)
total['total'] = total.sum(axis=1)
total.to_csv("data/part1/part1_daily_bus_data.csv", quoting=csv.QUOTE_NONE, encoding="utf-8", index_label="date")

df3 = pd.read_csv("data/part1/part1_daily_bus_data.csv")