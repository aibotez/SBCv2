    var file = "";
	var start = (new Date()).getTime();
	var WaitUpNums = 0;
	var FinshUpNums = 0;
	var UpManage = new Array();
	
	function GetFileMd5(file)
	{
		var blobSlice = File.prototype.slice || File.prototype.mozSlice || File.prototype.webkitSlice;
		chunkSize = 2097152; // 每次读取2MB
		var chunks = Math.ceil(file.size / chunkSize);
		var currentChunk = 0;
		spark = new SparkMD5.ArrayBuffer();
        frOnload = function(e){
            //log.innerHTML+="\n读取文件 "+parseInt(currentChunk+1)+" of "+chunks;
                spark.append(e.target.result);
                currentChunk++;
                if (currentChunk < chunks)
                    loadNext();
                else
				{
					upload(file,spark.end());
					//upload(file,spark.end());
					//console.log(spark.end());

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
	
	function size_format(size)
	{
		if (size < 1024)
		{return size + 'size'}
		if (1024 <= size && size< 1024*1024)
		{return (size/1024).toFixed(2) + 'KB'}
		if (1024*1024 <= size && size< 1024*1024*1024)
		{return (size/(1024*1024)).toFixed(2) + 'MB'}
		if (1024*1024*1024 <= size && size< 1024*1024*1024*1024)
		{return size/(1024*1024*1024).toFixed(2) + 'GB'}
		else(1024*1024*1024*1024 <= size)
		{return size/(1024*1024*1024*1024).toFixed(2) + 'TB'}	}
	
	function upcontrol(conid)
	{

		var fileid = conid.id;
		var filei = UpManage[fileid]['file'];
		var upact = UpManage[fileid]['isup'];
		if (upact)
		{
			UpManage[fileid]['isup']=0;
			
		}
		else{
			UpManage[fileid]['isup']=1;
			GetFileMd5(filei);
		}
		console.log(UpManage[fileid]['isup']);
	}
	
	function onChange(event) {
		var CurPath = document.getElementById("CurPath").innerText;
		start = (new Date()).getTime();
        file = event.target.files;
		SelectFilesNums = file.length;
		WaitUpNums = WaitUpNums+SelectFilesNums;
		document.getElementById("Updetails").style.display="";
		document.getElementById("UpdetailsTitle").innerText = WaitUpNums+"个文件正在上传";
		for (var i=0; i<SelectFilesNums;i++)
		{
			var div = document.getElementById("UpList");
			var label = document.createElement("label");
			label.innerText = file[i].name;
			div.appendChild(label);
			var div2 = document.createElement("div");
			div2.style = "width:100%;padding:0px 0px";
			div2.class = "container";
			div.appendChild(div2);
			var progress = document.createElement("progress");
			progress.id = CurPath+file[i].name+"progress";
			progress.max = "100";
			progress.value = "0";
			//progress.style = "width:60%;color:lightpink;";
			progress.style = "overflow:hidden;border-radius:1em;width:60%;color:lightpink;";
			div2.appendChild(progress);
			var label2 = document.createElement("label");
			label2.id = CurPath+file[i].name+"label";
			//label2.style = "display:table-cell;vertical-align:middle;font-size:12px;color:black;";
			label2.style = "position:absolute;left:10px;font-size:15px;color:black;";
			label2.innerText = "--/--";
			div2.appendChild(label2);
			var UpControl = document.createElement("input");
			UpControl.type="Button";
			UpControl.id = CurPath+file[i].name+"UpControl";
			//UpControl.onclick = "upcontrol(this)";
			UpControl.setAttribute("onclick","upcontrol(this)");
			UpControl.value="暂停/继续";
			
			div2.appendChild(UpControl);
			
			UpManage[CurPath+file[i].name+"UpControl"] = {'isUp':1,'file':file[i]};
			
			//UpManage.add(CurPath+file[i].name,{'isUp':1,'file':file[i]});
			//var FileMd5 = '0';
			FileMd5 = GetFileMd5(file[i]);
			//var starti = (new Date()).getTime();
			//while(FileMd5 == '0')
			//{console.log(FileMd5)}
			//console.log(FileMd5);
			//GetFileMd5(file[i]);
			//console.log(FileMd5);
			//upload(file[i]);
		}
        //console.log(file[0]);
		
    }
	
	function upfilechunk(file,CurPath,FileMd5,startchunk)
	{
		const chunkSize = 2*1024*1024;
		uploadact(startchunk);
		function uploadact(startchunk)
		{
			start = (new Date()).getTime();
			var isLastChunk = 0;
			  // 上传完成
			if (startchunk >= file.size) {
				FinshUpNums = FinshUpNums+1;
				document.getElementById("UpdetailsTitle").innerText = WaitUpNums+"个文件正在上传! "+
				"已完成"+FinshUpNums+"个文件";
				RefreshFiles({'id':CurPath});
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
			fd.append('isLastChunk',isLastChunk);
			var fileids = CurPath+file.name+"UpControl";
			
			let xhr = new XMLHttpRequest();
			xhr.open('post', '/Upfile/', true);
			xhr.onload = function() {
				if (this.readyState == 4 && this.status == 200 && UpManage[fileids]['isup']==1) {
					let progress = document.getElementById(CurPath+file.name+"progress");
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
		urlpath = "/CheckFile/";
		data={
			'CurPath':CurPath,
			'FileName':file.name,
			'FileMd5':FileMd5
		};
		var CheckFileRes = PostMethod(urlpath,data,0);
		console.log(CheckFileRes);
		if(CheckFileRes.exist)
		{
			var progress = document.getElementById(CurPath+file.name+"progress");
			progress.max = file.size;
			progress.value = file.size;
			RefreshFiles({'id':CurPath});
			FinshUpNums = FinshUpNums+1;
			document.getElementById("UpdetailsTitle").innerText = WaitUpNums+"个文件正在上传! "+"已完成"+FinshUpNums+"个文件";
			document.getElementById(CurPath+file.name+"label").innerText = size_format(file.size)+"/"+size_format(file.size)+" 秒传";
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