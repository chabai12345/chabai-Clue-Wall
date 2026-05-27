import os
os.chdir(os.path.dirname(__file__))
with open('static/index.html','r',encoding='utf-8') as f:
    c=f.read()

# Remove the separate cut button from sidebar
old='    <button class="btn-action" id="btn-connect" onclick="toggleConnectGrp()"><span class="s-icon">🔗</span>连线</button>\n\n    <button class="btn-action" id="btn-cut" onclick="toggleCut()"><span class="s-icon">✂️</span>切断</button>'
new='    <button class="btn-connectgrp" id="btn-connect" onclick="toggleConnectGrp()"><span class="s-icon">🔗</span>连线</button>'
c=c.replace(old,new)

# Replace toggleConnect function with the combined version (连线+切断)
old="// —— 连线模式 ——\n\nfunction toggleConnect() {\n    if (state.mode === 'connect') {\n        exitConnectMode();\n        return;\n    }\n    // 显示连线样式子菜单\n    var m = document.getElementById('conn-type-menu');\n    if (m) { m.remove(); return; }\n    m = document.createElement('div');\n    m.id = 'conn-type-menu';"
new="// —— 连线模式 ——\n\nfunction toggleConnectGrp() {\n    if (state.mode === 'connect') {\n        exitConnectMode();\n        return;\n    }\n    var m = document.getElementById('conn-type-menu');\n    if (m) { m.remove(); return; }\n    m = document.createElement('div');\n    m.id = 'conn-type-menu';"
c=c.replace(old,new)

# Replace the innerHTML of conn-type-menu to include 切断
old="m.innerHTML = '<button onclick=\"startConnectMode(\\'none\\')\" style=\"padding:8px 16px;border:none;border-radius:6px;background:transparent;color:#ddd;font-size:13px;cursor:pointer;text-align:left;display:flex;align-items:center;gap:8px;transition:background .1s;font-family:inherit;\">— 普通连线</button><button onclick=\"startConnectMode(\\'single\\')\" style=\"padding:8px 16px;border:none;border-radius:6px;background:transparent;color:#ddd;font-size:13px;cursor:pointer;text-align:left;display:flex;align-items:center;gap:8px;transition:background .1s;font-family:inherit;\">➡️ 单箭头</button><button onclick=\"startConnectMode(\\'double\\')\" style=\"padding:8px 16px;border:none;border-radius:6px;background:transparent;color:#ddd;font-size:13px;cursor:pointer;text-align:left;display:flex;align-items:center;gap:8px;transition:background .1s;font-family:inherit;\">↔️ 双箭头</button>';"
new="m.innerHTML = '<div style=\"padding:4px 8px;font-size:10px;color:#888;letter-spacing:1px;\">连线</div><button onclick=\"startConnectMode(\\'none\\')\" style=\"padding:8px 16px;border:none;border-radius:6px;background:transparent;color:#ddd;font-size:13px;cursor:pointer;text-align:left;display:flex;align-items:center;gap:8px;transition:background .1s;font-family:inherit;\">— 普通</button><button onclick=\"startConnectMode(\\'single\\')\" style=\"padding:8px 16px;border:none;border-radius:6px;background:transparent;color:#ddd;font-size:13px;cursor:pointer;text-align:left;display:flex;align-items:center;gap:8px;transition:background .1s;font-family:inherit;\">➡️ 单箭头</button><button onclick=\"startConnectMode(\\'double\\')\" style=\"padding:8px 16px;border:none;border-radius:6px;background:transparent;color:#ddd;font-size:13px;cursor:pointer;text-align:left;display:flex;align-items:center;gap:8px;transition:background .1s;font-family:inherit;\">↔️ 双箭头</button><div style=\"padding:4px 8px;font-size:10px;color:#888;letter-spacing:1px;margin-top:4px;\">工具</div><button onclick=\"toggleCut();var mm=document.getElementById(\\'conn-type-menu\\');if(mm)mm.remove()\" style=\"padding:8px 16px;border:none;border-radius:6px;background:transparent;color:#ddd;font-size:13px;cursor:pointer;text-align:left;display:flex;align-items:center;gap:8px;transition:background .1s;font-family:inherit;\">✂️ 切断</button>';"
c=c.replace(old,new)

# Fix remaining toggleConnect() callers to use exitConnectMode or toggleConnectGrp
# The one in handleConnectClick (when clicking same card)
c=c.replace("clearHighlights();\n        removeTempLine();\n        toggleConnect();\n    } else {", "clearHighlights();\n        removeTempLine();\n        exitConnectMode();\n    } else {")

# Fix Escape handler
c=c.replace("if (state.mode === 'connect') toggleConnect();", "if (state.mode === 'connect') exitConnectMode();")

with open('static/index.html','w',encoding='utf-8') as f:
    f.write(c)
print('ok')
