# ReleaseDateCrawler
商品販売日の取得クローラー
## 目的
勉強のための販売日クローラー作成<br>
ライブラリを使わずにクローラーを作成できるか確認する<br>
理解できるまで実装せず、検索する
 
## ざっくり疑問点
-  簡易設計書作成
- ネイティブで動かすには何が必要か確認
    - サーバーが必要かどうか
    - テーブルを使う必要があるか
        - csvを吐き出しても良いのではないか
    - 実際に環境が決まった後の環境構築
        - 使うのであればDockerなど

## メモ
- envでgoogleカレンダーと連携する？
- cronで毎月取得？
- サイトのデータ解析だけ汎用的に作る？

## 予定（随時更新）
- 11月
    - githubにてソース管理
    - サーバや保存場所の想定
    - コーディングはじめ

- 12月
    - コーディング、サーバに置いてみる

- １月
    - 遊戯王以外のサイトでも試す


## 開発環境（随時更新）
Python 3.9.5

## tips
### venv起動
.\.venv\Scripts\activate.bat
.\.venv\Scripts\Activate.ps1

### リリースコマンド
chalice package ../package  