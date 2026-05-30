#!/usr/bin/env python3
# カラーバリエーション内の8ページ間ナビゲーションリンクを、
# 本番URL(絶対パス)からフォルダ内の相対パスへ書き換える。
# これにより、色変更済みのページ同士をクリックで遷移できる
# （元のライブサイト=ベージュ系へ飛ばなくなる）。
#
# 使い方: python3 _fix_links.py <パレットのルートディレクトリ>
import os, sys

BASE = "https://dev.total-relaxation-tiara.com/"

# 本番URL → パレットルートからの相対ファイルパス（ローカルに存在する8ページのみ）
PAGES = {
    BASE:                       "index.html",
    BASE + "about/":            "about/index.html",
    BASE + "menu/":             "menu/index.html",
    BASE + "menu/basic_massage/": "menu/basic_massage/index.html",
    BASE + "menu/campaign/":    "menu/campaign/index.html",
    BASE + "menu/head_spa/":    "menu/head_spa/index.html",
    BASE + "menu/oilmassage/":  "menu/oilmassage/index.html",
    BASE + "menu/thai_stretch/": "menu/thai_stretch/index.html",
}


# フッター(.l-footer)の上下ボーダー（赤線）を、フッター背景色 --color_footer_bg に揃える。
# 各パレットの色変換でフッター背景は #28302a 等に置換済みのため、ボーダーが溶け込んで消える。
FOOTER_FIX_ID = "tiara-footer-border-fix"
FOOTER_FIX = (
    '<style id="%s">'
    '.l-footer,.w-beforeFooter,#before_footer_widget'
    '{border-color:var(--color_footer_bg)!important}'
    '</style>\n' % FOOTER_FIX_ID
)


def rewrite(root):
    count_files = 0
    count_links = 0
    for dirpath, _dirs, files in os.walk(root):
        for name in files:
            if not name.endswith(".html"):
                continue
            fpath = os.path.join(dirpath, name)
            relfile = os.path.relpath(fpath, root)          # 例: menu/basic_massage/index.html
            srcdir = os.path.dirname(relfile)               # 例: menu/basic_massage
            with open(fpath, encoding="utf-8") as fh:
                html = fh.read()
            orig = html
            for url, target in PAGES.items():
                rel = os.path.relpath(target, srcdir or ".")  # このページから見た相対パス
                # href="URL" を href="相対パス" に（末尾の " まで含めて厳密一致）
                html = html.replace('href="%s"' % url, 'href="%s"' % rel)
            # フッター上下の赤いボーダーをフッター背景色に合わせる（赤線を消す）補正を注入
            if FOOTER_FIX_ID not in html and "</head>" in html:
                html = html.replace("</head>", FOOTER_FIX + "</head>", 1)
            if html != orig:
                with open(fpath, "w", encoding="utf-8") as fh:
                    fh.write(html)
                count_files += 1
                count_links += orig.count('href="' + BASE)  # 概算
    print("  links rewritten / footer-fix injected in %d files (%s)" % (count_files, root))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python3 _fix_links.py <palette-root-dir>")
    rewrite(sys.argv[1])
