# awssaa

AWS Certified Solutions Architect – Associate (SAA-C03) の試験ポイントを、
**サービス間の違いを見分ける判断ポイント**中心にまとめた学習用リポジトリです。

外出先の隙間時間に1節ずつ読めるよう、各節を2〜3分の分量に揃えています。

👉 **[目次はこちら（docs/README.md）](./docs/README.md)**

## 構成
- `docs/01-compute.md` 〜 `docs/10-others.md` … 第1部 サービス別対策
- `docs/11-secure.md` 〜 `docs/14-cost.md` … 第2部 試験分野別対策（判断フロー中心）
- `docs/90-comparison.md` … 横断比較表（直前確認用）
- `docs/91-keywords.md` … 問題文キーワードの逆引き／暗記すべき数字

## Web版（スマホ用）
`web/artifact.html` + `web/content.js` は、docs のMarkdownを1枚のWebページにまとめたものです。
章のナビゲーション、全章横断の検索（サービス名を入れると判断表の該当行だけを抽出）、
読了チェックが使えます。Markdownを更新したら `python3 tools/build_content.py` で `web/content.js` を再生成します。

公開URL: https://claude.ai/code/artifact/72bf835a-9480-4034-826e-cd034496a035
