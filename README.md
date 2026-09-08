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

**ここが埋まらないまま公開すると、応募が1件も取れません。** 上から順に潰してください。

### 1. formrunの埋め込みタグ（最重要）

`index.html` の `<div class="form-slot">` の中身を、formrunの埋め込みタグに差し替えます。

**あわせてformrun側の設定が必須です。**
フォーム編集画面 → 完了画面 → **「外部ページ」** を選択 → `https://recruit.nexus-gym.com/thanks/` を入力。

これをやらないと、送信完了がformrunのドメイン上で起きてしまい、**コンバージョンが計測できません**（formrunの広告タグ機能はiframe埋め込みでは動きません）。

### 2. LINE公式アカウントの友だち追加URL

`href="#"` になっている箇所が3つあります。すべて実URLに差し替えてください。

```
index.html      … .line-block 内のボタン
thanks/index.html … 「LINEで質問する」
```

（ヒーローと追従バーの「LINEで応募」は `#line` へのページ内リンクなので差し替え不要です）

### 3. ファーストビューの写真

`.hero-photo` の中がプレースホルダになっています。写真ができたら差し替えてください。

```html
<div class="hero-photo">
  <img src="/assets/hero.webp" alt="" width="780" height="416" fetchpriority="high">
</div>
```

WebPに変換してから入れること。横780px程度あれば足ります。

### 4. OGP画像

`/assets/ogp.png`（1200×630）を用意して置いてください。未設置だとSNSやLINEで共有された際に画像が出ません。

### 5. 「1日の流れ」セクション

現在は一般的な内容で埋めてあります。実在の1名分のスケジュールに差し替えると説得力が上がります。

### 6. InstagramのURL

フッターのリンク先が既存サイトからの推定値です。正しいアカウントか確認してください。

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
