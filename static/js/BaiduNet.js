

function BaiduNetShow()
{
	var urlpath = '/BaiduNetUserExistCheck/'
	datas = {};
	let res = PostMethod(urlpath,datas,0);
	console.log(res);
	if(res.errno == '404')
	{
		var usercookie=prompt("输入cookie","");
		if (usercookie!=null && usercookie!="")
		{
			var urlpath = '/BaiduNetSaveUser/'
			datas = {'usercookie':usercookie};
			let res = PostMethod(urlpath,datas,0);
			if(res.res=='1')
			{
				
			}
		}
	}
}