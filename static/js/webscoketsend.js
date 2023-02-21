function sendMessagebyWebScoket(data)
{
	var host = window.location.host;
	var ws = new WebSocket("ws://"+host+"/getSerInfows/");
	ws.onopen = function(evt) 
	  {
		ws.send(JSON.stringify(data))
	  };
		 
	ws.onmessage = function(evt) 
	{
		var resdata = JSON.parse(evt.data)
		ws.close();
		return resdata;
	};
		 
	ws.onclose = function(evt) {
		return resdata;
		};
}