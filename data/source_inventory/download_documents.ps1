param([switch]$AllowCouncilCertificateException)
$ErrorActionPreference = 'Stop'
$inventory = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'download_inventory.json') -Raw | ConvertFrom-Json
$downloadRoot = Join-Path (Split-Path $PSScriptRoot -Parent) 'raw/council_documents'
New-Item -ItemType Directory -Force -Path $downloadRoot | Out-Null
$categories = @{}
$categoryNumber = 0
foreach ($row in $inventory) {
    if (-not $categories.ContainsKey($row.category)) {
        $categoryNumber++
        $label = ($row.category -replace '^.*?:\s*', '' -replace '[^a-zA-Z0-9]+', '_').Trim('_').ToLower()
        $categories[$row.category] = ('{0:D2}_{1}' -f $categoryNumber, $label)
    }
    $row | Add-Member -NotePropertyName folder -NotePropertyValue $categories[$row.category] -Force
}
foreach ($item in $inventory) {
    $folder = Join-Path $downloadRoot $item.folder
    New-Item -ItemType Directory -Force -Path $folder | Out-Null
    $filename = [uri]::UnescapeDataString(([uri]$item.url).Segments[-1])
    $target = Join-Path $folder ('{0:D3}--{1}' -f $item.inventory_id, $filename)
    if (Test-Path -LiteralPath $target) {
        Write-Output "Already downloaded: $filename"
        continue
    }
    try {
        $request = @{Uri=$item.url; OutFile="$target.partial"; TimeoutSec=120; ErrorAction='Stop'}
        # The council site currently has a certificate error. This optional exception is limited to it.
        if ($AllowCouncilCertificateException -and ([uri]$item.url).Host -eq 'www.chirunducouncil.gov.zm') {
            $request.SkipCertificateCheck = $true
        }
        Invoke-WebRequest @request
        Move-Item -LiteralPath "$target.partial" -Destination $target
        Write-Output "Downloaded: $filename"
    } catch {
        Write-Warning "Could not download ${filename}: $_"
    }
}
