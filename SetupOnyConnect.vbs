Dim objXMLHttp, objFSO, objShell, tempDir, extractDir, projectFolder, pythonExe

' Criar instâncias dos objetos necessários
Set objXMLHttp = CreateObject("MSXML2.XMLHTTP")
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objShell = CreateObject("WScript.Shell")

' Definir diretórios temporários
tempDir = objFSO.GetSpecialFolder(2) ' Pasta temp do usuário
extractDir = tempDir & "\OnyConnect"

' Baixar o repositório do GitHub diretamente (sem zip)
objXMLHttp.Open "GET", "https://github.com/SayesCode/OnyConnect", False
objXMLHttp.Send

' Salvar o conteúdo da resposta diretamente em uma pasta (não um arquivo zip)
If objXMLHttp.Status = 200 Then
    ' Criar diretório de extração
    If Not objFSO.FolderExists(extractDir) Then
        objFSO.CreateFolder(extractDir)
    End If

    ' Definir o nome do arquivo de saída (por exemplo, uma pasta ou arquivo em vez de ZIP)
    ' Dependendo da implementação, aqui você pode manipular os arquivos conforme necessário
    ' Exemplo: salvar os arquivos diretamente (sem usar ZIP)
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
    Set projectFolder = objFSO.GetFolder(extractDir)
End If

' Instalar as dependências do requirements.txt
If objFSO.FileExists(projectFolder.Path & "\requirements.txt") Then
    objShell.Run pythonExe & " -m pip install -r """ & projectFolder.Path & "\requirements.txt""", 1, True
End If

' Rodar o script Python
If objFSO.FolderExists(projectFolder.Path) Then
    objShell.Run pythonExe & " """ & projectFolder.Path & "\main.py""", 1, True
End If
