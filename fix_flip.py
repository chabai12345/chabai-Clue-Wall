import os
os.chdir(os.path.dirname(__file__))
with open('static/index.html','r',encoding='utf-8') as f:
    c=f.read()

# board-container: light yellow solid
old='#board-container {\n    position: fixed; top: 0; left: 64px; right: 0; bottom: 0;\n    overflow: hidden; cursor: grab;\n    background: #b8895e;\n    background-image:\n        radial-gradient(circle at 10% 20%, rgba(0,0,0,0.04) 1px, transparent 1px),\n        radial-gradient(circle at 30% 70%, rgba(0,0,0,0.03) 1px, transparent 1px),\n        radial-gradient(circle at 50% 30%, rgba(0,0,0,0.05) 1px, transparent 1px),\n        radial-gradient(circle at 70% 80%, rgba(0,0,0,0.03) 1px, transparent 1px),\n        radial-gradient(circle at 90% 10%, rgba(0,0,0,0.04) 1px, transparent 1px);\n    background-size: 200px 200px;'
new='#board-container {\n    position: fixed; top: 0; left: 64px; right: 0; bottom: 0;\n    overflow: hidden; cursor: grab;\n    background: #f5e6c8;'
c=c.replace(old,new)

# board: brown corkboard (with texture)
old='#board {\n    position: absolute; top: 0; left: 0;\n    transform-origin: 0 0;\n    min-width: 200%; min-height: 200%;\n    background: #b8895e;\n}'
new='#board {\n    position: absolute; top: 0; left: 0;\n    transform-origin: 0 0;\n    min-width: 200%; min-height: 200%;\n    background-color: #b8895e;\n    background-image:\n        radial-gradient(circle at 10% 20%, rgba(0,0,0,0.04) 1px, transparent 1px),\n        radial-gradient(circle at 30% 70%, rgba(0,0,0,0.03) 1px, transparent 1px),\n        radial-gradient(circle at 50% 30%, rgba(0,0,0,0.05) 1px, transparent 1px),\n        radial-gradient(circle at 70% 80%, rgba(0,0,0,0.03) 1px, transparent 1px),\n        radial-gradient(circle at 90% 10%, rgba(0,0,0,0.04) 1px, transparent 1px);\n    background-size: 200px 200px;\n}'
c=c.replace(old,new)

with open('static/index.html','w',encoding='utf-8') as f:
    f.write(c)
print('ok')
