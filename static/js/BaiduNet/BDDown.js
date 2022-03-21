
function BDDownS(DownLink,downfile) {
	let DownS=prompt("可复制以下链接使用工具高速下载，确认为直接下载(慢速，大文件(>60MB)不推荐)",DownLink.DownLink);
	let msg = "确定直接下载吗？下载大文件相当不推荐";
	if (confirm(msg)==true){
	DOwnAct(DownLink,downfile);
	}else{
	return false;
	}
}

function DOwnAct(DownLink,downfile)
{
		downurl = DownLink.DownLink;
		FileSize = DownLink.FileSize;

		if (FileSize<100*1024*1024)
		{
			let a = document.createElement('a');
			let filename = downfile.fename;
			a.href = downurl;
			a.click();
			a.remove();
			return;
		}
		//return;
	    var form = document.createElement('form');
        form.setAttribute('style','display:none');
        form.setAttribute('target','');
        form.setAttribute('method','post');
        form.setAttribute('action','/reD/')
        var inputContent = document.createElement('input')
        inputContent.setAttribute('type','hidden');
        inputContent.setAttribute('name','url');
        inputContent.setAttribute('value',downurl);
		var inputContent1 = document.createElement('input')
        inputContent1.setAttribute('type','hidden');
        inputContent1.setAttribute('name','Range');
        inputContent1.setAttribute('value','bytes=0-1024');
		var inputContent2 = document.createElement('input')
		inputContent2.setAttribute('type','hidden');
        inputContent2.setAttribute('name','FileName');
        inputContent2.setAttribute('value',downfile.fename);
		var inputContent3 = document.createElement('input')
		inputContent3.setAttribute('type','hidden');
        inputContent3.setAttribute('name','FileSize');
        inputContent3.setAttribute('value',FileSize);
		//console.log(downfiles[i]);
        $('body').append(form);
        form.append(inputContent);
		form.append(inputContent1);
		form.append(inputContent2);
		form.append(inputContent3);
        form.submit();
        form.remove();
}

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
		
		let urlpath = "/GetBDDownLink/"
		datas = downfiles[i];
		let DownLink = PostMethod(urlpath,datas,0);
		console.log(DownLink);
		if (DownLink.errno == '0')
		{
			downurl = DownLink.DownLink;
			BDDownS(DownLink,downfiles[i]);

		}
		return;

	}

}



function BDDownFilebyPost()
{
	var delay = 500;
	var downfiles = BDFindCheckdown();
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
		
		let urlpath = "GetBDDownLink/"
		datas = downfiles[i];
		let DownLink = PostMethod(urlpath,datas,0);
		if (DownLink.errno != '0')
		{return;}
	
	
		BDDownS(DownLink,downfiles[i]);
	

		
		
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