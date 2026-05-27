import os
os.chdir(os.path.dirname(__file__))
with open('static/index.html','r',encoding='utf-8') as f:
    c=f.read()

# 1. Replace hasArrow with arrowType in createConnection
old="        hasArrow: hasArrow !== undefined ? hasArrow : true,"
new="        arrowType: arrowType || 'single',"
c=c.replace(old,new)

# 2. Update createConnection function signature
old="function createConnection(fromId, toId, color, fontSize, controlX, controlY, hasArrow) {"
new="function createConnection(fromId, toId, color, fontSize, controlX, controlY, arrowType) {"
c=c.replace(old,new)

# 3. Replace hasArrow/conn.hasArrow with arrowType checks in renderConnection
old="    if (conn.hasArrow) {\n        path.setAttribute('marker-end', 'url(#arrowhead)');\n    }"
new="    if (conn.arrowType === 'single' || conn.arrowType === 'double') {\n        path.setAttribute('marker-end', 'url(#arrowhead)');\n    }\n    if (conn.arrowType === 'double') {\n        path.setAttribute('marker-start', 'url(#arrowhead)');\n    }"
c=c.replace(old,new)

# 4. Replace prompt-based editConnectionLabel with modal version
old="// 编辑连线名称和字号\nvar _editConnId = null;\n\nfunction editConnectionLabel(conn) {\n    _editConnId = conn.id;\n    document.getElementById('conn-name').value = conn.label || '';\n    document.getElementById('conn-fontsize').value = conn.fontSize || 14;\n    var abtn = document.getElementById('conn-arrow-btn');\n    abtn.textContent = conn.hasArrow ? '➡️ 显示' : '➡️ 隐藏';\n    abtn.style.background = conn.hasArrow ? '#d4a87a' : 'rgba(255,255,255,0.08)';\n    abtn.style.color = conn.hasArrow ? '#1a1510' : '#aaa';\n    document.getElementById('conn-modal').classList.add('active');\n}\n\nfunction closeConnModal() {\n    document.getElementById('conn-modal').classList.remove('active');\n}\n\nfunction saveConnDetail() {\n    var conn = state.connections.find(function(c) { return c.id === _editConnId; });\n    if (!conn) return;\n    conn.label = document.getElementById('conn-name').value;\n    if (conn.labelEl) conn.labelEl.textContent = conn.label;\n    var size = parseInt(document.getElementById('conn-fontsize').value);\n    if (size >= 10 && size <= 30) {\n        conn.fontSize = size;\n        if (conn.labelEl) conn.labelEl.style.fontSize = size + 'px';\n    }\n    closeConnModal();\n}\n\nfunction deleteConn() {\n    var conn = state.connections.find(function(c) { return c.id === _editConnId; });\n    if (conn) removeConnection(conn.id);\n    closeConnModal();\n}\n\ndocument.getElementById('conn-arrow-btn').addEventListener('click', function() {\n    var conn = state.connections.find(function(c) { return c.id === _editConnId; });\n    if (!conn) return;\n    conn.hasArrow = !conn.hasArrow;\n    this.textContent = conn.hasArrow ? '➡️ 显示' : '➡️ 隐藏';\n    this.style.background = conn.hasArrow ? '#d4a87a' : 'rgba(255,255,255,0.08)';\n    this.style.color = conn.hasArrow ? '#1a1510' : '#aaa';\n    renderConnection(conn);\n});"

new="// 编辑连线\nvar _editConnId = null;\n\nfunction editConnectionLabel(conn) {\n    _editConnId = conn.id;\n    document.getElementById('conn-name').value = conn.label || '';\n    document.getElementById('conn-fontsize').value = conn.fontSize || 14;\n    // highlight arrow type\n    ['none','single','double'].forEach(function(t) {\n        var btn = document.getElementById('conn-arrow-' + t);\n        if (conn.arrowType === t) { btn.style.background = '#d4a87a'; btn.style.color = '#1a1510'; }\n        else { btn.style.background = 'rgba(255,255,255,0.06)'; btn.style.color = '#aaa'; }\n    });\n    document.getElementById('conn-modal').classList.add('active');\n}\n\nfunction closeConnModal() {\n    document.getElementById('conn-modal').classList.remove('active');\n}\n\nfunction setConnArrow(t) {\n    var conn = state.connections.find(function(c) { return c.id === _editConnId; });\n    if (!conn) return;\n    conn.arrowType = t;\n    ['none','single','double'].forEach(function(x) {\n        var btn = document.getElementById('conn-arrow-' + x);\n        if (x === t) { btn.style.background = '#d4a87a'; btn.style.color = '#1a1510'; }\n        else { btn.style.background = 'rgba(255,255,255,0.06)'; btn.style.color = '#aaa'; }\n    });\n    renderConnection(conn);\n}\n\nfunction saveConnDetail() {\n    var conn = state.connections.find(function(c) { return c.id === _editConnId; });\n    if (!conn) return;\n    conn.label = document.getElementById('conn-name').value;\n    if (conn.labelEl) conn.labelEl.textContent = conn.label;\n    var size = parseInt(document.getElementById('conn-fontsize').value);\n    if (size >= 10 && size <= 30) {\n        conn.fontSize = size;\n        if (conn.labelEl) conn.labelEl.style.fontSize = size + 'px';\n    }\n    closeConnModal();\n}\n\nfunction deleteConn() {\n    var conn = state.connections.find(function(c) { return c.id === _editConnId; });\n    if (conn) removeConnection(conn.id);\n    closeConnModal();\n}"
c=c.replace(old,new)

# 5. Replace arrow field in saveBoard
old="            has_arrow: c.hasArrow,"
new="            arrow_type: c.arrowType,"
c=c.replace(old,new)

# 6. Replace arrow arg in loadBoard
old="createConnection(c.from_id, c.to_id, c.color, c.font_size || 14, c.control_x, c.control_y, c.has_arrow);"
new="createConnection(c.from_id, c.to_id, c.color, c.font_size || 14, c.control_x, c.control_y, c.arrow_type);"
c=c.replace(old,new)

# 7. Replace conn-modal HTML: arrow toggle -> three buttons
old='<div class=\"detail-field\">\n            <label>箭头</label>\n            <button id=\"conn-arrow-btn\" class=\"btn-primary\" style=\"padding:8px 16px;border:none;border-radius:6px;font-size:13px;cursor:pointer;font-family:inherit;\">➡️ 显示</button>\n        </div>'
new='<div class=\"detail-field\">\n            <label>连线样式</label>\n            <div style=\"display:flex;gap:6px;flex-wrap:wrap;\">\n                <button id=\"conn-arrow-none\" onclick=\"setConnArrow(\'none\')\" style=\"padding:6px 14px;border:none;border-radius:6px;font-size:12px;cursor:pointer;background:rgba(255,255,255,0.06);color:#aaa;font-family:inherit;\">— 普通</button>\n                <button id=\"conn-arrow-single\" onclick=\"setConnArrow(\'single\')\" style=\"padding:6px 14px;border:none;border-radius:6px;font-size:12px;cursor:pointer;background:rgba(255,255,255,0.06);color:#aaa;font-family:inherit;\">➡️ 单箭头</button>\n                <button id=\"conn-arrow-double\" onclick=\"setConnArrow(\'double\')\" style=\"padding:6px 14px;border:none;border-radius:6px;font-size:12px;cursor:pointer;background:rgba(255,255,255,0.06);color:#aaa;font-family:inherit;\">↔️ 双箭头</button>\n            </div>\n        </div>'
c=c.replace(old,new)

# 8. Update saveBoardAs to use arrowType
old="connections: state.connections.map(function(c) { return { id: c.id, from_id: c.fromId, to_id: c.toId, color: c.color, label: c.label, font_size: c.fontSize || 14, control_x: c.controlX, control_y: c.controlY }; })"
new="connections: state.connections.map(function(c) { return { id: c.id, from_id: c.fromId, to_id: c.toId, color: c.color, label: c.label, font_size: c.fontSize || 14, control_x: c.controlX, control_y: c.controlY, arrow_type: c.arrowType }; })"
c=c.replace(old,new)

with open('static/index.html','w',encoding='utf-8') as f:
    f.write(c)
print('ok')
