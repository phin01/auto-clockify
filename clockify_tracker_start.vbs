Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c pythonw gui.py"
oShell.Run strArgs, 0, false