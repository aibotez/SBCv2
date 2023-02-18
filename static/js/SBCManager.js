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