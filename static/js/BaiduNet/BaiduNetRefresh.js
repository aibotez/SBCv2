    
	function Result(response)
	{
		console.log(response);
	}
	function BaiduNetDealrefresh(act)
	{
		var files = Window.globalConfig.GlobalFiles;
		var CheckFiles = FindCheck(files);
		if(CheckFiles.length == 0 || CheckFiles[0].feisdir == 1)
		{
			BaiduNetRefreshAct(act);
		}
		else{
			//console.log(CheckFiles[0].fepath);
			ClearCheck();
			window.open("preview/?"+"filepath="+CheckFiles[0].fepath);
			//location.href="preview/?"+"filepath="+CheckFiles[0].fepath;
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
        var newUrl = "/?path="+encodeurl;
        history.pushState(stateObject,title,newUrl);
	}
	
	function BaiduNetRefreshFile(act)
    {

		
		var files = Window.globalConfig.GlobalFiles;
		setTimeout(() => {
			BaiduNetDealrefresh(act);
			}, 100);
	} 
	
	function BaiduNetRefreshFiles(act)
    {
		//console.log(act);
		
		BaiduNetRefreshAct(act);
	}