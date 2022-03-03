

function DownFilebyPost(files)
{
	var delay = 500;
	var downfiles = FindCheckdown(files);
	if (downfiles == "网页版不支持文件夹上传/下载")
	{
		alert("网页版不支持文件夹上传/下载");
		return;
	}
	//alert(downfiles.length);
	for(var i=0;i<downfiles.length;i++)
	{
		downfile = downfiles[i];
		downfile.fileId = "";
		var start = (new Date()).getTime();
        while((new Date()).getTime() - start < delay)
			{}
	    var form = document.createElement('form');
        form.setAttribute('style','display:none');
        form.setAttribute('target','');
        form.setAttribute('method','post');
        form.setAttribute('action','/FileDown/')
        var inputContent = document.createElement('input')
        inputContent.setAttribute('type','hidden');
        inputContent.setAttribute('name','downinfo');
        inputContent.setAttribute('value',JSON.stringify(downfile));
		//console.log(downfiles[i]);
        $('body').append(form);
        form.append(inputContent);
        form.submit();
        form.remove();
		
	}
}

function DownFilebyGet(files)
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
function FindCheckdown(files1)
{
	//var files = {{data|safe}};
	var files = Window.globalConfig.GlobalFiles;
	var Res = [];
	for (var i=0;i<files.length;i++)
	{
		file = files[i].filelj;
		if (document.getElementById(file+"Choseboxone").checked==true)
		{
			filename = files[i].filename;
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