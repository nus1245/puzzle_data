# PPTX -> 슬라이드별 PNG 렌더러 (PowerPoint COM 사용)
# 사용: powershell -File scripts\render_pptx.ps1 -Pptx <경로.pptx> -OutDir <출력폴더> [-Width 1920] [-Height 1080]
param(
    [Parameter(Mandatory = $true)][string]$Pptx,
    [Parameter(Mandatory = $true)][string]$OutDir,
    [int]$Width = 1920,
    [int]$Height = 1080
)

$ErrorActionPreference = "Stop"
$Pptx = (Resolve-Path -LiteralPath $Pptx).Path
if (-not (Test-Path -LiteralPath $OutDir)) { New-Item -ItemType Directory -Force -Path $OutDir | Out-Null }
$OutDir = (Resolve-Path -LiteralPath $OutDir).Path
Get-ChildItem -LiteralPath $OutDir -Include "*.PNG", "*.png" -ErrorAction SilentlyContinue | Remove-Item -Force

$app = New-Object -ComObject PowerPoint.Application
try {
    # ReadOnly=True, Untitled=False, WithWindow=False
    $pres = $app.Presentations.Open($Pptx, -1, 0, 0)
    try {
        $count = $pres.Slides.Count
        # 로캘에 따라 파일명이 Slide1.PNG / 슬라이드1.PNG 로 달라지므로 슬라이드별로 직접 내보낸다.
        for ($i = 1; $i -le $count; $i++) {
            $name = "slide-{0:D2}.png" -f $i
            $pres.Slides.Item($i).Export((Join-Path $OutDir $name), "PNG", $Width, $Height)
        }
        "Exported $count slides -> $OutDir"
    }
    finally { $pres.Close() }
}
finally { $app.Quit() }
