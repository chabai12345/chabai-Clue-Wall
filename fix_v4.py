import re

import os
os.chdir(os.path.dirname(__file__) or '.')
with open('static/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace toolbar CSS with sidebar CSS
old_css = '''/* ======== 工具栏 ======== */
.toolbar {
    position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
    height: 52px; display: flex; align-items: center; gap: 6px;
    padding: 0 16px;
    background: rgba(30, 25, 20, 0.92);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
.toolbar .sep {
    width: 1px; height: 28px; background: rgba(255,255,255,0.12); margin: 0 6px;
}
.toolbar .brand {
    color: #d4a87a; font-size: 15px; font-weight: 600; margin-right: 12px;
    letter-spacing: 1px;
}
.toolbar button {
    padding: 6px 14px; border: none; border-radius: 6px;
    font-size: 13px; cursor: pointer; transition: all .15s;
    display: flex; align-items: center; gap: 5px;
}
.toolbar button:hover { filter: brightness(1.15); transform: translateY(-1px); }
.toolbar button:active { transform: translateY(0); filter: brightness(0.9); }

.btn-char  { background: #c0392b; color: #fff; }
.btn-clue  { background: #d68910; color: #fff; }
.btn-place { background: #148f77; color: #fff; }
.btn-evidence { background: #7d3c98; color: #fff; }
.btn-action { background: rgba(255,255,255,0.08); color: #ccc; }
.btn-action:hover { background: rgba(255,255,255,0.15); color: #fff; }
.btn-danger { background: rgba(255,80,80,0.15); color: #ff6b6b; }
.btn-danger:hover { background: rgba(255,80,80,0.25); }
.btn-primary { background: #d4a87a; color: #1a1510; font-weight: 600; }
.btn-primary:hover { background: #e0b88a; }

.toolbar .mode-indicator {
    margin-left: auto; font-size: 12px; color: #e74c3c;
    padding: 4px 12px; border: 1px dashed #e74c3c; border-radius: 4px;
    display: none;
}
.toolbar .mode-indicator.active { display: flex; align-items: center; gap: 6px; }'''

new_css = '''/* ======== 侧边栏 ======== */
.sidebar {
    position: fixed; top: 0; left: 0; bottom: 0; z-index: 1000;
    width: 64px; display: flex; flex-direction: column; align-items: center;
    padding: 12px 0;
    background: rgba(30, 25, 20, 0.95);
    border-right: 1px solid rgba(255,255,255,0.06);
    gap: 2px;
}
.sidebar .brand {
    color: #d4a87a; font-size: 10px; font-weight: 600;
    letter-spacing: 0.5px; margin-bottom: 4px; text-align: center;
    line-height: 1.2;
}
.sidebar .sep {
    width: 28px; height: 1px; background: rgba(255,255,255,0.1); margin: 3px 0;
}
.sidebar button {
    width: 50px; padding: 6px 0; border: none; border-radius: 6px;
    font-size: 10px; cursor: pointer; transition: all .15s;
    display: flex; flex-direction: column; align-items: center;
    gap: 1px; line-height: 1.1;
}
.sidebar button .s-icon { font-size: 18px; }
.sidebar button:hover { filter: brightness(1.2); }
.sidebar .btn-card   { background: #7d3c98; color: #fff; }
.sidebar .btn-action { background: rgba(255,255,255,0.06); color: #aaa; }
.sidebar .btn-action:hover { background: rgba(255,255,255,0.12); color: #fff; }
.sidebar .btn-primary { background: #d4a87a; color: #1a1510; font-weight: 600; }
.sidebar .btn-primary:hover { background: #e0b88a; }
.sidebar .btn-danger { background: rgba(255,80,80,0.15); color: #ff6b6b; }
.sidebar .btn-danger:hover { background: rgba(255,80,80,0.25); }
.sidebar .btn-on { background: #d4a87a; color: #1a1510; }

.sidebar .mode-indicator {
    margin-top: auto; font-size: 10px; color: #e74c3c;
    padding: 2px 4px; border: 1px dashed #e74c3c; border-radius: 4px;
    display: none; text-align: center; line-height: 1.2; width: 54px;
}
.sidebar .mode-indicator.active { display: block; }
.sidebar .mode-indicator .exit-btn {
    background: rgba(255,255,255,0.15); border: none; color: #fff;
    border-radius: 4px; padding: 2px 6px; font-size: 9px;
    cursor: pointer; margin-top: 3px; width: 100%;
}

.btn-char  { background: #c0392b; color: #fff; }
.btn-clue  { background: #d68910; color: #fff; }
.btn-place { background: #148f77; color: #fff; }
.btn-evidence { background: #7d3c98; color: #fff; }
.btn-action { background: rgba(255,255,255,0.08); color: #ccc; }
.btn-action:hover { background: rgba(255,255,255,0.15); color: #fff; }
.btn-danger { background: rgba(255,80,80,0.15); color: #ff6b6b; }
.btn-danger:hover { background: rgba(255,80,80,0.25); }
.btn-primary { background: #d4a87a; color: #1a1510; font-weight: 600; }
.btn-primary:hover { background: #e0b88a; }'''

content = content.replace(old_css, new_css)

# 2. Replace toolbar HTML with sidebar
old_html = '''<!-- ====== 工具栏 ====== -->
<div class="toolbar" id="toolbar">
    <span class="brand">🎮 游戏档案</span>
    <button class="btn-char"  onclick="addCard('character')">👤 人物</button>
    <button class="btn-evidence" onclick="addCard('item')">📦 物品</button>
    <button class="btn-place" onclick="addCard('location')">📍 地点</button>
    <span class="sep"></span>
    <button class="btn-action" id="btn-connect" onclick="toggleConnect()">🔗 连线</button>
    <button class="btn-action" onclick="clearBoard()">🗑️ 清空</button>
    <span class="sep"></span>
    <button class="btn-primary" onclick="showSaveModal()">💾 保存</button>
    <button class="btn-action" onclick="showLoadModal()">📂 读取</button>
    <span class="mode-indicator" id="mode-indicator">
        <span>🔗</span> 连线模式 — 点击卡片连接
        <button onclick="toggleConnect()" style="background:rgba(255,255,255,0.15);border:none;color:#fff;border-radius:4px;padding:2px 8px;font-size:11px;cursor:pointer;margin-left:4px;">退出</button>
    </span>
</div>'''

new_html = '''<!-- ====== 侧边栏 ====== -->
<div class="sidebar" id="sidebar">
    <div class="brand">🎮<br>档案</div>
    <div class="sep"></div>
    <button class="btn-card" onclick="addCardPrompt()"><span class="s-icon">📇</span>卡片</button>
    <div class="sep"></div>
    <button class="btn-action" id="btn-connect" onclick="toggleConnect()"><span class="s-icon">🔗</span>连线</button>
    <button class="btn-action" id="btn-arrow" onclick="toggleArrow()"><span class="s-icon">➡️</span><span id="arrow-label">直线</span></button>
    <button class="btn-action" id="btn-cut" onclick="toggleCut()"><span class="s-icon">✂️</span>切断</button>
    <div class="sep"></div>
    <button class="btn-danger" onclick="clearBoard()"><span class="s-icon">🗑️</span>清空</button>
    <div class="sep"></div>
    <button class="btn-primary" onclick="showSaveModal()"><span class="s-icon">💾</span>保存</button>
    <button class="btn-action" onclick="showLoadModal()"><span class="s-icon">📂</span>读取</button>
    <div class="mode-indicator" id="mode-indicator">
        🔗<br>连线中
        <button class="exit-btn" onclick="toggleConnect()">退出</button>
    </div>
</div>'''

content = content.replace(old_html, new_html)

# 3. Update board-container: left:64px instead of top:52px left:0
content = content.replace(
    '#board-container {\n    position: fixed; top: 52px; left: 0; right: 0; bottom: 0;',
    '#board-container {\n    position: fixed; top: 0; left: 64px; right: 0; bottom: 0;')

# 4. Add arrowhead marker back to SVG
content = content.replace(
    '<svg id="svg-layer"></svg>',
    '''<svg id="svg-layer">
        <defs>
            <marker id="arrowhead" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke"/>
            </marker>
        </defs>
    </svg>''')

# 5. Add arrowMode, cutMode to state
content = content.replace(
    '    draggingConn: null,',
    '''    draggingConn: null,
    arrowMode: false,
    cutMode: false,''')

# 6. Add renderConnection arrow support
content = content.replace(
    "    path.style.filter = 'drop-shadow(0 1px 2px rgba(0,0,0,0.3))';",
    "    path.style.filter = 'drop-shadow(0 1px 2px rgba(0,0,0,0.3))';\n    if (state.arrowMode) {\n        path.setAttribute('marker-end', 'url(#arrowhead)');\n    }")

# 7. Add toggleArrow and toggleCut functions
old_fns = '''// —— 连线模式 ——

function toggleConnect() {'''
new_fns = '''// 箭头模式切换
function toggleArrow() {
    state.arrowMode = !state.arrowMode;
    var btn = document.getElementById('btn-arrow');
    var label = document.getElementById('arrow-label');
    if (state.arrowMode) {
        btn.classList.add('btn-on');
        label.textContent = '箭头';
    } else {
        btn.classList.remove('btn-on');
        label.textContent = '直线';
    }
    state.connections.forEach(function(c) { renderConnection(c); });
}

// 切断模式
function toggleCut() {
    state.cutMode = !state.cutMode;
    var btn = document.getElementById('btn-cut');
    if (state.cutMode) {
        btn.classList.add('btn-on');
        document.getElementById('board-container').style.cursor = 'not-allowed';
    } else {
        btn.classList.remove('btn-on');
        document.getElementById('board-container').style.cursor = '';
    }
}

// 添加卡片（弹出类型选择）
function addCardPrompt() {
    var type = prompt('卡片类型：\\n1 - 人物 👤\\n2 - 物品 📦\\n3 - 地点 📍', '1');
    if (type === null) return;
    type = type.trim();
    if (type === '1' || type === '人物' || type === '人') addCard('character');
    else if (type === '2' || type === '物品' || type === '物') addCard('item');
    else if (type === '3' || type === '地点' || type === '地') addCard('location');
    else showToast('输入 1/2/3');
}

// —— 连线模式 ——

function toggleConnect() {'''
content = content.replace(old_fns, new_fns)

# 8. Enable cut mode on connection click
old_cut = '''    // 双击连线 → 删除
    path.addEventListener('dblclick', (e) => {
        e.stopPropagation();
        removeConnection(conn.id);
    });'''
new_cut = '''    // 单击连线 → 编辑命名 或 切断
    path.addEventListener('click', (e) => {
        e.stopPropagation();
        if (state.cutMode) {
            removeConnection(conn.id);
            showToast('✂️ 已切断');
        } else {
            editConnectionLabel(conn);
        }
    });

    // 双击连线 → 删除
    path.addEventListener('dblclick', (e) => {
        e.stopPropagation();
        if (!state.cutMode) removeConnection(conn.id);
    });'''
content = content.replace(old_cut, new_cut)

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done! All changes applied.')
