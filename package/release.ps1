# リリース用スクリプト

pyxel package ..\app ..\app\mahjong_web.py

$dt = (Get-Date).ToString("yyMMdd")
$name = "app${dt}.pyxapp"

Move-Item app.pyxapp $name

