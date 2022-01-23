    function upload() {
        //背景恢复
        $(".progress").css("background", "#262626");
        //归零 隐藏
        $("#mt-progress-length").css({"width": "0%", "opacity": "1"});
        $("#mt-progress-value").html(0);


        //创建formData对象  初始化为form表单中的数据
        //需要添加其他数据  就可以使用 formData.append("property", "value");
        var formData = new FormData();
        var fileInput = document.getElementById("myFile");
        var file = fileInput.files[0];
        formData.append("file", file);

        // ajax异步上传
        $.ajax({
            url: "http://localhost:1001/login/upload",
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
    }

    //上传进度回调函数
    function resultProgress(e) {
        if (e.lengthComputable) {
            var percent = e.loaded / e.total * 100;
            $(".show_result").html(percent + "%");
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