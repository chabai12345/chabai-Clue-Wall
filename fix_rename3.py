import os
os.chdir(os.path.dirname(__file__))
with open('static/index.html','r',encoding='utf-8') as f:
    c=f.read()

# 1. Add rename button in board item
old='<button class="btn-primary" style="padding:4px 12px;font-size:12px;">读取</button>\n                    <button class="btn-danger" style="padding:4px 10px;font-size:12px;">删除</button>'
new='<button class="btn-primary" style="padding:4px 12px;font-size:12px;">读取</button>\n                    <button class="btn-action" style="padding:4px 8px;font-size:11px;color:#d4a87a;">重命名</button>\n                    <button class="btn-danger" style="padding:4px 10px;font-size:12px;">删除</button>'
c=c.replace(old,new)
print(f'replace 1: {old in c}')  # should be False now

# 2. Add handler for rename and update delete handler indexing
old2='item.querySelector(\'.actions button:last-child\').addEventListener(\'click\', async (e) => {\n                e.stopPropagation();\n                if (!confirm(`删除「${b.name}」？`)) return;\n                await fetch(\'/api/boards/\' + encodeURIComponent(b.name), { method: \'DELETE\' });\n                showLoadModal();'
new2='// 重命名\n            item.querySelector(\'.actions button:nth-child(2)\').addEventListener(\'click\', (e) => {\n                e.stopPropagation();\n                var nn = prompt(\'新名称：\', b.name);\n                if (!nn || nn === b.name) return;\n                fetch(\'/api/boards/\' + encodeURIComponent(b.name)).then(function(r) { return r.json(); }).then(function(d) {\n                    d.name = nn;\n                    fetch(\'/api/boards/\' + encodeURIComponent(nn), { method: \'POST\', headers: { \'Content-Type\': \'application/json\' }, body: JSON.stringify(d) }).then(function() {\n                        fetch(\'/api/boards/\' + encodeURIComponent(b.name), { method: \'DELETE\' }).then(function() { showLoadModal(); });\n                    });\n                });\n            });\n            item.querySelector(\'.actions button:last-child\').addEventListener(\'click\', async (e) => {\n                e.stopPropagation();\n                if (!confirm(`删除「${b.name}」？`)) return;\n                await fetch(\'/api/boards/\' + encodeURIComponent(b.name), { method: \'DELETE\' });\n                showLoadModal();'
c=c.replace(old2,new2)

with open('static/index.html','w',encoding='utf-8') as f:
    f.write(c)
print('ok')
