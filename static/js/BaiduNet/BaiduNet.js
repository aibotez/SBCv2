
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
		var usercookie=prompt("输入cookie;直接确认会下载获取cookie工具，可通过该工具获取cookie","");
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

function BDQuitLogin()
{
	let urlpath = '/BaiduNetQuitLogin/'
	datas = {};
	let res = PostMethod(urlpath,datas,0);
	if(res.res == '1')
	{
		window.location.href="/";
	}
}