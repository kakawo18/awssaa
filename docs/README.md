# AWS SAA 試験ポイント集（隙間時間用）

**サービス間の違いを「問題文のキーワード → 答え」で引けること**に特化した要点集。各節は2〜3分で読み切れる分量にしてあります。

## 使い方
1. 移動中は **第1部（章別）** を1節ずつ流し読み。
2. 週末など時間が取れるときに **第2部（分野別）** で判断フローを通す。
3. 試験直前は **付録A・B** だけを繰り返す。

---

## 第1部：サービス別対策

| 章 | 内容 | 山場（間違えやすい対比） |
|---|---|---|
| [第1章 コンピューティング](./01-compute.md) | EC2 / Auto Scaling / Beanstalk / Outposts / Batch / Lambda | 購入オプション、プレイスメントグループ、ASGのヘルスチェック |
| [第2章 ストレージ](./02-storage.md) | S3 / EBS / EFS / FSx / Backup / Storage Gateway | ストレージクラス、EBS vs EFS vs FSx |
| [第3章 ネットワーク](./03-network.md) | VPC / ELB / Route 53 / CloudFront / Global Accelerator | SG vs NACL、ALB vs NLB、CloudFront vs GA |
| [第4章 データベース](./04-database.md) | RDS / Aurora / DynamoDB / ElastiCache ほか | マルチAZ vs リードレプリカ、Redis vs Memcached |
| [第5章 セキュリティ](./05-security.md) | IAM / Identity Center / Cognito / WAF / KMS ほか | GuardDuty vs Inspector vs Macie vs Config |
| [第6章 アプリケーション統合](./06-integration.md) | SQS / SNS / EventBridge / Step Functions ほか | SQS vs SNS vs EventBridge vs Kinesis |
| [第7章 アナリティクス](./07-analytics.md) | Kinesis / Glue / Athena / Redshift ほか | Athena vs Redshift vs EMR、Streams vs Firehose |
| [第8章 管理・モニタリング](./08-management.md) | CloudWatch / CloudTrail / CloudFormation / SSM ほか | CloudWatch vs CloudTrail vs Config |
| [第9章 コンテナ](./09-container.md) | ECS / EKS / Fargate / ECR | ECS vs EKS、Fargate vs EC2起動タイプ |
| [第10章 その他](./10-others.md) | API Gateway / AI系 / コスト系 / 移行系 | DMS vs DataSync vs Snowball vs Transfer Family |

## 第2部：試験分野別対策

| 章 | 出題比率 | 内容 |
|---|---|---|
| [第11章 セキュアなアーキテクチャ](./11-secure.md) | 30% | アクセス管理／データ保護／多層防御／責任共有モデル |
| [第12章 弾力性に優れたアーキテクチャ](./12-resilient.md) | 26% | スケーリング／疎結合／サーバーレス／イベント駆動／DR戦略 |
| [第13章 高パフォーマンスなアーキテクチャ](./13-performance.md) | 24% | ストレージ／コンピューティング／DB／ネットワークの性能改善 |
| [第14章 コスト最適化](./14-cost.md) | 20% | コスト管理／各レイヤーの削減策 |

## 付録

| | |
|---|---|
| [付録A 横断比較表](./90-comparison.md) | 紛らわしいペアの決め手だけを集約（直前確認用） |
| [付録B キーワード逆引き](./91-keywords.md) | 問題文の言い回し → 正解の型／暗記すべき数字 |

---

### 全体を貫く4つの判断軸
1. **運用負荷**：「オーバーヘッドを最小限に」＝マネージド／サーバーレス。
2. **可用性**：単一AZ・単一インスタンスの選択肢は原則外す。
3. **コスト**：要件を満たす候補に絞ってから、その中の最安を選ぶ。
4. **セキュリティ**：認証情報を置かない・暗号化する・公開しない・最小権限。
