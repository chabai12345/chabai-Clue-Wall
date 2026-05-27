import re

with open(r'C:\Users\dengq.DESKTOP-FPEH2CV\Desktop\deepseek-workspace\detective-board\static\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add "卡片" label before the three card buttons
html = html.replace(
    '<div class="sep"></div>\n    <button class="btn-char" onclick="addCard(\'character\')"><span class="s-icon">👤</span>人物</button>\n    <button class="btn-item" onclick="addCard(\'item\')"><span class="s-icon">📦</span>物品</button>\n    <button class="btn-place" onclick="addCard(\'location\')"><span class="s-icon">📍</span>地点</button>',
    '<div class="s-label">卡片</div>\n    <button class="btn-char" onclick="addCard(\'character\')"><span class="s-icon">👤</span>人物</button>\n    <button class="btn-item" onclick="addCard(\'item\')"><span class="s-icon">📦</span>物品</button>\n    <button class="btn-place" onclick="addCard(\'location\')"><span class="s-icon">📍</span>地点</button>'
)

# 2. Add arrow toggle button
html = html.replace(
    '<button class="btn-action" id="btn-connect" onclick="toggleConnect()"><span class="s-icon">🔗</span>连线</button>',
    '<button class="btn-action" id="btn-connect" onclick="toggleConnect()"><span class="s-icon">🔗</span>连线</button>\n    <button class="btn-action" id="btn-arrow" onclick="toggleArrow()"><span class="s-icon">➡️</span><span id="arrow-label">直线</span></button>'
)

# 3. Add CSS for s-label
html = html.replace(
    '.sidebar .btn-danger:hover { background: rgba(255,80,80,0.25); }',
    '.sidebar .btn-danger:hover { background: rgba(255,80,80,0.25); }\n.sidebar .s-label { font-size: 8px; color: #666; text-transform: uppercase; letter-spacing: 1px; margin: 2px 0; width: 100%; text-align: center; }'
)

# 4. Add toggleArrow JS function and arrow state
html = html.replace(
    'justResized: false,\n    boardName: \'\',',
    'justResized: false,\n    arrowMode: false,\n    boardName: \'\','
)

arrow_func = '''
// 箭头模式切换
function toggleArrow() {
    state.arrowMode = !state.arrowMode;
    const btn = document.getElementById('btn-arrow');
    const label = document.getElementById('arrow-label');
    if (state.arrowMode) {
        btn.style.background = '#d4a87a';
        btn.style.color = '#1a1510';
        label.textContent = '箭头';
    } else {
        btn.style.background = '';
        btn.style.color = '';
        label.textContent = '直线';
    }
}
'''

html = html.replace(
    '// —— 连线模式 ——',
    arrow_func + '\n// —— 连线模式 ——'
)

with open(r'C:\Users\dengq.DESKTOP-FPEH2CV\Desktop\deepseek-workspace\detective-board\static\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Done')
