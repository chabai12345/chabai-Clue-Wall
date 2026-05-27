import os
os.chdir(os.path.dirname(__file__))
with open('static/index.html','r',encoding='utf-8') as f:
    c=f.read()

# Replace addCardPrompt function with submenu version
old='// 添加卡片（弹出类型选择）\nfunction addCardPrompt() {\n    var type = prompt(\'卡片类型：\\n1 - 人物 👤\\n2 - 物品 📦\\n3 - 地点 📍\', \'1\');\n    if (type === null) return;\n    type = type.trim();\n    if (type === \'1\' || type === \'人物\' || type === \'人\') addCard(\'character\');\n    else if (type === \'2\' || type === \'物品\' || type === \'物\') addCard(\'item\');\n    else if (type === \'3\' || type === \'地点\' || type === \'地\') addCard(\'location\');\n    else showToast(\'输入 1/2/3\');\n}'

new='// 卡片类型子菜单\nfunction addCardPrompt() {\n    var m = document.getElementById(\'card-menu\');\n    if (m) { m.remove(); return; }\n    m = document.createElement(\'div\');\n    m.id = \'card-menu\';\n    m.innerHTML = \'<button onclick="addCard(\\\'character\\\');closeCardMenu()"><span>👤</span>人物</button><button onclick="addCard(\\\'item\\\');closeCardMenu()"><span>📦</span>物品</button><button onclick="addCard(\\\'location\\\');closeCardMenu()"><span>📍</span>地点</button>\';\n    var btn = document.querySelector(\'.sidebar .btn-card\');\n    var rect = btn.getBoundingClientRect();\n    m.style.left = (rect.right + 4) + \'px\';\n    m.style.top = (rect.top - 4) + \'px\';\n    document.body.appendChild(m);\n    setTimeout(function() { document.addEventListener(\'click\', closeCardMenu); }, 10);\n}\nfunction closeCardMenu() {\n    var m = document.getElementById(\'card-menu\');\n    if (m) m.remove();\n    document.removeEventListener(\'click\', closeCardMenu);\n}'

c=c.replace(old,new)

# Add CSS for card menu
old_css='/* ======== 模态框 ======== */'
new_css='/* ======== 卡片子菜单 ======== */\n#card-menu {\n    position: fixed; z-index: 3000;\n    background: rgba(30,25,20,0.96);\n    border: 1px solid rgba(255,255,255,0.12);\n    border-radius: 8px;\n    padding: 4px;\n    display: flex; flex-direction: column; gap: 2px;\n    box-shadow: 0 8px 30px rgba(0,0,0,0.5);\n    backdrop-filter: blur(8px);\n}\n#card-menu button {\n    padding: 8px 16px; border: none; border-radius: 6px;\n    background: transparent; color: #ddd; font-size: 13px;\n    cursor: pointer; text-align: left;\n    display: flex; align-items: center; gap: 8px;\n    transition: background .1s;\n    font-family: inherit;\n}\n#card-menu button:hover { background: rgba(255,255,255,0.1); color: #fff; }\n#card-menu button span { font-size: 18px; }\n\n/* ======== 模态框 ======== */'
c=c.replace(old_css,new_css)

with open('static/index.html','w',encoding='utf-8') as f:
    f.write(c)
print('ok')
