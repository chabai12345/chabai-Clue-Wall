import os
os.chdir(os.path.dirname(__file__))
with open('static/index.html','r',encoding='utf-8') as f:
    c=f.read()

# Fix board-container: remove the duplicate background lines, keep light yellow
old='    overflow: hidden; cursor: grab;\n    background: #f5e6c8;\n    /* 软木板纹理 */\n    background: transparent;\n    background-image:\n        radial-gradient(circle at 10% 20%, rgba(0,0,0,0.04) 1px, transparent 1px),\n        radial-gradient(circle at 30% 70%, rgba(0,0,0,0.03) 1px, transparent 1px),\n        radial-gradient(circle at 50% 30%, rgba(0,0,0,0.05) 1px, transparent 1px),\n        radial-gradient(circle at 70% 80%, rgba(0,0,0,0.03) 1px, transparent 1px),\n        radial-gradient(circle at 90% 10%, rgba(0,0,0,0.04) 1px, transparent 1px);\n    background-size: 200px 200px;'
new='    overflow: hidden; cursor: grab;\n    background: #b8895e;\n    background-image:\n        radial-gradient(circle at 10% 20%, rgba(0,0,0,0.04) 1px, transparent 1px),\n        radial-gradient(circle at 30% 70%, rgba(0,0,0,0.03) 1px, transparent 1px),\n        radial-gradient(circle at 50% 30%, rgba(0,0,0,0.05) 1px, transparent 1px),\n        radial-gradient(circle at 70% 80%, rgba(0,0,0,0.03) 1px, transparent 1px),\n        radial-gradient(circle at 90% 10%, rgba(0,0,0,0.04) 1px, transparent 1px);\n    background-size: 200px 200px;'
c=c.replace(old,new)

# Add light yellow to #board itself (the transformable canvas)
old='#board {\n    position: absolute; top: 0; left: 0;\n    transform-origin: 0 0;\n}'
new='#board {\n    position: absolute; top: 0; left: 0;\n    transform-origin: 0 0;\n    min-width: 100%; min-height: 100%;\n    background: #f5e6c8;\n}'
c=c.replace(old,new)

# Fix card-image - remove the mistakenly added background
old='.card .card-image {\n    flex: 1; width: 100%; min-height: 80px;\n    display: flex; flex-direction: column;\n    overflow: hidden; cursor: grab;\n    background: #f5e6c8;\n}'
new='.card .card-image {\n    flex: 1; width: 100%; min-height: 80px;\n    display: flex; flex-direction: column;\n    overflow: hidden; cursor: grab;\n}'
c=c.replace(old,new)

# Remove the SVG red outline
c=c.replace('#svg-layer { outline: 1px solid red; }\n', '')

with open('static/index.html','w',encoding='utf-8') as f:
    f.write(c)
print('ok')
