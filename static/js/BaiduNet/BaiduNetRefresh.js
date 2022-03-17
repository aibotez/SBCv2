    
	function Result(response)
	{
		console.log(response);
	}
	function BaiduNetDealrefresh(act)
	{
		//console.log(act.id);
		if (document.getElementById(act.id).name == 1)
		{
			BaiduNetRefreshAct(act);
		}
		else
		{
			//window.open("preview/?"+"BDfilepath="+act.id);
		}

	}
	function BaiduNetRefreshAct(act)
	{
		var encodeurl = encodeURIComponent(Base64.decode(act.id))
        var cururl = 'http://'+window.location.host+'/BaiduNetShow/';
        $("#ShowMain").load(cururl,{"showpath": encodeurl},function(response){
			//console.log(response);
			//console.log({{data|safe}});
			});
        var stateObject = {};
        var title = "小黑云";
        var newUrl = "/BaiduNetHome?showpath="+encodeurl;
        history.pushState(stateObject,title,newUrl);
	}
	
	function BaiduNetRefreshFile(act)
    {

		
		//var files = Window.globalConfig.GlobalFiles;
		setTimeout(() => {
			//BaiduNetRefreshAct(act);
			BaiduNetDealrefresh(act);
			}, 100);
	} 
	
	function BaiduNetRefreshFiles(act)
    {
		//console.log(act);
		
		BaiduNetRefreshAct(act);
	}