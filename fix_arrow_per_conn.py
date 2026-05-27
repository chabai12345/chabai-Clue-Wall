import os
os.chdir(os.path.dirname(__file__))
with open('static/index.html','r',encoding='utf-8') as f:
    c=f.read()

# Modify editConnectionLabel to include arrow toggle
old='// 编辑连线名称和字号\nfunction editConnectionLabel(conn) {\n    const newLabel = prompt(\'为这条连线命名（留空清除）：\', conn.label || \'\');\n    if (newLabel === null) return;\n    conn.label = newLabel;\n    if (conn.labelEl) conn.labelEl.textContent = newLabel;\n\n    const sizeStr = prompt(\'字号 (10~30，默认14):\', String(conn.fontSize || 14));\n    if (sizeStr !== null) {\n        const size = parseInt(sizeStr);\n        if (size >= 10 && size <= 30) {\n            conn.fontSize = size;\n            if (conn.labelEl) conn.labelEl.style.fontSize = size + \'px\';\n        }\n    }\n}'
new='// 编辑连线名称和字号\nfunction editConnectionLabel(conn) {\n    var msg = \'连线：\' + (conn.label || \'未命名\');\n    msg += \'\\n当前箭头：\' + (conn.hasArrow ? \'显示\' : \'隐藏\');\n    msg += \'\\n\\n1 - 改名称\\n2 - 切换箭头\';'
new += '\n    var choice = prompt(msg);'
new += '\n    if (choice === null) return;'
new += '\n    if (choice === \'1\') {'
new += '\n        var newLabel = prompt(\'新名称（留空清除）：\', conn.label || \'\');'
new += '\n        if (newLabel === null) return;'
new += '\n        conn.label = newLabel;'
new += '\n        if (conn.labelEl) conn.labelEl.textContent = newLabel;'
new += '\n        var sizeStr = prompt(\'字号 (10~30，默认14):\', String(conn.fontSize || 14));'
new += '\n        if (sizeStr !== null) {'
new += '\n            var size = parseInt(sizeStr);'
new += '\n            if (size >= 10 && size <= 30) { conn.fontSize = size; if (conn.labelEl) conn.labelEl.style.fontSize = size + \'px\'; }'
new += '\n        }'
new += '\n    } else if (choice === \'2\') {'
new += '\n        conn.hasArrow = !conn.hasArrow;'
new += '\n        renderConnection(conn);'
new += '\n    }'
new += '\n}'
c=c.replace(old,new)

# Add has_arrow to saveBoard
old='            control_x: c.controlX,\n            control_y: c.controlY,'
new='            control_x: c.controlX,\n            control_y: c.controlY,\n            has_arrow: c.hasArrow,'
c=c.replace(old,new)

# Add has_arrow to loadBoard createConnection call - update the parameter passing
# loadBoard already passes 6 args to createConnection, let me add the 7th
old='createConnection(c.from_id, c.to_id, c.color, c.font_size || 14, c.control_x, c.control_y);'
new='createConnection(c.from_id, c.to_id, c.color, c.font_size || 14, c.control_x, c.control_y, c.has_arrow);'
c=c.replace(old,new)

# Update createConnection to accept hasArrow param
old='function createConnection(fromId, toId, color, fontSize, controlX, controlY) {'
new='function createConnection(fromId, toId, color, fontSize, controlX, controlY, hasArrow) {'
c=c.replace(old,new)

# Update the hasArrow default in createConnection
old='        hasArrow: true,'
new='        hasArrow: hasArrow !== undefined ? hasArrow : true,'
c=c.replace(old,new)

# Remove global arrowMode from state
old='    arrowMode: true,'
new=''
c=c.replace(old,new)

# Remove toggleArrow button from sidebar
old='    <button class="btn-action btn-on" id="btn-arrow" onclick="toggleArrow()"><span class="s-icon">➡️</span><span id="arrow-label">箭头</span></button>'
new=''
c=c.replace(old,new)

# Remove the entire toggleArrow function (from comment to closing brace)
old='// 箭头模式切换（已弃用，每条线独立控制）\nfunction toggleArrow() {\n    state.arrowMode = !state.arrowMode;\n    var btn = document.getElementById(\'btn-arrow\');\n    var label = document.getElementById(\'arrow-label\');\n    if (state.arrowMode) {\n        btn.classList.add(\'btn-on\');\n        label.textContent = \'箭头\';\n    } else {\n        btn.classList.remove(\'btn-on\');\n        label.textContent = \'直线\';\n    }\n    state.connections.forEach(function(c) { renderConnection(c); });\n}'
new=''
c=c.replace(old,new)

# Clean up any double blank lines from removals
c=c.replace('\n\n\n\n\n', '\n\n')
c=c.replace('\n\n\n\n', '\n\n')
c=c.replace('\n\n\n', '\n\n')

with open('static/index.html','w',encoding='utf-8') as f:
    f.write(c)
print('ok')
