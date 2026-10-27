# 빌드한 PPTX 를 PowerPoint 로 다시 저장하며 사용 글꼴(맑은 고딕·Consolas)을 파일에 포함시킨다.
# 글꼴이 없는 PC·Mac·웹 뷰어에서 대체 글꼴로 줄이 밀리는 현상을 막기 위한 후처리.
# 사용: powershell scripts\deck\embed_fonts.ps1 -Pptx outputs\pptx\puzzledata_repair_report.pptx
param([Parameter(Mandatory = $true)][string]$Pptx)
$full = (Resolve-Path $Pptx).Path
$tmp = [System.IO.Path]::ChangeExtension($full, ".embed.tmp.pptx")
if (Test-Path $tmp) { Remove-Item $tmp }
$app = New-Object -ComObject PowerPoint.Application
try {
    $pres = $app.Presentations.Open($full, $true, $false, $false)
    $pres.SaveAs($tmp, 24, -1)     # ppSaveAsOpenXMLPresentation, EmbedTrueTypeFonts = msoTrue
    $pres.Close()
}
finally { $app.Quit() }
Move-Item -Force $tmp $full
"글꼴 포함 저장 완료: $full ($([math]::Round((Get-Item $full).Length / 1KB)) KB)"
