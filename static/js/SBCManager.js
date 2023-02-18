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
		input1.id = i;
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
 
 function UpdateFiles()
 {
	 let res = GetStockUser();
	 var FileNoUser = res.NoUser;
	 var allstockFiles = res.all;
	 Updateact(allstockFiles);
	 
	 return
 }