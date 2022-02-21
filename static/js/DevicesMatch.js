


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
		document.getElementById("ShowMain").style.width = "100%";
		
	}
	else
	{
		document.documentElement.style.fontSize = ScWidth/90+'px';
		document.getElementById("div1").style.display="";
		document.getElementById("HightModeMenu").style.display="none";
	}
	
}