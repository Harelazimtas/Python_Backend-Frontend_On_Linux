//The url need to start with 'http'
function checkText(){
	let text=document.getElementById("URL").value;
	let label=document.getElementById("errorInsert");
	if(text.substring(0,4)!=="http"){
		label.textContent="Error url don't contain: 'http'";
		return false;	
	}
	label.textContent="";
	return true;
}
