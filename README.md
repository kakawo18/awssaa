# awssaa

AWS Certified Solutions Architect – Associate (SAA-C03) の試験ポイントを、
**サービス間の違いを見分ける判断ポイント**中心にまとめた学習用リポジトリです。

外出先の隙間時間に1節ずつ読めるよう、各節を2〜3分の分量に揃えています。

👉 **[目次はこちら（docs/README.md）](./docs/README.md)**

## 構成
- `docs/00-foundations.md` … 第0章 設計の基礎と問題の読み方（最初に読む）
- `docs/01-compute.md` 〜 `docs/10-others.md` … 第1部 サービス別対策
- `docs/11-secure.md` 〜 `docs/14-cost.md` … 第2部 試験分野別対策（判断フロー中心）
- `docs/90-comparison.md` … 横断比較表（直前確認用）
- `docs/91-keywords.md` … 問題文キーワードの逆引き／暗記すべき数字
- `exams/set-NN.md` … 問題解説集（1セット8〜15問・全33セット425問。セット33は本番形式の65問の模擬試験）

## 問題解説集
`exams/` は、教材で覚えた判断を設問の形で試すためのディレクトリです。
1セット8〜15問・目安15〜25分（模擬試験は65問・130分）、解答は折りたたみなので、GitHub上でもスマホでも隠したまま解けます。
解説は「正解の理由」より**他の選択肢を外す理由**に重点を置き、根拠となる教材の章を必ず示します。

👉 **[問題集の索引（exams/README.md）](./exams/README.md)**

本試験の問題は再現せず、出題形式に沿ったオリジナル問題のみを収録します。
セットを追加したら、形式の検証を実行します。

```
python3 tools/check_exams.py        # 選択肢・正解記号・外す理由・参照リンクの検証
python3 tools/test_check_exams.py   # 検証ツール自体の回帰テスト
python3 tools/build_exams.py        # exams/*.md → web/exams.js（Web版の問題モード用）
python3 tools/rebalance_answers.py  # 正解記号の偏りを是正（選択肢の並べ替え）
```

Web版では選択肢をタップすると正誤と解説が表示され、解答状況は端末に保存されます
（`docs/` の参照リンクはその章へ遷移します）。

## Web版（スマホ用）
👉 **https://kakawo18.github.io/awssaa/** （Safariで開いて「ホーム画面に追加」するとアプリのように使えます）

`web/artifact.html` + `web/content.js` は、docs のMarkdownを1枚のWebページにまとめたものです。
章のナビゲーション、全章横断の検索（サービス名を入れると判断表の該当行だけを抽出）、
読了チェック、本文中の公式出典リンク（新しいタブで開く）が使えます。

### 元データと生成物の関係
- **原本は `docs/*.md`**。教材の内容はここだけを編集する。
- `web/content.js` は `tools/build_content.py` が docs から生成する**生成物**。手で編集しない（次の再生成で消える）。
- `web/exams.js` も同様に `tools/build_exams.py` が `exams/*.md` から生成する**生成物**。
- `web/artifact.html` は表示側。章の一覧・グループ分けは `content.js` の `group` から作るので、章を増減するときは `tools/build_content.py` の `FILES` を直す。

### 再生成手順
```
python3 tools/build_content.py        # docs/*.md → web/content.js
python3 tools/build_exams.py          # exams/*.md → web/exams.js
python3 tools/test_build_content.py   # リンク変換・エスケープの回帰テスト
python3 tools/test_check_exams.py     # 問題集の形式チェックの回帰テスト
python3 tools/build_site.py           # web/ → site/（GitHub Pages 用の単体ページ。確認用）
```

`main` にプッシュすると GitHub Actions（`.github/workflows/pages.yml`）が形式チェックとテストを実行し、通れば `site/` を組み立てて GitHub Pages に公開します。`site/` は生成物なのでコミットしません。
Markdown のリンクは、`https://` の外部リンクだけをクリック可能な形で保持し、
`./03-network.md` のような教材内リンクは章への遷移に変換します。それ以外のスキームは無効化してラベルだけ残します。

公開URL:
- GitHub Pages（ログイン不要）: https://kakawo18.github.io/awssaa/
- Claude Artifact（本人のみ）: https://claude.ai/code/artifact/72bf835a-9480-4034-826e-cd034496a035

解答状況・読了チェックはブラウザに保存されるため、開くURLごとに別々に記録されます。
