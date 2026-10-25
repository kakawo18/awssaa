# 第10章 その他のAWSサービス

> **章の一言**：API基盤・AI/ML・コスト管理・データ移行など、第1〜9章に入らないサービスをまとめます。AI/MLサービスは「入力データ種別（画像・音声・文書など）」、データ移行・転送サービスは「移行対象（DB・ファイル・サーバー）と回線帯域」の観点から整理・識別できるようにします。

---

## 10.1 Amazon API Gateway

**概要**：スケーラブルなAPIの作成・公開・保守・監視・保護を一元的に提供するフルマネージド型サービス。サーバーレスアーキテクチャにおける外部リクエストの受付窓口となります。

**試験対策のポイント**
- **バックエンド統合**：AWS Lambdaを外部公開するための標準的なエントリーポイントとなります。また、Lambdaを介さずにDynamoDBやS3などの**AWSサービスAPIを直接呼び出すサービス統合（Direct Integration）**も可能であり、レイテンシとコストの削減に寄与します。
- **認証・認可（オーソライザー）**：
  - **Cognitoユーザープール**：JWT（JSON Web Token）を検証し、エンドユーザーの認証を行います。
  - **Lambdaオーソライザー**：独自のベアラートークン検証やサードパーティ認証基盤との連携を行います。
  - **IAM権限**：AWS SigV4署名を用いて、IAMユーザー・ロール単位で呼び出し権限を制御します（内部システム向け）。
- **トラフィック制御と保護**：
  - **使用量プランとAPIキー**：クライアントやAPIキーごとの利用枠（クォータ）や呼び出し頻度（レート制限）を管理します。
  - **スロットリング**：急激なトラフィック急増時にリクエストを抑制（429 Too Many Requests）し、バックエンドサービスを過負荷から保護します。
  - **API Gatewayキャッシュ**：ステージごとにTTLキャッシュを有効化し、同一リクエストに対するバックエンド呼び出しを抑止して応答性能を高めます。
- **デプロイと運用**：
  - **ステージとカナリアリリース**：開発・検証・本番などの環境（ステージ）を分離し、トラフィックの一部のみを新バージョンへ段階的に割り振るカナリアデプロイに対応。
  - **プライベートAPI**：インターフェース型VPCエンドポイント経由でのみアクセスを許可し、インターネットに公開しない社内専用APIを構築します。
  - **CORS（Cross-Origin Resource Sharing）**：ブラウザのJavaScriptからクロスオリジンで呼び出す場合は、API Gateway側でCORSヘッダー（OPTIONSメソッド等）を適切に設定します。

**APIタイプの選定基準**
| APIタイプ | 特徴と主なユースケース |
|---|---|
| **REST API** | APIキー、使用量プラン、キャッシュ、リクエスト/レスポンス変換、WAF連携など、HTTP APIにない機能を必要とする場合。 |
| **HTTP API** | REST APIに比べ**低レイテンシかつ低コスト**（最大70%安価）。LambdaやHTTPバックエンドへのシンプルなプロキシに最適。 |
| **WebSocket API** | クライアントとサーバー間で**双方向の永続接続**を維持し、リアルタイムチャットや通知システムを構築する場合。 |
| **AWS AppSync** | GraphQLエンドポイントを提供し、複数データソースの集約、柔軟なクエリ、オフライン同期を必要とする場合（→10.2）。 |

---

## 10.2 フロントエンド・モバイル向けサービス

| サービス | 概要 | 主な選定ポイント・キーワード |
|---|---|---|
| **AWS Amplify** | フロントエンドのホスティングとバックエンド構築 | Gitリポジトリと連携した静的Webアプリ（SPA）のCI/CDデプロイ、認証やAPIの迅速なプロビジョニング。 |
| **AWS AppSync** | フルマネージドGraphQLサービス | **必要なフィールドのみを単一リクエストで取得**、リアルタイムデータ購読（Subscription）、**モバイル端末のオフラインデータ同期**。 |
| **Amazon Pinpoint** | 顧客エンゲージメント・メッセージ配信。※2025年5月20日に新規受付終了、**2026年10月30日にサポート終了**（SMS・プッシュ等の送信機能はAWS End User Messagingへ移管） | ユーザーの行動分析に基づき、メール、SMS、プッシュ通知などのマルチチャネルでパーソナライズされたキャンペーンを配信する。 |
| **Amazon SES (Simple Email Service)** | 高スケーラビリティなメール送受信基盤 | 注文確認やパスワードリセットなどの**大量のトランザクションメールを安価に送信**する（システム通知用のSNS Eメールとの違いに留意）。 |
| **AWS Device Farm** | クラウド上のモバイル・Web実機テスト | 多種多様な実際のスマートフォンやブラウザ環境で、アプリの動作検証やパフォーマンステストを並列実行する。 |

---

## 10.3〜10.8 機械学習・AIサービス（入力データ別の整理）

事前学習済みのマネージドAIサービスは、専門的な機械学習モデルの構築知識なしにAPI経由で即座に利用できます。

| 入力データ／要件 | サービス | 主な機能・特徴 |
|---|---|---|
| **画像・動画** | **Amazon Rekognition** | 顔認識・照合、物体・シーン検出、不適切コンテンツの検出、画像内テキスト抽出。 |
| **スキャン文書・PDF** | **Amazon Textract** | 単なるOCRを超え、領収書や申請書の**フォーム項目（キーと値のペア）やテーブル構造を保持**したままテキストを抽出。 |
| **音声 → テキスト** | **Amazon Transcribe** | 音声のテキスト化（文字起こし）、複数話者の識別（話者分離）、リアルタイム字幕生成。 |
| **テキスト → 音声** | **Amazon Polly** | 自然な音声読み上げ（TTS: Text-to-Speech）、多言語対応、SSML（音声合成マークアップ言語）による発音制御。 |
| **テキストの自然言語処理** | **Amazon Comprehend** | 感情分析、キーフレーズ抽出、言語識別、固有表現認識、**個人情報（PII: 個人を特定できる情報）の検出**。 |
| **医療テキストの処理** | **Amazon Comprehend Medical** | 処方箋やカルテから病名・投薬内容・検査数値を抽出し、HIPAAコンプライアンスを支援。 |
| **多言語翻訳** | **Amazon Translate** | ニューラル機械翻訳を用いた高精度なテキスト翻訳。 |
| **対話型インターフェース** | **Amazon Lex** | 音声およびテキストによる対話型チャットボットの構築（Amazon Alexaと同一のコア技術）。 |
| **パーソナライズ推奨** | **Amazon Personalize** | ユーザーの行動履歴に基づき、個別最適化された製品・コンテンツのレコメンデーションエンジンを提供。 |
| **時系列予測** | **Amazon Forecast** | 過去の時系列データ（売上・需要・アクセス数など）に基づき、高精度な将来予測を生成。※2024年7月29日に新規顧客の受付を終了（後継はSageMaker Canvasの時系列予測）。 |
| **オンライン不正検知** | **Amazon Fraud Detector** | 新規アカウント作成や決済時の不正アクティビティを機械学習でリアルタイム判定。※2025年11月7日に新規顧客の受付を終了。 |
| **社内文書の自然言語検索** | **Amazon Kendra** | 機械学習を活用した高機能エンタープライズ内検索エンジン（S3、SharePoint、Salesforce等の横断検索）。※2026年7月30日に新規顧客の受付を終了（後継はAmazon Bedrock Managed Knowledge Base）。試験では今も「社内文書の自然言語検索＝Kendra」で出る。 |
| **フルカスタムML基盤** | **Amazon SageMaker** | 独自モデルのデータ準備、ノートブック開発、分散学習、チューニング、本番推論エンドポイントの運用までを一元提供。 |
| **生成AI基盤モデルの利用** | **Amazon Bedrock** | 業界をリードする基盤モデル（Titan、Claude、Llama等）をAPI経由で安全に利用・カスタマイズするサーバーレス基盤。 |

**典型的なアーキテクチャパターン**：
- S3への画像アップロード → S3イベント通知 → AWS Lambda → **Amazon Rekognition**でラベル検出 → 結果をDynamoDBへ保存。
- コールセンターの通話録音（S3） → **Amazon Transcribe**で文字起こし → **Amazon Comprehend**で顧客感情を分析。

### 取り違えやすい機能の対応

選択肢では、あるサービスの機能名を別のサービスに付けた「偽機能」がよく出ます。変換の向き（音声→文字か、文字→音声か）で見分けます。

| やりたいこと | 使う機能 | 取り違えやすい誤り |
|---|---|---|
| 複数ページのPDFから、項目と値・表を取り出す | **Textractの非同期の分析**（StartDocumentAnalysis。完了をSNSで受け取り、GetDocumentAnalysisで結果を取得）。複数ページの文書はPDFかTIFFで、非同期で処理する | 同期の AnalyzeDocument で一度に処理する／RekognitionのDetectTextで項目と値を取る |
| 音声の文字起こしから個人情報を除く | **Transcribeの個人情報の秘匿**（文字起こしの中の個人情報を `[PII]` に置き換える） | 保存後にMacieで消す（Macieは見つけて知らせるだけ） |
| テキストの個人情報を、保存する前に見つける | **ComprehendのDetectPiiEntities**（個人情報の種類と文字の位置を返す。伏せ字にする処理は呼び出す側で行う） | Macie（S3のデータを調べるサービス） |
| 2枚の写真の顔が同じ人物か確かめる | **RekognitionのCompareFaces**（1対1で比べて類似度を返す。既定のしきい値は80%） | コレクションに全員を登録して検索する（1対多の検索） |
| 読み上げの発音を直す（テキスト→音声） | **Pollyのレキシコン**（単語と読み方の対応表。SynthesizeSpeechで名前を指定） | Transcribeのカスタム語彙 |
| 専門用語の文字起こしを直す（音声→テキスト） | **Transcribeのカスタム語彙** | Pollyのレキシコン |
| 翻訳で、ブランド名などを決めた表記にする | **Translateのカスタム用語**（原文の言葉と訳語の対応をCSVなどで登録） | 「Translateのカスタム語彙」（存在しない） |
| 会話で必要な情報を聞き取り、システムを調べて答える | **Lexのボット＋Lambda関数**（必要な情報がそろったらLambda関数で処理する） | Polly・Transcribeでボットを作る |

出典：[Textractの複数ページの文書](https://docs.aws.amazon.com/textract/latest/dg/async-analyzing-with-sqs.html)・[Transcribeの個人情報の秘匿](https://docs.aws.amazon.com/transcribe/latest/dg/pii-redaction.html)・[ComprehendのPIIのリアルタイム分析](https://docs.aws.amazon.com/comprehend/latest/dg/realtime-pii-api.html)・[RekognitionのCompareFaces](https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CompareFaces.html)・[Pollyのレキシコン](https://docs.aws.amazon.com/polly/latest/dg/managing-lexicons.html)・[Transcribeのカスタム語彙](https://docs.aws.amazon.com/transcribe/latest/dg/improving-accuracy.html)・[Translateのカスタム用語](https://docs.aws.amazon.com/translate/latest/dg/how-custom-terminology.html)・[LexのFulfillment](https://docs.aws.amazon.com/lexv2/latest/dg/intent-fulfillment.html)（確認 2026-10-25）

### SageMakerの推論の4つの方式

| 方式 | 向いている使い方 | 上限・特徴 |
|---|---|---|
| **リアルタイム推論** | 常に低い遅延で答える | 入力は最大25 MB、処理は60秒まで。待っている間もインスタンスの料金がかかる |
| **サーバーレス推論** | たまにしか使わない・量が読めない。起動の待ち（コールドスタート）を許容できる | 入力は最大4 MB、処理は60秒まで。処理した時間だけ課金 |
| **非同期推論** | 大きな入力・長い処理を1件ずつ受け付け、終わったら通知する | 入力は最大1 GB、処理は最大1時間。結果はS3、完了はSNSで通知。処理がないときはインスタンスを0台まで減らせる |
| **バッチ変換** | S3にあるデータ全体をまとめて推論する（毎晩のスコアリングなど） | エンドポイントを持たず、ジョブの間だけインスタンスが動く |

学習の費用は、**マネージドスポットトレーニング**で下げます。スポットのキャパシティで学習ジョブを実行し、中断されたら次のスポットのインスタンスで再開します。**チェックポイントをS3に保存**しておけば、最初からではなく途中から再開できます。割引のコミットには、EC2向けのSavings Plansではなく**SageMaker Savings Plans**が対象です。

出典：[SageMakerの推論の方式](https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model-options.html)・[マネージドスポットトレーニング](https://docs.aws.amazon.com/sagemaker/latest/dg/model-managed-spot-training.html)・[チェックポイント](https://docs.aws.amazon.com/sagemaker/latest/dg/model-checkpoints.html)・[Savings PlansのFAQ](https://aws.amazon.com/savingsplans/faqs/)（確認 2026-10-25）

### Amazon Bedrockの構成で問われること

- **閉域で呼ぶ**：bedrock-runtime の**インターフェース型VPCエンドポイント（PrivateLink）**を作り、**プライベートDNSを有効**にすると、コードを変えずにVPCの中から呼べます。無効にすると、コードでエンドポイントのURLを指定し直す必要があります。ゲートウェイ型はS3とDynamoDBだけです。
- **入出力の安全対策**：**ガードレール**で、拒否する話題（例：銀行のチャットで投資の助言を扱わない）、機密情報のフィルター（個人情報を遮断またはマスク）、有害な内容のフィルターなどを設定し、プロンプトと回答に適用します。
- **大量の処理を安く**：**バッチ推論**は、S3に置いた多数の依頼をまとめて非同期で処理し、結果をS3に書き出します。対応するモデルでは、オンデマンドより安い価格です。

出典：[BedrockのインターフェースVPCエンドポイント](https://docs.aws.amazon.com/bedrock/latest/userguide/vpc-interface-endpoints.html)・[Bedrockのガードレール](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)・[Bedrockのバッチ推論](https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html)・[Bedrockの料金](https://aws.amazon.com/bedrock/pricing/)（確認 2026-10-25）

**新規の受付を終了した機能**：Rekognitionのストリーミング動画の分析は、2026年4月30日に新規の利用者の受付を終了しました（ほかのRekognitionの機能は影響を受けません）。Comprehendのトピックのモデリング・イベントの検出も、提供の変更の対象としてAWSの「Services in Maintenance」に載っています。古い問題集で正解になっていても、今の構成の正解にはしません（[Rekognitionの提供の変更](https://docs.aws.amazon.com/rekognition/latest/dg/rekognition-availability-changes.html)・[Services in Maintenance](https://docs.aws.amazon.com/general/latest/gr/maintenance_services.html)、確認 2026-10-25）。

---

## 10.9〜10.11 コスト管理サービス

### 10.9 AWS Cost Explorer
- **用途**：過去最大13か月のコストと使用状況の可視化・グラフ分析、**今後最大12か月の予測**。
- **推奨機能**：適切な**リザーブドインスタンス（RI）およびSavings Plansの購入推奨事項**を提示します。
- **ユースケース**：「どのAWSサービスやコスト配分タグに費用が発生しているかを視覚的に分析したい」場合に選定します。

### 10.10 AWS Budgets
- **用途**：月次・四半期・年次の**予算（コスト額、使用量、RI/Savings Plansの利用率・カバレッジ）を設定し、計画的な管理を行います**。
- **アラートと自動アクション**：実績値または予測値がしきい値を超えた際に、SNS通知やEメールアラートを発行します。さらに**Budgets Actions**を利用すれば、IAMポリシーの制限適用や特定EC2/RDSインスタンスの自動停止といった是正アクションを実行できます。
- **Cost Explorerとの違い**：「使いすぎの事前予防と制限（しきい値管理）」にはAWS Budgets、「発生した費用の詳細な事後分析・傾向把握」にはCost Explorerを用います。

### 10.11 AWS Cost and Usage Reports (CUR)
- **用途**：AWSにおける**最も詳細で網羅的な請求・利用実績データ**（時間単位・リソース単位・タグ情報付き）をS3バケットに出力します。
- **ユースケース**：出力されたCSV/Parquetデータを**Amazon Athena、Amazon Redshift、またはAmazon QuickSight**に取り込み、企業固有の複雑なコスト配賦や大規模な課金分析を実施する場合に利用します。

---

## 10.12 AWS Database Migration Service (DMS)

**概要**：データベースを**最小限のダウンタイムで稼働継続させたまま**AWSへ移行するためのマネージド型移行サービス。

- **同種移行と異種移行**：
  - **同種移行**（例：オンプレミスOracle → AWS RDS for Oracle、MySQL → RDS for MySQL）。
  - **異種移行**（例：Oracle → Amazon Aurora PostgreSQL）。エンジンが異なる場合は、まず**AWS Schema Conversion Tool (SCT)**を用いてテーブル定義・ビュー・ストアドプロシージャのスキーマ変換を行ってから、DMSでデータ移行を実施します。
- **継続的データレプリケーション（CDC: Change Data Capture）**：既存のデータベーストランザクションログを読み取り、初期移行後の変更差分をリアルタイムに同期し続けることで、切り替えに伴うサービス停止時間を最小化します。

---

## 10.13 AWS DataSync

**概要**：オンプレミスとAWS間、またはAWSストレージサービス間における**大容量ファイルデータの転送を自動化・高速化**するオンラインデータ転送サービス。

- **対応ストレージ**：NFS、SMB、HDFS、オブジェクトストレージと、**Amazon S3、Amazon EFS、Amazon FSx**との間の相互転送に対応。
- **特徴**：専用の軽量エージェントを導入し、独自プロトコルによる並列転送、帯域制御、暗号化、データ整合性検証、スケジュール同期を自動実行します。
- **Storage Gatewayとの明確な違い**：
  - **AWS DataSync**：データ移行や定期的な大容量バックアップなど、「**データを移動・同期する**」ためのツール。
  - **AWS Storage Gateway**：オンプレミスの業務システムからAWSクラウドストレージを「**日常的なハイブリッドストレージとして継続利用する**」ための仮想アプライアンス。

---

## 10.14 AWS Transfer Family

**概要**：**SFTP、FTPS、FTP、AS2**プロトコルを用いたファイル転送エンドポイントを完全マネージド型で提供し、転送されたファイルを直接**Amazon S3またはAmazon EFS**に格納するサービス。

- **選定のポイント**：既存の外部パートナーや取引先が**既存のSFTPクライアントや運用手順を変更できない**要件において、自社でSFTPサーバーのEC2インスタンスを管理・冗長化することなくクラウドへ統合したい場合に選定します。

---

## 10.15 その他の移行サービス一覧

| サービス | 概要 | 主な選定ポイント・キーワード |
|---|---|---|
| **AWS Snowball Edge** | 高耐久性の物理ストレージデバイスによるオフライン移送 | 数十TB〜数PBの大容量データ。**ネットワーク帯域が不十分で転送に数週間以上を要する**環境。エッジコンピューティング（EC2/Lambda）にも対応。※2025年11月7日以降は既存顧客のみ（新規顧客はDataSync／AWS Data Transfer Terminal を案内）。 |
| **AWS Snowcone** | 超小型・軽量（約8TB〜14TB）のポータブルデバイス。**2024年11月12日に提供終了** | エッジ環境、工場、ドローン、車載など、過酷な物理環境でのデータ収集・移送（古い設問でのみ登場）。 |
| **AWS Snowmobile** | 超大規模データ移送用の専用コンテナトラック。**2024年3月14日に完全終了** | 最大100PB/台のエクサバイト級データセンター全体のクラウド移行（古い設問でのみ登場）。 |
| **AWS Application Migration Service (MGN)** | サーバーのリフト＆シフト（ブロックレベル複製） | オンプレミスや他クラウドの仮想マシン・物理サーバーを、OSやアプリを変更せず**最小のダウンタイムでEC2へ自動リフト**する。 |
| **AWS Application Discovery Service** | 移行前のオンプレミス環境の構成調査。※2025年11月7日に新規顧客の受付を終了（後継はAWS Transform） | 既存サーバーのスペック、稼働率、ネットワーク依存関係を自動収集し、移行計画の策定を支援する。 |
| **AWS Migration Hub** | 移行プロジェクトの進捗を一元管理。※2025年11月7日に新規顧客の受付を終了（後継はAWS Transform） | MGNやDMSなど複数の移行ツールのステータスを単一ダッシュボードで追跡する。 |

**データ転送・移行手段の整理**
| 要件・制約 | 推奨されるサービス |
|---|---|
| ネットワーク回線経由では転送完了までに数週間〜数か月以上を要する大容量データ（数十TB〜PB規模） | **AWS Snowball Edge**（※新規顧客は受付終了。試験では今もこの要件の答え） |
| ネットワーク回線を利用した、ファイルサーバー（NFS/SMB）からS3/EFS/FSxへの自動かつ高速な同期・移行 | **AWS DataSync** |
| データベースを本番稼働させたまま、最小のダウンタイムでAWSデータベースへ移行 | **AWS DMS（異種DBの場合はAWS SCTを併用）** |
| 取引先が利用する既存のSFTPプロトコルを維持したまま、ファイルをS3へ安全に格納 | **AWS Transfer Family** |
| オンプレミスの既存アプリから、標準ストレージプロトコル（ファイル/ブロック/テープ）でS3を継続利用 | **AWS Storage Gateway** |
| 世界各地の分散拠点からAmazon S3バケットへの**アップロード遅延を最適化** | **S3 Transfer Acceleration** |

> [!NOTE]
> **Snowファミリーの提供状況（2026年9月確認）**：Snowconeは2024年11月12日に提供終了、Snowball Edgeは2025年11月7日から既存顧客のみ（2026年12月31日にサポート終了予定）、Snowmobileは2024年3月14日に完全終了。AWSは新規の移行に**DataSync**（オンライン）や**AWS Data Transfer Terminal**（物理持ち込み）を案内しています。ただしSAA-C03の設問は「帯域が足りない大容量移送＝Snowball」の前提で出ることが多いため、判断の対応関係はそのまま覚えておきます。

> [!NOTE]
> **この章のその他の提供状況（2026年9月確認）**：Pinpoint（2026年10月30日サポート終了）、Fraud Detector・Migration Hub・Application Discovery Service（2025年11月7日新規受付終了）、Kendra（2026年7月30日新規受付終了）、Forecast（2024年7月29日新規受付終了）。いずれも既存顧客は利用を続けられ、試験では従来の役割のまま出題され得ます。最新の状況は [AWS Product Lifecycle](https://aws.amazon.com/products/lifecycle/) で確認できます（Maintenance＝新規受付終了、Sunset＝サポート終了日が決定、Full Shutdown＝完全終了）。

---

[目次に戻る](./README.md) ／ 次の章：[第11章 セキュアなアーキテクチャの設計](./11-secure.md)

