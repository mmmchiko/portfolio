# portfolio

岐阜県新型コロナウイルス感染症に関する県内の感染動向、検査件数、相談受付件数

市町村別、年代別グラフ作成

# 概要
岐阜県オープンデータカタログサイト
https://gifu-opendata.pref.gifu.lg.jp
より、新型コロナウイルス感染症に関する県内の感染動向　陽性患者属性のデータをダウンロード。
市町村別、年代別にグラフを作成する。


# 主要機能

csvファイルのダウンロード

csvファイルを読込、市町村別/年代別に集計し、グラフ化


# 工夫した点

シンプルなコード設計


# 使用技術

言語・フレームワーク

Python 3.7.9 (開発環境)

Windowsバッチ

git

Jupyter Notebook


# 制作について

製作期間

2022年1月10日から現在


途中経過

2021年11月3日: Python学習を始める。東京大学提供「Pythonプログラミング入門」を利用。

2022年1月10日: プログラミング入門を終了。学習のため、本プログラムを作成開始。

2022年1月13日: ver1.0

2022年1月19日: ver1.1　積み上げグラフ追加

2022年1月22日: ver1.2　日付書式の変更に対応。公表_年月日（1～10000件 "yyyy/m/d"、10001件～ "yyyy-mm-dd"）と表記の揺れがあるため、"yyyy-mm-dd"で統一。

