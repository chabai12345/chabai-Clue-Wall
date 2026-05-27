import os
os.chdir(os.path.dirname(__file__))
with open('static/index.html','r',encoding='utf-8') as f:
    c=f.read()

# Clean up the rename code - remove the dead GET line and resp line
old='await fetch(\'/api/boards/\' + encodeURIComponent(b.name), { method: \'GET\' });\n                var data = await resp;\n                // Actually we need to fetch data first, then save with new name, delete old\n                var r'
new='var r'
c=c.replace(old,new)

with open('static/index.html','w',encoding='utf-8') as f:
    f.write(c)
print('ok')
