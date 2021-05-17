'#Language "WWB-COM"

Option Explicit

Sub Main
	Debug.Clear
	Dim app As Object
	Set app = CreateObject("CSTStudio.Application")
	Dim projectFilePath As String
	projectFilePath = GetFilePath$()
	Dim projectFileStatus As Boolean
	projectFileStatus = FileExists(projectFilePath)
	Dim project As Object

	If projectFileStatus = False Then
		Debug.Print("Could not find CST project file: " + projectFilePath)
		Exit All
	Else
		Debug.Print("Found " + projectFilePath)
	End If

	Set project = app.OpenFile(projectFilePath)

	Dim res1 As Object
	Set res1 = Result3D("^AC1")
	Debug.Print("AC1 Dimension: "+ res1.GetNx + ", " + res1.GetNy + ", " + res1.GetNz)
End Sub

Function FileExists(FilePath As String) As Boolean
	If Dir(FilePath) = "" Then
		FileExists = False
	Else
		FileExists = True
	End If
End Function
