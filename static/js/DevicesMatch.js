


Match();
function Match()
{
	
	//alert(document.documentElement.style.fontSize);
	var ScWidth = document.documentElement.clientWidth;
	var ScHeight = document.documentElement.clientHeight;
	
	let DPi = js_getDPI();

	let dpiperrem = 0;
	if(ScHeight>ScWidth)
	{
		//竖版
		//console.log('shu');
		//document.getElementById("div").style.flex-flow="column";
		dpiperrem = DPi[0]/8;
		//document.documentElement.style.fontSize = ScWidth/60+'px';
		document.documentElement.style.fontSize = dpiperrem+'px';
		document.getElementById("HomeMenudivLeft").style.display="none";
		document.getElementById("HightModeMenu").style.display="";
		//document.getElementById("FileLabel").style.width = "1000px";
		document.getElementById("ShowMain").style.width = "100%";
		AdjustHomeMenudiv(ScHeight,dpiperrem);
		//document.getElementById("ShowMain").style.height = ScHeight-100-0.03*ScHeight+"px";
		//document.getElementById("FilesData").style.width = ScWidth+"px";
		//console.log(ScWidth);
		
		
	}
	else
	{
		//document.documentElement.style.fontSize = ScWidth/90+'px';
		
		dpiperrem = DPi[0]/8;
		//document.getElementById("div").style.flex-flow="row";
		document.documentElement.style.fontSize = dpiperrem+'px';
		document.getElementById("NavandContent").style.height = "100%";
		
		document.getElementById("HomeMenudivLeft").style.display="";
		document.getElementById("HightModeMenu").style.display="none";
		//document.getElementById("ShowMain").style.height = "100%";
	}

	Window.globalConfig.remperdpi = 1/dpiperrem;

	
}

function AdjustHomeMenudiv(ScHeight,dpiperrem)
{
	RemAmount = ScHeight*(1/dpiperrem);
	//console.log(RemAmount);
	document.getElementById("NavandContent").style.height = RemAmount-7+"rem";
	
}

//获取DPI
function js_getDPI() {
    var arrDPI = new Array();
    if ( window.screen.deviceXDPI != undefined ) {
        arrDPI[0] = window.screen.deviceXDPI;
        arrDPI[1] = window.screen.deviceYDPI;
    }
    else {
        var tmpNode = document.createElement( "DIV" );
        tmpNode.style.cssText = "width:1in;height:1in;position:absolute;left:0px;top:0px;z-index:99;visibility:hidden";
        document.body.appendChild(tmpNode);
        arrDPI[0] = parseInt( tmpNode.offsetWidth );
        arrDPI[1] = parseInt( tmpNode.offsetHeight );
        tmpNode.parentNode.removeChild( tmpNode );
    }

    return arrDPI;
}