Dim objWinHttp, objFSO, objShell, tempDir, extractDir, projectFolder, pythonExe, zipFile

' Criar instâncias dos objetos necessários
Set objWinHttp = CreateObject("WinHttp.WinHttpRequest.5.1")
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objShell = CreateObject("WScript.Shell")

' Definir diretórios temporários
tempDir = objFSO.GetSpecialFolder(2) ' Pasta temp do usuário
extractDir = tempDir & "\OnyConnect"
zipFile = tempDir & "\OnyConnect.zip"

' Baixar o repositório do GitHub como um arquivo ZIP
objWinHttp.Open "GET", "https://github.com/SayesCode/OnyConnect/archive/refs/heads/main.zip", False
objWinHttp.Send

' Salvar o conteúdo como um arquivo ZIP
If objWinHttp.Status = 200 Then
    Set objFile = objFSO.CreateTextFile(zipFile, True)
    objFile.Write(objWinHttp.ResponseBody)
    objFile.Close
End If

' Verificar se o arquivo ZIP foi baixado corretamente
If objFSO.FileExists(zipFile) Then
    ' Criar diretório de extração
    If Not objFSO.FolderExists(extractDir) Then
        objFSO.CreateFolder(extractDir)
    End If

    ' Descompactar o arquivo ZIP
    Set objShellApp = CreateObject("Shell.Application")
    objShellApp.NameSpace(extractDir).CopyHere objShellApp.NameSpace(zipFile).Items, 4

    ' Esperar o processo de extração terminar
    WScript.Sleep 5000
End If

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

' Navegar até o diretório do projeto
If objFSO.FolderExists(extractDir) Then
    Set projectFolder = objFSO.GetFolder(extractDir & "\OnyConnect-main")
End If

' Instalar as dependências do requirements.txt
If objFSO.FileExists(projectFolder.Path & "\requirements.txt") Then
    objShell.Run pythonExe & " -m pip install -r """ & projectFolder.Path & "\requirements.txt""", 1, True
End If

' Rodar o script Python
If objFSO.FolderExists(projectFolder.Path) Then
    ' Abrir a janela do terminal de forma visível e manter aberta
    objShell.Run "cmd /K """ & pythonExe & " """ & projectFolder.Path & "\main.py""", 1, True
End If
