$failed = $false

Get-ChildItem .\tasks -Directory -Filter "task_*" |
    Sort-Object Name |
    ForEach-Object {
        Write-Host "`nRunning tests in $($_.Name)" -ForegroundColor Cyan

        Push-Location $_.FullName

        python -m pytest -q

        if ($LASTEXITCODE -ne 0) {
            $failed = $trues
            Write-Host "FAILED: $($_.Name)" -ForegroundColor Red
        }

        Pop-Location
    }

if ($failed) {
    Write-Host "`nSome tasks failed." -ForegroundColor Red
    exit 1
}

Write-Host "`nAll task tests passed." -ForegroundColor Green