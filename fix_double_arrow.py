import os
os.chdir(os.path.dirname(__file__))
with open('static/index.html','r',encoding='utf-8') as f:
    c=f.read()

# Add arrowhead-start marker
old='<marker id="arrowhead" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto">\n                <path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke"/>\n            </marker>'
new='<marker id="arrowhead" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto">\n                <path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke"/>\n            </marker>\n            <marker id="arrowhead-rev" viewBox="0 0 10 10" refX="0" refY="5" markerWidth="8" markerHeight="8" orient="auto">\n                <path d="M 10 0 L 0 5 L 10 10 z" fill="context-stroke"/>\n            </marker>'
c=c.replace(old,new)

# Use reversed marker for start
c=c.replace("path.setAttribute('marker-start', 'url(#arrowhead)')", "path.setAttribute('marker-start', 'url(#arrowhead-rev)')")

with open('static/index.html','w',encoding='utf-8') as f:
    f.write(c)
print('ok')
