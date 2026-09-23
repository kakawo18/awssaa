# 問題解説集

教材（[docs/](../docs/README.md)）で覚えた判断を、設問の形で試すためのディレクトリです。
教材が「表を引く」ためのものなのに対し、こちらは**判断を試す**ためのものです。

## 使い方

1. 1セット8〜15問・目安15〜25分。設問を読んで**自分の答えを決めてから**「解答と解説」を開きます。
2. 間違えた問題は、解説末尾の**参照**から教材の該当節に戻ります。
3. 2周目は正解の選択肢ではなく、**外した3つの理由を言えるか**で確認します。

> 解説は「正解の理由」より**他の選択肢を外す理由**に字数を割いています。
> 本番で迷うのは選択肢を絞りきれないときなので、そこが得点に直結します。

## セット一覧

| セット | 分野 | 問題数 | 主なテーマ |
|---|---|---|---|
| [セット01](./set-01.md) | 第1分野 セキュア（30%） | 10 | IAMロール／クロスアカウント／SCP／暗号化／検出系／WAF／Session Manager／責任共有 |
| [セット02](./set-02.md) | 第2分野 弾力性（26%） | 10 | ASGヘルスチェック／SQSバッファ／可視性タイムアウト／ファンアウト／DR戦略／リードレプリカ／NAT冗長／Global Accelerator |
| [セット03](./set-03.md) | 第3分野 高パフォーマンス（24%） | 10 | DAX／RDS Proxy／S3プレフィックス／FSx for Lustre／CPUクレジット／CloudFront／Athena最適化／ホットパーティション／OpenSearch／EFA |
| [セット04](./set-04.md) | 第4分野 コスト最適化（20%） | 10 | ライフサイクル／スポット／VPCエンドポイント／Aurora Serverless／Budgets vs Cost Explorer／Intelligent-Tiering／CloudFront配信コスト／購入方法の組み合わせ／TTL |
| [セット05](./set-05.md) | 総合（本番比率の混合） | 10 | Control Tower／DX暗号化／CloudHSM／API Gateway使用量プラン／Fargate移行／マルチAZ化／Firehose／Glue＋Athena／GWLB／gp2→gp3 |
| [セット06](./set-06.md) | **複合（分野をまたぐ）** | 10 | セキュリティ×コスト／可用性×コスト／性能×コスト／セキュリティ×弾力性／セキュリティ×性能／弾力性×性能／コスト×運用／3分野複合／全分野 |
| [セット07](./set-07.md) | **頻出① ネットワークと名前解決** | 10 | SG vs NACL／IP遮断／Route 53各ポリシー／エイリアス／ピアリング vs TGW／フローログ／接続ドレイニング／Lambda@Edge vs CloudFront Functions／Resolver／Egress-Only IGW |
| [セット08](./set-08.md) | **頻出② ストレージ選択と移行** | 10 | EFS／FSx for Windows／Tape Gateway／Snowball vs DataSync／DMS+SCT／Transfer Family／S3レプリケーション／インスタンスストア／マルチパート |
| [セット09](./set-09.md) | **頻出③ ID・運用・連携** | 10 | Cognito vs Identity Center vs AD Connector／明示的なDeny／Secrets Manager vs Parameter Store／CloudWatchエージェント／Config＋修復／EventBridge／Step Functions／ECSの2つのロール／Lambda同時実行／Patch Manager |
| [セット10](./set-10.md) | **頻出④ コンピューティング細目** | 10 | 予測スケーリング／ライフサイクルフック／Beanstalk Immutable／Image Builder／Hibernate／SnapStart／HTTP API／Amazon MQ／SNSフィルタリング／ウォームプール |
| [セット11](./set-11.md) | **頻出⑤ データベース細目** | 10 | Auroraバックトラック／高速クローン／RDS Blue-Green／Performance Insights／RCU計算／MemoryDB／Redshift Spectrum／同時実行スケーリング／特化型DB／RDS Proxyとフェイルオーバー |
| [セット12](./set-12.md) | **頻出⑥ 運用・エッジ・AI** | 10 | ACMのus-east-1／Shield Advanced／GuardDuty自動対応／DeletionPolicy／Health Dashboard／AIサービス選択／SES／Outposts系／MGN／Cost Anomaly Detection |
| [セット13](./set-13.md) | **2周目① 第1分野（30%）** | 12 | 信頼ポリシー vs 権限ポリシー／`aws:SourceVpce`／アクセス許可境界／Access Analyzer／KMSクロスアカウント／MFA削除 vs オブジェクトロック／Cognito IDプール／Network Firewall／Firewall Manager／RDS IAM認証／Inspector vs Config |
| [セット14](./set-14.md) | **2周目② 第2分野（26%）** | 10 | メッセージグループID／EventBridgeリプレイ／Express vs 標準ワークフロー／スロースタート／アラーム参照ヘルスチェック／マルチAZ DBクラスター／S3 RTC／デプロイサーキットブレーカー／拡張ファンアウト／自動復旧 |
| [セット15](./set-15.md) | **2周目③ 第3分野（24%）** | 10 | EBS帯域の上限／EFSスループットモード／キャッシュキー／クラスターモード／Auroraカスタムエンドポイント／Scan→Query＋GSI／クライアントアフィニティ／ジャンボフレーム／パーティション射影 |
| [セット16](./set-16.md) | **2周目④ 第4分野（20%）** | 8 | Compute Savings Plans／Convertible RI／EBSスナップショットアーカイブ／Intelligent-Tieringのアーカイブ階層／割引共有／価格クラス／Fargate Spot／AZ間転送 |
| [セット17](./set-17.md) | **複合2周目（分野をまたぐ）** | 10 | 署名付きURL＋Transfer Acceleration／Batch＋スポット／RDS Proxy＋Secrets Manager／DynamoDBグローバルテーブル／SCP＋コスト配分タグ／混合インスタンスポリシー／暗号化SQS＋DLQ／DX＋VPNバックアップ／Firehoseの形式変換／ステートレス化 |
| [セット18](./set-18.md) | **実戦演習①（本番比率）** | 15 | OACとSSE-KMS／MFA条件付きの引き受け／WAFレートベース／組織トレイル／猶予期間／EFS＋ASG(1/1)／SQSの最大同時実行数／Route 53で案内ページ／ホットシャード／Flink／Inferentia／ライフサイクル／Serverless v2の自動一時停止／Compute Savings Plans |
| [セット19](./set-19.md) | **実戦演習②（本番比率）** | 15 | プライベートAPI／シークレットの複製／ECSの`secrets`／Access Analyzerのポリシー生成／DNS Firewall＋Firewall Manager／クロスアカウントのイベントバス／Retry・Catch／Elastic Disaster Recovery／PITR＋削除保護／Redisのレプリカ／MSK／Glue ETL／Lambdaのarm64／I/O-Optimized／Budgets＋Anomaly Detection |
| [セット20](./set-20.md) | **実戦演習③（本番比率）** | 15 | SecureTransport／IMDSv2／`rds.force_ssl`／リージョン制限のSCP／Macie＋Security Hub／FIFOのグループIDと高スループット／オリジングループ／SQSで非同期化／AZ障害時の台数（静的安定性）／GSIの書き込み容量／zero-ETL／OpenSearchで全文検索／FargateとCompute SP／開発DBのシングルAZ／CloudFrontの圧縮 |
| [セット21](./set-21.md) | **実戦演習④（本番比率）** | 15 | オブジェクト所有権／エンドポイントポリシーと`aws:ResourceOrgID`／`iam:PassRole`／Cognitoの脅威保護／オブジェクトロック＋別アカウント複製／EventBridge Scheduler／大きなメッセージとS3／グローバルDBのスイッチオーバー／レイテンシー＋ヘルスチェック／Lambda＋EFS／PrivateLink／クローラー＋Athena／大容量取り出し／Redshift Serverless／ログの保持期間とIAクラス |

次に作るのは **セット22（実戦演習⑤）** です。

### セットの5つの系統

| 系統 | セット | ねらい |
|---|---|---|
| 分野別 | 01〜04 | 公式ガイドのタスクに沿って、分野ごとの基本を一通り |
| 形式別 | 05（総合）・06／17（複合） | 分野を見極める／複数要件を同時に満たす |
| **頻出テーマ別** | **07〜12** | **出題頻度が高いのに取り違えやすい対比**を集中的に。網羅よりも「落とせない論点」を優先 |
| **分野別2周目** | **13〜16** | 01〜04と同じ分野を**別角度から**。出題数は本番の配点比（12／10／10／8問）に合わせ、1周目で触れなかった細目を補強 |
| **実戦演習** | **18〜21** | 本番の配点比（5／4／3／3問）で分野を伏せて混ぜた15問セット。**数をこなして判断を速くする**ための演習。新しい論点と頻出論点の出し直しを混ぜている |

頻出セット（07〜09）は、既存問題の機械的なカバレッジ調査で**未出題だった21テーマ**（SG/NACLの戻り通信、Route 53のエイリアス、
Storage Gateway、DataSync、Snowball、DMS、Transfer Family、FSx for Windows、S3レプリケーション、IAM Identity Center、
Directory Service、Parameter Store、CloudWatchエージェント、ECSの2つのロール、Lambda@Edge、接続ドレイニング、
インスタンスストア、VPCピアリング/TGW、VPCフローログ、明示的なDeny ほか）を軸に構成しています。

### セット05・06・17の違い

- **セット05（総合）**：1問ごとは単一分野の設問だが、分野を伏せて出題する。**どの分野の問題かを見極める**練習。
- **セット06（複合）**：**1問の中に複数分野の要件が同時に登場**する。1つでも満たさない選択肢は不正解になるため、
  解説の冒頭に「**要件の分解**」を置き、要件を箇条に割ってから選択肢を外す手順を示している。本番で最も差がつく形式。
- **セット17（複合2周目）**：同じ形式で、頻出サービスの「**単体では正解だが、もう1つの要件で落ちる**」組み合わせを集めた。

## 記録

解いた結果を残しておくと、弱い分野が分かります。

| セット | 実施日 | 正答数 | 間違えた問題と理由 |
|---|---|---|---|
| set-01 |  | /10 |  |
| set-02 |  | /10 |  |
| set-03 |  | /10 |  |
| set-04 |  | /10 |  |
| set-05 |  | /10 |  |
| set-06 |  | /10 |  |
| set-07 |  | /10 |  |
| set-08 |  | /10 |  |
| set-09 |  | /10 |  |
| set-10 |  | /10 |  |
| set-11 |  | /10 |  |
| set-12 |  | /10 |  |
| set-13 |  | /12 |  |
| set-14 |  | /10 |  |
| set-15 |  | /10 |  |
| set-16 |  | /8 |  |
| set-17 |  | /10 |  |
| set-18 |  | /15 |  |
| set-19 |  | /15 |  |
| set-20 |  | /15 |  |
| set-21 |  | /15 |  |

## 出題の方針（公式試験ガイドに準拠）

出題範囲と形式は、AWSが公開している SAA-C03 試験ガイドに合わせています。

**試験の形式**
- 65問（採点対象50問＋採点対象外15問）。スコアは100〜1000のスケールドスコアで、**合格は720**。
- 設問形式は2種類。**単一選択**（4つの選択肢から1つ）と、**複数選択**（5つ以上の選択肢から2つ以上）。
- **未回答は不正解**として扱われ、当て推量による減点はありません。

**分野と配点**
| 分野 | 配点 | 主なタスク |
|---|---|---|
| 第1分野 セキュアなアーキテクチャ | 30% | 1.1 リソースへの安全なアクセス／1.2 安全なワークロードとアプリケーション／1.3 適切なデータセキュリティ管理 |
| 第2分野 弾力性に優れたアーキテクチャ | 26% | 2.1 スケーラブルで疎結合な設計／2.2 高可用性・耐障害性のある設計 |
| 第3分野 高パフォーマンスなアーキテクチャ | 24% | 3.1 ストレージ／3.2 コンピューティング／3.3 データベース／3.4 ネットワーク／3.5 **データの取り込みと変換** |
| 第4分野 コストを最適化したアーキテクチャ | 20% | 4.1 ストレージ／4.2 コンピューティング／4.3 データベース／4.4 ネットワーク |

**この問題集での扱い**
- **本試験の問題は再現しません。** 出題形式に沿ったオリジナル問題のみを収録します（市販問題集の複製も行いません）。
- 解説は必ず `docs/` の記述を根拠にし、**参照する章・節を明記**します。誤りが見つかったときに教材側とあわせて直せるようにするためです。
- 単一選択は選択肢4つ・正解1つ。複数選択は選択肢5つ以上・正解2つ以上とし、設問文に「**2つ選択してください**」と明示します。
- 複合問題（セット06・17）では、解説に「**要件の分解**」を必ず入れ、どの要件がどの分野に対応するかを明示します。
- 誤答も「ありそうな構成」にして、消去法の練習になるようにします。
- 難易度は★（知識の確認）／★★（本番相当）／★★★（要件の読み取りが必要）の3段階。
- **正解記号は A〜D に均等に散らす**（現在 A 30%／B 26%／C 23%／D 21%）。記号を見ただけで当てられる問題集にしないため、
  `tools/check_exams.py` が分布を毎回表示し、1文字が40%を超えると指摘します。偏った場合は
  `python3 tools/rebalance_answers.py` で選択肢の並びを入れ替えて是正できます（設問文と解説はそのまま）。

**出典**：[SAA-C03 試験ガイド（AWS公式）](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-associate-03/solutions-architect-associate-03.html)

## 形式チェック

ファイルを追加したら、構造の検証を実行します（選択肢の抜け、正解記号、外す理由の過不足、参照リンク切れを検出）。

```
python3 tools/check_exams.py
python3 tools/test_check_exams.py
```

---

[教材の目次へ](../docs/README.md)
