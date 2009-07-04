 $(document).ready(function(){

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

 });