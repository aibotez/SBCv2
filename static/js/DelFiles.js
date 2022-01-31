
function AckDel(ChoseFiles)
{
	//console.log(ChoseFiles);
	var urlpath = "/DelFiles/";
	var datas = {'data':ChoseFiles};
	var res = PostMethod(urlpath,JSON.stringify(datas),0);
	//console.log(res);
	var CurPath = document.getElementById("CurPath").innerText;
	var DelFilesDetails = document.getElementById("DelFilesDetails");
	DelFilesDetails.remove();
	RefreshFiles({'id':CurPath});
}

function CancelDel()
{
	var DelFilesDetails = document.getElementById("DelFilesDetails");
	DelFilesDetails.remove();
	//document.getElementById('DelFilesDetails').style.display = "none";
}

function DelFiles(files)
{
	
	//var files = {{data|safe}};
	var ChoseFiles = FindCheck(files);
    var ChoseFileLen = ChoseFiles.length;
	//console.log(ChoseFileLen);
    if (ChoseFileLen < 1)
       {return;}
	var bo = document.body;
	var div = document.createElement("div");
	div.id = "DelFilesDetails";
	div.style = "overflow:hidden;border-radius:10px;border:3px solid #ECF0F1;position:fixed;top:50%;left:50%;width:360px;height:200px;background-color:pink";
	
	var labeldiv = document.createElement("div");
	labeldiv.style = "width:100%;background-color:red";
	var label = document.createElement("label");
	label.style = "position:relative;left:20px;width:100%;font-size:15px;color:black;";
	label.innerText = "删除文件";
	labeldiv.appendChild(label);
	div.appendChild(labeldiv);
	
	var div_ = document.createElement("div");
	div_.style = "border-bottom:1px solid #CCC";
	div.appendChild(div_);
	
	var contentdiv = document.createElement("div");
	contentdiv.style="overflow-y: scroll;overflow-x:hidden;width:100%;height:70%;position:relative;left:20px;";
	var content = document.createElement("label");
	content.style="position:relative;left:0px";
	var s= "<br>是否要删除以下文件：<br><br>";
	for (var i=0;i<ChoseFileLen;i++)
	{
		s = s+ChoseFiles[i]['fename']+'<br>';
	}
	content.innerHTML = s;
	contentdiv.appendChild(content);
	
	var OperButtondiv = document.createElement("div");
	OperButtondiv.style = "position:relative;left:20px;";
	var AckButton = document.createElement("input");
	AckButton.type="Button";
	AckButton.style = "background-color:red;border-radius:5px;color:white";
	AckButton.value="确认删除";
	AckButton.onclick = function(){AckDel(ChoseFiles);};

	
	var CancelButton = document.createElement("input");
	CancelButton.type="Button";
	CancelButton.style="position:relative;left:30px;border-radius:5px;";
	CancelButton.value="取消";
	CancelButton.onclick = function(){CancelDel();};
	
	OperButtondiv.appendChild(AckButton);
	OperButtondiv.appendChild(CancelButton);
	
	
	
	div.appendChild(contentdiv);
	div.appendChild(OperButtondiv);
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