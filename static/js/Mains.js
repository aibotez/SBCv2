

function NavMeans(oper)
{
	var Chosed = "rgb(162, 217, 206)";
	var ids = ["NavMeans_Files","NavMeans_Photo","NavMeans_Video","NavMeans_Share"];
	if (document.getElementById(oper).style.backgroundColor == Chosed)
	{
		return;
	}
	
	document.getElementById(oper).style = "background-color:#A2D9CE;border-radius:10px;";
	for(let i=0;i<ids.length;i++)
	{
		if (ids[i] != oper)
		{
			document.getElementById(ids[i]).removeAttribute("style");
		}
	}
	return;
	//document.getElementById(ActId).style.backgroundColor = Chosed;

	
}