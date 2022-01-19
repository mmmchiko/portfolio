#
# 岐阜県新型コロナウイルス感染症に関する県内の感染動向、検査件数、相談受付件数
# 年代別積み上げグラフ作成
#
# partial release history:
# 2022/1/18 m.maruyama   Created
#
import csv, os
import pandas as pd
import glob
import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import datetime
from datetime import date, timedelta

#CSVファイルからdfへ変換
# フォルダ内のCSVファイルの一覧を取得
files = sorted(glob.glob('csv/*.csv'))
# ファイル数を取得
file_number = len(files)
# CSVファイルの中身を読み出して、リスト形式にまとめる
csv_list = []
for file in files:
    csv_list.append(pd.read_csv(file,encoding='shift_jis',skiprows=[1]))
# CSVファイルの結合
covid_data_org = pd.concat(csv_list)

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

# 指定日から今日までの行を設定
#d1 = date(2020,2,26)
d1 = date(2022,1,1)
d2 = datetime.date.today()

# X軸データ　日付
xDate = []
for i in range((d2 - d1).days + 1):
    date = d1 + timedelta(i)
    xDate.append(date)
    
# Y軸データ二次元配列
yData = []

# 年代＋日付を条件に該当行を抽出
for col, old in enumerate(columns1):
    covid_df1 = covid_data[covid_data['患者_年代'] == old]
    yDataOld = []

    # 日付を条件に該当行を抽出
    for row, date1 in enumerate(xDate):
        strdate = date1.strftime('%Y/%m/%d')
        strdate = strdate.replace('/0', '/')
        covid_df2 = covid_df1[covid_df1['公表_年月日'] == strdate]
        if len(covid_df2) :
            yDataOld.append(covid_df2.iat[0, 2])
        else :
            yDataOld.append(0)
    # Y軸データに年代別データを追加
    yData.append(yDataOld)
        
# グラフ出力
plt.figure(figsize=(12, 6))
plt.stackplot(
        xDate, 
        yData,
        labels = columns1,
        colors = None
)

# タイトル
dt_now = datetime.datetime.now()
plt.title("岐阜県内の感染動向（年代別）" + dt_now.strftime('%Y-%m-%d %H:%M:%S') + " 現在", fontname="MS Gothic")

# 軸ラベル
plt.xlabel("日付", fontname="MS Gothic")
plt.ylabel("人数", fontname="MS Gothic")

# 軸目盛
plt.yticks(np.arange(0, 500, step=50))

# 凡例
plt.legend(	bbox_to_anchor=(1.05, 1), 
		loc='upper left', 
		borderaxespad=0, 
		fontsize=12, 
		ncol=1, 
		prop={"family":"MS Gothic"})

# 画像ファイル保存
strfname = 'png/' + d2.strftime('%Y%m%d') + '_covidGifu_oldStack.png'
plt.savefig(strfname, bbox_inches='tight')

plt.show()
plt.close('all')
