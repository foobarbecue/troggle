
$(document).ready(function() { 

$('.searchable li').quicksearch({
  position: 'before',
  attached: 'ul.searchable',
  labelText: '',
  loaderText: '',
  delay: 100
})

$('table.searchable tr').quicksearch({
  position: 'before',
  attached: 'table.searchable:first',
});

$(".toggleEyeCandy").click(function () {
		  $(".leftMargin,.rightMargin").toggle("fade");
		  $(".toggleEyeCandy").toggle();
 });

$(".nav").css('opacity','7')
$(".footer").hide();
$(".fadeIn").hide();
setTimeout("$('.leftMargin.fadeIn').fadeIn(3000);",1000);
setTimeout("$('.rightMargin.fadeIn').fadeIn(3000);",2000);


/*$("#footerLinks").hover(
		  function() {$(".footer").fadeIn("slow")},
		  function() {$(".footer").fadeOut("slow")}		  
);*/

function linkHover(hoverLink,image){

$(hoverLink).hover(
		  function() {
			  $(image).fadeIn("slow");
			  $(hoverLink).css("background","gray");
		  },
		  function() {
			  $(image).fadeOut("slow");
			  $(hoverLink).css("background","black");
		  }		  
);



};

linkHover("#expoWebsiteLink","#richardBanner");
linkHover("#cuccLink","#timeMachine");
linkHover("#surveyBinderLink","#surveyHover");
linkHover("#troggle","#timeMachine");


});

function contentHeight(){
setMaxHeight($(".rightMargin,#content,.leftMargin,#col2"),$("#content"));
};

function setMaxHeight(group, target) {
	tallest = 0;
	group.each(function() {
		thisHeight = $(this).height();
		if(thisHeight > tallest) {
			tallest = thisHeight;
		}
	});
	target.height(tallest);
}


