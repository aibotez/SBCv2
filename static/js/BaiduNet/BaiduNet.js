
function SBCNetShow()
{
	window.location.href="/";
}


function BaiduNetShow()
{
	var urlpath = '/BaiduNetUserExistCheck/'
	datas = {};
	let res = PostMethod(urlpath,datas,0);
	//console.log(res);
	if(res.errno == '404')
	{
		var usercookie=prompt("输入cookie;直接确认会下载小黑云工具软件，该软件可以获取cookie，也可以通过该软件加速下载百度网盘资源","");
		if (usercookie == "")
		{
			DownGetCookieTool();
			return;
		}
		if (usercookie!=null && usercookie!="")
		{
			var urlpath = '/BaiduNetSaveUser/'
			datas = {'usercookie':usercookie};
			let res = PostMethod(urlpath,datas,0);
			if(res.res=='1')
			{
				//let Showpath = Base64.encode('/');
				//BaiduNetRefreshFile({'id':Showpath});
				window.location.href="/BaiduNetHome/?showpath=/";
			}
			if (res.res=='cookieerror')
			{
				BaiduNetShow();
			}
		}
	}
	else
	{
		let Showpath = Base64.encode('/');
		//BaiduNetRefreshFile({'id':Showpath});
		window.location.href="/BaiduNetHome/?showpath=/";
	}
}

function DownGetCookieTool()
{
	downurl = "/static/Tools/GetCookie/GetCookie.exe";
	let a = document.createElement('a');
	let filename = "GetCookie.exe";
	a.href = downurl;
	a.click();
	a.remove();
}


function BDQuitLogin() {
	var msg = "确定要退出百度云登录？退出后要重新登录";
	if (confirm(msg)==true){
	BDQuitLoginact();
	}else{
	return false;
	}
}
function BDQuitLoginact()
{
	let urlpath = '/BaiduNetQuitLogin/'
	datas = {};
	let res = PostMethod(urlpath,datas,0);
	if(res.res == '1')
	{
		window.location.href="/";
	}
}