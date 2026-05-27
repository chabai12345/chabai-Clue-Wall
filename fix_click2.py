import os
os.chdir(os.path.dirname(__file__))
with open('static/index.html','r',encoding='utf-8') as f:
    c=f.read()
old='// 单击连线 → 编辑命名 或 切断（已整合）\n    path.addEventListener(\'click\', (e) => {\n        e.stopPropagation();\n        editConnectionLabel(conn);\n    });\n\n    // 单击连线 → 编辑命名 或 切断\n    path.addEventListener(\'click\', (e) => {\n        e.stopPropagation();\n        if (state.cutMode) {\n            removeConnection(conn.id);\n            showToast(\'✂️ 已切断\');\n        } else {\n            editConnectionLabel(conn);\n        }\n    });'
new='// 单击连线 → 编辑命名 或 切断\n    path.addEventListener(\'click\', (e) => {\n        e.stopPropagation();\n        if (state.cutMode) {\n            removeConnection(conn.id);\n            showToast(\'✂️ 已切断\');\n        } else {\n            editConnectionLabel(conn);\n        }\n    });'
c=c.replace(old,new)
with open('static/index.html','w',encoding='utf-8') as f:
    f.write(c)
print('ok')
