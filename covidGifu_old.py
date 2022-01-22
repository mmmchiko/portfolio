#
# 岐阜県新型コロナウイルス感染症に関する県内の感染動向、検査件数、相談受付件数
# 年代別グラフ作成
#
# partial release history:
# 2022/1/13 m.maruyama   Created
#
import csv, os
import pandas as pd
import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import datetime
from datetime import date, timedelta

#CSVファイルからdfへ変換
covid_data_org = pd.read_csv('csv/210005_gifu_covid19_patients.csv',encoding = 'shift_jis')

covid_data = covid_data_org.copy()
#不要な列を削除
covid_data.drop([
    "全国地方公共団体コード", 
    "都道府県名", 
    "市区町村名", 
    "発症_年月日", 
    "患者_年代", 
    "患者_性別", 
    "患者_属性", 
    "患者_状態", 
    "患者_症状", 
    "患者_渡航歴の有無フラグ"], axis=1,inplace=True)

#年代毎に感染者数を集計
covid_data = covid_data_org.groupby(['公表_年月日', '患者_年代'], as_index=False).count()

# 出力
#covid_data.to_csv('covid_data_out.csv')

# グラフ用df作成
# 年代を列に設定
columns1 =[ "100歳以上",
            "10歳未満",
            "10代",
            "20代",
            "30代",
            "40代",
            "50代",
            "60代",
            "70代",
            "80代",
            "90代"]

# 2021/10/1から今日までの行を設定
d1 = date(2021,10,1)
d2 = datetime.date.today()

index1 = []
for i in range((d2 - d1).days + 1):
    date = d1 + timedelta(i)
    index1.append(date)
    
# データ部分をゼロクリア
list1 = [[0] * len(columns1)] * len(index1)

# グラフ用df作成
covid_grph = pd.DataFrame(data=list1, index=index1, columns=columns1)

# データ取得
# 日付を条件に該当行を抽出
for row, date1 in enumerate(index1):
#    strdate = date1.strftime('%Y/%m/%d')
#    strdate = strdate.replace('/0', '/')
    strdate = date1.strftime('%Y-%m-%d')
    covid_df1 = covid_data[covid_data['公表_年月日'] == strdate]
    
    # 年代＋日付を条件に該当行を抽出
    for col, old in enumerate(columns1):
        covid_df2 = covid_df1[covid_df1['患者_年代'] == old]
        if len(covid_df2) :
            covid_grph.iat[row, col] = covid_df2.iat[0,2]
        
# 出力
#covid_grph.to_csv('covid_grph_out.csv')

# グラフ出力
plt.figure()
covid_grph.plot(
        grid=True,
        colormap='Accent',
        legend=False,
        alpha=1,
        figsize=(12, 6))

# タイトル
# タイトル
dt_now = datetime.datetime.now()
plt.title("岐阜県内の感染動向（年代別）" + dt_now.strftime('%Y-%m-%d %H:%M:%S') + " 現在", fontname="MS Gothic")

# 軸ラベル
plt.xlabel("日付", fontname="MS Gothic")
plt.ylabel("人数", fontname="MS Gothic")

# 軸目盛
#plt.yticks(np.arange(0, 50, step=5))

# 凡例
plt.legend(	bbox_to_anchor=(1.05, 1), 
		loc='upper left', 
		borderaxespad=0, 
		fontsize=12, 
		ncol=1, 
		prop={"family":"MS Gothic"})

# 画像ファイル保存
strfname = 'png/' + d2.strftime('%Y%m%d') + '_covidGifu_old.png'
plt.savefig(strfname, bbox_inches='tight')

plt.close('all')
