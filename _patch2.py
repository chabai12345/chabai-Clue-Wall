with open(r'C:\Users\dengq.DESKTOP-FPEH2CV\Desktop\deepseek-workspace\detective-board\static\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add scissors button
old = '<button class="btn-action" id="btn-arrow" onclick="toggleArrow()"><span class="s-icon">➡️</span><span id="arrow-label">直线</span></button>'
new = '<button class="btn-action" id="btn-arrow" onclick="toggleArrow()"><span class="s-icon">➡️</span><span id="arrow-label">直线</span></button>\n    <button class="btn-action" id="btn-cut" onclick="toggleCut()"><span class="s-icon">✂️</span>切断</button>'
html = html.replace(old, new)

# 2. Add cutMode state
html = html.replace('arrowMode: false,', 'arrowMode: false,\n    cutMode: false,')

# 3. Add toggleCut function
cut_func = '''
// 切断模式
function toggleCut() {
    state.cutMode = !state.cutMode;
    const btn = document.getElementById('btn-cut');
    if (state.cutMode) {
        btn.style.background = '#c0392b';
        btn.style.color = '#fff';
        document.getElementById('board-container').style.cursor = 'not-allowed';
        showToast('✂️ 点击连线切断');
    } else {
        btn.style.background = '';
        btn.style.color = '';
        document.getElementById('board-container').style.cursor = '';
    }
}
'''
html = html.replace('// —— 连线模式 ——', cut_func + '\n// —— 连线模式 ——')

# 4. Modify connection click
html = html.replace(
    "path.addEventListener('click', (e) => {\n        e.stopPropagation();\n        editConnectionLabel(conn);\n    });",
    "path.addEventListener('click', (e) => {\n        e.stopPropagation();\n        if (state.cutMode) {\n            if (confirm('切断此连线？')) removeConnection(conn.id);\n        } else {\n            editConnectionLabel(conn);\n        }\n    });"
)

# 5. Modify label click
html = html.replace(
    "label.addEventListener('click', (e) => {\n        e.stopPropagation();\n        editConnectionLabel(conn);\n    });",
    "label.addEventListener('click', (e) => {\n        e.stopPropagation();\n        if (state.cutMode) {\n            removeConnection(conn.id);\n        } else {\n            editConnectionLabel(conn);\n        }\n    });"
)

with open(r'C:\Users\dengq.DESKTOP-FPEH2CV\Desktop\deepseek-workspace\detective-board\static\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Done')
