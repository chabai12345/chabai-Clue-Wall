Set fso = CreateObject("Scripting.FileSystemObject")
Set file = fso.OpenTextFile("static/index.html", 1)
content = file.ReadAll
file.Close

' Fix renderConnection - remove bad injected lines
old = "    const from = getPinPos(conn.fromId);" & vbCrLf & _
      "    const to = getPinPos(conn.toId);" & vbCrLf & _
      "    const cp = getConnControlPos(conn);" & vbCrLf & _
      "" & vbCrLf & _
      "    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');" & vbCrLf & _
      "    path.dataset.id = conn.id;" & vbCrLf & _
      "    const to = getPinPos(conn.toId);" & vbCrLf & _
      "" & vbCrLf & _
      "    const to = getPinPos(conn.toId);" & vbCrLf & _
      "    const to = getPinPos(conn.toId);"

new_ = "    const from = getPinPos(conn.fromId);" & vbCrLf & _
       "    const to = getPinPos(conn.toId);" & vbCrLf & _
       "    const cp = getConnControlPos(conn);"

pos = InStr(content, old)
If pos > 0 Then
    content = Left(content, pos-1) & new_ & Mid(content, pos + Len(old))
End If

Set out = fso.OpenTextFile("static/index.html", 2, False)
out.Write content
out.Close

WScript.Echo "Fixed!"
