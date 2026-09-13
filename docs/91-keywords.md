# 付録B 問題文キーワード → 候補と確認条件（逆引き）

> SAAの設問は**言い回しがパターン化**している。この表は、言い回しから**候補を思い出す**ためのもの。候補を挙げたら、**最後の列の条件を確認してから決める**。同じキーワードでも、接続元・データの鮮度・障害範囲・互換性によって答えは変わる。

---

## 要件を表すフレーズ

| 問題文の言い回し | 候補 | 最後に確認する条件 |
|---|---|---|
| **運用オーバーヘッドを最小限に** | マネージド／サーバーレス（Lambda、Fargate、Aurora Serverless、DynamoDB、Glue、Athena） | 実行時間（Lambda 15分）、OS 制御の要否、互換性、常時稼働か。自前 EC2 構築はこれらの制約がある場合にだけ残る |
| **最小限のコード変更で** / 既存のまま | 互換サービス（Amazon MQ、DocumentDB、Keyspaces、MSK、EKS、Babelfish、FSx、Transfer Family） | どのプロトコル・エンジンとの互換が要件か |
| **最もコスト効率が高い** | 要件を満たす構成群の中の最安（スポット、ライフサイクル、Intelligent-Tiering、Savings Plans、サーバーレス、gp3、Graviton） | 稼働時間、転送量、既存契約、停止可能性、中断許容。**要件（可用性・RTO）を下回る案は不正解** |
| **高可用性** | マルチAZ、ASG（min 2以上）、ELB、リージョン内冗長 | 設問が要求する障害範囲（インスタンス／AZ／リージョン）。誤削除には効かない |
| **災害対策（DR）／リージョン障害** | クロスリージョン（S3 CRR、Auroraグローバル、DynamoDBグローバルテーブル、Route 53フェイルオーバー） | RTO と RPO の数値。切替は自動か手動か |
| **RTO/RPOがほぼゼロ** | マルチサイト アクティブ/アクティブ | 複製方式が同期に近いか。コストは最高 |
| **数分以内に復旧、コストは抑えたい** | ウォームスタンバイ／パイロットライト | RTO を満たす起動手順があるか。RPO は複製方式で別に確認 |
| **スケーラブル／トラフィックが予測できない** | Auto Scaling、サーバーレス、DynamoDBオンデマンド | スパイクの立ち上がり速度（EC2 起動が間に合うか） |
| **疎結合にしたい／依存を減らす** | SQS、SNS、EventBridge | 同報か分担か。順序・再処理の要否 |
| **リアルタイム／ストリーミング** | Kinesis Data Streams、Firehose、Flink | 複数コンシューマーが読み直すか（Streams）、配送だけか（Firehose） |
| **一桁ミリ秒** | DynamoDB | アクセスパターンがキー検索で固定か |
| **マイクロ秒** | ElastiCache、DAX | 鮮度と整合性（TTL の間は古い。DAX は結果整合性のみ） |
| **サブミリ秒・数百GB/s（HPC）** | FSx for Lustre | S3 連携の要否、Linux か |
| **監査／誰が何をしたか** | CloudTrail | 90日超の保持が要るなら証跡（S3）か Lake |
| **コンプライアンス／改変不可／保持期間** | オブジェクトロック（コンプライアンスモード）、Vault Lock、Artifact | ルートでも削除不可でよいか（コンプライアンスモード） |
| **個人情報が含まれていないか** | Macie（S3）、Comprehend（テキスト） | 対象が S3 か、アプリ内のテキストか |
| **インターネットを経由させたくない** | VPCエンドポイント／PrivateLink／Direct Connect | **接続元は VPC 内かオンプレか**。S3 でもオンプレからはインターフェース型 |
| **パブリックIPを持たせずに更新・接続したい** | NAT Gateway（アウトバウンド）、**Session Manager**（接続）、VPCエンドポイント | 向き（インスタンスから外へ出るのか、人が入るのか）。Session Manager は外向き通信の経路にならない |
| **固定IPが必要（ファイアウォール登録）** | NLB、Global Accelerator、Elastic IP | プロトコル（HTTP なら GA→ALB か NLB→ALB） |
| **キーをコードに書かない** | IAMロール、Secrets Manager、Parameter Store | ローテーションが要るか（Secrets Manager） |
| **キーを自社で完全管理したい** | CloudHSM、SSE-C、インポートしたキーマテリアル | 規制が「AWS に鍵を触らせない」まで要求するか |
| **一時的にファイルを共有したい** | S3 事前署名URL | 有効期限と、発行者の権限 |
| **特定のIPアドレスからの攻撃を遮断** | NACL（L3/L4・サブネット単位）、WAF の IP セット（HTTP）、CloudFront 地理的制限（国単位） | 層（L3/L4 か HTTP か）と単位（IP か国か）。SG は拒否を書けない |
| **SQLインジェクション／XSS／ボット** | WAF | 付ける先は ALB／CloudFront／API Gateway（NLB 不可） |
| **大規模DDoSと請求の急増** | Shield Advanced | 費用保護と 24 時間対応が要件か |
| **開発者に決められた構成だけ使わせたい** | Service Catalog（＋SCP、アクセス許可境界） | 「使えるサービスの制限」（SCP）か「承認済み構成の提供」（Catalog）か |
| **複数アカウントを統制したい** | Organizations＋SCP、Control Tower、Firewall Manager | 統制だけか、ランディングゾーン構築まで要るか |
| **手作業のパッチ適用をやめたい** | Systems Manager Patch Manager | 対象が EC2（利用者責任）か、マネージドサービス（AWS 責任）か |
| **踏み台サーバーをなくしたい** | Session Manager | SSH ポートを閉じられるか。IAM で操作権限を管理できるか |
| **設定が勝手に変えられていないか** | AWS Config（＋自動修復） | 「変更の検知」か「誰が変えたか」（CloudTrail）か |
| **メモリ使用率を監視したい** | CloudWatchエージェント（カスタムメトリクス） | 標準メトリクスにない（ハイパーバイザー視点）ことを理解しているか |
| **ログから特定の文字列を検知して通知** | CloudWatch Logs メトリクスフィルタ＋アラーム | 通知先（SNS）と閾値 |
| **オンプレのデータを一度に大量移行** | Snowball（回線が細い）／DataSync（オンライン） | 回線帯域と期限で、物理移送が速いか |
| **DBを止めずに移行** | DMS（＋SCT） | 異種エンジン間か（SCT が要る） |
| **既存のSFTPを維持** | Transfer Family | プロトコル（SFTP/FTPS/FTP）と認証方法 |
| **セッション情報の保存場所** | ElastiCache（Redis）／DynamoDB | 消えてよいか（Memcached 不可）、複数 AZ で共有するか |
| **静的コンテンツの配信** | S3＋CloudFront（OAC） | バケットを非公開にできているか |
| **画像アップロード後の非同期処理** | S3イベント → SQS/SNS → Lambda | 処理系が1つ（SQS）か複数（SNS ファンアウト）か |
| **急なスパイクでDBが落ちる** | 前段にSQS（バッファ）／ElastiCache／DynamoDB | キューで吸収できる一時的なスパイクか、持続的な流入超過か（後者は処理能力の増強） |
| **同じ処理が2回実行された** | SQSの可視性タイムアウト延長／ワーカーの冪等性 | 再配信は FIFO でも起こる。FIFO の重複排除は送信側の重複だけ |
| **メッセージが失われる** | DLQ、保持期間の延長 | DLQ は隔離。監視と再処理の手順まであるか |
| **アプリは正常なのにヘルスチェックを通過してしまう** | ASGのヘルスチェックタイプを**ELB**にする | EC2 ステータスチェックだけではアプリ障害を検知できない |
| **東京だけでなく世界中で速く** | CloudFront、Global Accelerator、レイテンシールーティング、マルチリージョン | キャッシュが効く内容か。プロトコル。データの所在規制 |

---

## 数字で覚えるもの（主要な数値と公式出典）

> この表は確認日時点の現行仕様です。**既定値・上限（調整可／固定）・設計上の目安**を区別しています。実際の設問では明示された条件を優先してください。「従来」と書いた値は、古い設問がその値を前提にしていることがあるため併記しています。章本文の数値はこの表を正とし、食い違いがあればここを直してから本文を直す。

| 項目 | 値・種類 | 条件 | 根拠・確認日 |
|---|---|---|---|
| Lambda 最大実行時間 | 900秒（15分）・**上限（固定）** | 通常の関数。Lambda Managed Instances の非同期／イベントソース呼び出しは最大90分（例外扱い、SAA の主題ではない） | [Lambda クォータ](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html)・2026-09-13 |
| Lambda メモリ | 128 MB〜10,240 MB・**上限（固定）** | 1 MB 刻み。**CPU はメモリに比例**（1,769 MB で 1 vCPU 相当） | 同上・2026-09-13 |
| Lambda 同時実行数 | 1,000・**既定（調整可）** | リージョン単位。**新規アカウントはこれより低い**ことがあり、利用に応じて自動で引き上げ | 同上・2026-09-13 |
| Lambda `/tmp` | 512 MB〜10,240 MB・上限（固定） | 1 MB 刻み | 同上・2026-09-13 |
| Lambda デプロイパッケージ | zip 50 MB（直接）／解凍後 250 MB／コンテナイメージ 10 GB・上限（固定） | レイヤー含む | 同上・2026-09-13 |
| SQS メッセージ保持 | 既定4日・**既定**／60秒〜14日・上限（固定） | 標準・FIFO 共通 | [SQS メッセージクォータ](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html)・2026-09-13 |
| SQS メッセージ最大サイズ | 1,048,576 bytes（1 MiB）・上限（固定） | 送信するメッセージ本体。拡張クライアントで S3 参照にすればペイロード最大 2 GB。**従来は 256 KB** | 同上・2026-09-13 |
| SQS 可視性タイムアウト | 既定30秒・**既定**／0秒〜12時間・上限（固定） | 処理時間より長く設定するか、処理中に延長する | 同上・2026-09-13 |
| SQS 配信遅延（遅延キュー） | 既定0秒／最大15分・上限（固定） | 可視性タイムアウトとは別の時計 | 同上・2026-09-13 |
| SQS ロングポーリング | 最大20秒・上限（固定） | `WaitTimeSeconds` を 0 より大きくすると有効。既定は 0（ショートポーリング） | [ショート／ロングポーリング](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html)・2026-09-13 |
| SQS FIFO スループット | 300 TPS・**既定モード**（APIアクションごと・パーティションごと）／バッチ10件で3,000メッセージ/秒 | **高スループットモード**では us-east-1 等で最大 70,000 TPS、その他リージョンは既定 2,400 TPS 等。**TPS（API 呼び出し）とメッセージ/秒を混同しない** | [SQS メッセージクォータ](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html)・2026-09-13 |
| SQS FIFO 重複排除の窓 | 5分・固定 | 送信側の重複排除。受信側の再配信は防がない | [FIFO 正確に1回の処理](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-exactly-once-processing.html)・未確認（本文の記述に基づく） |
| S3 オブジェクト最大サイズ | 48.8 TiB・上限（固定） | マルチパートアップロード（最大10,000パート×最大5 GiB）。**従来は 5 TB** | [S3 マルチパートの上限](https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html)・2026-09-13 |
| S3 マルチパート | パート 5 MiB〜5 GiB、最大10,000パート・上限（固定） | 最後のパートに下限なし。100 MB 超で推奨。単一 PUT は 5 GiB まで | 同上・2026-09-13 |
| S3 リクエスト性能 | プレフィックスあたり 3,500 PUT/COPY/POST/DELETE・5,500 GET/HEAD 毎秒・**目安（少なくとも）** | プレフィックスを増やせば並列に伸びる。スケール中は 503 が出ることがある | [S3 性能の最適化](https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html)・2026-09-13 |
| S3 最低保存期間（課金） | Standard-IA 30日／One Zone-IA 30日／Glacier Instant 90日／Glacier Flexible 90日／Deep Archive 180日・課金条件 | 早期削除は残り期間分が課金される。IA 系は最小課金サイズ 128 KB | [S3 ストレージクラス](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html)・2026-09-13 |
| S3 Glacier 取り出し時間 | Flexible：迅速 1〜5分／標準 3〜5時間／大容量 5〜12時間。Deep Archive：標準 12時間以内／大容量 48時間以内・**目安（typically）** | Batch Operations 経由の標準は Flexible で「分〜5時間」、Deep Archive で 9〜12時間。250 MB 超の迅速取り出しはスループット制限あり | [アーカイブ取り出しオプション](https://docs.aws.amazon.com/AmazonS3/latest/userguide/restoring-objects-retrieval-options.html)・2026-09-13 |
| DynamoDB 項目サイズ | 400 KB・上限（固定） | 属性名と値を含む | [DynamoDB データ型と命名規則](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.NamingRulesDataTypes.html)・2026-09-13 |
| DynamoDB 読み書き単位 | 1 RCU＝4 KB を強い整合性で1回/秒（結果整合性なら 0.5 RCU、トランザクションなら 2 RCU）／1 WCU＝1 KB を1回/秒（トランザクションなら 2 WCU）・定義 | サイズは 4 KB／1 KB 単位に切り上げ | [DynamoDB 読み書き操作](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/read-write-operations.html)・2026-09-13 |
| DynamoDB PITR | 1〜35日・設定範囲 | 既定は無効。有効化後は継続バックアップ | [DynamoDB PITR](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/PointInTimeRecovery_Howitworks.html)・2026-09-13 |
| RDS 自動バックアップ保持 | 0〜35日・設定範囲 | 0 で無効。リードレプリカの元になっている場合は 0 にできない。Aurora はクラスター側で管理 | [ModifyDBInstance API](https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_ModifyDBInstance.html)・2026-09-13 |
| Aurora ストレージ上限 | 128 TiB または 256 TiB・上限（固定、**バージョン依存**） | 256 TiB は Aurora PostgreSQL 17.5／16.9／15.13 以降、Aurora MySQL 3.10 以降。それ以外は 128 TiB。10 GB 単位で自動拡張 | [Aurora クォータ](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_Limits.html)・2026-09-13 |
| Aurora リードレプリカ | 最大15台・上限（固定） | プライマリあたり。Aurora では引き上げ不可 | 同上・2026-09-13 |
| Aurora ストレージのコピー数 | 3 AZ × 2 ＝ 6 コピー・仕様 | 書き込みは 6 中 4、読み取りは 3 で成立 | 未確認（本文の記述に基づく。実装時に公式で再確認） |
| Kinesis Data Streams シャード | 書き込み 1 MB/秒または 1,000 レコード/秒、読み取り 2 MB/秒・上限（固定、プロビジョンドモード） | オンデマンドモードはシャードを意識しない。1 レコードの最大は 10 MiB（バースト用途） | [Kinesis クォータ](https://docs.aws.amazon.com/streams/latest/dev/service-sizes-and-limits.html)・2026-09-13 |
| Kinesis Data Streams 保持期間 | 24時間〜365日（8,760時間）・設定範囲 | 既定 24 時間。延長は追加料金 | 同上・2026-09-13 |
| VPC サブネットの予約 IP | 各サブネット 5個（先頭4つ＋末尾1つ）・仕様 | /28〜/16。/28 で使えるのは 11 個 | [サブネット CIDR](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html)・2026-09-13 |
| ELB 登録解除の遅延 | 300秒・**既定** | ALB のターゲットグループ属性。進行中のリクエストがなければ即完了 | [ALB ターゲットグループ属性](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/edit-target-group-attributes.html)・2026-09-13 |
| KMS キー削除の待機期間 | 7〜30日・設定範囲／既定 30日 | 待機中は暗号操作不可。取り消し可 | [KMS キーの削除](https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html)・2026-09-13 |
| KMS 自動ローテーション周期 | 90〜2,560日・設定範囲／既定 365日 | カスタマー管理キー（AWS 生成の対称暗号化キー）のみ。AWS 管理キーは年1回固定 | [KMS 自動ローテーション](https://docs.aws.amazon.com/kms/latest/developerguide/rotating-keys-enable.html)・2026-09-13 |
| CloudTrail イベント履歴 | 90日・仕様 | 管理イベントのみ。長期保持は証跡（S3）か CloudTrail Lake | [CloudTrail イベント履歴](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html)・2026-09-13 |
| EC2 スポット中断の通知 | 2分前・仕様 | 休止（hibernate）の場合は 2 分の猶予なし。通知はベストエフォート | [スポット中断通知](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-instance-termination-notices.html)・2026-09-13 |
| Firehose バッファ間隔 | 0〜900秒／既定 300秒（S3 等）・設定範囲 | 0 秒は対応宛先のみ。動的パーティショニング・S3 バックアップ先では不可。60 秒未満は S3 の PUT 料金が増える | [Firehose バッファリングヒント](https://docs.aws.amazon.com/firehose/latest/dev/create-configure-backup.html)・2026-09-13 |
| ACM エクスポート可能証明書 | 有効期間 198日、失効 45日前に自動更新・仕様 | 追加料金あり。更新後の配置は利用者が管理 | [ACM エクスポート可能証明書](https://docs.aws.amazon.com/acm/latest/userguide/acm-exportable-certificates.html)・2026-09-13 |

**未確認の項目**：SQS FIFO 重複排除の窓（5分）と Aurora の 6 コピー構成は、この改訂で公式ページを開いて再確認していない。本文の従来記述に基づくため、実装時に再確認する。

---

## 試験当日の解き方（第0章 0.5 と同じ手順）

1. **絶対に満たす条件を拾う**：可用性／RTO・RPO／保持期間／規制／互換性／実行時間の上限。「最も○○」の前に、まず落とせない条件を確定する。
2. **その条件を満たせない選択肢を外し、理由を言う**：「可用性要件があるのに単一AZだから」「15分を超えるからLambdaは不可」「NLBにWAFは付かないから」「マルチAZ DBインスタンス配置のスタンバイは読めないから」。単語の有無だけで外さない。
3. **残りから設問の優先事項で選ぶ**：「最もコスト効率」なら要件を満たす中で最安、「最も運用負荷が低い」ならマネージド度が高い方、「最も高性能」なら原因に効く対策。

---

[目次に戻る](./README.md) ／ [横断比較表](./90-comparison.md)
