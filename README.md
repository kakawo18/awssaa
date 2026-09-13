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

## Web版（スマホ用）
`web/artifact.html` + `web/content.js` は、docs のMarkdownを1枚のWebページにまとめたものです。
章のナビゲーション、全章横断の検索（サービス名を入れると判断表の該当行だけを抽出）、
読了チェック、本文中の公式出典リンク（新しいタブで開く）が使えます。

### 元データと生成物の関係
- **原本は `docs/*.md`**。教材の内容はここだけを編集する。
- `web/content.js` は `tools/build_content.py` が docs から生成する**生成物**。手で編集しない（次の再生成で消える）。
- `web/artifact.html` は表示側。章の一覧・グループ分けは `content.js` の `group` から作るので、章を増減するときは `tools/build_content.py` の `FILES` を直す。

### 再生成手順
```
python3 tools/build_content.py        # docs/*.md → web/content.js
python3 tools/test_build_content.py   # リンク変換・エスケープの回帰テスト
```
Markdown のリンクは、`https://` の外部リンクだけをクリック可能な形で保持し、
`./03-network.md` のような教材内リンクは章への遷移に変換します。それ以外のスキームは無効化してラベルだけ残します。

公開URL: https://claude.ai/code/artifact/72bf835a-9480-4034-826e-cd034496a035
