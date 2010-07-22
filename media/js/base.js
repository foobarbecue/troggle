/* The following serves to stretch the content div to the bottom of the margin images, or vice versa

function contentHeight(){
setMaxHeight($(".rightMargin,#content,.leftMargin,#col2"),$("#content"));
};

function setMaxHeight(group, target) {
	tallest = 0;
	group.each(function() {
		thisHeight = $(this).height();
		if(thisHeight > tallest) {
			tallest = thisHeight;
		};
	});
	target.height(tallest);
};

*/

/*This is the jquery stuff */
$(document).ready(function() {

$('#loading').hide()
$('div.figure').width($('div.figure img').width()+40)

//hide the all of the element with class msg_body
$(".collapse_body").hide();
$(".collapse_head").addClass("plus_icon");

//toggle on click header
$(".collapse_head").click(function()
{
$(this).next(".collapse_body").slideToggle(600);
$(this).toggleClass("plus_icon");
$(".collapse_body").not($(this).next(".collapse_body")).slideUp();
});

$('.searchable li').quicksearch({
  position: 'before',
  attached: 'ul.searchable',
  labelText: '',
  loaderText: '',
  delay: 100});

$('table.searchable tr').quicksearch({
  position: 'before',
  attached: 'table.searchable:first'});

$(".toggleMenu").click(function () {
		  $("ul.dropdown li:not(.toggleMenu)").toggle();
		  $(".toggleMenu").toggle();
 });
 
 $("a.closeDiv").click(function () {
		  $(this).parent().hide();
		});

/*$("#footerLinks").hover(
		  function() {$(".footer").fadeIn("slow")},
		  function() {$(".footer").fadeOut("slow")}
);*/

function linkHover(hoverLink,image){

$(hoverLink).bind('mouseover',
		  function() {
                          $(image).stop().css("opacity", "1.0").fadeIn("slow");
/*			  $(hoverLink).css("background","gray");*/
		  });
$(hoverLink).bind('mouseout',
		  function() {
			  $(image).stop().fadeOut("slow");
/*			  $(hoverLink).css("background","black");*/
		  }
);



};

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


/* Cookies */
function setCookie(c_name,value,expiredays)
{
var exdate=new Date();
exdate.setDate(exdate.getDate()+expiredays);
document.cookie=c_name + "=" +escape(value) +
((expiredays==null) ? "" : ";expires="+exdate.toGMTString()) + ";path=/";
}

function getCookie(c_name)
{
if (document.cookie.length>0)
  {
  c_start=document.cookie.indexOf(c_name + "=");
  if (c_start!=-1)
    {
    c_start=c_start + c_name.length+1;
    c_end=document.cookie.indexOf(";",c_start);
    if (c_end==-1) c_end=document.cookie.length;
    return unescape(document.cookie.substring(c_start,c_end));
    }
  }
return "";
};

/* Style Sheet Switcher */
   function switchStylestyle(styleName)
   {
      $('link[@rel*=style][title]').each(function(i)
      {
         this.disabled = true;
         if (this.getAttribute('title') == styleName) this.disabled = false;
      });
   }
