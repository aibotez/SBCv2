function FindCheck(files)
{
	//var files = {{data|safe}};
	var Res = [];
	for (var i=0;i<files.length;i++)
	{
		file = files[i].filelj;
		if (document.getElementById(file+"Choseboxone").checked==true)
		{
			filename = files[i].filename;
			feisdir =files[i].isdir;
			Res.push({'fename':filename,'fepath':file,'feisdir':feisdir});
		}
		
	}
	return Res;
}