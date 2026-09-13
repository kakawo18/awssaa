# 付録A 横断比較表（復習用）

> この表は**候補を素早く思い出すためのもの**です。手掛かりに合うサービスを挙げたら、最後の列の条件を確認してください。同じキーワードでも、接続元・データの鮮度・障害範囲・互換性によって答えは変わります。初読の入口にはせず、第0章→各章の仕組み→条件違いの例を読んだあとの復習表として使う。

---

## ストレージ

| 比較 | 候補の分かれ目 | 最後に確認する条件 |
|---|---|---|
| S3 / EBS / EFS | オブジェクト（HTTPで取得・容量無制限）＝S3／**単一EC2**のブロック＝EBS／**複数EC2で共有**＝EFS | 「複数から同時に」は共有ファイルかS3か（アプリがファイルシステムを要求するか）。EBSはAZ内・1台（io2 のマルチアタッチは例外） |
| EBS / インスタンスストア | 永続・AZ内でデタッチ可＝EBS／**停止で消える**超高速な一時領域＝インスタンスストア | 「消えてよいデータか」。バッファ・キャッシュ・スクラッチ以外にインスタンスストアを使わない |
| EFS / FSx for Windows | **Linux/NFS**＝EFS／**Windows/SMB/AD**＝FSx for Windows | プロトコル（NFS か SMB）と AD 統合の要否 |
| FSx for Lustre / EFS | **HPC・数百GB/s・S3連携**＝Lustre／汎用共有＝EFS | スループット要件が桁違いか。S3 のデータを一時的に高速処理するか |
| S3 Standard-IA / One Zone-IA | 可用性が必要＝Standard-IA／**再作成可能・最安**＝One Zone-IA | AZ 障害で消えてよいか（再作成できるか、レプリカか） |
| Glacier Instant / Flexible / Deep Archive | **ミリ秒**＝Instant／**分〜時間**＝Flexible／**12〜48時間・最安・長期**＝Deep Archive | 取り出しまでの許容時間と、最低保存期間（90日／90日／180日）（→付録B） |
| ライフサイクル / Intelligent-Tiering | パターンが**既知**＝ライフサイクル／**不明・変動**＝Intelligent-Tiering | アクセス頻度を予測できるか。128KB未満の小さなオブジェクトは Intelligent-Tiering の対象外 |
| Storage Gateway / DataSync | **使い続ける（ハイブリッド運用）**＝Gateway／**移す（移行・定期同期）**＝DataSync | オンプレから継続的に読み書きするか、一方向に転送するか |
| S3 Transfer Acceleration / CloudFront | **アップロード高速化**＝Transfer Acceleration／**配信高速化**＝CloudFront | 向き（アップロードか配信か） |

## コンピューティング

| 比較 | 候補の分かれ目 | 最後に確認する条件 |
|---|---|---|
| EC2 / Lambda | 15分超・OS制御・常時稼働＝EC2／イベント駆動・運用ゼロ＝Lambda | 実行時間、OS/ミドルウェアの制御要否、常時高負荷か（常時ならLambdaは割高） |
| ECS / EKS | Kubernetes のエコシステム・マニフェスト・既存クラスタとの互換が要件＝EKS／それ以外の新規コンテナ運用＝ECS | 「Kubernetes」の語があるかではなく、**Kubernetes 互換が要件か**。運用負荷最小なら ECS on Fargate が候補 |
| Fargate / EC2起動タイプ | サーバー管理なし＝Fargate／**GPU・特殊要件・RI活用**＝EC2 | GPU・特定インスタンス・デーモン常駐が要るか。常時稼働で RI/SP を使い切れるか |
| Lambda / Batch | 15分以内＝Lambda／**長時間の計算ジョブ**＝Batch | 実行時間と、ジョブキューやスポットの活用要否 |
| Batch / Step Functions | ジョブの**実行と並列化**＝Batch／**手順と分岐の制御**＝Step Functions | 「計算資源の管理」か「ワークフローの制御」か |
| Beanstalk / CloudFormation | アプリを載せるだけ＝Beanstalk／**インフラを厳密に定義**＝CloudFormation | インフラの細かい制御が要るか、アプリだけ乗せたいか |
| スポット / RI / Savings Plans | 中断可＝スポット／固定構成で最安＝RI／**柔軟に1〜3年**＝Savings Plans | 中断されて再実行できるか。1〜3年のコミットができるか。インスタンスタイプを変える可能性があるか |
| Dedicated Host / Dedicated Instance | **ソケット/コア単位のBYOL**＝Host／専有だけ＝Instance | ライセンスがソケット/コア数に紐づくか |

## ネットワーク

| 比較 | 候補の分かれ目 | 最後に確認する条件 |
|---|---|---|
| ALB / NLB | L7ルーティング・WAF＝ALB／**TCP/UDP・静的IP・超低遅延**＝NLB | プロトコル（HTTPか TCP/UDPか）、固定IPの要否、WAF の要否 |
| SG / NACL | ステートフル・許可のみ＝SG／**ステートレス・拒否できる**＝NACL | 拒否したい対象が L3/L4 でサブネット単位か。HTTP なら WAF、国単位なら CloudFront 地理的制限が候補（→第3章 3.2） |
| ゲートウェイ / インターフェースエンドポイント | **VPC内から S3・DynamoDB・追加料金なし**＝ゲートウェイ／その他のサービス、**またはオンプレ・ピアリング越しから**＝インターフェース（ENI・有料） | **接続元は VPC 内かオンプレか**。S3 でも接続元が VPC の外ならインターフェース型（→第3章 3.3） |
| ピアリング / Transit Gateway | 2〜数個・単純＝ピアリング／**多数・推移的・ハブ集約**＝TGW | VPC の数と、推移的ルーティングの要否。CIDR が重複していないか |
| Direct Connect / Site-to-Site VPN | **一貫した帯域・低遅延（数週間かかる）**＝DX／**すぐ・安い・暗号化済み**＝VPN | 開通までの猶予、帯域の一貫性要件、暗号化要件（DX は既定で暗号化されない） |
| CloudFront / Global Accelerator | **キャッシュ・HTTP**＝CloudFront／**静的IP・TCP/UDP・高速フェイルオーバー**＝GA | キャッシュが効く内容か、プロトコル、固定IPの要否 |
| Route 53 フェイルオーバー / Global Accelerator | DNSでよい＝Route 53／**TTLを待てない**＝GA | 切替の許容時間（TTL 分の遅れを許せるか） |
| CloudFront Functions / Lambda@Edge | 超軽量・ビューア側のみ＝Functions／**オリジンアクセス・重い処理**＝Lambda@Edge | 処理時間、外部アクセスの要否、実行タイミング（ビューア側かオリジン側か） |

## データベース

| 比較 | 候補の分かれ目 | 最後に確認する条件 |
|---|---|---|
| マルチAZ / リードレプリカ | **可用性**＝マルチAZ／**読み取り性能**＝リードレプリカ | 「マルチAZ」が**DBインスタンス配置**（スタンバイは読めない）か**DBクラスター配置**（読める）か。レプリカはアプリの接続先を変えるか（→第4章 4.1） |
| RDS / Aurora | Oracle/SQL Server/BYOL＝RDS／**性能・自動拡張・15レプリカ**＝Aurora | エンジンが MySQL/PostgreSQL 互換でよいか |
| Aurora Serverless / プロビジョンド | 断続的・予測不能＝Serverless v2／安定稼働＝プロビジョンド | 停止中の課金条件（最小 ACU、自動一時停止の対応バージョン）を確認 |
| RDS / DynamoDB | 結合・トランザクション・SQL＝RDS／**キー検索・一桁ミリ秒**＝DynamoDB | アクセスパターンが固定か（キー設計できるか）。結合やアドホッククエリが要るか |
| DynamoDB / DAX / ElastiCache | 一桁ミリ秒＝DynamoDB／**DynamoDB専用のマイクロ秒キャッシュ**＝DAX／汎用キャッシュ＝ElastiCache | 鮮度（TTL の間は古い）と整合性（DAX は結果整合性の読み取りのみ） |
| Redis / Memcached | **永続化・レプリケーション・高度なデータ型**＝Redis／単純・マルチスレッド＝Memcached | 消えて困るデータか、Pub/Sub やソート済みセットが要るか |
| ElastiCache / MemoryDB | キャッシュ＝ElastiCache／**プライマリDBとして耐久性が必要**＝MemoryDB | データの唯一のコピーになるか |
| QLDB / Managed Blockchain | 単一所有者の**改変不能な履歴**＝QLDB／**複数組織で分散検証**＝Blockchain | 信頼できる中央管理者がいるか |

## アプリケーション統合・分析

| 比較 | 候補の分かれ目 | 最後に確認する条件 |
|---|---|---|
| SQS / SNS | 1つの処理系がためて分担して処理＝SQS／**複数の処理系へ同報**＝SNS | **同報か分担か**。両方なら SNS→SQS のファンアウト（→第6章 6.1） |
| SNS / EventBridge | 単純な同報・低レイテンシ＝SNS／**内容でルーティング・AWSイベント・定期実行**＝EventBridge | 配信先を JSON の内容で分岐するか。AWS サービスのイベントを拾うか |
| SQS / Kinesis | **処理したワーカーが削除する仕事のキュー**＝SQS／**保持期間内に複数が何度も読み直せる・順序**＝Kinesis | 複数のコンシューマーが同じデータを読むか。再処理が要るか |
| Kinesis Data Streams / Firehose | カスタム処理・再処理・順序＝Streams／**S3等へ配送するだけ**＝Firehose | 後から読み直す必要があるか（Firehose は保持しない） |
| SQS / Amazon MQ | 新規開発＝SQS／**既存のJMS/AMQPアプリ**＝MQ | プロトコル互換が要件か |
| Athena / Redshift | S3にアドホックSQL＝Athena／**継続的な大規模BI**＝Redshift | クエリの頻度と規模。常時稼働の DWH が要るか |
| Athena / OpenSearch | SQLでの分析＝Athena／**全文検索・リアルタイム可視化**＝OpenSearch | 全文検索・ログ可視化か、SQL 集計か |
| Glue / EMR | サーバーレスETL＝Glue／**Hadoop/Sparkを制御**＝EMR | クラスタの細かい制御や既存 Hadoop 資産が要るか |
| Kinesis / MSK | 新規・マネージド＝Kinesis／**既存Kafka**＝MSK | Kafka 互換が要件か |

## セキュリティ・管理

| 比較 | 候補の分かれ目 | 最後に確認する条件 |
|---|---|---|
| CloudTrail / CloudWatch / Config | **誰がAPIを呼んだか**＝CloudTrail／**メトリクスとログ**＝CloudWatch／**設定の履歴と準拠**＝Config | 問いが「誰が」「性能」「設定」のどれか |
| GuardDuty / Inspector / Macie | **不審な振る舞い**／**脆弱性（CVE）**／**S3の機密データ** | 対象が「挙動」「ソフトウェア」「データ内容」のどれか |
| Security Hub / Detective | 結果の**集約**／原因の**調査** | 集約して見たいか、原因を掘りたいか |
| KMS / CloudHSM | マネージド・統合＝KMS／**専有HSM・FIPS 140-2 L3**＝CloudHSM | 規制で専有 HSM が要求されるか。AWS 統合サービスとの連携が要るか |
| Secrets Manager / Parameter Store | **自動ローテーション**が要る＝Secrets Manager／無料で十分＝Parameter Store | ローテーション要件と、周辺料金（Parameter Store の高度なパラメータは有料） |
| IAM Identity Center / Cognito | **AWSを操作する社員**＝Identity Center／**アプリの利用者**＝Cognito | 認証する主体が AWS の操作者か、アプリのエンドユーザーか |
| Managed Microsoft AD / AD Connector | AWS側にADを置く＝Managed／**オンプレADへ転送するだけ**＝AD Connector | AD を AWS 側で持つか、オンプレの AD をそのまま使うか |
| WAF / Shield / Network Firewall | L7のWeb攻撃＝WAF／**DDoS**＝Shield／**VPCのL3-L7フィルタ**＝Network Firewall | 守る層（HTTP か、ネットワーク全体か）と攻撃の種類 |
| Organizations / Control Tower | 請求と**SCP**＝Organizations／**ベストプラクティス構成を自動化**＝Control Tower | 統制だけか、ランディングゾーンの自動構築まで要るか |
| Trusted Advisor / Compute Optimizer | 5観点の**広く浅い点検**／**適正サイズの機械学習推奨** | サイズ推奨が欲しいか、全般的な点検か |
| Cost Explorer / Budgets / CUR | 分析＝Explorer／**事前アラート**＝Budgets／**最詳細データ**＝CUR | 「事前に」通知したいか、詳細データを自分で分析するか |
| Systems Manager / CloudFormation | 起動後の**運用・構成管理**＝SSM／**プロビジョニング**＝CloudFormation | 作る話か、作った後に運用する話か |

---

[目次に戻る](./README.md) ／ [キーワード逆引き](./91-keywords.md)
