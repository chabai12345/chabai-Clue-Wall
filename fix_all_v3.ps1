$f = "static/index.html"
$bytes = [System.IO.File]::ReadAllBytes((Resolve-Path $f))
$content = [System.Text.Encoding]::UTF8.GetString($bytes)

$content = $content.Replace(
"path.setAttribute('d', makeStringPath(from.x, from.y, to.x, to.y));",
"path.setAttribute('d', makeStringPath(from.x, from.y, to.x, to.y, cp.x, cp.y));")

$content = $content.Replace(
"    const cp = getConnControlPos(conn);" + [char]13 + [char]10 + "" + [char]13 + [char]10 + "    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');" + [char]13 + [char]10 + "    path.dataset.id = conn.id;" + [char]13 + [char]10 + "    const to = getPinPos(conn.toId);" + [char]13 + [char]10 + "" + [char]13 + [char]10 + "    const to = getPinPos(conn.toId);" + [char]13 + [char]10 + "    const to = getPinPos(conn.toId);",
"    const cp = getConnControlPos(conn);")

$content = $content.Replace(
"    arrowMode: false," + [char]13 + [char]10 + "    boardName: '',",
"    arrowMode: false," + [char]13 + [char]10 + "    draggingConn: null," + [char]13 + [char]10 + "    boardName: '',")

$p1click = "    path.addEventListener('click', (e) => {" + [char]13 + [char]10 + "        e.stopPropagation();" + [char]13 + [char]10 + "        editConnectionLabel(conn);" + [char]13 + [char]10 + "    });" + [char]13 + [char]10] + [char]13 + [char]10 + "    // "
$p1click = $p1click + ChrW(21452) + ChrW(20987) + " " + ChrW(36830) + ChrW(32447) + " " + ChrW(8594) + " " + ChrW(21034) + ChrW(38500)

$p1md = "    path.addEventListener('click', (e) => {" + [char]13 + [char]10 + "        e.stopPropagation();" + [char]13 + [char]10 + "        editConnectionLabel(conn);" + [char]13 + [char]10 + "    });" + [char]13 + [char]10] + [char]13 + [char]10 + "    path.addEventListener('mousedown', (e) => {" + [char]13 + [char]10 + "        if (e.button !== 0) return;" + [char]13 + [char]10 + "        var p = screenToBoard(e.clientX, e.clientY);" + [char]13 + [char]10 + "        var cp2 = getConnControlPos(conn);" + [char]13 + [char]10 + "        conn.controlX = cp2.x;" + [char]13 + [char]10 + "        conn.controlY = cp2.y;" + [char]13 + [char]10 + "        state.draggingConn = conn.id;" + [char]13 + [char]10 + "        e.stopPropagation();" + [char]13 + [char]10 + "        e.preventDefault();" + [char]13 + [char]10 + "    });" + [char]13 + [char]10] + [char]13 + [char]10 + "    // "
$p1md = $p1md + ChrW(21452) + ChrW(20987) + " " + ChrW(36830) + ChrW(32447) + " " + ChrW(8594) + " " + ChrW(21034) + ChrW(38500)

$content = $content.Replace($p1click, $p1md)

$kEscape = "// " + ChrW(25353) + " Escape " + ChrW(36864) + ChrW(20986) + ChrW(36830) + ChrW(32447) + ChrW(27169) + ChrW(24335)

$dragCode = "document.addEventListener('mousemove', function(e) {" + [char]13 + [char]10 + "    if (!state.draggingConn) return;" + [char]13 + [char]10 + "    var c = state.connections.find(function(x) { return x.id === state.draggingConn; });" + [char]13 + [char]10 + "    if (!c) return;" + [char]13 + [char]10 + "    var p2 = screenToBoard(e.clientX, e.clientY);" + [char]13 + [char]10 + "    c.controlX = p2.x;" + [char]13 + [char]10 + "    c.controlY = p2.y;" + [char]13 + [char]10 + "    updateConnection(c);" + [char]13 + [char]10 + "});" + [char]13 + [char]10 + "document.addEventListener('mouseup', function() { state.draggingConn = null; });" + [char]13 + [char]10] + [char]13 + [char]10 + $kEscape

$content = $content.Replace($kEscape, $dragCode)

$content = $content.Replace(
"        connections: state.connections.map(c => ({" + [char]13 + [char]10 + "            id: c.id," + [char]13 + [char]10 + "            from_id: c.fromId," + [char]13 + [char]10 + "            to_id: c.toId," + [char]13 + [char]10 + "            color: c.color," + [char]13 + [char]10 + "            label: c.label," + [char]13 + [char]10 + "            font_size: c.fontSize || 14," + [char]13 + [char]10 + "        })),",
"        connections: state.connections.map(c => ({" + [char]13 + [char]10 + "            id: c.id," + [char]13 + [char]10 + "            from_id: c.fromId," + [char]13 + [char]10 + "            to_id: c.toId," + [char]13 + [char]10 + "            color: c.color," + [char]13 + [char]10 + "            label: c.label," + [char]13 + [char]10 + "            font_size: c.fontSize || 14," + [char]13 + [char]10 + "            control_x: c.controlX," + [char]13 + [char]10 + "            control_y: c.controlY," + [char]13 + [char]10 + "        })),")

$content = $content.Replace(
"createConnection(c.from_id, c.to_id, c.color, c.font_size || 14);",
"createConnection(c.from_id, c.to_id, c.color, c.font_size || 14, c.control_x, c.control_y);")

[System.IO.File]::WriteAllText((Resolve-Path $f), $content, [System.Text.UTF8Encoding]::new($false))
Write-Host "Done"
