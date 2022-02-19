

function SBCShare()
{
	var menudropdown_content = document.getElementById("menudropdown-content");
	menudropdown_content.style.display = "none";
	var files = Window.globalConfig.GlobalFiles;
	var ChoseFiles = FindCheck(files);
    var ChoseFileLen = ChoseFiles.length;
	//console.log(ChoseFileLen);
    if (ChoseFileLen < 1)
       {return;}
    var bo = document.body;
	bo.style="background-color:#E5E7E9";
	var div = document.createElement("div");
	div.id = "DelFilesDetails";
	div.style = "background-color:white;overflow:hidden;border-radius:10px;border:3px solid #ECF0F1;position:fixed;top:10%;left:20%;width:500px;height:500px;";
	
	var labeldiv = document.createElement("div");
	labeldiv.style = "width:100%;";
	var label = document.createElement("label");
	label.style = "position:relative;top:10px;left:20px;width:100%;font-size:20px;color:black;";
	label.innerText = "分享文件";
	labeldiv.appendChild(label);
	div.appendChild(labeldiv);
	
	var Sharlabel = document.createElement("label");
	Sharlabel.innerHTML = "<br>是否要分享以下文件：<br><br>";
	Sharlabel.style = "position:relative;left:20px;width:100%;font-size:20px;color:black;";
	div.appendChild(Sharlabel);
	
	var contentdiv = document.createElement("div");
	contentdiv.style="overflow-y: scroll;overflow-x:hidden;width:100%;height:40%;position:relative;left:20px;";
	var content = document.createElement("label");
	content.style="position:relative;left:0px";
	var s= "";
	for (var i=0;i<ChoseFileLen;i++)
	{
		s = s+ChoseFiles[i]['fename']+'<br>';
	}
	content.innerHTML = s;
	contentdiv.appendChild(content);
	
	
	
	
	div.appendChild(contentdiv);
	bo.appendChild(div);
	
	
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