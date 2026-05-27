import os
os.chdir(os.path.dirname(__file__))
with open('static/index.html','r',encoding='utf-8') as f:
    c=f.read()

# 1. Add rename button in board item template
old='<button class="btn-danger" style="padding:4px 10px;font-size:12px;">删除</button>'
new='<button class="btn-action" style="padding:4px 8px;font-size:11px;">✏️</button>\n                    <button class="btn-danger" style="padding:4px 10px;font-size:12px;">删除</button>'
c=c.replace(old,new)

# 2. Add rename click handler (after the delete handler)
old_click='item.querySelector(\'.actions button:last-child\').addEventListener(\'click\', async (e) => {'
new_click='// 重命名\n            item.querySelector(\'.actions button:nth-child(2)\').addEventListener(\'click\', async (e) => {\n                e.stopPropagation();\n                var newName = prompt(\'新名称：\', b.name);\n                if (!newName || newName === b.name) return;\n                await fetch(\'/api/boards/\' + encodeURIComponent(b.name), { method: \'GET\' });\n                var data = await resp;\n                // Actually we need to fetch data first, then save with new name, delete old\n                var r = await fetch(\'/api/boards/\' + encodeURIComponent(b.name));\n                var d = await r.json();\n                d.name = newName;\n                await fetch(\'/api/boards/\' + encodeURIComponent(newName), { method: \'POST\', headers: { \'Content-Type\': \'application/json\' }, body: JSON.stringify(d) });\n                await fetch(\'/api/boards/\' + encodeURIComponent(b.name), { method: \'DELETE\' });\n                showLoadModal();\n            });\n            item.querySelector(\'.actions button:last-child\').addEventListener(\'click\', async (e) => {'
c=c.replace(old_click,new_click)

with open('static/index.html','w',encoding='utf-8') as f:
    f.write(c)
print('ok')
