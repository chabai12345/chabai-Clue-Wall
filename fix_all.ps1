$file = "static/index.html"
$content = [System.IO.File]::ReadAllText((Resolve-Path $file))

# 1. makeStringPath - add cx,cy params + getConnControlPos
$content = $content.Replace(
'function makeStringPath(x1, y1, x2, y2) {
    const dx = x2 - x1;
    const dy = y2 - y1;
    const cx = (x1 + x2) / 2;
    const cy = (y1 + y2) / 2 + Math.min(Math.abs(dx) * 0.12, 40);
    return `M ${x1} ${y1} Q ${cx} ${cy} ${x2} ${y2}`;
}',
'function makeStringPath(x1, y1, x2, y2, cx, cy) {
    if (cx === undefined || cy === undefined) {
        const dx = x2 - x1;
        cx = (x1 + x2) / 2;
        cy = (y1 + y2) / 2 + Math.min(Math.abs(dx) * 0.12, 40);
    }
    return `M ${x1} ${y1} Q ${cx} ${cy} ${x2} ${y2}`;
}

function getConnControlPos(conn) {
    const from = getPinPos(conn.fromId);
    const to = getPinPos(conn.toId);
    if (conn.controlX !== null && conn.controlY !== null) {
        return { x: conn.controlX, y: conn.controlY };
    }
    const dx = to.x - from.x;
    return {
        x: (from.x + to.x) / 2,
        y: (from.y + to.y) / 2 + Math.min(Math.abs(dx) * 0.12, 40),
    };
}')

# 2. createConnection - add controlX/controlY/handleEl
$content = $content.Replace(
'function createConnection(fromId, toId, color, fontSize) {
    const conn = {
        id: connId(),
        fromId,
        toId,
        color: color || CONN_COLORS[nextConnColor++ % CONN_COLORS.length],
        label: '''',
        fontSize: fontSize || 14,
        lineEl: null,
        labelEl: null,
    };',
'function createConnection(fromId, toId, color, fontSize, controlX, controlY) {
    const conn = {
        id: connId(),
        fromId,
        toId,
        color: color || CONN_COLORS[nextConnColor++ % CONN_COLORS.length],
        label: '''',
        fontSize: fontSize || 14,
        controlX: controlX ?? null,
        controlY: controlY ?? null,
        lineEl: null,
        labelEl: null,
        handleEl: null,
    };')

# 3. renderConnection - add cp, pass to makeStringPath
$content = $content.Replace(
'    const from = getPinPos(conn.fromId);
    const to = getPinPos(conn.toId);

    const path = document.createElementNS(''http://www.w3.org/2000/svg'', ''path'');
    path.dataset.id = conn.id;
    path.setAttribute(''d'', makeStringPath(from.x, from.y, to.x, to.y));',
'    const from = getPinPos(conn.fromId);
    const to = getPinPos(conn.toId);
    const cp = getConnControlPos(conn);

    const path = document.createElementNS(''http://www.w3.org/2000/svg'', ''path'');
    path.dataset.id = conn.id;
    path.setAttribute(''d'', makeStringPath(from.x, from.y, to.x, to.y, cp.x, cp.y));')

# 4. updateConnection - add cp, pass to makeStringPath
$content = $content.Replace(
'    const from = getPinPos(conn.fromId);
    const to = getPinPos(conn.toId);
    conn.lineEl.setAttribute(''d'', makeStringPath(from.x, from.y, to.x, to.y));',
'    const from = getPinPos(conn.fromId);
    const to = getPinPos(conn.toId);
    const cp = getConnControlPos(conn);
    conn.lineEl.setAttribute(''d'', makeStringPath(from.x, from.y, to.x, to.y, cp.x, cp.y));')

# 5. Add mousedown on path for curve drag
$content = $content.Replace(
'    path.addEventListener(''click'', (e) => {
        e.stopPropagation();
        editConnectionLabel(conn);
    });',
'    path.addEventListener(''click'', (e) => {
        e.stopPropagation();
        editConnectionLabel(conn);
    });

    path.addEventListener(''mousedown'', (e) => {
        if (e.button !== 0) return;
        const pos = screenToBoard(e.clientX, e.clientY);
        const cp = getConnControlPos(conn);
        conn.controlX = cp.x;
        conn.controlY = cp.y;
        state.draggingConn = conn.id;
        e.stopPropagation();
        e.preventDefault();
    });')

# 6. Add draggingConn to state
$content = $content.Replace(
'    arrowMode: false,
    boardName: '''',',
'    arrowMode: false,
    draggingConn: null,
    boardName: '''',')

# 7. Add curvature drag handlers before "按 Escape"
$content = $content.Replace(
'// 按 Escape 退出连线模式',
"var _curveDragMousemove = function(e) {
    if (!state.draggingConn) return;
    var conn = state.connections.find(function(c) { return c.id === state.draggingConn; });
    if (!conn) return;
    var pos = screenToBoard(e.clientX, e.clientY);
    conn.controlX = pos.x;
    conn.controlY = pos.y;
    updateConnection(conn);
};
var _curveDragMouseup = function() {
    state.draggingConn = null;
};
document.addEventListener('mousemove', _curveDragMousemove);
document.addEventListener('mouseup', _curveDragMouseup);

// 按 Escape 退出连线模式")

# 8. saveBoard - include controlX/controlY
$content = $content.Replace(
'        connections: state.connections.map(c => ({
            id: c.id,
            from_id: c.fromId,
            to_id: c.toId,
            color: c.color,
            label: c.label,
            font_size: c.fontSize || 14,
        })),',
'        connections: state.connections.map(c => ({
            id: c.id,
            from_id: c.fromId,
            to_id: c.toId,
            color: c.color,
            label: c.label,
            font_size: c.fontSize || 14,
            control_x: c.controlX,
            control_y: c.controlY,
        })),')

# 9. loadBoard - restore controlX/controlY
$content = $content.Replace(
'            createConnection(c.from_id, c.to_id, c.color, c.font_size || 14);',
'            createConnection(c.from_id, c.to_id, c.color, c.font_size || 14, c.control_x, c.control_y);')

# 10. removeConnection - also remove handleEl
$content = $content.Replace(
'    if (conn.lineEl) conn.lineEl.remove();
    if (conn.labelEl) conn.labelEl.remove();',
'    if (conn.lineEl) conn.lineEl.remove();
    if (conn.labelEl) conn.labelEl.remove();
    if (conn.handleEl) conn.handleEl.remove();')

[System.IO.File]::WriteAllText((Resolve-Path $file), $content, [System.Text.UTF8Encoding]::new($false))
Write-Host "Done!"
