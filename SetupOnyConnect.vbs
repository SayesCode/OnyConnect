Dim objXMLHttp, objFSO, objShell, zipFile, tempDir, extractDir, pythonInstalled, projectFolder, pythonExe

' Criar instâncias dos objetos necessários
Set objXMLHttp = CreateObject("MSXML2.XMLHTTP")
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objShell = CreateObject("WScript.Shell")

' Definir diretórios temporários
tempDir = objFSO.GetSpecialFolder(2) ' Pasta temp do usuário
zipFile = tempDir & "\OnyConnect.zip"
extractDir = tempDir & "\OnyConnect"

' Baixar o arquivo ZIP do repositório GitHub
objXMLHttp.Open "GET", "https://github.com/SayesCode/OnyConnect/archive/refs/heads/main.zip", False
objXMLHttp.Send

' Salvar o conteúdo do ZIP no diretório temporário
If objXMLHttp.Status = 200 Then
    Set objFile = objFSO.CreateTextFile(zipFile, True)
    objFile.Write objXMLHttp.responseBody
    objFile.Close
End If

' Extrair o conteúdo do arquivo ZIP
Set objShell = CreateObject("Shell.Application")
objShell.NameSpace(extractDir).CopyHere objShell.NameSpace(zipFile).Items

' Aguardar a extração do ZIP
WScript.Sleep 5000

' Verificar se o Python está instalado
On Error Resume Next
Set pythonInstalled = objShell.Exec("python --version")
If Err.Number <> 0 Then
    ' Instalar o Python caso não esteja instalado
    objShell.Run "msiexec /i https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe /quiet InstallAllUsers=1 PrependPath=1"
    WScript.Sleep 10000 ' Esperar o Python ser instalado
End If
On Error GoTo 0

' Definir caminho do executável do Python
pythonExe = "python"

' Navegar até o diretório do projeto extraído
Set objFSO = CreateObject("Scripting.FileSystemObject")
If objFSO.FolderExists(extractDir) Then
    Set projectFolder = objFSO.GetFolder(extractDir)
    For Each subFolder In projectFolder.Subfolders
        If subFolder.Name = "OnyConnect" Then
            Set projectFolder = subFolder
            Exit For
        End If
    Next
End If

' Instalar as dependências do requirements.txt
If objFSO.FileExists(projectFolder.Path & "\requirements.txt") Then
    objShell.Run pythonExe & " -m pip install -r """ & projectFolder.Path & "\requirements.txt""", 1, True
End If

objShell.Run "cls", 0, True

' Rodar o script Python
If objFSO.FolderExists(projectFolder.Path) Then
    objShell.Run pythonExe & " """ & projectFolder.Path & "\main.py""", 1, True
End If
