function GetStockUser()
 {
	 let res = PostMethod('/GetStockFilesAll/',{},0);
	 return res
 }
 
 function Updateact(Files)
 {
	var tbody = document.getElementById("UserTable");
	for (let i=0;i<Files.length;i++)
	{
		let tr = document.createElement("tr");
		tr.class = "change";
		let td1 = document.createElement("td");
		let input1 = document.createElement("input");
		input1.id = 'FIles'+i.toString();
		input1.type="checkbox";
		td1.appendChild(input1);
		let th1 = document.createElement("th");
		th1.style.width = "5%";
		th1.scope="row";
		th1.innerText = i;
		let td2 = document.createElement("td");
		td2.style.width = "45%";
		td2.innerText = Files[i].FileName;
		let td3 = document.createElement("td");
		td3.style.width = "30%";
		td3.innerText = Files[i].MD5;
		let td4 = document.createElement("td");
		td4.style.width = "10%";
		td4.innerText = Files[i].FileSizestr;
		let td5 = document.createElement("td");
		td5.style.width = "5%";
		td5.innerText = Files[i].FileType;
		tr.appendChild(td1);
		tr.appendChild(th1);
		tr.appendChild(td2);
		tr.appendChild(td3);
		tr.appendChild(td4);
		tr.appendChild(td5);
		tbody.appendChild(tr);
	}
	
	 
 }
 
 function UpdateFiles(judge)
 {
	 console.log(judge)
	 let res = GetStockUser();
	 var FileNoUser = res.NoUser;
	 var allstockFiles = res.all;
	 if(judge==1)
	 {
		 Filesall = allstockFiles
	 }
	 else
	 {
		 Filesall = FileNoUser
	 }
	 var tbody = document.getElementById("UserTable");
	 while(tbody.firstChild) { 
	    tbody.removeChild(tbody.firstChild); 
		} 
	 Updateact(Filesall);
	 
	 return
 }
 function FileChosedAll()
 {
    for(let i =0;i<Filesall.length;i++)
    {
        document.getElementById('FIles'+i.toString()).checked = 1;
    }
 }
 function GetFileChoseds()
 {
	let Choseds = [];
	for(let i =0;i<Filesall.length;i++)
	{
		if(document.getElementById('FIles'+i.toString()).checked==1)
        Choseds.push(Filesall[i]);
    }
	return Choseds
 }
 function DelFiles()
 {

	 let Chosed = GetFileChoseds();
	 if(Chosed.length>0)
	 {
		let ret = confirm('确认删除'+Chosed.length+'个文件？');
		if (ret==false)
		{
			return;
		}
		console.log(ret)
		let res = PostMethod('/DelStockFiles/',JSON.stringify({'Files':Chosed}),0);
	 }
	 
 }
 
 
 
 
  function CPUusedShow()
 {
	var CPUusedChart = echarts.init(document.getElementById('CPUused'));
        pieHuanOption = {
            // 标题
            title: {
				left:'center',
                text: 'CPU用量'
            },
            // 不同区域的颜色
            color: ['#65a5ff', '#dcebff'],

	    graphic: {
	        type: 'text',
	        top: 'center',
	        left: 'center',
	        zlevel:0,
	        style: {
	            text: '30%',
	            fontSize: 16,
	            textAlign:'center',
	            fontWeight: 'bold'
//<!--	            fontWeight: 'bold'		文字字体的粗细，可选'normal'，'bold'，'bolder'，'lighter'-->
	        }
	    },
            series: [
                {
                   // name: '磁盘用量',
                    type: 'pie',
                    // 数组的第一项是内半径，第二项是外半径；可以设置不同的内外半径显示成圆环图
                    radius: ['40%', '60%'],
                    // 饼图的中心（圆心）坐标，数组的第一项是横坐标，第二项是纵坐标；设置成百分比时第一项是相对于容器宽度，第二项是相对于容器高度
                    center: ['50%', '50%'],
                    itemStyle: {
                        // 显示图例
                        normal: {
                            label: {
								fontSize: 18,
                                show: true
                            },
                            labelLine: {
                                show: true
                            }
                        },

                    },
                    data: [
                        { value: 3, name: '已使用' },
                        { value: 7, name: '剩余' }
                    ]
                }
            ]
        };
        CPUusedChart.setOption(pieHuanOption);
 }
  function MemusedShow()
 {
	var MemusedChart = echarts.init(document.getElementById('Memused'));
        pieHuanOption = {
            // 标题
            title: {
				left:'center',
                text: '内存用量'
            },
            // 不同区域的颜色
            color: ['#65a5ff', '#dcebff'],

	    graphic: {
	        type: 'text',
	        top: 'center',
	        left: 'center',
	        zlevel:0,
	        style: {
	            text: '',
	            fontSize: 16,
	            textAlign:'center',
	            fontWeight: 'bold'
//<!--	            fontWeight: 'bold'		文字字体的粗细，可选'normal'，'bold'，'bolder'，'lighter'-->
	        }
	    },
            series: [
                {
                    name: '磁盘用量',
                    type: 'pie',
                    // 数组的第一项是内半径，第二项是外半径；可以设置不同的内外半径显示成圆环图
                    radius: ['40%', '60%'],
                    // 饼图的中心（圆心）坐标，数组的第一项是横坐标，第二项是纵坐标；设置成百分比时第一项是相对于容器宽度，第二项是相对于容器高度
                    center: ['50%', '50%'],
                    itemStyle: {
                        // 显示图例
                        normal: {
                            label: {
								fontSize: 18,
                                show: true
                            },
                            labelLine: {
                                show: true
                            }
                        },

                    },
                    data: [
                        { value: 0, name: '已使用' },
                        { value: 10, name: '剩余' }
                    ]
                }
            ]
        };
        MemusedChart.setOption(pieHuanOption);
 }
 function DiskusedShow()
 {
	var DiskusedChart = echarts.init(document.getElementById('Diskused'));
        pieHuanOption = {
            // 标题
            title: {
				left:'center',
                text: '磁盘用量'
            },
            // 不同区域的颜色
            color: ['#65a5ff', '#dcebff'],

	    graphic: 
		{
	        type: 'text',
	        top: 'center',
	        left: 'center',
	        zlevel:0,
	        style: 
			{
	            text: '',
	            fontSize: 16,
	            textAlign:'center',
	            fontWeight: 'bold'
//<!--	            fontWeight: 'bold'		文字字体的粗细，可选'normal'，'bold'，'bolder'，'lighter'-->
	        }
	    },
            series: [
                {
                    name: '磁盘用量',
                    type: 'pie',
                    // 数组的第一项是内半径，第二项是外半径；可以设置不同的内外半径显示成圆环图
                    radius: ['40%', '60%'],
                    // 饼图的中心（圆心）坐标，数组的第一项是横坐标，第二项是纵坐标；设置成百分比时第一项是相对于容器宽度，第二项是相对于容器高度
                    center: ['50%', '50%'],
                    itemStyle: {
                        // 显示图例
                        normal: {
                            label: {
								fontSize: 18,
                                show: true
                            },
                            labelLine: {
                                show: true
                            }
                        },

                    },
                    data: [
                        { value: 0, name: '已使用' },
                        { value: 10, name: '剩余' }
                    ]
                }
            ]
        };
        DiskusedChart.setOption(pieHuanOption);
 }
 
 function NetWork()
 {
	 // 基于准备好的dom，初始化echarts实例
	var NetusedChart = echarts.init(document.getElementById('Netused'));
	// 指定图表的配置项和数据
	var option = {
	title:{left:'center',
	text:'网络',
	sped:'B',
	//subtext:'数据纯属虚构',
	},
	legend: {
		
		data: ["下载", "上传"],
        top: "10%",
        textStyle: {
            
            fontSize: 14
		},
	},

	xAxis: {

		name: 'S',
		type: 'category',
		boundaryGap: false,
		data: [0]
	},
	yAxis: {
		name: 'KB',
		type: 'value'
	},
	series: [
		{
			name: "下载",
			symbol: 'none',
			data: [0],
			data1: [0],
			type: 'line',
			areaStyle: {}
		},
		{
			name: "上传",
			symbol: 'none',
			data: [0],
			data1: [0],
			type: 'line',
			areaStyle: {},
			
			itemStyle:
			{
				normal:
				{
					lineStyle:
					{
						width:2,
						type:'dashed'  //'dotted'点型虚线 'solid'实线 'dashed'线性虚线
					}
				}
			},
		}
	]
	};
	// 使用刚指定的配置项和数据显示图表。
	NetusedChart.setOption(option);
	 
 }

  function refreshData11()
  {
	  setInterval(refreshData1, 1000);
  }
  function refreshCpuData(res)
  {
	    var chart = echarts.getInstanceByDom(document.getElementById('CPUused'));
        var option = chart.getOption();
		option.series[0].data[0].value = res.Cpu.cpu_percent;

		option.series[0].data[1].value = 100-res.Cpu.cpu_percent;
		option.graphic[0].elements[0].style.text = res.Cpu.cpu_percent.toString()+'%\n'+res.Cpu.cpu_counts_phs.toString()+'/'+res.Cpu.cpu_counts_logi.toString();
		chart.setOption(option);	
  }
  
  function refreshMemData(res)
  {
	    var chart = echarts.getInstanceByDom(document.getElementById('Memused'));
        var option = chart.getOption();
		option.series[0].data[0].value = res.Mem.MemPercent;

		option.series[0].data[1].value = 100-res.Mem.MemPercent;

		option.graphic[0].elements[0].style.text = res.Mem.MemPercent.toString()+'%\n'+res.Mem.MemUsed+'/'+res.Mem.MemTotal;
		chart.setOption(option);	
  }
  function refreshHardwareData(res)
  {
	    var chart = echarts.getInstanceByDom(document.getElementById('Diskused'));
        var option = chart.getOption();
		option.series[0].data[0].value = res.Disk.diskpars[0].parper;
		option.series[0].data[1].value = 100-res.Disk.diskpars[0].parper;
		option.graphic[0].elements[0].style.text = res.Disk.diskpars[0].parper.toString()+'%\n'+res.Disk.diskpars[0].parsizeused+'/'+res.Disk.diskpars[0].parsizetotal;
		chart.setOption(option);	
  }
  function refreshNetData(res)
  {
	  	NetSpeeds = res.Net;
        var chartNet = echarts.getInstanceByDom(document.getElementById('Netused'));
        var option = chartNet.getOption();
		xdata = option.xAxis[0].data
		xdata.push(xdata[xdata.length-1]+1)
		ydataDown = option.series[0].data1
		ydataUp = option.series[1].data1
		ydataDown.push(res.Net[0])
		ydataUp.push(res.Net[1])
		
		units = ['B/s','KB/s','MB/s','GB/s'];
		ydataDownMax = Math.max.apply(null, ydataDown);
		ydataUpMax = Math.max.apply(null, ydataUp);
		//ydataUpMax = ydataUp1.sort().reverse()[0];
		let ydataMax = Math.max.apply(null, [ydataDownMax,ydataUpMax]);;
		let j = 0;
		while (ydataMax>1000)
		{
			ydataMax = ydataMax/1024;
			j = j+1 ;
		}
		unit = units[j]
		
		if (xdata.length >60)
		{
			xdata.pop();
			ydataDown.shift();
			ydataUp.shift();
		}
		option.series[0].data1 = ydataDown;
		option.series[1].data1 = ydataUp;
		let ydataDown1 = [];
		let ydataUp1 = [];
		for(let tmp = 0;tmp<xdata.length;tmp++)
		{
			ydataDown1.push(ydataDown[tmp]/(1024**j));
			ydataUp1.push(ydataUp[tmp]/(1024**j));
		}

        option.series[0].data = ydataDown1;
		option.series[1].data = ydataUp1;
		option.data = xdata;
		option.yAxis[0].name = unit
        chartNet.setOption(option);
  }

  function refreshData()
  {
	  var host = window.location.host;
	  var cookie = document.cookie;
	  var ws = new WebSocket("ws://"+host+"/getSerInfows/");
	  ws.onopen = function(evt) {
			console.log("Connection open ...");
			window.setInteGetSerInfos = setInterval(() => 
			{
				ws.send(JSON.stringify(
				{
				'coks':cookie.replace('coks=','').replace('"','').replace('"',''),
				'SerInfos':1,
				'DiskIndex':1
				}))
			
			}, 1000)
		};
		 
		ws.onmessage = function(evt) {
			
			resdata = JSON.parse(evt.data)
			if (resdata.res==0)
			{
				console.log(resdata)
				ws.close();
				clearInterval(window.setInteGetSerInfos);
				return
			}
			//console.log(resdata)
			refreshNetData(resdata);
			refreshHardwareData(resdata);
			refreshMemData(resdata);
			refreshCpuData(resdata);
		};
		 
		ws.onclose = function(evt) {
			console.log("Connection closed.");
			clearInterval(window.setInteGetSerInfos);
		};

  }
  
 function refreshData1() {
        //刷新数据
		let res = PostMethod('/GetSerInfos/',JSON.stringify({'disk':1}),0);
		//console.log(res);
		refreshNetData(res);
		refreshHardwareData(res);
		refreshMemData(res);
		refreshCpuData(res);
    }
function clearcontent(elementID)
{ 
	var div = document.getElementById(elementID); 
	while(div.firstChild)
	{ 
	    div.removeChild(div.firstChild); 
	}
}

function ModBCstockact(Modedstock)
{
	
	var cookie = document.cookie;
	data = {
		'coks':cookie.replace('coks=','').replace('"','').replace('"',''),
		'ModSBCstock':Modedstock,
	}
	res = sendMessagebyWebScoket(data);
	
}

function ModSBCstockShow(diskinfos)
{
	let ModSBCsctockul = document.getElementById("ModSBCsctockul");
	clearcontent("ModSBCsctockul");
	
	for (let i=0;i<diskinfos.length;i++)
	{
		info = diskinfos[i]
		let parinfo = info.parinfo;
		parsizetotal = info.parsizetotal;
		parsizeused = info.parsizeused;
		parper = info.parper;
		let li = document.createElement("li");
		let a = document.createElement("a");
		a.className = "dropdown-item"
		a.href='javascript:void(0)'
		a.onclick=function(){ModBCstockact(parinfo)}
		a.innerText = parinfo + '  ' +parsizeused+'/'+parsizetotal+'  '+parper.toString()+'%';
		li.appendChild(a);
		ModSBCsctockul.appendChild(li);
		
	}
	
}
function MountDiskShowact(MountedDisk)
{
	var ret = prompt('准备挂载'+MountedDisk+'\n输入要挂载的路径', '/mnt/SBC/');
	if(ret !== null && ret != '') 
	{
　　	MountPath = ret;
	}
	var cookie = document.cookie;
	data = {
		'coks':cookie.replace('coks=','').replace('"','').replace('"',''),
		'MountDisk':MountedDisk,
		'MountPath':MountPath
	}
	res = sendMessagebyWebScoket(data);
}
function MountDiskShow(diskinfos)
{
	let ModSBCsctockul = document.getElementById("MountDiskul");
	clearcontent("MountDiskul");
	
	for (let i=0;i<diskinfos.length;i++)
	{
		info = diskinfos[i]
		let device = info.Device;
		DiskSize = info.DiskSize;
		parsizetotal = DiskSize.total;
		parsizeused = DiskSize.used;
		parper = DiskSize.percent;
		let li = document.createElement("li");
		let a = document.createElement("a");
		a.className = "dropdown-item"
		a.href='javascript:void(0)'
		a.onclick=function(){MountDiskShowact(device)}
		a.innerText = device + '  ' +parsizeused+'/'+parsizetotal+'  '+parper.toString()+'%';
		li.appendChild(a);
		ModSBCsctockul.appendChild(li);
		
	}
	
}

function MountDisk()
{
	var host = window.location.host;
	var cookie = document.cookie;
	var ws = new WebSocket("ws://"+host+"/getSerInfows/");
	ws.onopen = function(evt) 
	    {
			ws.send(JSON.stringify(
				{
				'coks':cookie.replace('coks=','').replace('"','').replace('"',''),
				'GetMountDisks':1,
				}))
			ws.onmessage = function(evt) {
			
			resdata = JSON.parse(evt.data)
			if (resdata.res==0)
			{
				console.log(resdata)
				ws.close();
				return
			}
			console.log(resdata)
			disks = resdata.data;
			MountDiskShow(disks)
			//diskinfos = resdata.Disk.diskpars;
			//ModSBCstockShow(diskinfos);
		};
	    };
}
function ModSBCstock()
{
	  var host = window.location.host;
	  var cookie = document.cookie;
	  var ws = new WebSocket("ws://"+host+"/getSerInfows/");
	  ws.onopen = function(evt) 
	    {
			console.log("Connection open ...");
			ws.send(JSON.stringify(
				{
				'coks':cookie.replace('coks=','').replace('"','').replace('"',''),
				'SerInfos':1,
				}))
	    };
		 
	  ws.onmessage = function(evt) {
			
			resdata = JSON.parse(evt.data)
			if (resdata.res==0)
			{
				console.log(resdata)
				ws.close();
				return
			}
			console.log(resdata)
			diskinfos = resdata.Disk.diskpars;
			ModSBCstockShow(diskinfos);
		};
		 
	  ws.onclose = function(evt) {
			console.log("Connection closed.");
		};
}

function ModLabel(data0)

{
	data = data0.DiskSMARTInfo;
	datasize = data0.DiskSize;
	document.getElementById("TempLabel").innerText = data.Temp;
	document.getElementById("StateLabel").innerText = data.DiskState;
	//document.getElementById("TempLabel").innerText = data.Temp+' &#8451';
	document.getElementById("DeviceModeLabel").innerText = data.DeviceModel;

	document.getElementById("SerialNumberLabel").innerText = '序列号：'+data.SerialNumber;
	document.getElementById("DeviceIDLabel").innerText = '固件号：'+data.FirmwareVersion;
	document.getElementById("HealthStateLabel").innerText = data.SMARToverallhealth;
	if(data.DiskState != '良好')
	{
		document.getElementById("StateLabel").style.color = '#E74C3C';
		document.getElementById("HealthStateLabel").style.backgroundColor = 'yellow';
	}
	document.getElementById("rpmLabel").innerText = data.RotationRate;
	document.getElementById("UsedCapLabel").innerText = datasize.used;
	document.getElementById("TotalCapLabel").innerText = datasize.total;
	document.getElementById("PowerTimeLabel").innerText = data.Power_On_Hours;
	document.getElementById("PowerCountLabel").innerText = data.Power_Cycle_Count;
	document.getElementById("SataModeLabel").innerText = data.SATAVersion;
	
	document.getElementById("tablelabel").innerText = data.ATTRIBUTE;
	
}
 function DiskHealthInfo() {
	  var host = window.location.host;
	  var cookie = document.cookie;
	  var ws = new WebSocket("ws://"+host+"/getSerInfows/");
	  ws.onopen = function(evt) 
	    {
			console.log("Connection open ...");
			ws.send(JSON.stringify(
				{
				'coks':cookie.replace('coks=','').replace('"','').replace('"',''),
				'DiskHealthInfo':1,
				'DiskIndex':1
				}))
	    };
		 
	  ws.onmessage = function(evt) {
			
			resdata = JSON.parse(evt.data)
			if (resdata.res==0)
			{
				console.log(resdata)
				ws.close();
				return
			}
			console.log(resdata);
			ModLabel(resdata);
		};
		 
	  ws.onclose = function(evt) {
			console.log("Connection closed.");
		};
    }
