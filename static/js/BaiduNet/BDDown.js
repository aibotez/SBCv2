

function BDDownFilebyGet()
{
	
	var delay = 500;
	var downfiles = BDFindCheckdown();
	console.log(downfiles);

	if (downfiles == "网页版不支持文件夹上传/下载")
	{
		alert("网页版不支持文件夹上传/下载");
		
	}
	for(let i=0;i<downfiles.length;i++)
	{
		var start = (new Date()).getTime();
        while((new Date()).getTime() - start < delay)
			{}
		
		let urlpath = "GetBDDownLink/"
		datas = downfiles[i];
		let DownLink = PostMethod(urlpath,datas,0);
		console.log(DownLink);
		if (DownLink.errno == '0')
		{
			downurl = DownLink.DownLink;
			let a = document.createElement('a');
			let filename = downfiles[i].fename;
			//a.href = downurl;
			a.href = 'reD/?url='+Base64.encode(downurl);
			a.click();
			a.remove();
		}
		return;

	}

}

function BDFindCheckdown()
{
	//var files = {{data|safe}};
	var files = Window.globalConfig.GlobalBDFiles;
	var Res = [];
	for (var i=0;i<files.length;i++)
	{
		file = files[i].filelj;
		if (document.getElementById(file+"Choseboxone").checked==true)
		{
			filename = files[i].server_filename;
			feisdir =files[i].isdir;
			if (feisdir == 1)
			{
				msg = "网页版不支持文件夹上传/下载";
				return msg;
			}
			Res.push({'fename':filename,'fepath':Base64.decode(file)});
		}
		
	}
	return Res;
}