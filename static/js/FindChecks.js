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
			filepath = Base64.decode(file)
			//console.log(file);
			Res.push({'fename':filename,'fepath':filepath,'feisdir':feisdir,'fileId':file});
		}
		
	}
	return Res;
}