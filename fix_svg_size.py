import os
os.chdir(os.path.dirname(__file__))
with open('static/index.html','r',encoding='utf-8') as f:
    c=f.read()

old = '''function updateSvgSize() {
    // expand SVG to cover board content
    let maxX = 2000, maxY = 2000;
    state.cards.forEach(c => {
        if (c.x + 300 > maxX) maxX = c.x + 300;
        if (c.y + 200 > maxY) maxY = c.y + 200;
    });
    svg.setAttribute('width', maxX);
    svg.setAttribute('height', maxY);
    svg.style.width = maxX + 'px';
    svg.style.height = maxY + 'px';
}'''

new = '''function updateSvgSize() {
    // expand SVG to cover cards + connections
    let maxX = 2000, maxY = 2000;
    state.cards.forEach(c => {
        if (c.x + 300 > maxX) maxX = c.x + 300;
        if (c.y + 200 > maxY) maxY = c.y + 200;
    });
    state.connections.forEach(cn => {
        var f = getPinPos(cn.fromId), t = getPinPos(cn.toId);
        var cp = getConnControlPos(cn);
        var pts = [f, t, cp];
        pts.forEach(function(p) {
            if (p.x + 50 > maxX) maxX = p.x + 50;
            if (p.y + 50 > maxY) maxY = p.y + 50;
        });
    });
    svg.setAttribute('width', maxX);
    svg.setAttribute('height', maxY);
    svg.style.width = maxX + 'px';
    svg.style.height = maxY + 'px';
}'''

c=c.replace(old, new)

with open('static/index.html','w',encoding='utf-8') as f:
    f.write(c)
print('ok')
