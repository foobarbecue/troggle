
	mnuItmLst=document.getElementsByClassName("menuBarItem")
	function highlight(div){
	for (var i = 0, divIter; divIter = mnuItmLst[i]; i++) {
			if (divIter.style.backgroundColor!="rgb(102, 102, 102)"){
			divIter.style.backgroundColor="#EBEBEB";
			}
		}
		if (div.style.backgroundColor!="rgb(102, 102, 102)"){
			div.style.backgroundColor="#B0B0B0";
		}
	}
	
	function unhighlight(div){
		if (div.style.backgroundColor=="#EBEBEB"){
			div.style.backgroundColor="#EBEBEB";
		}
	}
	
	function choose(div){
		for (var i = 0, divIter; divIter = mnuItmLst[i]; i++) {
			document.getElementById(divIter.id+"Content").style.display="none";
			}
		document.getElementById(div.id+"Content").style.display="block";
		for (var i = 0, divIter; divIter = mnuItmLst[i]; i++) {
			document.getElementById(divIter.id).style.backgroundColor="#EBEBEB";
			}
		div.style.backgroundColor="#666666";
	}
	
	function redirectSurvey(){
		window.location = "{{ settings.URL_ROOT }}/survey/" + document.getElementById("expeditionChooser").value + "%23" + document.getElementById("surveyChooser").value;
		document.getElementById("progressTableContent").style.display='hidden'
	}
	
	function redirectYear(){
		window.location = "{{ settings.URL_ROOT }}/survey/" + document.getElementById("expeditionChooser").value + "%23"
	}

	


