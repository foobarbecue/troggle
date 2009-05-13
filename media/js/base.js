
  function showDiv(collapsed,expanded){
        document.getElementById(collapsed).style.display = 'none';
	document.getElementById(expanded).style.display = 'block';
      }
      
  function hideDiv(collapsed,expanded){
        document.getElementById(collapsed).style.display = 'block';
	document.getElementById(expanded).style.display = 'none';
      }

   function makeDivTransparent(div){
	document.getElementById(div).style.backgroundColor = 'transparent';
      }



hex=0 // Initial color value.
leftPos=25
year=1976
currentDate= new Date()
currentYear = currentDate.getFullYear()
function fadeText(){ 
if(hex<153) { //If color is not black yet
	hex=hex+10; // increase color darkness
	leftPos-=1;
	document.getElementById("expoHeader").style.color="rgb("+0+","+hex+","+0+")";	
//	document.getElementById("expoFinalDate").style.color="rgb("+0+","+hex+","+0+")";	
	document.getElementById("expoHeader").style.left=leftPos;
	setTimeout("fadeText()",50)
	setTimeout("countUpYear()",1000)
}
else {
	hex=0;
	leftPos=25;
}
}

function countUpYear(){
	if (year<currentYear) {
//		alert (year+''+currentYear)
		year=year+1
		document.getElementById("expoFinalDate").innerHTML="<h1>"+year+"</h1>"
		setTimeout("countUpYear()",1000)
	}
}