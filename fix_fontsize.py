import os
os.chdir(os.path.dirname(__file__))
with open('static/index.html','r',encoding='utf-8') as f:
    c=f.read()

# Add font size input before the save/delete buttons
old='<div style="display:flex;gap:3px;">\n        <button onclick="saveConnDetail()" style="padding:4px 12px;border:none;border-radius:4px;font-size:11px;cursor:pointer;background:#d4a87a;color:#1a1510;font-family:inherit;">💾</button>\n        <button onclick="deleteConn()" style="padding:4px 12px;border:none;border-radius:4px;font-size:11px;cursor:pointer;background:rgba(255,80,80,0.15);color:#ff6b6b;font-family:inherit;">🗑️</button>\n    </div>'
new='<div style="display:flex;gap:4px;margin-bottom:6px;align-items:center;">\n        <input id="conn-fontsize" type="number" value="14" min="10" max="30" style="width:50px;padding:3px 4px;border-radius:4px;border:1px solid rgba(255,255,255,0.12);background:rgba(255,255,255,0.06);color:#eee;font-size:11px;outline:none;text-align:center;">\n        <span style="color:#888;font-size:10px;">字号</span>\n    </div>\n    <div style="display:flex;gap:3px;">\n        <button onclick="saveConnDetail()" style="padding:4px 12px;border:none;border-radius:4px;font-size:11px;cursor:pointer;background:#d4a87a;color:#1a1510;font-family:inherit;">💾</button>\n        <button onclick="deleteConn()" style="padding:4px 12px;border:none;border-radius:4px;font-size:11px;cursor:pointer;background:rgba(255,80,80,0.15);color:#ff6b6b;font-family:inherit;">🗑️</button>\n    </div>'
c=c.replace(old,new)

with open('static/index.html','w',encoding='utf-8') as f:
    f.write(c)
print('ok')
