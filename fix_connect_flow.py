import os
os.chdir(os.path.dirname(__file__))
with open('static/index.html','r',encoding='utf-8') as f:
    c=f.read()

# Add pendingArrowType to state
old="    cutMode: false,"
new="    cutMode: false,\n    pendingArrowType: 'single',"
c=c.replace(old,new)

# Replace toggleConnect to show submenu
old="// —— 连线模式 ——\n\nfunction toggleConnect() {\n    if (state.mode === 'connect') {\n        state.mode = 'normal';\n        state.connectFrom = null;\n        btnConnect.classList.remove('btn-primary');\n        btnConnect.classList.add('btn-action');\n        container.classList.remove('connect-mode');\n        modeIndicator.classList.remove('active');\n        clearHighlights();\n        removeTempLine();\n    } else {\n        state.mode = 'connect';\n        state.connectFrom = null;\n        btnConnect.classList.remove('btn-action');\n        btnConnect.classList.add('btn-primary');\n        container.classList.add('connect-mode');\n        modeIndicator.classList.add('active');\n    }\n}"
new='// —— 连线模式 ——\n\nfunction toggleConnect() {\n    if (state.mode === \'connect\') {\n        exitConnectMode();\n        return;\n    }\n    // 显示连线样式子菜单\n    var m = document.getElementById(\'conn-type-menu\');\n    if (m) { m.remove(); return; }\n    m = document.createElement(\'div\');\n    m.id = \'conn-type-menu\';\n    m.style.cssText = \'position:fixed;z-index:3000;background:rgba(30,25,20,0.96);border:1px solid rgba(255,255,255,0.12);border-radius:8px;padding:4px;display:flex;flex-direction:column;gap:2px;box-shadow:0 8px 30px rgba(0,0,0,0.5);backdrop-filter:blur(8px);\';\n    m.innerHTML = \'<button onclick="startConnectMode(\\\'none\\\')" style="padding:8px 16px;border:none;border-radius:6px;background:transparent;color:#ddd;font-size:13px;cursor:pointer;text-align:left;display:flex;align-items:center;gap:8px;transition:background .1s;font-family:inherit;">— 普通连线</button><button onclick="startConnectMode(\\\'single\\\')" style="padding:8px 16px;border:none;border-radius:6px;background:transparent;color:#ddd;font-size:13px;cursor:pointer;text-align:left;display:flex;align-items:center;gap:8px;transition:background .1s;font-family:inherit;">➡️ 单箭头</button><button onclick="startConnectMode(\\\'double\\\')" style="padding:8px 16px;border:none;border-radius:6px;background:transparent;color:#ddd;font-size:13px;cursor:pointer;text-align:left;display:flex;align-items:center;gap:8px;transition:background .1s;font-family:inherit;">↔️ 双箭头</button>\';\n    var btn = document.getElementById(\'btn-connect\');\n    var rect = btn.getBoundingClientRect();\n    m.style.left = (rect.right + 4) + \'px\';\n    m.style.top = (rect.top - 4) + \'px\';\n    document.body.appendChild(m);\n    setTimeout(function() { document.addEventListener(\'click\', function _close(e) { if (!e.target.closest(\'#conn-type-menu\')) { var mm = document.getElementById(\'conn-type-menu\'); if (mm) mm.remove(); document.removeEventListener(\'click\', _close); } }); }, 10);\n}\n\nfunction startConnectMode(type) {\n    state.pendingArrowType = type;\n    var m = document.getElementById(\'conn-type-menu\');\n    if (m) m.remove();\n    state.mode = \'connect\';\n    state.connectFrom = null;\n    btnConnect.classList.remove(\'btn-action\');\n    btnConnect.classList.add(\'btn-primary\');\n    container.classList.add(\'connect-mode\');\n    modeIndicator.classList.add(\'active\');\n}\n\nfunction exitConnectMode() {\n    state.mode = \'normal\';\n    state.connectFrom = null;\n    btnConnect.classList.remove(\'btn-primary\');\n    btnConnect.classList.add(\'btn-action\');\n    container.classList.remove(\'connect-mode\');\n    modeIndicator.classList.remove(\'active\');\n    clearHighlights();\n    removeTempLine();\n}'
c=c.replace(old,new)

# Update createConnection to use pendingArrowType
old="        arrowType: arrowType || 'single',"
new="        arrowType: arrowType || state.pendingArrowType || 'single',"
c=c.replace(old,new)

# Also update handleConnectClick - it calls createConnection without arrowType, should use pending
# createConnection already defaults to pendingArrowType now

with open('static/index.html','w',encoding='utf-8') as f:
    f.write(c)
print('ok')
