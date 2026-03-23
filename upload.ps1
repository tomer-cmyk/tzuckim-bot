$token = 'REPLACE_WITH_TOKEN'
$repo = 'tomer-cmyk/tzuckim-bot'
$files = @('app.py', 'requirements.txt', 'Procfile', 'system_prompt.txt', '.gitignore')

foreach ($fname in $files) {
    $path = "C:\Users\lena\Desktop\tzuckim-bot\$fname"
    $bytes = [System.IO.File]::ReadAllBytes($path)
    $content = [System.Convert]::ToBase64String($bytes)
    $body = @{message="add $fname"; content=$content} | ConvertTo-Json
    try {
        $result = Invoke-RestMethod -Uri "https://api.github.com/repos/$repo/contents/$fname" -Method PUT -Headers @{Authorization="token $token"; 'Content-Type'='application/json'} -Body $body
        Write-Host "OK: $fname"
    } catch {
        Write-Host "ERROR $($fname): $($_.Exception.Message)"
    }
}
Write-Host "Done!"
