# PPTX -> 슬라이드 PNG 렌더 + 텍스트 실측(줄 수·경계) JSON (PowerPoint COM)
# 사용: .\scripts\deck\render_audit.ps1 -Pptx <pptx> -OutDir <png 폴더> -Json <audit.json> [-Pdf <pdf 경로>]
param(
    [Parameter(Mandatory = $true)][string]$Pptx,
    [Parameter(Mandatory = $true)][string]$OutDir,
    [Parameter(Mandatory = $true)][string]$Json,
    [string]$Pdf = ""
)
$ErrorActionPreference = "Stop"
$Pptx = (Resolve-Path -LiteralPath $Pptx).Path
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$OutDir = (Resolve-Path -LiteralPath $OutDir).Path
Get-ChildItem -LiteralPath $OutDir -Filter "*.png" -ErrorAction SilentlyContinue | Remove-Item -Force

# 사용자가 이미 PowerPoint 를 쓰고 있었다면 종료하지 않는다.
$wasRunning = @(Get-Process POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
$app = New-Object -ComObject PowerPoint.Application
$rows = New-Object System.Collections.ArrayList
try {
    $pres = $app.Presentations.Open($Pptx, -1, 0, 0)     # ReadOnly, Untitled=False, WithWindow=False
    try {
        $i = 0
        foreach ($sl in $pres.Slides) {
            $i++
            $sl.Export((Join-Path $OutDir ("slide-{0:D2}.png" -f $i)), "PNG", 1920, 1080)
            foreach ($sh in $sl.Shapes) {
                if ($sh.HasTextFrame -ne 0 -and $sh.TextFrame2.HasText -ne 0) {
                    $tr = $sh.TextFrame2.TextRange
                    $lines = -1
                    try { $lines = $tr.Lines().Count } catch { }
                    [void]$rows.Add([pscustomobject]@{
                        slide = $i; name = $sh.Name; lines = $lines
                        boundW = [math]::Round($tr.BoundWidth, 2); boundH = [math]::Round($tr.BoundHeight, 2)
                        boundL = [math]::Round($tr.BoundLeft, 2);  boundT = [math]::Round($tr.BoundTop, 2)
                        left = [math]::Round($sh.Left, 2); top = [math]::Round($sh.Top, 2)
                        width = [math]::Round($sh.Width, 2); height = [math]::Round($sh.Height, 2)
                    })
                }
            }
        }
        if ($Pdf -ne "") {
            $pdfPath = [System.IO.Path]::GetFullPath($Pdf)
            $pres.SaveAs($pdfPath, 32)                  # ppSaveAsPDF
        }
        "Exported $i slides -> $OutDir ; text shapes audited: $($rows.Count)"
    }
    finally { $pres.Close() }
}
finally { if (-not $wasRunning) { $app.Quit() } }
$rows | ConvertTo-Json -Depth 3 | Set-Content -Encoding UTF8 -LiteralPath $Json
