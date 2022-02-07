
function Ack()
{}
function Cancel()
{}

function NewFolder()
{
	var CurPath = document.getElementById("CurPath").innerText;
	var bo = document.body;
	var NFdiv = document.createElement("div");
	NFdiv.style="background-color:white;position: fixed;border-radius:10px;border:3px solid #ECF0F1;top:30%;left:40%;width:340px;height:336px;";
	
	var labeldiv = document.createElement("div");
	labeldiv.style = "width:100%;";
	var label = document.createElement("label");
	label.style = "position:relative;left:20px;width:100%;font-size:20px;color:black;";
	label.innerText = "新建文件夹";
	labeldiv.appendChild(label);
	NFdiv.appendChild(labeldiv);
	
	var div_ = document.createElement("div");
	div_.style = "border-bottom:1px solid #CCC";
	div.appendChild(div_);
	
	var imgdiv = document.createElement("div");
	imgdiv.style = "position:relative;top:10px;left:100px;height:35%;width:35%;";
	var img = document.createElement("img");
	img.src = "/static/img/folder.png";
	img.style="height:100%;width:100%;";
	imgdiv.appendChild(img);
	
	var inputdiv = document.createElement("div");
	inputdiv.style = "position:relative;top:200px;left:30px;height:28px;width:80%;";
	var input = document.createElement("input");
	input.type="text";
	input.value="新建文件夹";
	input.style = "font-size:18px;border-radius:5px;border:0;position:relative;height:100%;width:100%;background-color:#B2BABB";
	inputdiv.appendChild(input);
	
	var OperButtondiv = document.createElement("div");
	OperButtondiv.style = "position:relative;left:30px;top:270px";
	var AckButton = document.createElement("input");
	AckButton.type="Button";
	AckButton.style = "cursor:pointer;border-radius:5px;height:30px;";
	AckButton.value="确 认";
	AckButton.onclick = function(){Ack();};

	
	var CancelButton = document.createElement("input");
	CancelButton.type="Button";
	CancelButton.style="cursor:pointer;position:relative;left:30px;border-radius:5px;height:30px;";
	CancelButton.value="取 消";
	CancelButton.onclick = function(){Cancel();};
	
	OperButtondiv.appendChild(AckButton);
	OperButtondiv.appendChild(CancelButton);
	
	

	NFdiv.appendChild(OperButtondiv);
	NFdiv.appendChild(inputdiv);
	NFdiv.appendChild(imgdiv);
	bo.appendChild(NFdiv);
	bo.style="background-color:#E5E7E9";
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