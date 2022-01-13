#
# 岐阜県新型コロナウイルス感染症に関する県内の感染動向、検査件数、相談受付件数
# 市町村別グラフ作成
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

#市町村毎に感染者数を集計
covid_data = covid_data_org.groupby(['公表_年月日', '患者_居住地'], as_index=False).count()

# 出力
#covid_data.to_csv('covid_data_out.csv')

# グラフ用df作成
# 42市町村を列に設定
columns1 =["安八町",
            "池田町",
            "揖斐川町",
            "恵那市",
            "大垣市",
            "大野町",
            "海津市",
            "各務原市",
            "笠松町",
            "可児市",
            "川辺町",
            "北方町",
            "岐南町",
            "岐阜市",
            "郡上市",
            "下呂市",
            "神戸町",
            "坂祝町",
            "白川町",
            "白川村",
            "関ケ原町",
            "関市",
            "高山市",
            "多治見市",
            "垂井町",
            "土岐市",
            "富加町",
            "中津川市",
            "羽島市",
            "東白川村",
            "飛騨市",
            "七宗町",
            "瑞浪市",
            "瑞穂市",
            "御嵩町",
            "美濃加茂市",
            "美濃市",
            "本巣市",
            "八百津町",
            "山県市",
            "養老町",
            "輪之内町"]

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
    strdate = date1.strftime('%Y/%m/%d')
    strdate = strdate.replace('/0', '/')
    covid_df1 = covid_data[covid_data['公表_年月日'] == strdate]
    
    # 42市町村＋日付を条件に該当行を抽出
    for col, city in enumerate(columns1):
        covid_df2 = covid_df1[covid_df1['患者_居住地'] == city]
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
plt.title("岐阜県内の感染動向（市町村別）", fontname="MS Gothic")

# 軸ラベル
plt.xlabel("日付", fontname="MS Gothic")
plt.ylabel("人数", fontname="MS Gothic")

# 軸目盛
plt.yticks(np.arange(0, 30, step=5))

# 凡例
plt.legend(	bbox_to_anchor=(1.05, 1), 
		loc='upper left', 
		borderaxespad=0, 
		fontsize=12, 
		ncol=3, 
		prop={"family":"MS Gothic"})

# 画像ファイル保存
strfname = 'png/' + d2.strftime('%Y%m%d') + '_covidGifu_city.png'
plt.savefig(strfname, bbox_inches='tight')

plt.close('all')
