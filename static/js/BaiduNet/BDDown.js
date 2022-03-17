

function BDDownFilebyGet(files)
{
	
	var delay = 500;
	var downfiles = FindCheckdown(files);
	if (downfiles == "网页版不支持文件夹上传/下载")
	{
		alert("网页版不支持文件夹上传/下载");
		return;
	}
	for(var i=0;i<downfiles.length;i++)
	{
		var start = (new Date()).getTime();
        while((new Date()).getTime() - start < delay)
			{}
		cururl = 'http://'+window.location.host;
		urli = cururl+'/FileDown/?downinfo='+encodeURIComponent(JSON.stringify(downfiles[i]));
		var a = document.createElement('a');
		var filename = downfiles[i].fename;
		a.href = urli;
		a.click();
		a.remove();
	}

}