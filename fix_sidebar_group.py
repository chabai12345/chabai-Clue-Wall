import os
os.chdir(os.path.dirname(__file__))
with open('static/index.html','r',encoding='utf-8') as f:
    c=f.read()

# Add btn-connect CSS color
old='.sidebar .btn-card   { background: #7d3c98; color: #fff; }\n.sidebar .btn-archive { background: #b8860b; color: #fff; }'
new='.sidebar .btn-card   { background: #7d3c98; color: #fff; }\n.sidebar .btn-archive { background: #b8860b; color: #fff; }\n.sidebar .btn-connectgrp { background: #c0392b; color: #fff; }'
c=c.replace(old,new)

# Replace sidebar: merge 连线+切断 into a group button, remove separate cut
old='    <button class="btn-action" id="btn-connect" onclick="toggleConnect()"><span class="s-icon">🔗</span>连线</button>\n\n    <button class="btn-action" id="btn-cut" onclick="toggleCut()"><span class="s-icon">✂️</span>切断</button>'
new='    <button class="btn-connectgrp" id="btn-connectgrp" onclick="toggleConnectGrp()"><span class="s-icon">🔗</span>连线</button>'
c=c.replace(old,new)

# Rename toggleConnect to toggleConnectGrp and make it show a submenu
old='function toggleConnect() {'
new='function toggleConnectGrp() {'
c=c.replace(old,new)

# Actually, I need to modify toggleConnectGrp to show a submenu with 连线+切断 options
# Let me find the current toggleConnect function (now renamed to toggleConnectGrp)
# The function starts with "function toggleConnectGrp() {" and shows the arrow type submenu
# I need to replace it to show a submenu with 连线/切断 first

old='function toggleConnectGrp() {\n    if (state.mode === \'connect\') {\n        exitConnectMode();\n        return;\n    }\n    // 显示连线样式子菜单\n    var m = document.getElementById(\'conn-type-menu\');\n    if (m) { m.remove(); return; }\n    m = document.createElement(\'div\');\n    m.id = \'conn-type-menu\';'
new='function toggleConnectGrp() {\n    if (state.mode === \'connect\') {\n        exitConnectMode();\n        return;\n    }\n    // 显示连线子菜单\n    var m = document.getElementById(\'conn-type-menu\');\n    if (m) { m.remove(); return; }\n    m = document.createElement(\'div\');\n    m.id = \'conn-type-menu\';'
c=c.replace(old,new)

# Update the innerHTML of the menu to have two sections: 连线 options and 切断
# Need to find the m.innerHTML line and change it

old="m.innerHTML = '<button onclick=\"startConnectMode(\\'none\\')\" style=\"padding:8px 16px;border:none;border-radius:6px;background:transparent;color:#ddd;font-size:13px;cursor:pointer;text-align:left;display:flex;align-items:center;gap:8px;transition:background .1s;font-family:inherit;\">— 普通连线</button><button onclick=\"startConnectMode(\\'single\\')\" style=\"padding:8px 16px;border:none;border-radius:6px;background:transparent;color:#ddd;font-size:13px;cursor:pointer;text-align:left;display:flex;align-items:center;gap:8px;transition:background .1s;font-family:inherit;\">➡️ 单箭头</button><button onclick=\"startConnectMode(\\'double\\')\" style=\"padding:8px 16px;border:none;border-radius:6px;background:transparent;color:#ddd;font-size:13px;cursor:pointer;text-align:left;display:flex;align-items:center;gap:8px;transition:background .1s;font-family:inherit;\">↔️ 双箭头</button>';"
new="m.innerHTML = '<div style=\"padding:4px 8px;font-size:10px;color:#888;text-transform:uppercase;letter-spacing:1px;\">连线</div><button onclick=\"startConnectMode(\\'none\\')\" style=\"padding:8px 16px;border:none;border-radius:6px;background:transparent;color:#ddd;font-size:13px;cursor:pointer;text-align:left;display:flex;align-items:center;gap:8px;transition:background .1s;font-family:inherit;\">— 普通</button><button onclick=\"startConnectMode(\\'single\\')\" style=\"padding:8px 16px;border:none;border-radius:6px;background:transparent;color:#ddd;font-size:13px;cursor:pointer;text-align:left;display:flex;align-items:center;gap:8px;transition:background .1s;font-family:inherit;\">➡️ 单箭头</button><button onclick=\"startConnectMode(\\'double\\')\" style=\"padding:8px 16px;border:none;border-radius:6px;background:transparent;color:#ddd;font-size:13px;cursor:pointer;text-align:left;display:flex;align-items:center;gap:8px;transition:background .1s;font-family:inherit;\">↔️ 双箭头</button><div style=\"padding:4px 8px;font-size:10px;color:#888;text-transform:uppercase;letter-spacing:1px;margin-top:4px;\">工具</div><button onclick=\"toggleCut();closeConnTypeMenu()\" style=\"padding:8px 16px;border:none;border-radius:6px;background:transparent;color:#ddd;font-size:13px;cursor:pointer;text-align:left;display:flex;align-items:center;gap:8px;transition:background .1s;font-family:inherit;\">✂️ 切断</button>';"
c=c.replace(old,new)

# Add closeConnTypeMenu helper
old='function startConnectMode(type) {'
new='function closeConnTypeMenu() { var m = document.getElementById(\'conn-type-menu\'); if (m) m.remove(); }\n\nfunction startConnectMode(type) {'
c=c.replace(old,new)

with open('static/index.html','w',encoding='utf-8') as f:
    f.write(c)
print('ok')
