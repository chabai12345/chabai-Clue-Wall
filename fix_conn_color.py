import os
os.chdir(os.path.dirname(__file__))
with open('static/index.html','r',encoding='utf-8') as f:
    c=f.read()

# Add color buttons after arrow buttons in conn-menu
old='<div style="display:flex;gap:4px;margin-bottom:6px;align-items:center;">\n        <input id="conn-fontsize" type="number" value="14" min="10" max="30" style="width:50px;padding:3px 4px;border-radius:4px;border:1px solid rgba(255,255,255,0.12);background:rgba(255,255,255,0.06);color:#eee;font-size:11px;outline:none;text-align:center;">\n        <span style="color:#888;font-size:10px;">字号</span>\n    </div>'
new='<div style="display:flex;gap:3px;margin-bottom:6px;flex-wrap:wrap;">\n        <button class="cc" data-c="#e74c3c" style="width:18px;height:18px;border-radius:50%;border:2px solid rgba(255,255,255,0.2);cursor:pointer;background:#e74c3c;padding:0;"></button>\n        <button class="cc" data-c="#3498db" style="width:18px;height:18px;border-radius:50%;border:2px solid rgba(255,255,255,0.2);cursor:pointer;background:#3498db;padding:0;"></button>\n        <button class="cc" data-c="#f1c40f" style="width:18px;height:18px;border-radius:50%;border:2px solid rgba(255,255,255,0.2);cursor:pointer;background:#f1c40f;padding:0;"></button>\n        <button class="cc" data-c="#2ecc71" style="width:18px;height:18px;border-radius:50%;border:2px solid rgba(255,255,255,0.2);cursor:pointer;background:#2ecc71;padding:0;"></button>\n        <button class="cc" data-c="#9b59b6" style="width:18px;height:18px;border-radius:50%;border:2px solid rgba(255,255,255,0.2);cursor:pointer;background:#9b59b6;padding:0;"></button>\n        <button class="cc" data-c="#e67e22" style="width:18px;height:18px;border-radius:50%;border:2px solid rgba(255,255,255,0.2);cursor:pointer;background:#e67e22;padding:0;"></button>\n        <button class="cc" data-c="#1abc9c" style="width:18px;height:18px;border-radius:50%;border:2px solid rgba(255,255,255,0.2);cursor:pointer;background:#1abc9c;padding:0;"></button>\n    </div>\n    <div style="display:flex;gap:4px;margin-bottom:6px;align-items:center;">\n        <input id="conn-fontsize" type="number" value="14" min="10" max="30" style="width:50px;padding:3px 4px;border-radius:4px;border:1px solid rgba(255,255,255,0.12);background:rgba(255,255,255,0.06);color:#eee;font-size:11px;outline:none;text-align:center;">\n        <span style="color:#888;font-size:10px;">字号</span>\n    </div>'
c=c.replace(old,new)

# Add color click handlers in the JS (after setConnArrow)
old='}\n\nfunction saveConnDetail() {'
new='}\n\n// 连线颜色选择\ndocument.addEventListener(\'click\', function(e) {\n    if (e.target.classList.contains(\'cc\')) {\n        var conn = state.connections.find(function(c) { return c.id === _editConnId; });\n        if (!conn) return;\n        conn.color = e.target.getAttribute(\'data-c\');\n        renderConnection(conn);\n    }\n});\n\nfunction saveConnDetail() {'
c=c.replace(old,new)

with open('static/index.html','w',encoding='utf-8') as f:
    f.write(c)
print('ok')
