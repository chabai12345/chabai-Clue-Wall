import os
os.chdir(os.path.dirname(__file__))
with open('static/index.html','r',encoding='utf-8') as f:
    c=f.read()

# Add connection detail modal HTML before the detail-modal
old='<!-- ====== 卡片详情模态框 ====== -->'
new='<!-- ====== 连线详情模态框 ====== -->\n<div class="modal-overlay" id="conn-modal">\n    <div class="modal" style="width:340px;">\n        <h2>🔗 连线</h2>\n        <div class="detail-field">\n            <label>名称</label>\n            <input type="text" id="conn-name" placeholder="输入名称..." style="width:100%;padding:8px 10px;border-radius:6px;border:1px solid rgba(255,255,255,0.12);background:rgba(255,255,255,0.06);color:#eee;font-size:14px;outline:none;font-family:inherit;">\n        </div>\n        <div class="detail-field">\n            <label>字号 (10~30)</label>\n            <input type="number" id="conn-fontsize" value="14" min="10" max="30" style="width:80px;padding:8px 10px;border-radius:6px;border:1px solid rgba(255,255,255,0.12);background:rgba(255,255,255,0.06);color:#eee;font-size:14px;outline:none;">\n        </div>\n        <div class="detail-field">\n            <label>箭头</label>\n            <button id="conn-arrow-btn" class="btn-primary" style="padding:8px 16px;border:none;border-radius:6px;font-size:13px;cursor:pointer;font-family:inherit;">➡️ 显示</button>\n        </div>\n        <div class="modal-actions">\n            <button class="btn-primary" onclick="saveConnDetail()" style="padding:8px 20px;border:none;border-radius:6px;font-size:13px;cursor:pointer;font-family:inherit;">💾 保存</button>\n            <button class="btn-action" onclick="closeConnModal()" style="padding:8px 20px;border:none;border-radius:6px;font-size:13px;cursor:pointer;color:#ccc;font-family:inherit;">关闭</button>\n            <button class="btn-danger" onclick="deleteConn()" style="padding:8px 20px;border:none;border-radius:6px;font-size:13px;cursor:pointer;margin-left:auto;font-family:inherit;">🗑️ 删除</button>\n        </div>\n    </div>\n</div>\n\n<!-- ====== 卡片详情模态框 ====== -->'
c=c.replace(old,new)

# Add connection detail JS functions before the editConnectionLabel
old='// 编辑连线名称和字号\nfunction editConnectionLabel(conn) {\n    var msg = \'连线：\' + (conn.label || \'未命名\');\n    msg += \'\\n当前箭头：\' + (conn.hasArrow ? \'显示\' : \'隐藏\');\n    msg += \'\\n\\n1 - 改名称\\n2 - 切换箭头\';'
old += '\n    var choice = prompt(msg);'
old += '\n    if (choice === null) return;'
old += '\n    if (choice === \'1\') {'
old += '\n        var newLabel = prompt(\'新名称（留空清除）：\', conn.label || \'\');'
old += '\n        if (newLabel === null) return;'
old += '\n        conn.label = newLabel;'
old += '\n        if (conn.labelEl) conn.labelEl.textContent = newLabel;'
old += '\n        var sizeStr = prompt(\'字号 (10~30，默认14):\', String(conn.fontSize || 14));'
old += '\n        if (sizeStr !== null) {'
old += '\n            var size = parseInt(sizeStr);'
old += '\n            if (size >= 10 && size <= 30) { conn.fontSize = size; if (conn.labelEl) conn.labelEl.style.fontSize = size + \'px\'; }'
old += '\n        }'
old += '\n    } else if (choice === \'2\') {'
old += '\n        conn.hasArrow = !conn.hasArrow;'
old += '\n        renderConnection(conn);'
old += '\n    }'
old += '\n}'

new='// 编辑连线名称和字号\nvar _editConnId = null;\n\nfunction editConnectionLabel(conn) {\n    _editConnId = conn.id;\n    document.getElementById(\'conn-name\').value = conn.label || \'\';\n    document.getElementById(\'conn-fontsize\').value = conn.fontSize || 14;\n    var abtn = document.getElementById(\'conn-arrow-btn\');\n    abtn.textContent = conn.hasArrow ? \'➡️ 显示\' : \'➡️ 隐藏\';\n    abtn.style.background = conn.hasArrow ? \'#d4a87a\' : \'rgba(255,255,255,0.08)\';\n    abtn.style.color = conn.hasArrow ? \'#1a1510\' : \'#aaa\';\n    document.getElementById(\'conn-modal\').classList.add(\'active\');\n}\n\nfunction closeConnModal() {\n    document.getElementById(\'conn-modal\').classList.remove(\'active\');\n}\n\nfunction saveConnDetail() {\n    var conn = state.connections.find(function(c) { return c.id === _editConnId; });\n    if (!conn) return;\n    conn.label = document.getElementById(\'conn-name\').value;\n    if (conn.labelEl) conn.labelEl.textContent = conn.label;\n    var size = parseInt(document.getElementById(\'conn-fontsize\').value);\n    if (size >= 10 && size <= 30) {\n        conn.fontSize = size;\n        if (conn.labelEl) conn.labelEl.style.fontSize = size + \'px\';\n    }\n    closeConnModal();\n}\n\nfunction deleteConn() {\n    var conn = state.connections.find(function(c) { return c.id === _editConnId; });\n    if (conn) removeConnection(conn.id);\n    closeConnModal();\n}'

# Wire up arrow toggle button
new += '\ndocument.getElementById(\'conn-arrow-btn\').addEventListener(\'click\', function() {\n    var conn = state.connections.find(function(c) { return c.id === _editConnId; });\n    if (!conn) return;\n    conn.hasArrow = !conn.hasArrow;\n    this.textContent = conn.hasArrow ? \'➡️ 显示\' : \'➡️ 隐藏\';\n    this.style.background = conn.hasArrow ? \'#d4a87a\' : \'rgba(255,255,255,0.08)\';\n    this.style.color = conn.hasArrow ? \'#1a1510\' : \'#aaa\';\n    renderConnection(conn);\n});'

c=c.replace(old,new)

with open('static/index.html','w',encoding='utf-8') as f:
    f.write(c)
print('ok')
