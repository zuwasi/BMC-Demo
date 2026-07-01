<#
  reset-demo.ps1 - Reset the sensor demo to the buggy baseline (count = 20).

  Redeploys the pre-built "baseline" ECR image to the sensor Lambda using the
  shared S3 terraform state, then verifies the live endpoint returns 20.

  Usage:  powershell -ExecutionPolicy Bypass -File reset-demo.ps1
#>

$ErrorActionPreference = "Stop"
$InfraDir = Join-Path $PSScriptRoot "infra"

# --- AWS credentials (from the User environment) ---
$env:AWS_ACCESS_KEY_ID     = [Environment]::GetEnvironmentVariable("AWS_ACCESS_KEY_ID", "User")
$env:AWS_SECRET_ACCESS_KEY = [Environment]::GetEnvironmentVariable("AWS_SECRET_ACCESS_KEY", "User")
$env:AWS_DEFAULT_REGION    = "eu-west-1"
if (-not $env:AWS_ACCESS_KEY_ID) { throw "AWS_ACCESS_KEY_ID is not set in the User environment." }

# --- locate terraform ---
$tf = (Get-Command terraform -ErrorAction SilentlyContinue).Source
if (-not $tf) { $tf = "C:\Amp_demos\AT-Tiny-Assemblomator\bin\terraform.exe" }
if (-not (Test-Path $tf)) { throw "terraform executable not found." }

Write-Host "==> Redeploying buggy baseline image (count should become 20)..." -ForegroundColor Cyan
& $tf -chdir="$InfraDir" init -input=false -reconfigure | Out-Null
& $tf -chdir="$InfraDir" apply -input=false -auto-approve `
    "-var-file=environments/dev.tfvars" "-var=image_tag=baseline" | Select-Object -Last 3

$endpoint = (& $tf -chdir="$InfraDir" output -raw sensor_endpoint).Trim()
Write-Host "`n==> Endpoint: $endpoint" -ForegroundColor Cyan

Start-Sleep -Seconds 3
$resp = (curl.exe -s $endpoint | ConvertFrom-Json)
Write-Host ("==> Live result: count={0}  expected={1}  ok={2}" -f $resp.count, $resp.expected, $resp.ok) `
    -ForegroundColor Yellow

if ($resp.count -eq 20) {
    Write-Host "`nRESET OK - demo is back to the buggy state (20). Ready for a new ticket." -ForegroundColor Green
} else {
    Write-Host "`nWARNING: expected count=20 but got $($resp.count)." -ForegroundColor Red
}
