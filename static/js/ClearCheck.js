function ClearCheck()
{
	var files = Window.globalConfig.GlobalFiles;
	var Res = [];
	for (var i=0;i<files.length;i++)
	{
		file = files[i].filelj;
		if (document.getElementById(file+"Choseboxone").checked==true)
		{
			document.getElementById(file+"Choseboxone").checked = false;
		}
		
	}
	return Res;
}