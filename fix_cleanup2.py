import os
os.chdir(os.path.dirname(__file__))
with open('static/index.html','r',encoding='utf-8') as f:
    c=f.read()

# Remove old conn-arrow-btn references
old="    var abtn = document.getElementById('conn-arrow-btn');\n    abtn.textContent = (conn.arrowType === 'single' ? '➡️' : '↔️');\n    abtn.style.background = '#d4a87a';\n    abtn.style.color = '#1a1510';"
c=c.replace(old,'    // arrow type handled by set buttons')

# Remove old event listener
old2="document.getElementById('conn-arrow-btn').addEventListener('click', function() {\n    var conn = state.connections.find(function(c) { return c.id === _editConnId; });\n    if (!conn) return;\n    conn.arrowType = conn.arrowType === 'single' ? 'none' : 'single';\n    this.textContent = (conn.arrowType === 'single' ? '➡️' : '↔️');\n    this.style.background = '#d4a87a';\n    this.style.color = '#1a1510';\n    renderConnection(conn);\n});"
c=c.replace(old2,'')

# Remove entire toggleArrow function (dead code)
old3="// 箭头模式切换（已弃用，每条线独立控制）\nfunction toggleArrow() {\n    state.arrowMode = !state.arrowMode;\n    var btn = document.getElementById('btn-arrow');\n    var label = document.getElementById('arrow-label');\n    if (conn.hasArrow) {\n        btn.classList.add('btn-on');\n        label.textContent = '箭头';\n    } else {\n        btn.classList.remove('btn-on');\n        label.textContent = '直线';\n    }\n    state.connections.forEach(function(c) { renderConnection(c); });\n}"
c=c.replace(old3,'')

with open('static/index.html','w',encoding='utf-8') as f:
    f.write(c)
print('ok')
