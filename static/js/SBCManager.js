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
	var pieHuan = echarts.init(document.getElementById('CPUused'));
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
        pieHuan.setOption(pieHuanOption);
 }
  function MemusedShow()
 {
	var pieHuan = echarts.init(document.getElementById('Memused'));
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
	            text: '100GB/7TB',
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
                        { value: 3, name: '已使用' },
                        { value: 7, name: '剩余' }
                    ]
                }
            ]
        };
        pieHuan.setOption(pieHuanOption);
 }
 function DiskusedShow()
 {
	var pieHuan = echarts.init(document.getElementById('Diskused'));
        pieHuanOption = {
            // 标题
            title: {
				left:'center',
                text: '磁盘用量'
            },
            // 不同区域的颜色
            color: ['#65a5ff', '#dcebff'],

	    graphic: {
	        type: 'text',
	        top: 'center',
	        left: 'center',
	        zlevel:0,
	        style: {
	            text: '100GB/7TB',
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
                        { value: 3, name: '已使用' },
                        { value: 7, name: '剩余' }
                    ]
                }
            ]
        };
        pieHuan.setOption(pieHuanOption);
 }
 
 function NetWork()
 {
	 // 基于准备好的dom，初始化echarts实例
	var myChart = echarts.init(document.getElementById('Netused'));
	// 指定图表的配置项和数据
	var option = {
	title:{left:'center',
	text:'网络',
	//subtext:'数据纯属虚构',
	},
	legend: {
		
		data: ["下载", "上传"],
        top: "10%",
        textStyle: {
            color: "#1FC3CE",
            fontSize: 14
		},
	},

	xAxis: {
	type: 'category',
	boundaryGap: false,
	data: ['1','2','3','4','5','6']
	},
	yAxis: {
	type: 'value'
	},
	series: [
		{
			name: "下载",
			symbol: 'none',
			data: [920, 801, 964, 1390, 1530, 1620],
			type: 'line',
			areaStyle: {}
		},
		{
			name: "上传",
			symbol: 'none',
			data: [420, 932, 901, 934, 1290, 1330],
			//stack: '总量',
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
	myChart.setOption(option);
	 
 }