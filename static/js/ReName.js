function Rename(files)
{
	var ChoseFiles = FindCheck(files);
    var ChoseFileLen = ChoseFiles.length;
	//console.log(ChoseFileLen);
    if (ChoseFileLen < 1)
       {return;}
    var ChoseFile = ChoseFiles[0];
	
    //console.log(ChoseFile);
	var ChoseFileid = ChoseFile["fepath"];
	//document.getElementById(ChoseFileid+"Choseboxone").disabled="disabled";
	var SureButtonid = document.getElementById(ChoseFileid+"ReNameSure");
	var CancelButtonid = document.getElementById(ChoseFileid+"ReNameCancel");
	document.getElementById(ChoseFileid).style.display="none";
	document.getElementById(ChoseFileid+"ReName").style.display="";
	
	SureButtonid.style = "margin-left:3px;cursor:pointer;background-image: url(/static/img/Sure.jpg);width:20px;height:20px;background-size:20px 20px; border:0;";
	CancelButtonid.style = "margin-left:3px;cursor:pointer;background-image: url(/static/img/Cancel.jpg);width:20px;height:20px;background-size:20px 20px; border:0;";
}
function ReNameCancel(act)
{
	var ChoseFileid = act.name;
		document.getElementById(ChoseFileid).style.display="";
	document.getElementById(ChoseFileid+"ReName").style.display="none";
}
function ReNameAct(act)
{
	if (act.id.indexOf("ReNameCancel") != -1)
	{
		//console.log(act.id);
		return;
	}
	var ReNamePath = act.name;
	var ReNameTextid = act.name+"ReNameText";
	var NewName = document.getElementById(ReNameTextid).value;
	//console.log(NewName);
	var OldNamePath = act.name;
	
	data={
		'OldNamePath':OldNamePath,
		'NewName':NewName,
	}
	var res = PostMethod("/ReName/",data,0);

	
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