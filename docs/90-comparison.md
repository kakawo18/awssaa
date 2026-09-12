# 付録A 横断比較表（試験直前用）

> 迷いやすいペアだけを集めた。**「決め手」の列の単語が問題文にあれば即決**できる状態を目指す。

---

## ストレージ

| 比較 | 決め手 |
|---|---|
| S3 / EBS / EFS | オブジェクト（HTTPで取得・容量無制限）＝S3／**単一EC2**のブロック＝EBS／**複数EC2で共有**＝EFS |
| EBS / インスタンスストア | 永続・AZ内でデタッチ可＝EBS／**停止で消える**超高速な一時領域＝インスタンスストア |
| EFS / FSx for Windows | **Linux/NFS**＝EFS／**Windows/SMB/AD**＝FSx for Windows |
| FSx for Lustre / EFS | **HPC・数百GB/s・S3連携**＝Lustre／汎用共有＝EFS |
| S3 Standard-IA / One Zone-IA | 可用性が必要＝Standard-IA／**再作成可能・最安**＝One Zone-IA |
| Glacier Instant / Flexible / Deep Archive | **ミリ秒**＝Instant／**分〜時間**＝Flexible／**12〜48時間・最安・長期**＝Deep Archive |
| ライフサイクル / Intelligent-Tiering | パターンが**既知**＝ライフサイクル／**不明・変動**＝Intelligent-Tiering |
| Storage Gateway / DataSync | **使い続ける（ハイブリッド運用）**＝Gateway／**移す（移行・定期同期）**＝DataSync |
| S3 Transfer Acceleration / CloudFront | **アップロード高速化**＝Transfer Acceleration／**配信高速化**＝CloudFront |

## コンピューティング

| 比較 | 決め手 |
|---|---|
| EC2 / Lambda | 15分超・OS制御・常時稼働＝EC2／イベント駆動・運用ゼロ＝Lambda |
| ECS / EKS | **Kubernetesの記述があるか**だけ |
| Fargate / EC2起動タイプ | サーバー管理なし＝Fargate／**GPU・特殊要件・RI活用**＝EC2 |
| Lambda / Batch | 15分以内＝Lambda／**長時間の計算ジョブ**＝Batch |
| Batch / Step Functions | ジョブの**実行と並列化**＝Batch／**手順と分岐の制御**＝Step Functions |
| Beanstalk / CloudFormation | アプリを載せるだけ＝Beanstalk／**インフラを厳密に定義**＝CloudFormation |
| スポット / RI / Savings Plans | 中断可＝スポット／固定構成で最安＝RI／**柔軟に1〜3年**＝Savings Plans |
| Dedicated Host / Dedicated Instance | **ソケット/コア単位のBYOL**＝Host／専有だけ＝Instance |

## ネットワーク

| 比較 | 決め手 |
|---|---|
| ALB / NLB | L7ルーティング・WAF＝ALB／**TCP/UDP・静的IP・超低遅延**＝NLB |
| SG / NACL | ステートフル・許可のみ＝SG／**ステートレス・拒否できる（IPブロック）**＝NACL |
| ゲートウェイ / インターフェースエンドポイント | **S3・DynamoDBのみ・無料**＝ゲートウェイ／その他・ENI・有料＝インターフェース |
| ピアリング / Transit Gateway | 2〜数個・単純＝ピアリング／**多数・推移的・ハブ集約**＝TGW |
| Direct Connect / Site-to-Site VPN | **一貫した帯域・低遅延（数週間かかる）**＝DX／**すぐ・安い・暗号化済み**＝VPN |
| CloudFront / Global Accelerator | **キャッシュ・HTTP**＝CloudFront／**静的IP・TCP/UDP・高速フェイルオーバー**＝GA |
| Route 53 フェイルオーバー / Global Accelerator | DNSでよい＝Route 53／**TTLを待てない**＝GA |
| CloudFront Functions / Lambda@Edge | 超軽量・ビューア側のみ＝Functions／**オリジンアクセス・重い処理**＝Lambda@Edge |

## データベース

| 比較 | 決め手 |
|---|---|
| マルチAZ / リードレプリカ | **可用性**＝マルチAZ／**読み取り性能**＝リードレプリカ |
| RDS / Aurora | Oracle/SQL Server/BYOL＝RDS／**性能・自動拡張・15レプリカ**＝Aurora |
| Aurora Serverless / プロビジョンド | 断続的・予測不能＝Serverless v2／安定稼働＝プロビジョンド |
| RDS / DynamoDB | 結合・トランザクション・SQL＝RDS／**キー検索・一桁ミリ秒・無限スケール**＝DynamoDB |
| DynamoDB / DAX / ElastiCache | 一桁ミリ秒＝DynamoDB／**DynamoDB専用のマイクロ秒キャッシュ**＝DAX／汎用キャッシュ＝ElastiCache |
| Redis / Memcached | **永続化・レプリケーション・高度なデータ型**＝Redis／単純・マルチスレッド＝Memcached |
| ElastiCache / MemoryDB | キャッシュ＝ElastiCache／**プライマリDBとして耐久性が必要**＝MemoryDB |
| QLDB / Managed Blockchain | 単一所有者の**改変不能な履歴**＝QLDB／**複数組織で分散検証**＝Blockchain |

## アプリケーション統合・分析

| 比較 | 決め手 |
|---|---|
| SQS / SNS | ためて1つの受信側が処理＝SQS／**複数へ同報**＝SNS |
| SNS / EventBridge | 単純な同報・低レイテンシ＝SNS／**内容でルーティング・AWSイベント・定期実行**＝EventBridge |
| SQS / Kinesis | 消費したら消える＝SQS／**保持して複数が何度も読む・順序**＝Kinesis |
| Kinesis Data Streams / Firehose | カスタム処理・再処理・順序＝Streams／**S3等へ配送するだけ**＝Firehose |
| SQS / Amazon MQ | 新規開発＝SQS／**既存のJMS/AMQPアプリ**＝MQ |
| Athena / Redshift | S3にアドホックSQL＝Athena／**継続的な大規模BI**＝Redshift |
| Athena / OpenSearch | SQLでの分析＝Athena／**全文検索・リアルタイム可視化**＝OpenSearch |
| Glue / EMR | サーバーレスETL＝Glue／**Hadoop/Sparkを制御**＝EMR |
| Kinesis / MSK | 新規・マネージド＝Kinesis／**既存Kafka**＝MSK |

## セキュリティ・管理

| 比較 | 決め手 |
|---|---|
| CloudTrail / CloudWatch / Config | **誰がAPIを呼んだか**＝CloudTrail／**メトリクスとログ**＝CloudWatch／**設定の履歴と準拠**＝Config |
| GuardDuty / Inspector / Macie | **不審な振る舞い**／**脆弱性（CVE）**／**S3の機密データ** |
| Security Hub / Detective | 結果の**集約**／原因の**調査** |
| KMS / CloudHSM | マネージド・統合＝KMS／**専有HSM・FIPS 140-2 L3**＝CloudHSM |
| Secrets Manager / Parameter Store | **自動ローテーション**が要る＝Secrets Manager／無料で十分＝Parameter Store |
| IAM Identity Center / Cognito | **AWSを操作する社員**＝Identity Center／**アプリの利用者**＝Cognito |
| Managed Microsoft AD / AD Connector | AWS側にADを置く＝Managed／**オンプレADへ転送するだけ**＝AD Connector |
| WAF / Shield / Network Firewall | L7のWeb攻撃＝WAF／**DDoS**＝Shield／**VPCのL3-L7フィルタ**＝Network Firewall |
| Organizations / Control Tower | 請求と**SCP**＝Organizations／**ベストプラクティス構成を自動化**＝Control Tower |
| Trusted Advisor / Compute Optimizer | 5観点の**広く浅い点検**／**適正サイズの機械学習推奨** |
| Cost Explorer / Budgets / CUR | 分析＝Explorer／**事前アラート**＝Budgets／**最詳細データ**＝CUR |
| Systems Manager / CloudFormation | 起動後の**運用・構成管理**＝SSM／**プロビジョニング**＝CloudFormation |

---

[目次に戻る](./README.md) ／ [キーワード逆引き](./91-keywords.md)
