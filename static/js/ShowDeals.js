
var imgdata = [];
function ShowconDeals(imgs)
{
	imgdata = imgs;
	imgsLen = imgs.length;
	if (imgsLen<=0)
	{return;}
	
	urlpath = '/GetImgCon/'
	datas = {'imgdata':imgs};
	var res = SendMPostMethod(urlpath,JSON.stringify(datas),1);
	//console.log(res.src);
	for(let i=0;i<imgsLen;i++)
	{
		imgpath = imgs[0].fepath;
		imgconid = Base64.encode(imgpath);
	}
}
function DealCon(resdata)
{
	imgsLen = imgdata.length;
	for(let i=0;i<imgsLen;i++)
	{
		imgpath = imgdata[i].fepath;
		imgconid = Base64.encode(imgpath)+"Imgcon";
		document.getElementById(imgconid).src = resdata.src[i];
	}
}
function SendMPostMethod(urlpath,datas,isSanc)
{
	var resdata = '';
	$.ajax({
        async: isSanc,
        type: "POST",
        url: urlpath,
        data: datas,
        dataType: "json",
        success: function (data) {DealCon(data)},
        error: function () { },
        complete: function (data) {}
    })
	
}