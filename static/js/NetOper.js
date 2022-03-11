
function QuitLogin()
{
	var urlpath = '/QuitLogin/'
	datas = {};
	var res = PostMethod(urlpath,datas,0);
	//console.log(res);
	if(res.res == 'ok')
	{
		window.location.href="/login/";
	}
}