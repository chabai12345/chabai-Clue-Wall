$f = "static/index.html"
$old = "static/old.txt"
$new = "static/new.txt"

# Read with correct UTF-8
Add-Type -AssemblyName System.Text.Encoding
$bytes = [System.IO.File]::ReadAllBytes((Resolve-Path $f))
$content = [System.Text.Encoding]::UTF8.GetString($bytes)

# Fix 1: renderConnection - pass cp to makeStringPath
$content = $content.Replace(
"path.setAttribute('d', makeStringPath(from.x, from.y, to.x, to.y));",
"path.setAttribute('d', makeStringPath(from.x, from.y, to.x, to.y, cp.x, cp.y));")

# Fix 2: updateConnection - remove duplicates + pass cp
# First remove the bad duplicate lines
$content = $content.Replace(
"    const to = getPinPos(conn.toId);`r`n    const to = getPinPos(conn.toId);`r`n    conn.lineEl.setAttribute('d', makeStringPath(from.x, from.y, to.x, to.y, cp.x, cp.y));",
"    conn.lineEl.setAttribute('d', makeStringPath(from.x, from.y, to.x, to.y, cp.x, cp.y));")

# Fix 3: remove the other bad path block in updateConnection
$content = $content.Replace(
"    const cp = getConnControlPos(conn);`r`n`r`n    const path = document.createElementNS('http__DELETE__www.w3.org/2000/svg', 'path');",
"    const cp = getConnControlPos(conn);")
$content = $content.Replace("__DELETE__", "//")

# Actually, simpler - just remove the bad path block
$content = $content.Replace(
"    const cp = getConnControlPos(conn);`r`n`r`n    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');`r`n    path.dataset.id = conn.id;`r`n    const to = getPinPos(conn.toId);`r`n`r`n    const to = getPinPos(conn.toId);`r`n    const to = getPinPos(conn.toId);",
"    const cp = getConnControlPos(conn);")

# Fix 4: Add draggingConn to state
$content = $content.Replace(
"    arrowMode: false,`r`n    boardName: '',",
"    arrowMode: false,`r`n    draggingConn: null,`r`n    boardName: '',")

# Fix 5: Add path mousedown for curve drag (after click handler)
$content = $content.Replace(
"    path.addEventListener('click', (e) => {`r`n        e.stopPropagation();`r`n        editConnectionLabel(conn);`r`n    });`r`n`r`n    // 双击连线 → 删除",
"    path.addEventListener('click', (e) => {`r`n        e.stopPropagation();`r`n        editConnectionLabel(conn);`r`n    });`r`n`r`n    path.addEventListener('mousedown', (e) => {`r`n        if (e.button !== 0) return;`r`n        var p = screenToBoard(e.clientX, e.clientY);`r`n        var cp2 = getConnControlPos(conn);`r`n        conn.controlX = cp2.x;`r`n        conn.controlY = cp2.y;`r`n        state.draggingConn = conn.id;`r`n        e.stopPropagation();`r`n        e.preventDefault();`r`n    });`r`n`r`n    // 双击连线 → 删除")

# Fix 6: Add global drag handlers
$content = $content.Replace(
"// 按 Escape 退出连线模式",
"document.addEventListener('mousemove', function(e) {`r`n    if (!state.draggingConn) return;`r`n    var c = state.connections.find(function(x) { return x.id === state.draggingConn; });`r`n    if (!c) return;`r`n    var p2 = screenToBoard(e.clientX, e.clientY);`r`n    c.controlX = p2.x;`r`n    c.controlY = p2.y;`r`n    updateConnection(c);`r`n});`r`ndocument.addEventListener('mouseup', function() { state.draggingConn = null; });`r`n`r`n// 按 Escape 退出连线模式")

# Fix 7: saveBoard - include control_x/control_y
$content = $content.Replace(
"        connections: state.connections.map(c => ({`r`n            id: c.id,`r`n            from_id: c.fromId,`r`n            to_id: c.toId,`r`n            color: c.color,`r`n            label: c.label,`r`n            font_size: c.fontSize || 14,`r`n        })),",
"        connections: state.connections.map(c => ({`r`n            id: c.id,`r`n            from_id: c.fromId,`r`n            to_id: c.toId,`r`n            color: c.color,`r`n            label: c.label,`r`n            font_size: c.fontSize || 14,`r`n            control_x: c.controlX,`r`n            control_y: c.controlY,`r`n        })),")

# Fix 8: loadBoard - pass control_x/control_y
$content = $content.Replace(
"createConnection(c.from_id, c.to_id, c.color, c.font_size || 14);",
"createConnection(c.from_id, c.to_id, c.color, c.font_size || 14, c.control_x, c.control_y);")

# Write back with correct UTF-8
[System.IO.File]::WriteAllText((Resolve-Path $f), $content, [System.Text.UTF8Encoding]::new($false))
Write-Host "Done"
