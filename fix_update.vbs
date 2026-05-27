Set fso = CreateObject("Scripting.FileSystemObject")
Set file = fso.OpenTextFile("static/index.html", 1)
content = file.ReadAll
file.Close

' Fix updateConnection - remove bad injected lines
' The bad pattern is:
'     const cp = getConnControlPos(conn);
'     
'     const path = document.createElementNS(...)
'     path.dataset.id = conn.id;
'     const to = getPinPos(conn.toId);
'     
'     const to = getPinPos(conn.toId);
'     const to = getPinPos(conn.toId);

old = "    const cp = getConnControlPos(conn);" & vbCrLf & _
      "" & vbCrLf & _
      "    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');" & vbCrLf & _
      "    path.dataset.id = conn.id;" & vbCrLf & _
      "    const to = getPinPos(conn.toId);" & vbCrLf & _
      "" & vbCrLf & _
      "    const to = getPinPos(conn.toId);" & vbCrLf & _
      "    const to = getPinPos(conn.toId);"

new_ = "    const cp = getConnControlPos(conn);"

' Replace only first occurrence (in updateConnection)
pos = InStr(content, old)
If pos > 0 Then
    content = Left(content, pos-1) & new_ & Mid(content, pos + Len(old))
End If

Set out = fso.OpenTextFile("static/index.html", 2, False)
out.Write content
out.Close

WScript.Echo "Fixed!"
