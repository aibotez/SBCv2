

function NavMeans(oper)
{

	var Chosed = "#A2D9CE";
	var unChosed = "#ADADAD";
	if(oper == "Files")
	{
		ActId = "NavMeans_Files";
		if (document.getElementById(ActId).style.backgroundColor == Chosed)
		{
			return;
		}
		else{
			document.getElementById(ActId).style.backgroundColor = Chosed;
			document.getElementById("NavMeans_NetSet").style.backgroundColor = unChosed;
			return;
		}
	}
	
	if(oper == "NetSet")
	{
		ActId = "NavMeans_NetSet";
		if (document.getElementById(ActId).style.backgroundColor == Chosed)
		{
			return;
		}
		else{
			document.getElementById(ActId).style.backgroundColor = Chosed;
			document.getElementById("NavMeans_Files").style.backgroundColor = unChosed;
			return;
		}
	}
	
}