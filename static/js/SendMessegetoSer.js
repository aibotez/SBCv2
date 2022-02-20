function PostMethod(urlpath,datas,isSanc)
{
	var resdata = '';
	$.ajax({
        async: isSanc,
        type: "POST",
        url: urlpath,
        data: datas,
        dataType: "json",
        success: function (data) {resdata = data;},
        error: function () { },
        complete: function (data) {}
    })
	//alert(resdata.res);
	return resdata;
	
}