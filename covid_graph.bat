@echo off

wget --secure-protocol=TLSv1_2 https://gifu-opendata.pref.gifu.lg.jp/dataset/4661bf9d-6f75-43fb-9d59-f02eb84bb6e3/resource/9c35ee55-a140-4cd8-a266-a74edf60aa80/download/210005_gifu_covid19_patients.csv -O ./csv/210005_gifu_covid19_patients.csv
echo �_�E�����[�h���������܂����B

covidGifu_city.py
echo �s�����ʃO���t�쐬���������܂����B

covidGifu_old.py
echo �N��ʃO���t�쐬���������܂����B

pause

