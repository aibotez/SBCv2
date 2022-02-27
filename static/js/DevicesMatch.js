


Match();
function Match()
{
	
	//alert(document.documentElement.style.fontSize);
	var ScWidth = document.documentElement.clientWidth;
	var ScHeight = document.documentElement.clientHeight;


	if(ScHeight>ScWidth)
	{
		//竖版
		document.documentElement.style.fontSize = ScWidth/60+'px';
		document.getElementById("div1").style.display="none";
		document.getElementById("HightModeMenu").style.display="";
		//document.getElementById("FileLabel").style.width = "1000px";
		document.getElementById("ShowMain").style.width = "100%";
		document.getElementById("ShowMain").style.height = ScHeight-100-0.03*ScHeight+"px";
		//document.getElementById("FilesData").style.width = ScWidth+"px";
		//console.log(ScWidth);
		
		
	}
	else
	{
		document.documentElement.style.fontSize = ScWidth/90+'px';
		document.getElementById("div1").style.display="";
		document.getElementById("HightModeMenu").style.display="none";
		//document.getElementById("ShowMain").style.height = "100%";
	}
	
}