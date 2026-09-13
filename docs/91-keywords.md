# 付録B 設問キーワード逆引きと主要数値基準

> **本付録の活用法**：AWS SAA試験の設問で頻出する「典型的な要件表現」から、検討すべきアーキテクチャの候補を迅速に想起し、前提条件を検証するための逆引きリファレンスである。表層的なキーワードだけで短絡的に選択せず、第3列に記載された技術的制約（接続元、データ鮮度、障害スコープ、互換性等）を満たしているかを必ず確認すること。

---

## 設問キーワード逆引き一覧

| 設問における典型的な要件・キーワード | 検討すべきアーキテクチャ・候補サービス | 選定時に必ず検証すべき条件・制約 |
|---|---|---|
| **「運用オーバーヘッド（管理工数）を最小限に」** | フルマネージドサービス／サーバーレス（AWS Lambda、AWS Fargate、Aurora Serverless、DynamoDB、AWS Glue、Amazon Athena） | 処理時間の上限（Lambdaは15分以内）、OSカーネル制御の要否、既存アプリとの互換性、および定常的な高負荷特性の有無（常時稼働ではEC2の方が割安になる場合がある）。 |
| **「最小限のコード変更で」「既存システムをそのまま移行」** | 各種マネージド互換サービス（Amazon MQ、Amazon DocumentDB、Amazon Keyspaces、Amazon MSK、Amazon EKS、Babelfish for Aurora PostgreSQL、Amazon FSx、AWS Transfer Family） | 既存システムが依存しているプロトコル（JMS, AMQP等）やデータベースエンジンとの完全な互換性が満たされているか。 |
| **「最もコスト効率が高い構成」** | 要件を満たす選択肢群の中で最も安価な構成（スポットインスタンス、S3ライフサイクル、S3 Intelligent-Tiering、Savings Plans、サーバーレス、EBS gp3、AWS Graviton） | 稼働時間、データ転送量、停止可能性、中断許容度。**設問の可用性・耐障害性要件（マルチAZ等）やRTO/RPOを満たせない安価な選択肢は誤答となる**。 |
| **「高可用性を実現する」** | マルチAZ配置、Auto Scalingグループ（`Min=2` 以上）、Elastic Load Balancing、リージョン内冗長化 | 設問が求める障害耐性の範囲（単一インスタンス、AZ障害、リージョン障害）。※マルチAZは論理的な誤削除やデータ破損には効果がない。 |
| **「ディザスタリカバリ（DR）」「リージョン規模の障害に備える」** | クロスリージョン展開（S3 クロスリージョンレプリケーション、Auroraグローバルデータベース、DynamoDBグローバルテーブル、Route 53 DNSフェイルオーバー） | 目標復旧時間（RTO）と目標復旧時点（RPO）の数値基準、およびフェイルオーバー処理が自動か手動か。 |
| **「RTOおよびRPOをほぼゼロに抑える」** | マルチサイト（アクティブ/アクティブ）構成 | データレプリケーション方式が同期またはニアリアルタイム同期か。インフラ運用コストは最高水準となる。 |
| **「数分〜数十分以内に復旧させ、コストは最小限に抑える」** | ウォームスタンバイ構成 または パイロットライト構成 | RTOを満たすためのプロビジョニング手順が自動化されているか。RPOはDBレプリケーション遅延によって決定される。 |
| **「スケーラブル」「急激で予測不能なトラフィック変動」** | EC2 Auto Scaling、サーバーレス（API Gateway ＋ Lambda）、DynamoDBオンデマンドモード | スパイク発生時の立ち上がり速度（EC2インスタンスの初期化時間が数分かかる点に留意し、ウォームプール等の要否を検証）。 |
| **「疎結合アーキテクチャ」「コンポーネント間の依存を排除」** | Amazon SQS、Amazon SNS、Amazon EventBridge | 単一ワーカーによる分担処理（SQS）か、複数購読者への一斉配信（SNS同報）か。処理順序（FIFO）や再試行制御の要否。 |
| **「リアルタイム処理」「ストリーミングデータの取り込み」** | Amazon Kinesis Data Streams、Kinesis Data Firehose、Managed Service for Apache Flink | 複数のコンシューマーが同一データを反復処理するか（Streams）、S3/Redshift等へ自動ロードするだけか（Firehose）。 |
| **「一桁ミリ秒の応答レイテンシ」** | Amazon DynamoDB（オンデマンド/プロビジョンド） | アクセスパターンがプライマリキー検索として事前に固定・設計可能か。 |
| **「マイクロ秒の極めて低い応答レイテンシ」** | Amazon ElastiCache（Redis/Memcached）、Amazon DynamoDB Accelerator (DAX) | データの鮮度要件（キャッシュ有効期限中の遅延許容）および整合性要件（DAXは結果整合性の読み取りのみをキャッシュ）。 |
| **「サブミリ秒・数百GB/s規模のスループット（HPC・機械学習）」** | Amazon FSx for Lustre | Amazon S3バケットとの透過的な連携要件、およびクライアントがLinux OSか。 |
| **「API呼び出しの監査」「誰がいつ何を実行したかを追跡」** | AWS CloudTrail（管理イベント、データイベント） | 90日を超える長期保管が必要な場合は、S3バケットへの証跡（Trail）出力またはCloudTrail Lakeが必須。 |
| **「コンプライアンス準拠」「データの改変・削除防止（WORM要件）」** | Amazon S3 オブジェクトロック（コンプライアンスモード）、AWS Backup Vault Lock | ルートユーザーであってもロック期間中の削除を不可とする厳格な法的規制か（コンプライアンスモード）。 |
| **「個人情報（PII）や機密データが含まれていないかを検出」** | Amazon Macie（S3バケットのスキャン）、Amazon Comprehend（テキストからのPII抽出） | 検査対象がS3上のオブジェクトストレージか、アプリケーション内部で処理される自然言語テキストか。 |
| **「通信をパブリックインターネットに一切出さない」** | VPCエンドポイント（Gateway / Interface）、AWS PrivateLink、AWS Direct Connect | **接続元クライアントの物理的な位置が同一VPC内か、オンプレミスか**。S3であってもオンプレミスからの閉域アクセスにはインターフェース型エンドポイントが必須。 |
| **「EC2にパブリックIPを持たせずに管理・アクセスしたい」** | NAT Gateway（アウトバウンド通信用）、**AWS Systems Manager Session Manager**（安全なインバウンドシェル接続）、VPCエンドポイント | 通信の方向性（サーバーから外部APIへ出る通信か、運用者がサーバーへ入る操作か）。※Session Managerは踏み台サーバーやSSHポート開放を完全排除する。 |
| **「固定パブリックIPアドレスが必要（外部FW登録等）」** | Network Load Balancer (NLB)、AWS Global Accelerator、Elastic IPアドレス | プロトコル要件（HTTP/HTTPSを終端したい場合は、Global Accelerator ＋ ALB または NLB ＋ ALBの組み合わせ）。 |
| **「ソースコード内に認証情報を埋め込まない」** | IAMロール（EC2/Lambda用）、AWS Secrets Manager、AWS Systems Manager Parameter Store | パスワードやアクセストークンの自動ローテーション機能が必要か（Secrets Manager）。 |
| **「暗号鍵を自社の専有ハードウェアで完全に制御したい」** | AWS CloudHSM、SSE-C（顧客提供鍵）、KMSへのインポートキー | 規制要件が「AWSオペレーターによる鍵への物理的アクセスの完全排除（FIPS 140-2 レベル3）」を義務付けているか。 |
| **「外部パートナーやユーザーへ特定ファイルを一時的に安全共有」** | Amazon S3 事前署名URL（Presigned URL） | URLの有効期限設定、および発行主体であるIAMロールの適切なアクセス権限付与。 |
| **「特定IPアドレスやCIDRブロックからの攻撃を遮断」** | ネットワークACL（サブネット単位・L3/L4の拒否ルール）、AWS WAF（HTTP/HTTPSのIPセット拒否）、CloudFront 地理的制限（国単位遮断） | 遮断すべきネットワーク階層（L3/L4パケットか、L7 HTTPリクエストか）。※セキュリティグループは拒否（Deny）ルールを定義できない。 |
| **「SQLインジェクション、クロスサイトスクリプティング（XSS）防御」** | AWS WAF（マネージドルール、レート制限） | WAFの関連付け先がApplication Load Balancer、Amazon CloudFront、Amazon API Gatewayのいずれかであること（NLBには適用不可）。 |
| **「大規模DDoS攻撃からの防御と請求保護」** | AWS Shield Advanced | 専門チーム（SRT）による24時間年中無休の対応や、DDoS攻撃起因のコスト急増に対する経済的保護が求められているか。 |
| **「開発者が起動できるインフラ構成を承認済みのものだけに制限」** | AWS Service Catalog（＋SCP、IAMアクセス許可境界） | ガバナンスの焦点が「利用可能なサービスそのものの制限（SCP）」か、「承認されたテンプレートのセルフサービス提供（Service Catalog）」か。 |
| **「複数アカウントのガバナンスとガードレールの一元管理」** | AWS Organizations ＋ SCP、AWS Control Tower、AWS Firewall Manager | 単なる請求・ポリシー統合か、ランディングゾーン全体のベストプラクティス自動構築（Control Tower）か。 |
| **「EC2インスタンスへの手動パッチ適用を自動化したい」** | AWS Systems Manager Patch Manager | パッチ適用の対象がEC2ゲストOS（利用者責任）か、マネージドサービス（AWS責任）か。 |
| **「踏み台サーバー（Bastion Host）とSSHキー管理を廃止したい」** | AWS Systems Manager Session Manager | インバウンド22番ポートを安全に閉じ、IAMとCloudTrailによってシェル操作ログを集中管理する。 |
| **「リソースの設定が勝手に変更されていないかを継続的に監査」** | AWS Config（マネージドルール ＋ SSM Automation自動修復） | 評価の目的が「リソース構成の時系列変更履歴とコンプライアンス準拠（Config）」か、「API操作者の特定（CloudTrail）」か。 |
| **「EC2インスタンスのメモリ使用率やディスク空き容量を監視」** | CloudWatchエージェント（Unified Agent）の導入によるカスタムメトリクス収集 | メモリやディスク内部情報はゲストOS内部のリソースであり、ハイパーバイザー側の標準メトリクスでは取得できないことの理解。 |
| **「ログファイル内の特定文字列（ERROR等）を検知して通知」** | CloudWatch Logs メトリクスフィルタ ＋ CloudWatch アラーム ＋ Amazon SNS | 検出パターンの定義、数値メトリクスへの変換、およびSNSトピック経由の管理者通知。 |
| **「オンプレミスから大容量データをネットワーク帯域を圧迫せず移行」** | AWS Snowball Edge（物理アプライアンス輸送）／AWS DataSync（専用線・オンライン高速同期） | ネットワーク帯域幅と移行期限の比較（数週間〜数か月かかる場合はSnowball等のオフライン物理移送が最速かつ安価）。 |
| **「データベースを本番稼働させたままAWSへ移行」** | AWS Database Migration Service (DMS) ＋ AWS SCT | 同種エンジン間移行か、異種エンジン間移行か（異種の場合は事前にAWS SCTによるスキーマ変換が必須）。 |
| **「取引先の既存SFTPワークフローを変更せずにS3へ格納」** | AWS Transfer Family（SFTP/FTPS/FTPエンドポイント） | 外部パートナーのクライアントソフトやプロトコルを変更せず、バックエンドをS3/EFSに統合する。 |
| **「Webセッション情報の外部集中管理」** | Amazon ElastiCache（Redis）／Amazon DynamoDB | ノード障害時にもセッションを消失させないためのマルチAZ・永続化要件（Memcachedは永続化非対応のため不適）。 |
| **「静的Webコンテンツの安全かつ低遅延なグローバル配信」** | Amazon S3 ＋ Amazon CloudFront（オリジンアクセスコントロール: OAC） | S3バケットのパブリックアクセスを完全に遮断し、CloudFrontからの署名リクエストのみをバケットポリシーで許可する構成。 |
| **「画像アップロードを契機とした非同期バックグラウンド処理」** | S3イベント通知 → Amazon SQS / SNS → AWS Lambda / ECS | 後続処理を実行するシステムが単一（SQSバッファ）か、複数システムへの同時通知（SNSファンアウト）か。 |
| **「アクセススパイクによるバックエンドデータベースの過負荷・停止防止」** | 前段へのAmazon SQS配置によるバッファリング、Amazon ElastiCacheによる読み取りオフロード | スパイクが一時的なトラフィック集中か（SQSで吸収可能）、持続的な容量不足か（DBスケーリングが必要）。 |
| **「メッセージの重複処理によるデータ不整合の防止」** | SQS可視性タイムアウトの適正化 ＋ ワーカー処理の**冪等性（Idempotency）の担保** | SQS標準キューだけでなくFIFOキューであってもネットワーク再送等により重複配信は発生し得るため、アプリケーション側で冪等性を確保する。 |
| **「処理に失敗したメッセージの消失防止」** | **デッドレターキュー（DLQ）**の構成 ＋ CloudWatchアラームによる滞留監視 | 失敗メッセージを隔離するだけでなく、原因調査後に再処理（Redrive）を行う運用フローを整備する。 |
| **「Webアプリがエラーを返しているのにEC2が正常と判定される」** | Auto Scalingグループのヘルスチェックタイプを**「ELB」**に変更する | EC2標準のステータスチェック（ハイパーバイザー/ハードウェア健全性）だけでは、OS内部のWebサーバープロセスの死活を検知できないため。 |
| **「世界中の分散拠点からのアクセスレイテンシを均一に短縮」** | Amazon CloudFront、AWS Global Accelerator、Route 53 レイテンシーベースルーティング | 対象コンテンツがエッジでキャッシュ可能か（CloudFront）、非HTTP・動的パケットか（Global Accelerator）。 |

---

## 主要な数値クォータと仕様基準一覧

本表に記載された仕様数値は、公式ドキュメントに準拠した基準値である。**「デフォルト値」「調整可能な上限」「固定のハードリミット」「設計上の推奨目安」**の区分を意識して活用すること。

「仕様・基準値」末尾のタグが区分（既定／上限（調整可）／上限（固定）／目安／設定範囲／仕様）を示す。「根拠」列の日付は、実際にそのページを開いて値を確認した日。「未確認」は本文の記述に基づいており、実装時に再確認する。「従来は〜」と書いた値は、古い設問がその値を前提にしていることがあるため併記している。設問に条件が明示されていればそちらを優先する。

| 設計項目 | 仕様・基準値 | 区分・条件 | 公式ドキュメント・根拠 |
|---|---|---|---|
| **AWS Lambda 最大実行時間** | **900秒（15分）**・**上限（固定）** | ハードリミット（固定上限）。Lambda Managed Instances の非同期／イベントソース呼び出しのみ最大90分（例外） | [Lambda クォータ](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html)・2026-09-13 |
| **AWS Lambda メモリ割り当て** | **128 MB 〜 10,240 MB（10 GB）**・上限（固定） | 1 MB刻みで設定可能。CPUパワーはメモリ量に正比例（1,769 MBで1 vCPU相当） | 同上・2026-09-13 |
| **AWS Lambda 同時実行数** | **1,000**（初期デフォルト値）・**既定（調整可）** | リージョン単位のソフトリミット（申請により引き上げ可能）。新規アカウントはこれより低く設定され、利用に応じて自動で引き上げられる | 同上・2026-09-13 |
| **AWS Lambda 一時ストレージ（`/tmp`）** | **512 MB 〜 10,240 MB（10 GB）**・上限（固定） | 1 MB刻みで設定可能 | 同上・2026-09-13 |
| **AWS Lambda パッケージサイズ** | 直接zip: 50 MB / 解凍後: 250 MB / コンテナイメージ: 10 GB・上限（固定） | ハードリミット（レイヤーを含む） | 同上・2026-09-13 |
| **Amazon SQS メッセージ保持期間** | **デフォルト: 4日間** / 設定範囲: 60秒 〜 14日間・**既定／設定範囲** | 標準キュー・FIFOキュー共通 | [SQS クォータ](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html)・2026-09-13 |
| **Amazon SQS メッセージ最大サイズ** | **1,048,576 バイト（1 MiB）**・**上限（固定）** | 単一メッセージ本体の上限。拡張クライアントライブラリとS3を併用すれば最大2 GB。**従来は 256 KB**（古い設問はこの値を前提にしていることがある） | 同上・2026-09-13 |
| **Amazon SQS 可視性タイムアウト** | **デフォルト: 30秒** / 設定範囲: 0秒 〜 12時間・**既定／設定範囲** | ワーカー処理時間に応じて設定。API呼び出しにより処理中の延長も可能 | 同上・2026-09-13 |
| **Amazon SQS 配信遅延（遅延キュー）** | デフォルト: 0秒 / 最大: 15分・既定／上限（固定） | キュー全体またはメッセージ単位で設定可能 | 同上・2026-09-13 |
| **Amazon SQS ロングポーリング待機時間** | **最大: 20秒**・上限（固定） | `WaitTimeSeconds` を1〜20秒に設定。空の受信APIコールを削減してコスト抑制 | [SQS ポーリング](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html)・2026-09-13 |
| **Amazon SQS FIFO スループット** | デフォルト: 300 TPS（バッチ10件で最大3,000メッセージ/秒）・**既定モード**（APIアクション・パーティションごと） | **高スループットモード**を有効化することで数万TPSまで拡張可能。TPS（API 呼び出し数）とメッセージ/秒を混同しない | [SQS クォータ](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html)・2026-09-13 |
| **Amazon SQS FIFO 重複排除期間** | **5分間**・仕様 | 送信側のメッセージ重複排除ID（MessageDeduplicationId）に基づくウィンドウ | [FIFO 正確に1回の処理](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-exactly-once-processing.html)・未確認（本文の記述に基づく） |
| **Amazon S3 単一オブジェクト最大サイズ** | **48.8 TiB**・**上限（固定）** | マルチパートアップロード利用時（最大10,000パート × 最大5 GiB/パート）。**従来は 5 TB**（古い設問はこの値を前提にしていることがある） | [S3 オブジェクトサイズ制限](https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html)・2026-09-13 |
| **Amazon S3 単一PUTリクエスト上限** | **5 GiB**・上限（固定） | 100 MBを超えるオブジェクトはマルチパートアップロードの利用が強く推奨される | 同上・2026-09-13 |
| **Amazon S3 プレフィックス別リクエスト性能** | **毎秒 3,500 PUT/POST/DELETE、毎秒 5,500 GET/HEAD**・**目安（「少なくとも」）** | プレフィックスあたりのベースライン性能。プレフィックスを分散することで線形にスケール。スケール中は一時的に 503 が返ることがある | [S3 パフォーマンス最適化](https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html)・2026-09-13 |
| **Amazon S3 最低保管期間（課金）** | Standard-IA: 30日 / One Zone-IA: 30日 / Glacier Instant: 90日 / Glacier Flexible: 90日 / Glacier Deep Archive: 180日・課金条件 | 期間未満で削除・移行した場合でも最低日数分の料金が発生。IA 系は最小課金サイズ 128 KB | [S3 ストレージクラス](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html)・2026-09-13 |
| **Amazon S3 Glacier 取り出し所要時間** | Flexible: 迅速（1〜5分）、標準（3〜5時間）、大容量（5〜12時間） / Deep Archive: 標準（12時間以内）、大容量（48時間以内）・**目安（typically）** | 設計時の目安所要時間 | [S3 アーカイブ復元](https://docs.aws.amazon.com/AmazonS3/latest/userguide/restoring-objects-retrieval-options.html)・2026-09-13 |
| **Amazon DynamoDB 単一項目サイズ上限** | **400 KB**・上限（固定） | 属性名と属性値のバイナリ合計サイズ | [DynamoDB 仕様](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.NamingRulesDataTypes.html)・2026-09-13 |
| **Amazon DynamoDB キャパシティ単位の定義** | 1 RCU = 4 KBの項目を強い整合性で1回/秒（結果整合性は0.5 RCU、トランザクションは2 RCU）<br>1 WCU = 1 KBの項目を1回/秒（トランザクションは2 WCU）・定義 | 読み書きデータ量は4 KB / 1 KB単位に切り上げて計算 | [DynamoDB キャパシティ](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/read-write-operations.html)・2026-09-13 |
| **Amazon DynamoDB ポイントインタイムリカバリ（PITR）** | **過去35日間**・設定範囲（1〜35日） | 有効化後、秒単位の任意の時点へテーブルを復元可能 | [DynamoDB PITR](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/PointInTimeRecovery_Howitworks.html)・2026-09-13 |
| **Amazon RDS 自動バックアップ保持期間** | **0日 〜 35日間**（デフォルト: 7日間）・設定範囲 | 0日に設定すると自動バックアップが無効化される（リードレプリカが存在する場合は無効化不可） | [ModifyDBInstance API（0〜35日の制約の記載元）](https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_ModifyDBInstance.html)・2026-09-13 ／ [RDS バックアップ概要](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html) |
| **Amazon Aurora ストレージ上限** | **128 TiB または 256 TiB**（エンジンバージョン依存）・**上限（固定・バージョン依存）** | 10 GB単位で自動拡張。Aurora PostgreSQL 15.13+/16.9+/17.5+、Aurora MySQL 3.10+で256 TiB対応 | [Aurora クォータ](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_Limits.html)・2026-09-13 |
| **Amazon Aurora リードレプリカ最大数** | **最大15台**・上限（固定、引き上げ不可） | プライマリクラスタ配下に配置可能 | 同上・2026-09-13 |
| **Amazon Aurora ストレージの物理冗長性** | **3つのアベイラビリティゾーンにまたがる6つのコピー**・仕様 | クォーラム構成（書き込みは6中4、読み取りは6中3の合意で成立） | [Aurora ストレージアーキテクチャ](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Overview.StorageReliability.html)・未確認（本文の記述に基づく） |
| **Amazon Kinesis Data Streams シャード性能** | 書き込み: 1 MB/秒 または 1,000 レコード/秒<br>読み取り: 2 MB/秒・上限（固定） | プロビジョンドモード時のシャード1つあたりの上限。1 レコードの最大は 10 MiB（バースト用途） | [Kinesis クォータ](https://docs.aws.amazon.com/streams/latest/dev/service-sizes-and-limits.html)・2026-09-13 |
| **Amazon Kinesis Data Streams データ保持期間** | **デフォルト: 24時間** / 設定範囲: 24時間 〜 365日間（8,760時間）・既定／設定範囲 | 24時間を超える保持は追加料金が発生 | 同上・2026-09-13 |
| **Amazon VPC サブネット内の予約IPアドレス** | **各サブネットごとに先頭4個 ＋ 末尾1個の計5個**・仕様 | ネットワークアドレス、VPCルーター、DNSサーバー、将来用、ブロードキャストアドレス | [VPC サイジング](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html)・2026-09-13 |
| **ELB 登録解除の遅延（Deregistration Delay）** | **デフォルト: 300秒** / 設定範囲: 0秒 〜 3,600秒・**既定**／設定範囲 | ターゲットの切り離し時に処理中の既存リクエスト完了を待機する接続ドレイン時間 | [ALB ターゲットグループ属性](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/edit-target-group-attributes.html)・2026-09-13 |
| **AWS KMS キー削除待機期間** | **7日間 〜 30日間**（デフォルト: 30日間）・設定範囲／既定 | 誤削除防止のための強制待機期間。待機中は暗号化・復号操作不可、削除取り消し可能 | [KMS キー削除](https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html)・2026-09-13 |
| **AWS KMS 自動ローテーション周期** | **90日 〜 2,560日間**（デフォルト: 365日 / 年1回）・設定範囲／既定 | カスタマー管理キー（対称暗号化キー）で設定可能。AWSマネージドキーは年1回固定 | [KMS ローテーション](https://docs.aws.amazon.com/kms/latest/developerguide/rotating-keys-enable.html)・2026-09-13 |
| **AWS CloudTrail イベント履歴保持期間** | **直近90日間**・仕様 | マネジメントコンソールのイベント履歴。90日を超える保管はS3への証跡作成が必要 | [CloudTrail イベント履歴](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html)・2026-09-13 |
| **Amazon EC2 スポットインスタンス中断通知** | **終了の2分前**・仕様 | CloudWatch Events/EventBridgeおよびインスタンスメタデータ経由で通知。休止（hibernate）の場合は2分の猶予なし。通知はベストエフォート | [スポット中断通知](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-instance-termination-notices.html)・2026-09-13 |
| **Kinesis Data Firehose バッファリング間隔** | **0秒 〜 900秒（15分）** / デフォルト: 300秒・設定範囲／既定 | バッファサイズ（1 MB〜128 MB）または指定間隔のいずれかを満たした時点で配信。0 秒は対応宛先のみで、動的パーティショニングと S3 バックアップ先では不可。60 秒未満は S3 の PUT 料金が増える | [Firehose 設定](https://docs.aws.amazon.com/firehose/latest/dev/create-configure-backup.html)・2026-09-13 |
| **ACM エクスポート可能なパブリック証明書** | **有効期間 198日**／失効の45日前に自動更新・仕様 | 追加料金あり。エクスポート後の配置と更新後の再配置は利用者が管理する | [ACM エクスポート可能証明書](https://docs.aws.amazon.com/acm/latest/userguide/acm-exportable-certificates.html)・2026-09-13 |

---

## 本番試験における解答プロセス（推奨手順）

設問を解く際は、以下の3ステップに従って思考を展開することで、ミスを最小限に抑え正解率を高めることができる。

1. **前提となる絶対条件・制約の抽出**：
   - 設問文から「可用性要件（単一AZ耐性かリージョン耐性か）」「目標復旧指標（RTO/RPOの数値）」「データ保持・コンプライアンス要件」「既存資産とのプロトコル互換性」「実行時間制限」などの**外せない絶対条件**を特定する。
   - 「最もコスト効率の高い」「運用負荷を最小限に」といった比較形容詞に惑わされる前に、まず満たすべき必要条件を確定させる。
2. **要件を満たせない不適格な選択肢の論理的除外（消去法）**：
   - 「高可用性が求められているのに単一AZ構成になっている」「処理時間が30分かかるのにLambdaを選んでいる」「NLBに直接AWS WAFをアタッチしようとしている」「RDSマルチAZのスタンバイに読み取りクエリを向けようとしている」など、明確な技術的矛盾を理由に誤答を排除する。
3. **最優先の評価軸に基づく最終選定**：
   - 条件を満たす有効な選択肢が複数残った段階で、設問が求める優先評価軸に従って比較する。
     - **「最もコスト効率が良い」**：条件を満たす構成の中で、インフラ利用料金が最も安価なものを選択。
     - **「運用負荷（管理工数）を最小限に」**：サーバーレスやフルマネージドサービスを最優先で選択。
     - **「パフォーマンスを最大化」**：性能低下の根本原因にダイレクトに効くキャッシュや並列化構成を選択。

---

[目次に戻る](./README.md) ／ [付録A 横断比較表](./90-comparison.md)

