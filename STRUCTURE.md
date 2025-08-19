amongq/ # プロジェクトルート
│
├─ bot.py # BOT 起動用メインファイル
├─ .env # Discord トークン等の環境変数
│
├─ commands/ # コマンド別の Cog ファイル
│ ├─ create.py # 部屋作成コマンド
│ ├─ setcapacity.py # 定員変更コマンド（管理者専用）
│ ├─ cancel.py # /cancel コマンド（必要に応じて）
│ ├─ list_participants.py # /list コマンド
│
├─ reactions/ # リアクション処理関連
│ └─ participant.py # リアクション押下・削除時の処理
│
├─ utils/ # 共通ユーティリティ
│ ├─ persistence.py # JSON 保存・読み込み
│ └─ errors.py # エラーメッセージ送信関数
│
├─ config.py # 定数等（MAX_PARTICIPANTS など）
│
└─ room_data/ # 各部屋の JSON データ保存先
└─ <部屋 ID>.json

- participant.py がリアクション管理の中心で、ここで参加・補欠・繰り上げ処理を行う
- cogs/ 内のファイルは主にスラッシュコマンド用
- room_data/ に JSON を保存して再起動後も状態を保持
- utils/ は共通関数をまとめたフォルダ
