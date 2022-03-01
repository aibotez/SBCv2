    
	function Result(response)
	{
		console.log(response);
	}
	function Dealrefresh(act)
	{
		var files = Window.globalConfig.GlobalFiles;
		var CheckFiles = FindCheck(files);
		if(CheckFiles.length == 0 || CheckFiles[0].feisdir == 1)
		{
			RefreshAct(act);
		}
		else{
			
		}
	}
	function RefreshAct(act)
	{
		var encodeurl = encodeURIComponent(Base64.decode(act.id))
        var cururl = 'http://'+window.location.host+'/RefreshFiles/';
        $("#ShowMain").load(cururl,{"ids": encodeurl},function(response){
			//console.log(response);
			//console.log({{data|safe}});
			});
        var stateObject = {};
        var title = "小黑云";
        var newUrl = "/?path="+encodeurl;
        history.pushState(stateObject,title,newUrl);
	}
	function RefreshFiles(act)
    {
		//console.log(act);
		
		var files = Window.globalConfig.GlobalFiles;
		setTimeout(() => {
			Dealrefresh(act);
			}, 100);
	}