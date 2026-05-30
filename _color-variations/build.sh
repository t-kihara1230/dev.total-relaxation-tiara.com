#!/usr/bin/env bash
# トータルリラクゼーション ティアラ — カラーバリエーション生成スクリプト
# 元デザイン（暖色ブラウン/ベージュ系）のブランドカラーのみを置換し、
# 成功/エラー/情報などの機能色（アイコン等）はそのまま維持します。
set -euo pipefail
cd "$(dirname "$0")/.."

FILES=(
  index.html
  about/index.html
  menu/index.html
  menu/thai_stretch/index.html
  menu/basic_massage/index.html
  menu/campaign/index.html
  menu/head_spa/index.html
  menu/oilmassage/index.html
)

# 各パレット: ディレクトリ名 と 13個の置換値(from固定)
# 順番: main dark soft ink footer bg bgalt bgwarm gold blush  rgbaMain rgbaThin rgbaDark
build() {
  local dir="$1"; shift
  local main="$1" dark="$2" soft="$3" ink="$4" footer="$5" bg="$6" bgalt="$7" bgwarm="$8" gold="$9" blush="${10}"
  local rgbaMain="${11}" rgbaThin="${12}" rgbaDark="${13}"
  local out="_color-variations/$dir"
  for f in "${FILES[@]}"; do
    mkdir -p "$out/$(dirname "$f")"
    sed \
      -e "s/#c19268/$main/gI" \
      -e "s/#9a7048/$dark/gI" \
      -e "s/#5c4a3a/$soft/gI" \
      -e "s/#2e2620/$ink/gI" \
      -e "s/#2b211c/$footer/gI" \
      -e "s/#fdfaf6/$bg/gI" \
      -e "s/#f5ebdf/$bgalt/gI" \
      -e "s/#f0e3d0/$bgwarm/gI" \
      -e "s/#d4b896/$gold/gI" \
      -e "s/#e8c9a0/$blush/gI" \
      -e "s/193,146,104/$rgbaMain/g" \
      -e "s/241, *183, *130/$rgbaThin/g" \
      -e "s/145, *110, *78/$rgbaDark/g" \
      "$f" > "$out/$f"
  done
  echo "built: $out"
}

#       dir                  main      dark      soft      ink       footer    bg        bgalt     bgwarm    gold      blush     rgbaMain      rgbaThin      rgbaDark
build "01-sage-green"       "#8fa37a" "#5f7350" "#4c5647" "#29302a" "#28302a" "#f8faf5" "#edf3e7" "#e4eedb" "#c1cfae" "#d3e0bf" "143,163,122" "190,205,165" "95,115,80"
build "02-aqua-mint"        "#6caba0" "#4a8278" "#45575a" "#243030" "#213030" "#f5fafa" "#e6f3f1" "#daeeeb" "#a8d3cb" "#c1e1da" "108,171,160" "150,205,196" "74,130,120"
build "03-lavender-greige"  "#9d8fb5" "#71648c" "#514a5a" "#2b2730" "#292530" "#faf8fc" "#efebf5" "#e7e0f0" "#c7bed6" "#ddd2e6" "157,143,181" "195,180,215" "113,100,140"
