import os
os.chdir(os.path.dirname(__file__))
with open('static/index.html','r',encoding='utf-8') as f:
    c=f.read()

# Replace remaining hasArrow/conn-arrow-btn references
c=c.replace("conn.hasArrow ? '➡️ 显示' : '➡️ 隐藏'","(conn.arrowType === 'single' ? '➡️' : '↔️')")
c=c.replace("conn.hasArrow ? '#d4a87a' : 'rgba(255,255,255,0.08)'","'#d4a87a'")
c=c.replace("conn.hasArrow ? '#1a1510' : '#aaa'","'#1a1510'")
c=c.replace("conn.hasArrow = !conn.hasArrow;","conn.arrowType = conn.arrowType === 'single' ? 'none' : 'single';")

# Replace editConnectionLabel with the correct version
old="// 编辑连线\nvar _editConnId = null;\n\nfunction editConnectionLabel(conn) {\n    _editConnId = conn.id;\n    document.getElementById('conn-name').value = conn.label || '';\n    document.getElementById('conn-fontsize').value = conn.fontSize || 14;\n    // highlight arrow type\n    ['none','single','double'].forEach(function(t) {\n        var btn = document.getElementById('conn-arrow-' + t);\n        if (conn.arrowType === t) { btn.style.background = '#d4a87a'; btn.style.color = '#1a1510'; }\n        else { btn.style.background = 'rgba(255,255,255,0.06)'; btn.style.color = '#aaa'; }\n    });\n    document.getElementById('conn-modal').classList.add('active');\n}\n\nfunction closeConnModal() {\n    document.getElementById('conn-modal').classList.remove('active');\n}\n\nfunction setConnArrow(t) {\n    var conn = state.connections.find(function(c) { return c.id === _editConnId; });\n    if (!conn) return;\n    conn.arrowType = t;\n    ['none','single','double'].forEach(function(x) {\n        var btn = document.getElementById('conn-arrow-' + x);\n        if (x === t) { btn.style.background = '#d4a87a'; btn.style.color = '#1a1510'; }\n        else { btn.style.background = 'rgba(255,255,255,0.06)'; btn.style.color = '#aaa'; }\n    });\n    renderConnection(conn);\n}\n\nfunction saveConnDetail() {\n    var conn = state.connections.find(function(c) { return c.id === _editConnId; });\n    if (!conn) return;\n    conn.label = document.getElementById('conn-name').value;\n    if (conn.labelEl) conn.labelEl.textContent = conn.label;\n    var size = parseInt(document.getElementById('conn-fontsize').value);\n    if (size >= 10 && size <= 30) {\n        conn.fontSize = size;\n        if (conn.labelEl) conn.labelEl.style.fontSize = size + 'px';\n    }\n    closeConnModal();\n}\n\nfunction deleteConn() {\n    var conn = state.connections.find(function(c) { return c.id === _editConnId; });\n    if (conn) removeConnection(conn.id);\n    closeConnModal();\n}"

# The new complete block
new="// 编辑连线\nvar _editConnId = null;\n\nfunction editConnectionLabel(conn) {\n    _editConnId = conn.id;\n    document.getElementById('conn-name').value = conn.label || '';\n    document.getElementById('conn-fontsize').value = conn.fontSize || 14;\n    ['none','single','double'].forEach(function(t) {\n        var btn = document.getElementById('conn-arrow-' + t);\n        if (conn.arrowType === t) { btn.style.background = '#d4a87a'; btn.style.color = '#1a1510'; }\n        else { btn.style.background = 'rgba(255,255,255,0.06)'; btn.style.color = '#aaa'; }\n    });\n    document.getElementById('conn-modal').classList.add('active');\n}\n\nfunction closeConnModal() {\n    document.getElementById('conn-modal').classList.remove('active');\n}\n\nfunction setConnArrow(t) {\n    var conn = state.connections.find(function(c) { return c.id === _editConnId; });\n    if (!conn) return;\n    conn.arrowType = t;\n    ['none','single','double'].forEach(function(x) {\n        var btn = document.getElementById('conn-arrow-' + x);\n        if (x === t) { btn.style.background = '#d4a87a'; btn.style.color = '#1a1510'; }\n        else { btn.style.background = 'rgba(255,255,255,0.06)'; btn.style.color = '#aaa'; }\n    });\n    renderConnection(conn);\n}\n\nfunction saveConnDetail() {\n    var conn = state.connections.find(function(c) { return c.id === _editConnId; });\n    if (!conn) return;\n    conn.label = document.getElementById('conn-name').value;\n    if (conn.labelEl) conn.labelEl.textContent = conn.label;\n    var size = parseInt(document.getElementById('conn-fontsize').value);\n    if (size >= 10 && size <= 30) {\n        conn.fontSize = size;\n        if (conn.labelEl) conn.labelEl.style.fontSize = size + 'px';\n    }\n    closeConnModal();\n}\n\nfunction deleteConn() {\n    var conn = state.connections.find(function(c) { return c.id === _editConnId; });\n    if (conn) removeConnection(conn.id);\n    closeConnModal();\n}\n"

c=c.replace(old,new)

# Remove the old event listener for conn-arrow-btn
old2="document.getElementById('conn-arrow-btn').addEventListener('click', function() {\n    var conn = state.connections.find(function(c) { return c.id === _editConnId; });\n    if (!conn) return;\n    conn.hasArrow = !conn.hasArrow;\n    this.textContent = conn.hasArrow ? '➡️ 显示' : '➡️ 隐藏';\n    this.style.background = conn.hasArrow ? '#d4a87a' : 'rgba(255,255,255,0.08)';\n    this.style.color = conn.hasArrow ? '#1a1510' : '#aaa';\n    renderConnection(conn);\n});"
c=c.replace(old2,'')

with open('static/index.html','w',encoding='utf-8') as f:
    f.write(c)
print('ok')
