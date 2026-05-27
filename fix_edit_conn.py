import os
os.chdir(os.path.dirname(__file__))
with open('static/index.html','r',encoding='utf-8') as f:
    c=f.read()

# Fix editConnectionLabel - remove references to missing elements
old='function editConnectionLabel(conn) {\n    _editConnId = conn.id;\n    document.getElementById(\'conn-name\').value = conn.label || \'\';\n    document.getElementById(\'conn-fontsize\').value = conn.fontSize || 14;\n    // arrow type handled by set buttons\n    document.getElementById(\'conn-modal\').classList.add(\'active\');\n}'
new='function editConnectionLabel(conn) {\n    _editConnId = conn.id;\n    var m = document.getElementById(\'conn-menu\');\n    document.getElementById(\'conn-name\').value = conn.label || \'\';\n    [\'none\',\'single\',\'double\'].forEach(function(t) {\n        var btn = document.getElementById(\'conn-arrow-\' + t);\n        if (conn.arrowType === t) { btn.style.background = \'#d4a87a\'; btn.style.color = \'#1a1510\'; }\n        else { btn.style.background = \'rgba(255,255,255,0.06)\'; btn.style.color = \'#aaa\'; }\n    });\n    var from = getPinPos(conn.fromId);\n    var to = getPinPos(conn.toId);\n    var mx = (from.x + to.x) / 2, my = (from.y + to.y) / 2;\n    var rect = container.getBoundingClientRect();\n    var sx = mx * state.scale + state.panX + rect.left;\n    var sy = my * state.scale + state.panY + rect.top;\n    m.style.left = Math.min(sx, window.innerWidth - 180) + \'px\';\n    m.style.top = Math.min(sy, window.innerHeight - 160) + \'px\';\n    m.style.display = \'block\';\n    setTimeout(function() { document.addEventListener(\'click\', closeConnMenu); }, 10);\n}'
c=c.replace(old,new)

with open('static/index.html','w',encoding='utf-8') as f:
    f.write(c)
print('ok')
