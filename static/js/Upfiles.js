    var file = "";
	var Files = [];
	var start = (new Date()).getTime();
	var WaitUpNums = 0;
	var FinshUpNums = 0;
	var UpingNums = 0;
	var UpNums = 2;
	var CurUpIter = 0;
	var UpManage = new Array();
	
	
	function GetFileMd51(file)
	{
		var blobSlice = File.prototype.slice || File.prototype.mozSlice || File.prototype.webkitSlice;
		var chunkSize = 2097152; // 每次读取2MB
		var chunks = Math.ceil(file.size / chunkSize);
		var currentChunk = 0;
		var spark = new SparkMD5.ArrayBuffer();
        frOnload = function(e){
            //log.innerHTML+="\n读取文件 "+parseInt(currentChunk+1)+" of "+chunks;
                spark.append(e.target.result);
                currentChunk++;
                if (currentChunk < chunks)
				{
					//document.getElementById(CurPath+file.name+"label").innerText ="正在扫描文件 "+(100*currentChunk/chunks).toFixed(2)+"%";
					loadNext();
				}
                    
                else
				{
					//UpManage[Manageid]['md5']=spark.end();
					console.log(spark.end());
					console.log(file);


					return spark.end();
				}
					//console.log(spark.end());
					//return 123;
                    //log.innerHTML+="\n读取完成！\n\n文件md5:"+spark.end()+"\n";
            }
		
        frOnerror = function () {
			return 'md5ReadFaile';
            //upload(file,'md5ReadFaile');
            };
		function loadNext() {
            var fileReader = new FileReader();
            fileReader.onload = frOnload;
            fileReader.onerror = frOnerror;
            var start = currentChunk * chunkSize,
            end = ((start + chunkSize) >= file.size) ? file.size : start + chunkSize;
            fileReader.readAsArrayBuffer(blobSlice.call(file, start, end));
            };
		loadNext();

	}
	
	
	function GetFileMd50(file,Manageid,CurPath)
	{
		console.log(file.name);
	}
	function GetFileMd5(file,Manageid,CurPath)
	{
		let filei = file;
		let blobSlice = File.prototype.slice || File.prototype.mozSlice || File.prototype.webkitSlice;
		let chunkSize = 1024*1024; // 每次读取2MB
		let chunks = Math.ceil(file.size / chunkSize);
		let currentChunk = 0;
		let spark = new SparkMD5.ArrayBuffer();
        let frOnload = function(e){
            //log.innerHTML+="\n读取文件 "+parseInt(currentChunk+1)+" of "+chunks;
                spark.append(e.target.result);
                currentChunk++;
                if (currentChunk < chunks)
				{
					console.log(filei.name);
					document.getElementById(CurPath+file.name+"label").innerText ="正在扫描文件 "+(100*currentChunk/chunks).toFixed(2)+"%";
					loadNext();
				}
                    
                else
				{
					let FileMd5 = spark.end().toString();
					document.getElementById(CurPath+file.name+"label").innerText ="扫描完成！";
					UpManage[Manageid]['md5']=FileMd5;
					//upload(file,FileMd5);
					UpingNums = UpingNums-1;
					UpFileEx();

					return spark.end();
				}
					//console.log(spark.end());
					//return 123;
                    //log.innerHTML+="\n读取完成！\n\n文件md5:"+spark.end()+"\n";
            }
		
        let frOnerror = function () {
			return 'md5ReadFaile';
            //upload(file,'md5ReadFaile');
            };
		function loadNext() {
            let fileReader = new FileReader();
            fileReader.onload = frOnload;
            fileReader.onerror = frOnerror;
            let starti = currentChunk * chunkSize,
            end = ((starti + chunkSize) >= file.size) ? file.size : starti + chunkSize;
            fileReader.readAsArrayBuffer(blobSlice.call(file, starti, end));
            };
		loadNext();

	}
	
	function size_format(size)
	{
		
		if (size < 1024)
		{return size + 'size'}
		if (1024 <= size && size< 1024*1024)
		{return (size/1024).toFixed(2) + 'KB'}
		if (1024*1024 <= size && size< 1024*1024*1024)
		{return (size/(1024*1024)).toFixed(2) + 'MB'}
		if (1024*1024*1024 <= size && size< 1024*1024*1024*1024)
		{return (size/(1024*1024*1024)).toFixed(2) + 'GB'}
		else(1024*1024*1024*1024 <= size)
		{return (size/(1024*1024*1024*1024)).toFixed(2) + 'TB'}	}
	
	function upcontrol(conid)
	{

		var fileid = conid.id;
		var filei = UpManage[fileid]['file'];
		var upact = UpManage[fileid]['isUp'];
		//console.log(upact);
		if (upact == 1)
		{
			UpManage[fileid]['isUp']=0;
			//document.getElementById(fileid).name = 0;
			
			document.getElementById(fileid).style = "background-image: url(/static/img/start.png);width: 23px;height: 23px;background-size:23px 23px; border: 0;";
			
		}
		else{
			UpManage[fileid]['isUp']=1;
			//document.getElementById(fileid).name = 1;
			FileMd5 = UpManage[fileid]['md5'];
			file = UpManage[fileid]['file'];
			document.getElementById(fileid).style = "background-image: url(/static/img/plause.png);width: 23px;height: 23px;background-size:23px 23px; border: 0;";
			upload(file,FileMd5);
			//GetFileMd5(filei);
		}
		//console.log(UpManage[fileid]['isUp']);
	}
	
	function UpFileEx()
	{
		var IterLen = UpNums-UpingNums;
		var CurPath = document.getElementById("CurPath").innerText;
		var CurUpIteri = CurUpIter
		for(let i=CurUpIteri;i<CurUpIteri+IterLen;i++)
		{
			//console.log(CurUpIteri+IterLen);
			if(i<Files.length)
			{
				console.log(i);
				setTimeout(function(){
　　			GetFileMd5(file[i],CurPath+file[i].name+"UpControl",CurPath);
				}, i*0);
				//GetFileMd5(Files[i],CurPath+Files[i].name+"UpControl",CurPath);
				console.log(Files[i].name+"UpControl");
				CurUpIter = CurUpIter+1;
				UpingNums = UpingNums+1;
			}


		}
	}
	
	function onChange(event) {
		CurUpIter = 0;
		//UpingNums = 0;
		alert(UpingNums);
		document.getElementById("Upmenudropdown-content").style.display = "none";
		var CurPath = document.getElementById("CurPath").innerText;
		start = (new Date()).getTime();
        file = event.target.files;
		Files = file;
		SelectFilesNums = file.length;
		WaitUpNums = WaitUpNums+SelectFilesNums;
		document.getElementById("Updetails").style.display="";
		document.getElementById("UpdetailsTitle").innerText = WaitUpNums+"个文件正在上传";
		for (let i=0; i<SelectFilesNums;i++)
		{
			var div = document.getElementById("UpList");
			var divtitle = document.createElement("div");
			
			var label = document.createElement("label");
			label.innerText = file[i].name;
			divtitle.appendChild(label);
			div.appendChild(divtitle);
			var div2 = document.createElement("div");
			div2.style = "float:left;width:100%;";
			//div2.class = "container";
			//div.appendChild(div2);
			var progress = document.createElement("progress");
			progress.id = CurPath+file[i].name+"progress";
			progress.max = "100";
			progress.value = "0";
			//progress.style = "width:60%;color:lightpink;";
			progress.style = "overflow:hidden;border-radius:1em;width:100%;color:lightpink;";
			//div2.appendChild(progress);
			
			
			var divSpeed = document.createElement("div");
			divSpeed.style = "float:left;height:100%;width:80%;";
			div2.appendChild(divSpeed);
			divSpeed.appendChild(progress);
			
			
			
			
			
			var label2 = document.createElement("label");
			label2.id = CurPath+file[i].name+"label";
			//label2.style = "display:table-cell;vertical-align:middle;font-size:12px;color:black;";
			label2.style = "width:100%;font-size:15px;color:black;";
			label2.innerText = "--/--";
			//div2.appendChild(label2);
			var UpControl = document.createElement("input");
			UpControl.type="Button";
			UpControl.id = CurPath+file[i].name+"UpControl";
			//UpControl.onclick = "upcontrol(this)";
			UpControl.setAttribute("onclick","upcontrol(this)");
			//UpControl.value="暂停/继续";position:relative;top:-10px;
			UpControl.style = "background-image: url(/static/img/plause.png);width:23px;height:23px;background-size:23px 23px; border:0;";
			UpControl.name=1;
			
			//div2.appendChild(UpControl);
			
			
			
			var divSpeedlabel = document.createElement("div");
			divSpeedlabel.style = "position:relative;top:-19px;left:10px;float:left;height:100%;width:60%;";
			div2.appendChild(divSpeedlabel);
			divSpeedlabel.appendChild(label2);
			
			var divbutton = document.createElement("div");
			divbutton.style = "float:left;position:relative;top:-21px;left:100px;";
			div2.appendChild(divbutton);
			divbutton.appendChild(UpControl);
			
			
			div.appendChild(div2);
			UpManage[CurPath+file[i].name+"UpControl"] = {'isUp':1,'file':file[i]};
			
			//UpManage.add(CurPath+file[i].name,{'isUp':1,'file':file[i]});
			//var FileMd5 = '0';
			//GetFileMd51(file[i]);
			
			//setTimeout(function(){
　　			//GetFileMd5(file[i],CurPath+file[i].name+"UpControl",CurPath);
			//}, 500);
			//GetFileMd5(file[i],CurPath+file[i].name+"UpControl",CurPath);
			
			//var starti = (new Date()).getTime();
			//while(FileMd5 == '0')
			//{console.log(FileMd5)}
			//console.log(FileMd5);
			//GetFileMd5(file[i]);
			//console.log(FileMd5);
			//upload(file[i]);
		}
		setTimeout("UpFileEx()", 100)
		//UpFileEx();
		
    }
	
	function upfilechunk(file,CurPath,FileMd5,startchunk)
	{
		const chunkSize = 512*1024;
		uploadact(startchunk);
		function uploadact(startchunk)
		{
			start = (new Date()).getTime();
			var isLastChunk = 0;
			  // 上传完成
			if (startchunk >= file.size) {
				FinshUpNums = FinshUpNums+1;
				UpingNums = UpingNums-1;
				document.getElementById(CurPath+file.name+"UpControl").disabled = true;
				document.getElementById(CurPath+file.name+"UpControl").style = "background-image: url(/static/img/finish.jpg);width: 23px;height: 23px;background-size:23px 23px; border: 0;";
				document.getElementById("UpdetailsTitle").innerText = WaitUpNums+"个文件正在上传! "+
				"已完成"+FinshUpNums+"个文件";
				RefreshFiles({'id':Base64.encode(CurPath)});
				UpFileEx();
				return;
			}
			let endchunk = (startchunk + chunkSize > file.size) ? file.size : (startchunk + chunkSize);
			let fd = new FormData();
			fd.append("file",file.slice(startchunk, endchunk));
			if(endchunk>= file.size)
			{isLastChunk = 1}
			fd.append("FileMd5",FileMd5);
			fd.append('CurPath',CurPath);
			fd.append('FileName',file.name);
			fd.append('FileSize',file.size);
			fd.append('webkitRelativePath',file.webkitRelativePath);
			fd.append('isLastChunk',isLastChunk);
			let xhr = new XMLHttpRequest();
			xhr.open('post', '/Upfile/', true);
			xhr.onload = function() {
				if (this.readyState == 4 && this.status == 200 && UpManage[CurPath+file.name+"UpControl"]['isUp']==1) {
					let progress = document.getElementById(CurPath+file.name+"progress");
					//console.log(document.getElementById(CurPath+file.name+"UpControl").name);
					progress.max = file.size;
					progress.value = endchunk;
					var Upspeed = size_format(1000*(endchunk-startchunk)/((new Date()).getTime() - start))+"/s";
					document.getElementById(CurPath+file.name+"label").innerText = size_format(endchunk)+"/"+size_format(file.size)+" "+Upspeed;
					uploadact(endchunk);
				}
			}
			xhr.send(fd);
		}
	}
	
	function upload(file,FileMd5) {
		//var FileMd5 = GetFileMd5(file);
		//console.log(FileMd5);
		//console.log(UpManage);
		var CurPath = document.getElementById("CurPath").innerText;
		document.getElementById(CurPath+file.name+"label").innerText = size_format(0)+"/"+size_format(file.size)+"";
		urlpath = "/CheckFile/";
		data={
			'CurPath':CurPath,
			'FileName':file.name,
			'FileMd5':FileMd5,
			'FileSize':file.size,
			'webkitRelativePath':file.webkitRelativePath,
		};
		var CheckFileRes = PostMethod(urlpath,data,0);
		//console.log(CheckFileRes);
		if(CheckFileRes.exist)
		{
			var progress = document.getElementById(CurPath+file.name+"progress");
			progress.max = file.size;
			progress.value = file.size;
			RefreshFiles({'id':Base64.encode(CurPath)});
			FinshUpNums = FinshUpNums+1;
			UpingNums = UpingNums-1;
			//console.log(222);
			document.getElementById(CurPath+file.name+"UpControl").disabled = true;
			document.getElementById(CurPath+file.name+"UpControl").style = "background-image: url(/static/img/finish.jpg);width: 23px;height: 23px;background-size:23px 23px; border: 0;";
			document.getElementById("UpdetailsTitle").innerText = WaitUpNums+"个文件正在上传! "+"已完成"+FinshUpNums+"个文件";
			//console.log(" 秒传");
			document.getElementById(CurPath+file.name+"label").innerText = size_format(file.size)+"/"+size_format(file.size)+" 秒传";
			UpFileEx();
			return;
		}
		var startchunk = CheckFileRes.FileStart;
		upfilechunk(file,CurPath,FileMd5,startchunk);
		

	}
	function backup()
	{
		var cururl = 'http://'+window.location.host;
		var UpUrl = cururl+'/Upfile/';
        //创建formData对象  初始化为form表单中的数据
        //需要添加其他数据  就可以使用 formData.append("property", "value");
        var formData = new FormData();
        //var fileInput = document.getElementById("myFile");
        //var file = fileInput.files[0];
		//console.log(file.name)
        formData.append("file",file);
		formData.append("FileMd5",FileMd5);
		//alert(formData);
        // ajax异步上传
        $.ajax({
            url: UpUrl,
            type: "POST",
            data: formData,
            contentType: false, //必须false才会自动加上正确的Content-Type
            processData: false,  //必须false才会避开jQuery对 formdata 的默认处理
            enctype: 'multipart/form-data',
            xhr: function () {
                //获取ajax中的ajaxSettings的xhr对象  为他的upload属性绑定progress事件的处理函数
                var myXhr = $.ajaxSettings.xhr();
                if (myXhr.upload) {
                    //检查其属性upload是否存在
                    myXhr.upload.addEventListener("progress", resultProgress, false);
                }
                return myXhr;
            },
            success: function (data) {
                console.log("aaa");
            },
            error: function (data) {
                console.log("cccc");
            }
        })
  

		//上传进度回调函数
		function resultProgress(e) {
			//console.log(e);
			//console.log(file);
			if (e.lengthComputable) {
				var percent = e.loaded / e.total * 100;
				var Upspeed = size_format(1000*e.loaded/((new Date()).getTime() - start))+"/s";
				document.getElementById(file.name+"progress").value = percent;
				document.getElementById(file.name+"label").innerText = size_format(e.loaded)+"/"+size_format(e.total)
				+" "+Upspeed;
				//$(".show_result").html(percent + "%");
				var percentStr = String(percent);
				if (percentStr == "100") {
					percentStr = "100.0";
				}
				percentStr = percentStr.substring(0, percentStr.indexOf("."));
				$("#mt-progress-value").html(percentStr);
				$("#mt-progress-length").css("width", percentStr + "%");

				if (percentStr == "100") {
					setTimeout(function () {
						//背景成绿色
						$(".progress").css("background", "#15AD66");
						//归零 隐藏
						$("#mt-progress-length").css({"width": "0%", "opacity": "0"});
					}, 500);


				}
			}
		}
	}