/* The following serves to stretch the content div to the bottom of the margin images, or vice versa*/

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


/*This is the jquery stuff */
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

$(".toggleMenu").click(function () {								 
		  $("ul.dropdown li:not(.toggleMenu)").toggle();
		  $(".toggleMenu").toggle();
 });

$(".footer").hide();
$(".fadeIn").hide();
setTimeout("$('.leftMargin.fadeIn').fadeIn(3000);",1000);
setTimeout("$('.rightMargin.fadeIn').fadeIn(3000);",2000);
$("a.closeDiv").click(function () {
		  $(this).parent().hide();
		});

/*$("#footerLinks").hover(
		  function() {$(".footer").fadeIn("slow")},
		  function() {$(".footer").fadeOut("slow")}		  
);*/

function linkHover(hoverLink,image){

$(hoverLink).hover(
		  function() {
			  $(image).fadeIn("slow");
/*			  $(hoverLink).css("background","gray");*/
		  },
		  function() {
			  $(image).fadeOut("slow");
/*			  $(hoverLink).css("background","black");*/
		  }		  
);



};

linkHover("#cavesLink","#richardBanner");
linkHover("#caversLink","#timeMachine");
linkHover("#surveyBinderLink","#surveyHover");
linkHover("#troggle","#timeMachine");

/*dropdown (well, up actually) menu code from http://css-tricks.com/simple-jquery-dropdowns/*/
$("ul.dropdown li").hover(
	function(){
		$(this).addClass("hover");
		$('ul:first',this).css('visibility','visible')
	},
	
	function(){
        $(this).removeClass("hover");
        $('ul:first',this).css('visibility', 'hidden');		
	});

	$("ul.dropdown li ul li:has(ul)").find("a:first").append(" &raquo; ");
/* end dropdown menu code */
	
});

