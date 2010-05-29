 $(document).ready(function(){

/*begin ajax query stuff for getting next QM number*/
$('.number:first').append("<a href='javascript:void(0)'  class='next_qm_link'>get next number</a>");

new_qm_link=function(e){
if ($('#id_cave:first')[0].value != "")
{

$.post('/newqmnumber/',{'cave':$('#id_cave')[0].value,'year':$('#id_expedition')[0].value}, function(data){
    $('#id_QMs_found-0-number')[0].value=data;
});
}
else {
alert('Please choose a cave and try again.')
};
};

$('.next_qm_link').bind("click", new_qm_link);
/*end ajax query stuff for getting next QM number*/

/*begin ajax query stuff for getting suggestions view*/



suggestions_query=function(){
slug=$('#id_slug')[0].value;
date=$('#id_date')[0].value;
$.post('/lbo_suggestions/',{'slug':slug,'date':date}, function(data){
    if ($('#suggestions').length>0){
    $('#suggestions').replaceWith(data);
    }
    else{
    $('#id_text').parent().append(data);
    }
});
};

$('#id_text').parent().append("<a href='javascript:void(0)'  class='update_suggestions'>get / update suggestions</a>");

$(".update_suggestions").bind("click", suggestions_query);

replace=function(from,to){
    $('#id_text').text($('#id_text').text().replace(from,to))
    $('[name=_continue]').click()
    
    }

suggestions_query();
/*end*/



/*begin reccomendations stuff*/


/*search for QMs
suspect_QMs=$('#id_text')[0].value.match(/\b(\d\d)-(\d\d\w?)\b/g);
linked_QMs=

$('#suggestions').append(
"\
<h2>May I reccomend:</h2>\
Putting in wikilinks for the following QMs:\
"
);
$('#suggestions').append('<li>'+suspect_QMs.join('</li><li>')+</li>);*/


/*end reccomendations stuff*/








 });