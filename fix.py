import re

with open('static/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. makeStringPath add cx,cy params
content = content.replace(
    'function makeStringPath(x1, y1, x2, y2) {',
    'function makeStringPath(x1, y1, x2, y2, cx, cy) {')

# 2. makeStringPath body - if cx/cy undefined use default
old = '''    const dx = x2 - x1;
    const dy = y2 - y1;
    const cx = (x1 + x2) / 2;
    const cy = (y1 + y2) / 2 + Math.min(Math.abs(dx) * 0.12, 40);
    return `M ${x1} ${y1} Q ${cx} ${cy} ${x2} ${y2}`;
}'''
new = '''    if (cx === undefined || cy === undefined) {
        const dx = x2 - x1;
        cx = (x1 + x2) / 2;
        cy = (y1 + y2) / 2 + Math.min(Math.abs(dx) * 0.12, 40);
    }
    return `M ${x1} ${y1} Q ${cx} ${cy} ${x2} ${y2}`;
}'''
content = content.replace(old, new)

# 3. Add getConnControlPos function after makeStringPath
old = '''    return `M ${x1} ${y1} Q ${cx} ${cy} ${x2} ${y2}`;
}

// 编辑连线名称和字号'''
new = '''    return `M ${x1} ${y1} Q ${cx} ${cy} ${x2} ${y2}`;
}

// 获取连线控制点
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
}

// 编辑连线名称和字号'''
content = content.replace(old, new)

# 4. createConnection add controlX/Y, handleEl
old = '''function createConnection(fromId, toId, color, fontSize) {
    const conn = {
        id: connId(),
        fromId,
        toId,
        color: color || CONN_COLORS[nextConnColor++ % CONN_COLORS.length],
        label: '',
        fontSize: fontSize || 14,
        lineEl: null,
        labelEl: null,
    };'''
new = '''function createConnection(fromId, toId, color, fontSize, controlX, controlY) {
    const conn = {
        id: connId(),
        fromId,
        toId,
        color: color || CONN_COLORS[nextConnColor++ % CONN_COLORS.length],
        label: '',
        fontSize: fontSize || 14,
        controlX: controlX ?? null,
        controlY: controlY ?? null,
        lineEl: null,
        labelEl: null,
        handleEl: null,
    };'''
content = content.replace(old, new)

# 5. renderConnection add cp + pass to makeStringPath
old = '''    const from = getPinPos(conn.fromId);
    const to = getPinPos(conn.toId);

    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.dataset.id = conn.id;
    path.setAttribute('d', makeStringPath(from.x, from.y, to.x, to.y));'''
new = '''    const from = getPinPos(conn.fromId);
    const to = getPinPos(conn.toId);
    const cp = getConnControlPos(conn);

    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.dataset.id = conn.id;
    path.setAttribute('d', makeStringPath(from.x, from.y, to.x, to.y, cp.x, cp.y));'''
content = content.replace(old, new)

# 6. updateConnection add cp + pass to makeStringPath
old = '''    const from = getPinPos(conn.fromId);
    const to = getPinPos(conn.toId);
    conn.lineEl.setAttribute('d', makeStringPath(from.x, from.y, to.x, to.y));'''
new = '''    const from = getPinPos(conn.fromId);
    const to = getPinPos(conn.toId);
    const cp = getConnControlPos(conn);
    conn.lineEl.setAttribute('d', makeStringPath(from.x, from.y, to.x, to.y, cp.x, cp.y));'''
content = content.replace(old, new)

# 7. Add draggingConn to state
content = content.replace(
    '    justResized: false,\n    boardName: '',',
    '    justResized: false,\n    draggingConn: null,\n    boardName: '',\n')

# 8. Add path mousedown in renderConnection
old = '''    // 双击连线 → 删除
    path.addEventListener('dblclick', (e) => {
        e.stopPropagation();
        removeConnection(conn.id);
    });
    path.title = '单击命名，双击删除';'''
new = '''    // 双击连线 → 删除
    path.addEventListener('dblclick', (e) => {
        e.stopPropagation();
        removeConnection(conn.id);
    });

    path.addEventListener('mousedown', (e) => {
        if (e.button !== 0) return;
        var p = screenToBoard(e.clientX, e.clientY);
        var cp2 = getConnControlPos(conn);
        conn.controlX = cp2.x;
        conn.controlY = cp2.y;
        state.draggingConn = conn.id;
        e.stopPropagation();
    });

    path.title = '单击命名，双击删除';'''
content = content.replace(old, new)

# 9. Add drag handlers
old = '''// 按 Escape 退出连线模式'''
new = '''// 曲度拖拽
document.addEventListener('mousemove', function(e) {
    if (!state.draggingConn) return;
    var c = state.connections.find(function(x) { return x.id === state.draggingConn; });
    if (!c) return;
    var p2 = screenToBoard(e.clientX, e.clientY);
    c.controlX = p2.x;
    c.controlY = p2.y;
    updateConnection(c);
});
document.addEventListener('mouseup', function() { state.draggingConn = null; });

// 按 Escape 退出连线模式'''
content = content.replace(old, new)

# 10. saveBoard include control_x/Y
old = '''            color: c.color,
            label: c.label,
            font_size: c.fontSize || 14,
        })),'''
new = '''            color: c.color,
            label: c.label,
            font_size: c.fontSize || 14,
            control_x: c.controlX,
            control_y: c.controlY,
        })),'''
content = content.replace(old, new)

# 11. loadBoard pass control_x/Y
content = content.replace(
    'createConnection(c.from_id, c.to_id, c.color, c.font_size || 14);',
    'createConnection(c.from_id, c.to_id, c.color, c.font_size || 14, c.control_x, c.control_y);')

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done!')
