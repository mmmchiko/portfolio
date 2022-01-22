#
# 岐阜県新型コロナウイルス感染症に関する県内の感染動向、検査件数、相談受付件数
# 市町村別グラフ作成
#
# partial release history:
# 2022/1/18 m.maruyama   Created
#
import csv, os
import glob
import pandas as pd
import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import datetime
from datetime import date, timedelta

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

#不要な列を削除
covid_data_org.drop(
    covid_data_org.columns[[13, 14, 15, 16]], axis=1,inplace=True)

#不要な列を削除
covid_data_org.drop([
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

# 公表_年月日　1～10000件 "yyyy/m/d"　10001件～ "yyyy-mm-dd"
# 日付書式を統一
#covid_data_org.replace({'公表_年月日': {'-0': '/'}}, inplace=True)
#covid_data_org.replace({'公表_年月日': {'-': '/'}}, inplace=True)

#市町村毎に感染者数を集計
covid_data = covid_data_org.groupby(['公表_年月日', '患者_居住地'], as_index=False).count()

# 出力
covid_data.to_csv('covid_data_out.csv')

# グラフ用df作成
# 42市町村を列に設定
columns1 =[	"岐阜市",
            "羽島市",
            "各務原市",
            "山県市",
            "瑞穂市",
            "本巣市",
            "笠松町",
            "岐南町",
            "北方町",
            "大垣市",
            "海津市",
            "養老町",
            "関ケ原町",
            "垂井町",
            "安八町",
            "神戸町",
            "輪之内町",
            "池田町",
            "揖斐川町",
            "大野町",
            "関市",
            "美濃市",
            "美濃加茂市",
            "可児市",
            "郡上市",
            "川辺町",
            "坂祝町",
            "白川町",
            "富加町",
            "東白川村",
            "七宗町",
            "八百津町",
            "御嵩町",
            "多治見市",
            "中津川市",
            "瑞浪市",
            "恵那市",
            "土岐市",
            "高山市",
            "飛騨市",
            "下呂市",
            "白川村"]

# 42市町村別カラー
colorlist =["#aaaaff",
            "#8080ff",
            "#5555ff",
            "#2b2bff",
            "#0000ff",
            "#0000d5",
            "#0000aa",
            "#0000aa",
            "#000080",
            "#ffaaaa",
            "#ff8080",
            "#ff5555",
            "#ff2b2b",
            "#ff2b2b",
            "#ff0000",
            "#ff0000",
            "#ff0000",
            "#d50000",
            "#d50000",
            "#d50000",
            "#aaffaa",
            "#80ff80",
            "#55ff55",
            "#2bff2b",
            "#00ff00",
            "#00d500",
            "#00d500",
            "#00d500",
            "#00d500",
            "#00d500",
            "#00d500",
            "#00d500",
            "#00aa00",
            "#ffaad5",
            "#ff80bf",
            "#ff55aa",
            "#ff2b95",
            "#ff0080",
            "#aad5ff",
            "#80bfff",
            "#55aaff",
            "#2b95ff"]

# X軸データリスト
# 指定日から今日までの行を設定
#d1 = date(2020,2,26)
d1 = date(2022,1,1)
d2 = datetime.date.today()

xDate = []
for i in range((d2 - d1).days + 1):
    date = d1 + timedelta(i)
    xDate.append(date)
    
# Y軸データ二次元配列
yData = []

# 42市町村＋日付を条件に該当行を抽出
for col, city in enumerate(columns1):
    covid_df1 = covid_data[covid_data['患者_居住地'] == city]
    yDataCity = []

    # 日付を条件に該当行を抽出
    for row, date1 in enumerate(xDate):
        strdate = date1.strftime('%Y-%m-%d')
#        strdate = strdate.replace('/0', '/')
        covid_df2 = covid_df1[covid_df1['公表_年月日'] == strdate]
        if len(covid_df2) :
            yDataCity.append(covid_df2.iat[0, 2])
        else :
            yDataCity.append(0)
    # Y軸データに市町村別データを追加
    yData.append(yDataCity)
#    print(yData)
        
# グラフ出力
plt.figure(figsize=(12, 6))
plt.stackplot(
        xDate, 
        yData,
        labels = columns1,
        colors = colorlist
)

# タイトル
dt_now = datetime.datetime.now()
plt.title("岐阜県内の感染動向（市町村別）" + dt_now.strftime('%Y-%m-%d %H:%M:%S') + " 現在", fontname="MS Gothic")

# 軸ラベル
plt.xlabel("日付", fontname="MS Gothic")
plt.ylabel("人数", fontname="MS Gothic")

# 軸目盛
#plt.yticks(np.arange(0, 500, step=50))

# 凡例
plt.legend(
        bbox_to_anchor=(1.05, 1), 
		loc='upper left', 
		borderaxespad=0, 
		fontsize=12, 
		ncol=3, 
		prop={"family":"MS Gothic"})

# 画像ファイル保存
strfname = 'png/' + d2.strftime('%Y%m%d') + '_covidGifu_cityStack.png'
plt.savefig(strfname, bbox_inches='tight')

plt.show()
plt.close('all')
