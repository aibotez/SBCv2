

function BaiduNetShow()
{
	var urlpath = '/BaiduNetUserExistCheck/'
	datas = {};
	var res = PostMethod(urlpath,datas,0);
	console.log(res);
}