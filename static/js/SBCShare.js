
var ShareFileInfo = [];

function FinshShare()
{
	CancelShare();
}

function SureShare()
{
	var ShareFeDateDur = document.getElementById("SharemenudropdownB").innerHTML;
	var SharePass = document.getElementById("SharePass").value;
	postdata={
		'ShareFile':ShareFileInfo,
		'ShareDateDur':ShareFeDateDur,
		'SharePass':SharePass
	}
	var urlpath = "/CreatShareFile/";
	var jsondata = JSON.stringify(postdata);
	var res = PostMethod(urlpath,jsondata,0);
	//CancelShare();
	console.log(res);
	document.getElementById("ShareUrlContent").innerHTML=res.res;
	var div = document.getElementById("ShareFiles");
	div.style.height = "300px";
	document.getElementById("ShareSetShow").style.display="none";
	document.getElementById("ShareUrlShow").style.display="";
	//var SSureButtonid = document.getElementById("ShareFilesUrlbutton");
	//SSureButtonid.style = "position:relative;top:1px;border-radius:5px;cursor:pointer;background-image: url(/static/img/Sure.jpg);width:24px;height:24px;background-size:24px 24px; border:0;";

}
function CancelShare()
{
	var bo = document.body;
	bo.style="background-color:white";
	document.getElementById("ShareFiles").style.display="none";
}

function SBCShare()
{
	var menudropdown_content = document.getElementById("menudropdown-content");
	document.getElementById("ShareUrlShow").style.display="none";
	document.getElementById("ShareSetShow").style.display="";
	menudropdown_content.style.display = "none";
	var files = Window.globalConfig.GlobalFiles;
	var ChoseFiles = FindCheck(files);
    var ChoseFileLen = ChoseFiles.length;
	//console.log(ChoseFileLen);
    if (ChoseFileLen < 1)
       {return;}
	ShareFileInfo = ChoseFiles;
    var bo = document.body;
	bo.style="background-color:#E5E7E9";
	
	var div = document.getElementById("ShareFiles");
	div.style.height = "500px";
	var content = document.getElementById("ShareContentDetails");
	var s= "";
	for (var i=0;i<ChoseFileLen;i++)
	{
		s = s+ChoseFiles[i]['fename']+'<br>';
	}
	content.innerHTML = s;
	div.style.display = "";
	
	

	
	
}
function ShareDuring(dataDur)
{
	var Sharemenudropdown_content = document.getElementById("Sharemenudropdown-content");
	Sharemenudropdown_content.style.display = "none";
	if (dataDur ==1)
	{
		FeDataDur = "1天";
	}
	else if (dataDur ==2)
	{
		FeDataDur = "7天";
	}
	else if (dataDur ==3)
	{
		FeDataDur = "1个月";
	}
	else
	{
		FeDataDur = "永久";
	}
	document.getElementById("SharemenudropdownB").innerHTML = FeDataDur;

}
