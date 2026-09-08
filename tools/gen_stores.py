#!/usr/bin/env python3
"""店舗一覧セクションのHTMLを生成して index.html の <!--STORES--> を置換する。
店舗が増減したらこのファイルの AREAS を直して再実行すること。
出典: nexus-gym.com の店舗一覧（2026-09-07 時点で実測 72 店舗）
"""
import pathlib, html

AREAS = [
    ("tokyo", "東京", [
        "乃木坂・赤坂店", "三田店", "渋谷・神泉店", "笹塚店", "白金台・高輪台店",
        "西馬込店", "西馬込ANNEX店", "馬込店", "蒲田・蓮沼店", "久が原店",
        "北千束店", "長原店", "石川台店", "武蔵新田店", "大森北口山王店",
        "池上店", "千鳥町店", "雪が谷大塚店", "雑色店", "清澄白河店",
        "東日本橋店", "月島店", "新中野店", "中野店", "沼袋店",
        "中野富士見町店", "中野新橋店", "菊川店", "上野店", "西荻窪店",
        "太子堂店", "池ノ上店", "明大前店", "奥沢店", "白山店",
        "千駄木店", "本駒込店", "西葛西店", "練馬店", "新江古田店",
        "上板橋店", "梅島・西新井店",
    ]),
    ("kanagawa", "神奈川", [
        "横浜店", "岸根公園店", "綱島店", "市ヶ尾店", "弘明寺店",
        "高田駅前店", "十日市場店", "大口店", "三ツ境店", "大船店",
        "仲町台店", "白楽店", "日吉店", "希望ヶ丘店", "三ツ沢上町店",
        "鹿島田・新川崎店", "登戸店",
    ]),
    ("kanto", "関東その他", [
        "大宮店（埼玉）", "太田店（群馬）", "足利店（栃木）",
    ]),
    ("kansai", "関西", [
        "福島店", "豊中店", "曽根店", "服部天神店", "総持寺店", "緑地公園店",
    ]),
    ("tokai", "東海", ["名古屋今池店", "本山店"]),
    ("kyushu", "九州", ["天神店", "平尾店"]),
]

VISIBLE = 14  # 折りたたまずに最初から見せる件数

PIN = '<svg width="13" height="13" style="color:var(--accent-deep)"><use href="#i-pin"/></svg>'


def li(name):
    return f'      <li>{PIN}<span>{html.escape(name)}</span></li>'


def store_list(names, cls=""):
    attr = f' class="stores {cls}"'.replace("  ", " ").rstrip()
    rows = "\n".join(li(n) for n in names)
    return f'    <ul{attr}>\n{rows}\n    </ul>'


def build():
    tabs = ['  <div class="tabs" role="tablist" aria-label="エリアで絞り込む">']
    for i, (slug, label, names) in enumerate(AREAS):
        sel = "true" if i == 0 else "false"
        tabs.append(
            f'    <button class="tab" type="button" role="tab" id="tab-{slug}" '
            f'aria-selected="{sel}" aria-controls="panel-{slug}" data-area="{slug}">'
            f'{label}<span class="c">{len(names)}</span></button>'
        )
    tabs.append("  </div>")

    panels = []
    for i, (slug, label, names) in enumerate(AREAS):
        head = names[:VISIBLE]
        tail = names[VISIBLE:]
        parts = [
            f'  <div class="area-panel" id="panel-{slug}" role="tabpanel" '
            f'aria-labelledby="tab-{slug}" data-area="{slug}">',
            store_list(head),
        ]
        if tail:
            parts.append('    <details class="more">')
            parts.append(
                f'      <summary>{label}の店舗をすべて見る（{len(names)}店舗）'
                f'<svg class="chev" width="16" height="16"><use href="#i-chev"/></svg></summary>'
            )
            parts.append(store_list(tail))
            parts.append("    </details>")
        parts.append("  </div>")
        panels.append("\n".join(parts))

    return "\n".join(tabs) + "\n" + "\n".join(panels)


def main():
    idx = pathlib.Path(__file__).resolve().parent.parent / "index.html"
    s = idx.read_text(encoding="utf-8")
    a, b = "<!--STORES:START-->", "<!--STORES:END-->"
    if a not in s or b not in s:
        raise SystemExit("index.html に STORES:START / STORES:END マーカーが見つかりません。")
    head, rest = s.split(a, 1)
    _, tail = rest.split(b, 1)
    idx.write_text(head + a + "\n" + build() + "\n  " + b + tail, encoding="utf-8")
    total = sum(len(a[2]) for a in AREAS)
    print(f"店舗セクションを生成しました: 全{total}店舗 / {len(AREAS)}エリア")


if __name__ == "__main__":
    main()
