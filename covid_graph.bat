@echo off

wget --secure-protocol=TLSv1_2 https://gifu-opendata.pref.gifu.lg.jp/dataset/4661bf9d-6f75-43fb-9d59-f02eb84bb6e3/resource/9c35ee55-a140-4cd8-a266-a74edf60aa80/download/210005_gifu_covid19_patients.csv -O ./csv/210005_gifu_covid19_patients.csv
echo ダウンロードが完了しました。

covidGifu_city.py
echo 市町村別グラフ作成が完了しました。

covidGifu_old.py
echo 年代別グラフ作成が完了しました。

pause

