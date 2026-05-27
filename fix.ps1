$content = Get-Content 'static/index.html' -Raw

# Fix renderConnection - remove the bad injected path block
$content = $content -replace [regex]::Escape("    const cp = getConnControlPos(conn);`r`n`r`n    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');`r`n    path.dataset.id = conn.id;`r`n    const to = getPinPos(conn.toId);`r`n`r`n    const to = getPinPos(conn.toId);`r`n    const to = getPinPos(conn.toId);"), "    const cp = getConnControlPos(conn);"

Set-Content 'static/index.html' $content

Write-Host "Fixed!"
