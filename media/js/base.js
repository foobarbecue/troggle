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
		};
	});
	target.height(tallest);
};



/*This is the jquery stuff */
$(document).ready(function() {

$('.searchable li').quicksearch({
  position: 'before',
  attached: 'ul.searchable',
  labelText: '',
  loaderText: '',
  delay: 100});

$('table.searchable tr').quicksearch({
  position: 'before',
  attached: 'table.searchable:first'});

$(".killEyeCandy").click(function () {
                                         killEyeCandy();
                                         setCookie("eyeCandy", "False", 100);
                                        }
                           );

$(".showEyeCandy").click(function () {
		                         showEyeCandy();
		                         setCookie("eyeCandy", "True", 100);
                                        }
                           );

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

function showEyeCandy(){
contentHeight();
switchStylestyle("eyeCandy");
$("#eyeCandyFooterPopUps").load("/eyecandy");
$(".leftMargin,.rightMargin").show();
$(".showEyeCandy").hide();
$(".killEyeCandy").show();
linkHover("#cavesLink","#richardBanner");
linkHover("#caversLink","#timeMachine");
linkHover("#surveyBinderLink","#surveyHover");
linkHover("#troggle","#timeMachine");
};

function killEyeCandy(){
$("#content").removeAttr("style")
switchStylestyle("plain");
$(".leftMargin,.rightMargin").hide();
$(".showEyeCandy").show();
$(".killEyeCandy").hide();
$("#cavesLink").unbind('mouseover').unbind('mouseout');
$("#caversLink").unbind('mouseover').unbind('mouseout');
$("#surveyBinderLink").unbind('mouseover').unbind('mouseout');
$("#troggle").unbind('mouseover').unbind('mouseout');
};

if (getCookie("eyeCandy") == "False")
    {killEyeCandy();}
else
    {showEyeCandy();
     $(".footer").hide();
     $(".fadeIn").hide();
     setTimeout("$('.leftMargin.fadeIn').fadeIn(3000);",1000);
     setTimeout("$('.rightMargin.fadeIn').fadeIn(3000);",2000);
     }

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