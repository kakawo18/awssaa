# 付録B 問題文キーワード → 正解の型（逆引き）

> SAAは**言い回しがパターン化**している。この対応表を反射で出せると、選択肢を読む前に答えが絞れる。

---

## 要件を表すフレーズ

| 問題文の言い回し | 反射で出す答え |
|---|---|
| **運用オーバーヘッドを最小限に** | マネージド／サーバーレス（Lambda、Fargate、Aurora Serverless、DynamoDB、Glue、Athena）。自前EC2構築は不正解 |
| **最小限のコード変更で** / 既存のまま | 互換サービス（Amazon MQ、DocumentDB、Keyspaces、MSK、EKS、Babelfish、FSx、Transfer Family） |
| **最もコスト効率が高い** | スポット、ライフサイクル、Intelligent-Tiering、Savings Plans、サーバーレス、gp3、Graviton（ただし要件を満たす範囲で） |
| **高可用性** | マルチAZ、ASG、ELB、リージョン内冗長 |
| **災害対策（DR）／リージョン障害** | クロスリージョン（S3 CRR、Auroraグローバル、DynamoDBグローバルテーブル、Route 53フェイルオーバー） |
| **RTO/RPOがほぼゼロ** | マルチサイト アクティブ/アクティブ |
| **数分以内に復旧、コストは抑えたい** | ウォームスタンバイ／パイロットライト |
| **スケーラブル／トラフィックが予測できない** | Auto Scaling、サーバーレス、DynamoDBオンデマンド |
| **疎結合にしたい／依存を減らす** | SQS、SNS、EventBridge |
| **リアルタイム／ストリーミング** | Kinesis Data Streams、Firehose、Flink |
| **一桁ミリ秒** | DynamoDB |
| **マイクロ秒** | ElastiCache、DAX |
| **サブミリ秒・数百GB/s（HPC）** | FSx for Lustre |
| **監査／誰が何をしたか** | CloudTrail |
| **コンプライアンス／改変不可／保持期間** | オブジェクトロック（コンプライアンスモード）、Vault Lock、Artifact |
| **個人情報が含まれていないか** | Macie（S3）、Comprehend（テキスト） |
| **インターネットを経由させたくない** | VPCエンドポイント／PrivateLink／Direct Connect |
| **パブリックIPを持たせずに更新・接続したい** | NAT Gateway（アウトバウンド）、**Session Manager**（接続）、VPCエンドポイント |
| **固定IPが必要（ファイアウォール登録）** | NLB、Global Accelerator、Elastic IP |
| **キーをコードに書かない** | IAMロール、Secrets Manager、Parameter Store |
| **キーを自社で完全管理したい** | CloudHSM、SSE-C、インポートしたキーマテリアル |
| **一時的にファイルを共有したい** | S3 事前署名URL |
| **特定のIPアドレスからの攻撃を遮断** | NACL（またはWAFのIPセット） |
| **SQLインジェクション／XSS／ボット** | WAF |
| **大規模DDoSと請求の急増** | Shield Advanced |
| **開発者に決められた構成だけ使わせたい** | Service Catalog（＋SCP、アクセス許可境界） |
| **複数アカウントを統制したい** | Organizations＋SCP、Control Tower、Firewall Manager |
| **手作業のパッチ適用をやめたい** | Systems Manager Patch Manager |
| **踏み台サーバーをなくしたい** | Session Manager |
| **設定が勝手に変えられていないか** | AWS Config（＋自動修復） |
| **メモリ使用率を監視したい** | CloudWatchエージェント（カスタムメトリクス） |
| **ログから特定の文字列を検知して通知** | CloudWatch Logs メトリクスフィルタ＋アラーム |
| **オンプレのデータを一度に大量移行** | Snowball（回線が細い）／DataSync（オンライン） |
| **DBを止めずに移行** | DMS（＋SCT） |
| **既存のSFTPを維持** | Transfer Family |
| **セッション情報の保存場所** | ElastiCache（Redis）／DynamoDB |
| **静的コンテンツの配信** | S3＋CloudFront（OAC） |
| **画像アップロード後の非同期処理** | S3イベント → SQS/SNS → Lambda |
| **急なスパイクでDBが落ちる** | 前段にSQS（バッファ）／ElastiCache／DynamoDB |
| **同じ処理が2回実行された** | SQSの可視性タイムアウト／FIFOキュー／冪等性の実装 |
| **メッセージが失われる** | DLQ、保持期間の延長 |
| **アプリは正常なのにヘルスチェックを通過してしまう** | ASGのヘルスチェックタイプを**ELB**にする |
| **東京だけでなく世界中で速く** | CloudFront、Global Accelerator、レイテンシールーティング、マルチリージョン |

---

## 数字で覚えるもの（頻出）

| 項目 | 値 |
|---|---|
| Lambda 最大実行時間 / メモリ | 15分 / 10GB（メモリ増＝CPU増） |
| Lambda 既定の同時実行数 | 1,000（アカウント単位） |
| SQS メッセージ保持 / 最大サイズ / 可視性タイムアウト既定 | 最大14日（既定4日）/ 256KB / 30秒 |
| SQS FIFO スループット | 300 TPS（バッチで3,000） |
| SQS ロングポーリング最大 | 20秒 |
| S3 オブジェクト最大 / マルチパート必須 | 5TB / 5GB超 |
| S3 性能 | プレフィックスあたり 3,500 PUT・5,500 GET 毎秒 |
| S3 最低保存期間 | IA 30日／Glacier 90日／Deep Archive 180日 |
| Glacier 取り出し | 迅速1〜5分／標準3〜5時間／大容量5〜12時間、Deep Archive 12〜48時間 |
| DynamoDB 項目サイズ / PITR | 400KB / 35日 |
| DynamoDB キャパシティ | 1 RCU＝4KB強整合1回/秒（結果整合なら2回）、1 WCU＝1KB 1回/秒 |
| RDS 自動バックアップ保持 | 1〜35日（0で無効） |
| Aurora ストレージ / レプリカ / コピー数 | 128TB / 15台 / 3AZ×2＝6 |
| Kinesis シャード | 書き込み1MB・1,000レコード/秒、読み取り2MB/秒、保持1〜365日 |
| VPC サブネットの予約IP | 各サブネット5個 |
| ELB 登録解除の遅延 既定 | 300秒 |
| KMS キー削除の待機期間 | 7〜30日 |
| CloudTrail イベント履歴 | 90日（証跡はS3に無期限） |
| EC2 スポット中断の通知 | 2分前 |

---

## 試験当日の解き方（3ステップ）

1. **要件語を拾う**：可用性／コスト／レイテンシ／運用負荷／規制のどれが主題かを最初に確定する。
2. **明らかな不正解を消す**：要件を満たさないもの（単一AZ、15分超のLambda、EC2にACM証明書、NLBにWAF、マルチAZで読み取り分散 など）。
3. **残りから「最も○○」を選ぶ**：設問が「最もコスト効率」なら安い方、「最も運用負荷が低い」ならマネージド度が高い方。

---

[目次に戻る](./README.md) ／ [横断比較表](./90-comparison.md)
