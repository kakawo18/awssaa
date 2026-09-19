# 問題セット12 ｜ 頻出⑥：セキュリティ運用・IaC・エッジ・AI

> 全10問・目安15分。各問の「解答と解説」を開くと正解が表示されます。
> 本試験の問題は含みません。出題形式に沿ったオリジナル問題です。
>
> **このセットのねらい**：証明書のリージョン制約、検出から自動対応までの流れ、スタック削除時の保護、
> エッジロケーションの使い分け、AIサービスの入力別の選択など、**知識として問われる論点**を集めています。

---

### Q1 ｜ 証明書 ｜ ★★

CloudFrontディストリビューションに独自ドメインのHTTPS証明書を設定しようとしたところ、**ACMで発行済みの証明書が選択肢に表示されません**。証明書は東京リージョン（ap-northeast-1）で発行しています。適切な対処はどれですか。

- **A.** AWS Private CAで証明書を再発行する
- **B.** CloudFrontのディストリビューションを東京リージョンで作り直す
- **C.** 証明書をALBに関連付けてから、CloudFrontのオリジンをALBに変更する
- **D.** 証明書をバージニア北部（us-east-1）で発行またはインポートし直す

<details>
<summary>解答と解説</summary>

**正解：D**

**決め手**：**CloudFrontで使うACM証明書は、バージニア北部（us-east-1）である必要があります**（CloudFrontがグローバルサービスのため）。ALB用は、そのALBと同じリージョンで発行します。

**他の選択肢を外す理由**
- **A**：Private CAは社内向けのプライベート証明書用で、一般の利用者が検証できる公開証明書にはなりません。
- **B**：CloudFrontはグローバルサービスで、リージョンを指定して作成するものではありません。
- **C**：ALBに証明書を付けても、CloudFrontのビューア向け証明書の要件（us-east-1）は変わりません。

**参照**：[第5章 5.7 AWS Certificate Manager](../docs/05-security.md) ／ [第3章 3.6 CloudFrontとGlobal Accelerator](../docs/03-network.md)

</details>

---

### Q2 ｜ DDoS対策 ｜ ★★★

大規模なキャンペーンを控え、DDoS攻撃への備えを強化します。要件は (1) 攻撃中に**AWSの専門チームの支援**を受けられる、(2) 攻撃に起因して急増したスケーリング費用の**補償**を受けられる、(3) L7の攻撃にも対応する、の3つです。適切な選択はどれですか。

- **A.** AWS Shield Advanced を契約する
- **B.** AWS Shield Standard を有効化する
- **C.** AWS WAFのレートベースルールのみを設定する
- **D.** Network Firewallを導入する

<details>
<summary>解答と解説</summary>

**正解：A**

**決め手**：**SRT（Shield Response Team）の支援と、DDoSに起因するスケーリング費用の補償はShield Advancedの機能**です。要件(1)(2)が出たら即決できます。

**他の選択肢を外す理由**
- **B**：StandardはすべてのAWS利用者に自動適用される基本的なL3/L4防御で、専門チームの支援や費用補償はありません。
- **C**：WAFは有効な対策ですが、単体では支援体制や費用補償は付きません。
- **D**：Network FirewallはVPCのトラフィック検査用で、大規模DDoSの緩和を担う製品ではありません。

**参照**：[第5章 5.6 AWS Shield](../docs/05-security.md) ／ [第11章 11.3 多層防御](../docs/11-secure.md)

</details>

---

### Q3 ｜ 検出から対応まで ｜ ★★★

GuardDutyが「EC2インスタンスが既知のマルウェア配布元と通信している」という検出結果を出したとき、**人手を介さずに自動で当該インスタンスを隔離**したいと考えています。適切な構成はどれですか。

- **A.** GuardDutyの検出結果をCloudTrailに記録し、定期的に確認する
- **B.** GuardDutyの検出結果をEventBridgeルールで受け、Lambdaで隔離用セキュリティグループへ付け替える
- **C.** AWS Configルールで、GuardDutyの検出結果を評価して修復する
- **D.** Security Hubで検出結果を集約し、担当者へメール通知する

<details>
<summary>解答と解説</summary>

**正解：B**

**決め手**：**検出（GuardDuty）→ 振り分け（EventBridge）→ 対応（Lambda／SSM Automation）**が自動対応の定型パターンです。

**他の選択肢を外す理由**
- **A**：CloudTrailはAPI操作の記録であり、検出結果の保存先でも自動対応の仕組みでもありません。
- **C**：Configが評価するのは**リソースの設定**で、GuardDutyの検出結果を入力とする仕組みではありません。
- **D**：集約と通知までで、**自動で隔離する**という要件を満たしません。

**参照**：[第5章 5.11 Amazon GuardDuty](../docs/05-security.md) ／ [第6章 6.3 Amazon EventBridge](../docs/06-integration.md)

</details>

---

### Q4 ｜ IaC ｜ ★★★

CloudFormationで構築した検証環境を削除する際、**RDSインスタンスのデータだけは残したい**（またはスナップショットとして保全したい）と考えています。適切な方法はどれですか。

- **A.** スタックを削除する前に、RDSに削除保護を設定する
- **B.** テンプレートのRDSリソースに `DeletionPolicy: Snapshot`（または `Retain`）を指定する
- **C.** スタックポリシーで、RDSリソースの更新を拒否する
- **D.** スタックを削除せず、手動でリソースを1つずつ削除する

<details>
<summary>解答と解説</summary>

**正解：B**

**決め手**：**DeletionPolicy はスタック削除時のリソースの扱いを指定**します。`Snapshot` はスナップショットを残して削除、`Retain` はリソースを残します。データ消失事故を防ぐ定番の設定です。

**他の選択肢を外す理由**
- **A**：削除保護が有効だとスタックの削除自体が失敗し、中途半端な状態になります（データ保全の仕組みではありません）。
- **C**：スタックポリシーは**更新時**の保護で、削除時の挙動は制御しません。
- **D**：手動削除はスタックとの整合性が崩れ、再現性も失われます。

**参照**：[第8章 8.3 AWS CloudFormation](../docs/08-management.md)

</details>

---

### Q5 ｜ 障害情報 ｜ ★★

あるリージョンで自社システムに断続的な障害が出ています。**AWS側のサービス障害やメンテナンスが、自分のアカウントのリソースに影響していないか**を確認したいと考えています。適切なサービスはどれですか。

- **A.** AWS Health Dashboard（アカウント固有のイベントを含む）
- **B.** Amazon CloudWatch の標準メトリクス
- **C.** AWS Trusted Advisor
- **D.** AWS CloudTrail

<details>
<summary>解答と解説</summary>

**正解：A**

**決め手**：**AWS側の障害・メンテナンス・自分のリソースへの影響を知らせるのがHealth Dashboard**です。EventBridgeと連携して自動通知もできます。

**他の選択肢を外す理由**
- **B**：CloudWatchは自分のリソースの状態を示すもので、AWS基盤側の障害情報は扱いません。
- **C**：Trusted Advisorはベストプラクティスの点検で、障害情報の通知はしません。
- **D**：CloudTrailは自分のアカウントでのAPI操作の記録です。

**参照**：[第8章 8.8 その他の管理、監視、ガバナンスサービス](../docs/08-management.md)

</details>

---

### Q6 ｜ AIサービス ｜ ★★

3つの要件に最も適したサービスの組み合わせはどれですか。

1. スキャンした**請求書PDFから、表とフォームの項目を構造化データとして**抽出したい
2. コールセンターの**通話音声を文字起こし**したい
3. 文字起こしした内容から**苦情かどうかの感情**を判定したい

- **A.** 1: Amazon Comprehend ／ 2: Amazon Transcribe ／ 3: Amazon Textract
- **B.** 1: Amazon Rekognition ／ 2: Amazon Polly ／ 3: Amazon Translate
- **C.** 1: Amazon Textract ／ 2: Amazon Transcribe ／ 3: Amazon Comprehend
- **D.** 1: Amazon Textract ／ 2: Amazon Polly ／ 3: Amazon Comprehend

<details>
<summary>解答と解説</summary>

**正解：C**

**決め手**：**入力の種類で一意に決まります**。文書＝Textract（単なるOCRではなく表・フォームの構造化）、音声→テキスト＝Transcribe、テキストの意味・感情＝Comprehend。

**他の選択肢を外す理由**
- **A**：ComprehendとTextractの役割が入れ替わっています。
- **B**：Rekognitionは画像・動画、Pollyは**テキスト→音声**（向きが逆）、Translateは翻訳です。
- **D**：Pollyは読み上げであり、音声の文字起こしはできません。

**参照**：[第10章 10.3〜10.8 機械学習・AIサービス](../docs/10-others.md)

</details>

---

### Q7 ｜ メール送信 ｜ ★★

ECサイトから、**注文確認メールを1日あたり10万通**送信します。HTMLメールのテンプレート管理と、バウンス率・苦情率の把握が必要です。適切なサービスはどれですか。

- **A.** Amazon SES
- **B.** Amazon SNSのEメールサブスクリプション
- **C.** Amazon Pinpoint のプッシュ通知
- **D.** Amazon WorkMail

<details>
<summary>解答と解説</summary>

**正解：A**

**決め手**：**大量のトランザクションメール送信はSES**です。テンプレート、配信統計（バウンス・苦情）、専用IPなどの機能を備えます。

**他の選択肢を外す理由**
- **B**：SNSのEメールは運用通知向けで、**購読者による購読確認が必要**なうえHTMLテンプレートも使えません。顧客向けの大量送信には適しません。
- **C**：Pinpointはキャンペーン配信やセグメント配信の基盤で、プッシュ通知は今回の要件と異なります（メール送信自体はSESの仕組みを使います）。
- **D**：WorkMailは社内向けのメールボックスサービスです。

**参照**：[第10章 10.2 フロントエンド・モバイル向けサービス](../docs/10-others.md)

</details>

---

### Q8 ｜ エッジロケーション ｜ ★★★

3つの要件に最も適したサービスの組み合わせはどれですか。

1. 法規制により、**データを自社データセンターの外に出せない**が、AWSのAPIで運用したい
2. 都市部の利用者へ、**一桁ミリ秒**のレイテンシで動画編集アプリを提供したい
3. **5G回線のモバイル端末**に対し、超低遅延で推論結果を返したい

- **A.** 1: AWS Outposts ／ 2: Amazon CloudFront ／ 3: AWS Local Zones
- **B.** 1: AWS Local Zones ／ 2: AWS Outposts ／ 3: Amazon CloudFront
- **C.** 1: AWS Outposts ／ 2: AWS Local Zones ／ 3: AWS Wavelength
- **D.** 1: AWS Snowball Edge ／ 2: AWS Wavelength ／ 3: AWS Local Zones

<details>
<summary>解答と解説</summary>

**正解：C**

**決め手**：**自社DC内＝Outposts／大都市圏の一桁ミリ秒＝Local Zones／5Gキャリア網＝Wavelength**。3つは設置場所で区別します。

**他の選択肢を外す理由**
- **A**：CloudFrontはコンテンツ配信のキャッシュで、アプリケーションの実行環境ではありません。
- **B**：1と2が逆です。Local Zonesは自社データセンターではなくAWSが運営する小規模拠点です。
- **D**：Snowball Edgeは一時的な現場処理やデータ移送用で、常設の低遅延基盤ではありません。

**参照**：[第1章 1.4 AWS Outposts](../docs/01-compute.md) ／ [付録A ネットワーク](../docs/90-comparison.md)

</details>

---

### Q9 ｜ サーバー移行 ｜ ★★

オンプレミスで稼働する**200台の仮想サーバー**をAWSへ移行します。要件は (1) アプリケーションを書き換えずそのまま移す、(2) 切り替え時のダウンタイムを**数分**に抑える、(3) 移行前に各サーバーの依存関係と使用状況を把握する、の3つです。適切な組み合わせはどれですか。

- **A.** 各サーバーのAMIを手動で作成し、順次起動する
- **B.** AWS DataSync で仮想ディスクをコピーし、EC2で起動する
- **C.** AWS Database Migration Service (DMS) で移行する
- **D.** AWS Application Discovery Service で調査し、AWS Application Migration Service (MGN) で移行する

<details>
<summary>解答と解説</summary>

**正解：D**

**決め手**：**リフト＆シフト＝MGN**（ブロックレベルの継続的複製でダウンタイムを最小化）、**移行前の資産調査＝Application Discovery Service**。移行の定型セットです。

**他の選択肢を外す理由**
- **A**：200台を手作業で扱うのは非現実的で、ダウンタイムも長くなります。
- **B**：DataSyncはファイル転送サービスで、稼働中サーバーの継続的複製やカットオーバーの仕組みはありません。
- **C**：DMSはデータベースの移行ツールで、サーバー全体の移行には使いません。

**参照**：[第10章 10.15 その他の移行サービス](../docs/10-others.md)

</details>

---

### Q10 ｜ コストの監視 ｜ ★★

先月、設定ミスにより特定サービスの利用料が通常の10倍に膨らみ、月末の請求で初めて気づきました。**早期に気づける仕組み**を用意します。**適切な対策を2つ選択してください。**

- **A.** AWS Cost and Usage Report をS3へ出力する設定を有効にする
- **B.** すべてのリソースにコスト配分タグを付与する
- **C.** AWS Cost Anomaly Detection を設定し、異常な支出パターンを検知したら通知する
- **D.** Cost Explorer で毎月末にレポートを確認する運用を定める
- **E.** AWS Budgets で予算と**予測超過**のしきい値を設定し、アラートを受け取る

<details>
<summary>解答と解説</summary>

**正解：C・E**

**決め手**：**気づく仕組み＝能動的に通知が飛ぶもの**です。Cost Anomaly Detectionは機械学習で異常を検知し、Budgetsはしきい値（実績・予測）超過で通知します。

**他の選択肢を外す理由**
- **A**：CURは詳細データの出力であり、それ自体は通知しません（分析の材料です）。
- **B**：タグは可視化・配賦の前提として有用ですが、単体では異常を知らせません。
- **D**：月末の確認では「請求で初めて気づく」という現状と大差ありません。

**参照**：[第14章 14.1 コスト管理ツールの使い分け](../docs/14-cost.md) ／ [第10章 10.9〜10.11 コスト管理サービス](../docs/10-others.md)

</details>

---

[問題集の索引に戻る](./README.md) ／ 前：[セット11 データベース細目](./set-11.md)
