function Rename(files)
{
	var ChoseFiles = FindCheck(files);
    var ChoseFileLen = ChoseFiles.length;
	//console.log(ChoseFileLen);
    if (ChoseFileLen < 1)
       {return;}
    var ChoseFile = ChoseFiles[0];
    console.log(ChoseFile);
	
}


function FindCheck(files)
{
	//var files = {{data|safe}};
	var Res = [];
	for (var i=0;i<files.length;i++)
	{
		file = files[i].filelj;
		if (document.getElementsByName(file)[0].checked==true)
		{
			filename = files[i].filename;
			feisdir =files[i].isdir;
			Res.push({'fename':filename,'fepath':file,'feisdir':feisdir});
		}
		
	}
	return Res;
}