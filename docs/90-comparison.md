# 付録A 横断比較表（復習用）

> **本表の活用法**：類似・競合するAWSサービスの選定において、素早く候補を絞り込み、最終的な判断を下すための整理表である。キーワードの表層的な一致だけで安易に判断せず、第3列に記載された「接続元」「データの整合性・鮮度」「耐障害性の範囲」「プロトコル互換性」などの詳細制約を必ず検証すること。本編各章で基礎概念と動作メカニズムを理解した後の総点検・直前復習ツールとして活用する。

---

## ストレージ

| 比較対象 | 主要な判断軸・使い分け | 設計時に検証すべき条件・制約 |
|---|---|---|
| **S3 / EBS / EFS** | オブジェクト形式（HTTP経由・容量無制限）＝**S3**／単一インスタンス専用ブロック＝**EBS**／複数インスタンス同時共有ファイル＝**EFS** | 「複数から同時に読み書きする」要件において、標準POSIXファイルシステムが必要か（EFS）、API経由のオブジェクトアクセスでよいか（S3）。※EBSは同一AZ・単一インスタンスが原則（io2のMulti-Attachを除く）。 |
| **EBS / インスタンスストア** | 永続的・AZ内で付け替え可能＝**EBS**／ホスト停止時に消滅する超高速NVMe一時領域＝**インスタンスストア** | 「データ消失が許容されるワークロードか」。キャッシュ、バッファ、スクラッチ領域以外の永続データにインスタンスストア単体を使用してはならない。 |
| **EFS / FSx for Windows** | Linuxネイティブ（NFSプロトコル）＝**EFS**／Windows・Active Directory統合（SMBプロトコル）＝**FSx for Windows** | クライアントOSの種類、プロトコル（NFSかSMBか）、およびActive Directory認証の要否。 |
| **FSx for Lustre / EFS** | HPC・機械学習・数百GB/s以上の高スループット・S3連携＝**FSx for Lustre**／汎用共有ファイル＝**EFS** | スループット要件の桁数、およびAmazon S3データレイクとの透過的な高速連携が必要か。 |
| **S3 Standard-IA / One Zone-IA** | 複数AZの耐障害性が必要＝**Standard-IA**／再生成可能で単一AZで最安＝**One Zone-IA** | AZ障害によるデータ消失が許容されるか（再作成可能なサムネイル、他リージョンの複製等）。 |
| **Glacier Instant / Flexible / Deep Archive** | ミリ秒単位の即時取り出し＝**Instant**／数分〜数時間＝**Flexible**／12〜48時間の最安長期保管＝**Deep Archive** | 取り出しまでに許容される時間、および最低保管期間（Instant: 90日 / Flexible: 90日 / Deep Archive: 180日）。 |
| **ライフサイクル / Intelligent-Tiering** | アクセス頻度の低下パターンが既知＝**ライフサイクル**／アクセス頻度が予測不能・不規則＝**Intelligent-Tiering** | アクセス頻度の予測可能性。※128KB未満の極小オブジェクトはIntelligent-Tieringの自動階層化対象外。 |
| **Storage Gateway / DataSync** | オンプレミスからAWSストレージを**日常的に継続利用**＝**Storage Gateway**／オンプレミス↔AWS間の**移行・定期同期**＝**DataSync** | オンプレミス業務アプリからハイブリッドで読み書きし続けるか、一方向にバッチ同期するか。 |
| **S3 Transfer Acceleration / CloudFront** | S3バケットへの**アップロード高速化**＝**Transfer Acceleration** | グローバルエンドユーザーへの**コンテンツ配信・キャッシュ**＝**CloudFront** | トラフィックの方向（インバウンドアップロードか、アウトバウンド配信か）。 |

---

## コンピューティング

| 比較対象 | 主要な判断軸・使い分け | 設計時に検証すべき条件・制約 |
|---|---|---|
| **EC2 / Lambda** | 15分超の処理・OS完全制御・常時高負荷＝**EC2**／イベント駆動・インフラ管理不要＝**Lambda** | 連続実行時間（Lambdaは最大15分）、OS/ミドルウェアの制御要否、トラフィックの定常性（常時高負荷ではEC2のRI/SPが割安）。 |
| **ECS / EKS** | AWSネイティブで管理負荷を最小化＝**ECS**／Kubernetesエコシステム・既存マニフェスト流用＝**EKS** | 単にコンテナを動かしたいだけか、Kubernetes（kubectl, Helm, CRD）の互換性が必須要件か。 |
| **Fargate / EC2起動タイプ** | サーバー管理不要のサーバーレス運用＝**Fargate**／GPU利用・特殊カーネル・高密度集約＝**EC2** | GPU利用、特定インスタンスファミリの指定、デーモンセット等のホスト制御が必要か。 |
| **Lambda / AWS Batch** | 実行時間15分以内の軽量処理＝**Lambda** | 15分を超える長時間の並列計算バッチ・ジョブキュー＝**AWS Batch** | 処理時間、およびスポットインスタンスによるコスト最適化の要否。 |
| **AWS Batch / Step Functions** | 大規模計算ジョブのスケジューリング・実行＝**AWS Batch**／処理手順・条件分岐・エラー処理のフロー制御＝**Step Functions** | 「計算リソースとジョブの実行基盤」か、「複数サービスのワークフロー制御」か。 |
| **Elastic Beanstalk / CloudFormation** | アプリケーションコード中心の自動展開＝**Beanstalk**／インフラ全体の厳密なIaC定義＝**CloudFormation** | インフラの高度なカスタマイズが必要か、Webアプリ環境の迅速な構築を最優先とするか。 |
| **スポット / RI / Savings Plans** | 中断耐性のあるワークロード＝**スポット**／特定インスタンスの最安コミット＝**RI**／柔軟な1〜3年コミット＝**Savings Plans** | 中断発生時に再実行可能なアーキテクチャか。将来的なインスタンスタイプ変更の可能性があるか。 |
| **Dedicated Host / Dedicated Instance** | ソケット数・物理コア単位のBYOLライセンス管理＝**Dedicated Host**／他テナントとのハードウェア分離のみ＝**Dedicated Instance** | ソフトウェアライセンスが物理ソケット・物理コア数にバインドされているか。 |

---

## ネットワーク

| 比較対象 | 主要な判断軸・使い分け | 設計時に検証すべき条件・制約 |
|---|---|---|
| **ALB / NLB** | HTTP/HTTPS、L7パスルーティング、WAF連携＝**ALB**／TCP/UDP、固定IP、超低遅延、高スループット＝**NLB** | プロトコル種別、固定グローバルIPの要否、およびWAFによるWebアプリケーション保護の要否。 |
| **セキュリティグループ / ネットワークACL** | ステートフル・インスタンス単位・許可のみ＝**SG**／ステートレス・サブネット単位・明示的拒否＝**NACL** | 特定IPアドレスの遮断（Deny）が必要か（L3/L4遮断はNACL、HTTPリクエスト遮断はWAF、国単位はCloudFront）。 |
| **ゲートウェイ型 / インターフェース型エンドポイント** | VPC内からのS3/DynamoDBアクセス（追加料金なし）＝**ゲートウェイ型**／その他のサービス、またはオンプレミス/ピアリング経由＝**インターフェース型** | **接続元が同一VPC内か、オンプレミス/別VPCか**。S3であってもオンプレミスやDirect Connect経由でアクセスする場合はインターフェース型が必須。 |
| **VPCピアリング / Transit Gateway** | 少数のVPC間を1対1で直接接続＝**ピアリング**／多数のVPC・オンプレミスをハブ＆スポークで集約＝**Transit Gateway** | VPCの接続数、および推移的ルーティング（Transitive Routing）の要否。CIDRブロックの重複がないか。 |
| **Direct Connect / Site-to-Site VPN** | 安定した広帯域・極めて低いジッター（納期数週間）＝**Direct Connect**／即時導入・低コスト・標準IPsec暗号化＝**VPN** | 開通までのリードタイム、回線帯域の安定性要件、および暗号化要件（DXは標準では平文通信）。 |
| **CloudFront / Global Accelerator** | HTTP/HTTPSコンテンツのキャッシュとエッジ配信＝**CloudFront**／非HTTP（TCP/UDP）、静的Anycast IP、高速フェイルオーバー＝**Global Accelerator** | キャッシュが有効なコンテンツか、プロトコル種別、および固定IPアドレスがクライアント要件か。 |
| **Route 53 フェイルオーバー / Global Accelerator** | DNSレベルの切り替え（TTLの遅延許容）＝**Route 53**／IPレベルの即時切り替え（数秒〜数十秒）＝**Global Accelerator** | 障害発生時のフェイルオーバー許容時間（DNSキャッシュTTLの影響を排除したいか）。 |
| **CloudFront Functions / Lambda@Edge** | 超軽量・サブミリ秒・ビューア側イベントのみ＝**CloudFront Functions**／オリジン側イベント・外部ネットワークアクセス・重い処理＝**Lambda@Edge** | 処理時間、外部API呼び出しの要否、およびリクエストボディの参照要否。 |

---

## データベース

| 比較対象 | 主要な判断軸・使い分け | 設計時に検証すべき条件・制約 |
|---|---|---|
| **RDSマルチAZ / リードレプリカ** | 高可用性・障害時の自動フェイルオーバー＝**マルチAZ**／読み取り負荷分散・参照性能向上＝**リードレプリカ** | 「スタンバイインスタンスは参照クエリを処理できない（マルチAZ DBインスタンス）」点に留意。読み取り分散にはアプリ側の接続先変更が必要。 |
| **Amazon RDS / Amazon Aurora** | 商用DBエンジン（Oracle/SQL Server）やBYOL＝**RDS**／高スループット・最大15台の高速自動拡張レプリカ＝**Aurora** | データベースエンジンがMySQL/PostgreSQL互換で要件を満たせるか。 |
| **Aurora Serverless v2 / プロビジョンド** | トラフィックが不規則・急激なスパイク＝**Serverless v2**／定常的・予測可能な高負荷＝**プロビジョンド** | アイドル時の最小ACU課金、および長期リザーブドインスタンスによる割引メリットとの比較。 |
| **Amazon RDS / Amazon DynamoDB** | 複雑な結合・ACIDトランザクション・SQLクエリ＝**RDS**／キーバリュ型・一桁ミリ秒・水平無限スケール＝**DynamoDB** | データアクセスパターンが事前に固定・設計可能か。アドホックな集計や複雑なJOINが必要か。 |
| **DynamoDB / DAX / ElastiCache** | 一桁ミリ秒のNoSQL＝**DynamoDB**／DynamoDB専用のマイクロ秒インメモリキャッシュ＝**DAX**／RDBMS等の汎用キャッシュ＝**ElastiCache** | データの整合性要件（DAXは結果整合性の読み取りのみをキャッシュ）。 |
| **Redis / Memcached** | データの永続化・レプリケーション・複雑なデータ構造＝**Redis**／シンプルなKVS・マルチスレッド処理＝**Memcached** | ノード障害時のデータ永続化やPub/Sub機能が必要か。 |
| **ElastiCache / Amazon MemoryDB** | 一時的なキャッシュ層＝**ElastiCache**／プライマリデータベースとしての高耐久性と超低遅延を両立＝**MemoryDB** | データが消失してもバックエンドから再生成可能か、唯一の正本データストアとなるか。 |
| **Amazon QLDB / Managed Blockchain** | 中央集権的な管理者による改ざん不能な台帳履歴＝**QLDB**／複数企業・組織間で信頼を分散するコンソーシアム＝**Managed Blockchain** | 信頼できる中央管理主体が存在するか、分散合意形成が必要か。 |

---

## アプリケーション統合・分析

| 比較対象 | 主要な判断軸・使い分け | 設計時に検証すべき条件・制約 |
|---|---|---|
| **Amazon SQS / Amazon SNS** | メッセージのキューイング・分散ワーカーでの分担処理＝**SQS**／複数購読者への一斉配信（Pub/Sub同報）＝**SNS** | 「1対1の分担（キュー）」か「1対Nの同報（トピック）」か。双方を組み合わせる場合はSNS→SQSのファンアウト構成。 |
| **Amazon SNS / Amazon EventBridge** | シンプルなPub/Sub同報・極低遅延＝**SNS**／ペイロード内容に基づくルーティング・AWSイベント連携・スキーマレジストリ＝**EventBridge** | メッセージのJSON属性による高度なフィルタリングや、SaaS/AWSサービス連携が必要か。 |
| **Amazon SQS / Amazon Kinesis Data Streams** | 処理完了後にメッセージを削除するタスクキュー＝**SQS**／同一ストリームを複数コンシューマーが繰り返し読み直す時系列データ＝**Kinesis** | 順序保証の要件、および保持期間内における複数コンシューマーによる並列・再処理の要否。 |
| **Kinesis Data Streams / Kinesis Data Firehose** | リアルタイムカスタム処理・データ保持・順序維持＝**Data Streams**／S3・Redshift・OpenSearch等へのサーバーレス自動ロード＝**Firehose** | データをストリーム内に一時保持して複数回読み出す必要があるか、単なるS3等への配信か。 |
| **Amazon SQS / Amazon MQ** | クラウドネイティブな新規開発＝**SQS**／既存のメッセージングプロトコル（JMS, AMQP, MQTT等）の移行＝**Amazon MQ** | オープン標準プロトコルとの後方互換性が必須要件か。 |
| **Amazon Athena / Amazon Redshift** | S3上のデータに対するサーバーレス・アドホックSQL分析＝**Athena**／常時高頻度で実行されるペタバイト級エンタープライズDWH・BI＝**Redshift** | クエリの実行頻度、応答速度要件、および常時稼働DWHのコスト対効果。 |
| **Amazon Athena / Amazon OpenSearch Service** | SQLによるリレーショナル・集計分析＝**Athena**／全文フリーワード検索・ログ分析・リアルタイム可視化（Kibana）＝**OpenSearch** | 分析対象のデータ形式、および全文検索やログ監視ダッシュボードが主目的か。 |
| **AWS Glue / Amazon EMR** | サーバーレスETL・データカタログ・ジョブ管理＝**Glue**／Hadoop/Sparkクラスタのきめ細かな制御・大規模並列分散処理＝**EMR** | 基盤インフラの制御要否、および既存のHadoop/Sparkエコシステム資産の活用要否。 |
| **Amazon Kinesis / Amazon MSK** | 完全マネージド・AWSネイティブなストリーミング＝**Kinesis**／Apache Kafkaとの完全な互換性・既存資産移行＝**Amazon MSK** | Kafkaエコシステム（Kafka Connect, Schema Registry等）の利用が必須か。 |

---

## セキュリティ・運用管理

| 比較対象 | 主要な判断軸・使い分け | 設計時に検証すべき条件・制約 |
|---|---|---|
| **CloudTrail / CloudWatch / AWS Config** | API操作履歴（誰が・いつ・何を）＝**CloudTrail**／リソースの性能メトリクスとログ＝**CloudWatch**／リソース設定の履歴とルール準拠性＝**AWS Config** | 監視・監査の対象が「ユーザー操作」「システム状態」「構成の整合性」のどれか。 |
| **GuardDuty / Inspector / Macie** | アカウントや通信の脅威・振る舞い検知＝**GuardDuty**／EC2・ECR・LambdaのOS/パッケージ脆弱性検査＝**Inspector**／S3内の個人情報・機密データ検出＝**Macie** | 検知対象が「不審なアクティビティ」「ソフトウェア脆弱性」「機密データの漏洩リスク」のどれか。 |
| **AWS Security Hub / Amazon Detective** | セキュリティ検出結果の**一元集約とコンプライアンス評価**＝**Security Hub**／インシデントの根本原因・影響範囲の**深掘りグラフ調査**＝**Detective** | 「現状の課題集約」か、「発生した侵害原因の追跡分析」か。 |
| **AWS KMS / AWS CloudHSM** | マルチテナント・マネージド暗号化・AWSネイティブ統合＝**KMS**／シングルテナント・FIPS 140-2 レベル3専用ハードウェア＝**CloudHSM** | 法規制や企業規程で専用ハードウェアによる鍵管理が義務付けられているか。 |
| **Secrets Manager / Parameter Store** | パスワードの**自動ローテーション**・シークレット管理＝**Secrets Manager**／軽量な設定値管理・無料標準パラメータ＝**Parameter Store** | 認証情報の自動更新機能が必要か、またはシンプルな環境変数・構成管理で十分か。 |
| **IAM Identity Center / Amazon Cognito** | 社内従業員のAWSコンソール/CLIログイン・SSO＝**IAM Identity Center** | Web/モバイルアプリケーションのエンドユーザー認証＝**Cognito** | 認証対象が「社内管理者・開発者」か、「一般消費者・アプリ顧客」か。 |
| **Managed Microsoft AD / AD Connector** | クラウド上にフルマネージドActive Directoryを構築＝**Managed AD**／オンプレミスの既存ADへ認証要求を中継プロキシ＝**AD Connector** | AWS側で独立したドメインコントローラーを保持するか、オンプレミスADを正本として直結するか。 |
| **AWS WAF / AWS Shield / Network Firewall** | L7 Webレイヤーの攻撃遮断（SQLi, XSS）＝**WAF**／L3/L4 DDoS攻撃防御＝**Shield**／VPC全体のL3-L7ステートフルパケット検査＝**Network Firewall** | 保護対象のレイヤー（HTTPトラフィックか、VPCネットワーク全体か）と脅威の種類。 |
| **AWS Organizations / AWS Control Tower** | マルチアカウントの一括請求とSCP＝**Organizations**／ランディングゾーン構築とガードレール自動適用＝**Control Tower** | 組織ポリシーの個別適用か、マルチアカウント基盤のベストプラクティス自動構築か。 |
| **AWS Trusted Advisor / Compute Optimizer** | コスト・性能・耐障害性・セキュリティの**総合点検**＝**Trusted Advisor**／機械学習による**インスタンス適正サイズの具体的推奨**＝**Compute Optimizer** | アカウント全体のベストプラクティス監査か、リソースのサイジング最適化か。 |
| **AWS Systems Manager / CloudFormation** | 稼働中サーバー群の**運用管理・パッチ適用・コマンド実行**＝**SSM**／インフラリソース全体の**プロビジョニング自動化（IaC）**＝**CloudFormation** | 「リソース作成後の定常運用」か、「インフラの初期構築・再現」か。 |

---

[目次に戻る](./README.md) ／ [付録B キーワード逆引き](./91-keywords.md)

