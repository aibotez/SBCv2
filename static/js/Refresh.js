    function RefreshFiles(act)
    {
		//console.log(act);
        var encodeurl = encodeURIComponent(act.id)
        var cururl = 'http://'+window.location.host+'/RefreshFiles/';
        $("#ShowMain").load(cururl,{"ids": encodeurl});
        var stateObject = {};
        var title = "小黑云";
        var newUrl = "/?path="+encodeurl;
        history.pushState(stateObject,title,newUrl);
	}