# NEXUS パーソナルトレーナー採用LP

`recruit.nexus-gym.com` で公開する静的LP。ビルド不要。HTMLとCSSとごく少量のJSだけです。

```
index.html        本編（全12セクション）
styles.css        スタイル。色は既存サイトのCSS変数からの実測値
main.js           追従CTAバーの表示制御 / エリアタブ / CTAクリック計測
thanks/index.html 応募完了ページ（formrunの遷移先）
tools/gen_stores.py  店舗一覧セクションの生成スクリプト
_headers          Cloudflare Pages 用のヘッダー設定
assets/           画像置き場（現在は空）
```

---

## 公開前に必ず差し替えるもの

### 済んだもの

- ~~formrunの埋め込みタグ~~ 設置済み
- ~~LINEの友だち追加URL~~ 設置済み（`https://lin.ee/tHo9VZW`、3箇所）

### formrun側で1つだけ設定が必要です

フォーム編集画面 → **完了画面** → **「外部ページ」** → `https://recruit.nexus-gym.com/thanks/`

埋め込みタグに `data-formrun-redirect="true"` が付いているので、この設定を入れれば送信後に自社のサンクスページへ飛びます。**設定しないと、完了がformrunのドメイン上で起きてコンバージョンが取れません。**

`.pages.dev` で先にテストするなら、いったん `https://nexus-recruit-lp.pages.dev/thanks/` を入れておいて、独自ドメイン公開時に差し替えてください。

### 写真（暫定でUnsplashを使用中）

実写真が届くまでのつなぎとして、Unsplashのフリー素材を3枚使っています。**Unsplashのライセンスは商用利用可・帰属表示不要**ですが、出所は記録として残してあります。

| 位置 | 画像 | 撮影者 |
|---|---|---|
| ファーストビュー | ダンベルラック | thisGUYshoots（@block_08） |
| 写真バンドA（04と05のあいだ） | バーベルを持ち上げる背中 | Morrow Solutions（@morrowsolutions） |
| 写真バンドB（07と08のあいだ） | ケトルベルの寄り | ÇAĞIN KARGI（@caginkargi） |

`images.unsplash.com` のURLを直接参照しています。ファイルをリポジトリに持っていないので、差し替えは `src` を書き換えるだけです。

**選定の基準**：①人物の顔や場所が特定できないこと、②他社ロゴや英文サインが写り込んでいないこと、③大型のオープンフロアが写っていないこと。③は、NEXUSが**完全個室**のパーソナルジムなので、広いジムのフロアが写ると実態と食い違うためです。この基準で候補10枚のうち7枚を落としました。

すべて `.scrim` クラスで暗幕をかけています。ブランドのダークグリーンに色調を寄せる処理と、人物を「風景の一部」として見せる処理を兼ねています。

### 実写真への差し替え方

1. `/assets/` にWebPで置く（横960px程度で十分）
2. `index.html` の該当 `<img src>` を `/assets/hero.webp` などに変更
3. **`.scrim` に `is-light` を追加**して暗幕を薄くする — 自社の写真なら暗くする理由がないので

```html
<div class="hero-photo scrim is-light">
  <img src="/assets/hero.webp" alt="" width="960" height="500" fetchpriority="high">
</div>
```

### OGP画像

`/assets/ogp.png`（1200×630）を作成済み。ブランドカラーと実数値だけで組んであるので、写真の差し替えとは独立しています。

---

## ローカルで確認する

```bash
python3 -m http.server 8000
# → http://localhost:8000/
```

ブラウザの開発者ツールでiPhone表示にして確認してください。**スマホ実機でも1回は見てください。** 追従CTAバーとホームインジケータの重なりは実機でしか分かりません。

---

## 店舗リストを更新する

店舗が増減したら、`tools/gen_stores.py` の `AREAS` を編集して実行します。

```bash
python3 tools/gen_stores.py
```

`index.html` の `<!--STORES:START-->` 〜 `<!--STORES:END-->` の間が置き換わります。**タブの件数（東京42など）も自動で計算される**ので、数字を手で直す必要はありません。

なお本文中の「全国70店舗以上」という表記は、出店のたびに直さずに済むよう幅を持たせています。こちらは手動です（`index.html` に3箇所）。

---

## デプロイ（Cloudflare Pages / GitHub連携）

### 初回だけ

1. このディレクトリをGitリポジトリにしてGitHubへpush
2. Cloudflareダッシュボード → **Workers & Pages** → Create → **Pages** → **Connect to Git**
3. リポジトリを選択
4. ビルド設定
   - フレームワークプリセット：**None**
   - ビルドコマンド：**空欄**
   - ビルド出力ディレクトリ：**`/`**
5. Save and Deploy

### カスタムドメイン

**Cloudflare側が先です。逆にすると522エラーになります。**

1. プロジェクト → **Custom domains** → Set up a domain → `recruit.nexus-gym.com`
2. 表示される `【プロジェクト名】.pages.dev` を控える
3. クライアントにCNAME追加を依頼（`DNS設定のご依頼_NEXUS採用サイト.docx` の「値」欄に②の文字列を記入して送付）

### 2回目以降

`git push` するだけで自動デプロイされます。ブランチにpushすればプレビューURLが別に発行されます。

---

## 計測

GTMコンテナ `GTM-TMS968DN` を全ページに設置済みです。GTM側で以下を設定してください。

| dataLayerイベント | 発火場所 | 用途 |
|---|---|---|
| `trainer_application_complete` | `/thanks/` 読み込み時 | **コンバージョン。** Meta Pixel の Lead をここで発火させる |
| `cta_click` | 各CTAのクリック時 | どのボタンが押されているかの分析用。`cta_id` で判別 |

`cta_id` の値：`hero-line` / `hero-form` / `salary` / `members` / `benefits` / `bar-line` / `bar-form` / `line-main`

Conversions API の設定も忘れずに。`nexus-gym.com` のドメイン認証は済んでいるので、そのまま進められます。

---

## 実装上の判断メモ

- **フォントは3ファミリーのみ**（Noto Serif JP / Noto Sans JP / Archivo）。既存の採用ページは6ファミリー読み込んでいてCSSだけで297KBありました。表示速度が直帰に直結するため絞っています。**追加しないでください。**
- **明朝は見出しだけ。** 数字と要点はゴシック＋Archivo。給与額を明朝で組むと瞬間的に読めません。
- **クリーム面のグリーン文字は `--accent-deep`（#127D24）**。`--accent`（#3DBB2A）はクリーム上でコントラストが足りません。
- **グローバルナビは意図的に置いていません。** 広告流入を応募以外に逃がさないためです。フッターも法定表記のみ。
- **FAQは `<details>` 要素**で組んであるので、JSが落ちても開閉します。
- **エリアタブはJSが必要ですが**、落ちた場合は全エリアが表示されるだけで情報は失われません。
- 全長は約11,500px（390px幅）。旧LPは同条件で20,000px超あったので、ほぼ半分になっています。

---

## 公開後のチェックリスト

- [ ] `https://recruit.nexus-gym.com/` が開き、鍵マークが付く
- [ ] スマホ実機（iOS / Android）で表示崩れがない
- [ ] 追従CTAバーがホームインジケータに被っていない
- [ ] フォームから1件送信し、**formrunの管理画面に届く**
- [ ] 送信後 `/thanks/` に遷移する
- [ ] `/thanks/` でMeta側がイベントを受信している（テストイベントで確認）
- [ ] フッターの3リンクが開く
- [ ] LINEボタンが正しいアカウントに飛ぶ
