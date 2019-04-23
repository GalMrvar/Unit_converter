function startMining(currency){
    var ps = require("python-shell")
    var path = require("path")

    var options = {
        scriptPath : path.join(__dirname, '/../../'),
        args : [currency]
    }
    ps.PythonShell.run('hello.py',options,function(err, results){
		if(err) throw err;
		//swal(results[0]);
		document.getElementById("vaja").innerHTML = results[0];
	});
    //var cur = new python('Miner.py', options);
    
   // cur.on('message',function(message){
    //    alert("kurac");
    //    swal(message);
   // })

}
jQuery(document).ready(function($) {
	//$("#content").show(200);
	$("#wallets").submit(function(e){
		e.preventDefault();
	});
});