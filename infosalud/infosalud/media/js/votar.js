/* $(function() {
        $('.star').click(function(){
        	
          $(this).addClass('on rating');
          $(this).prevAll().addClass('on rating');
          $(this).nextAll().removeClass('on rating');  
          //	How to select the parent div of 'this'?
          $(this).parent().addClass('rated');
          var hit_id = $('#hit_id').val()
          var n_votos = $('#n_votos').val()
          var m_votos = $('#m_votos').val()
          var rating = $(this).siblings().add(this).filter('.rating').length
          $.ajax({
                    url:"/rate/",
                    type: "GET",
                    data: ({'id':hit_id}),
                    async: false,
                    success: function(data){
                        $('.votado').html(data)
                    },
                    error:function (xhr, ajaxOptions, thrownError){
                        alert(thrownError);
                    },
                });
        });
      });

      $(function() {
        $('.star').hover(
          function(){
            $(this).addClass('on');
            $(this).prevAll().addClass('on');
            $(this).nextAll().removeClass('on');
          },
          function(){
            $(this).siblings().add(this).removeClass('on');
            $(this).siblings().add(this).filter('.rating').addClass('on');
          }
        );
      }); */

$(document).ready(function()
{
$("span.on_img").mouseover(function ()
{
$(this).addClass("over_img");
});

$("span.on_img").mouseout(function ()
{
$(this).removeClass("over_img");
});
});

//Show The Love
$(function() {
$(".love").click(function() 
{
var hit_id = $('#hit_id').val()
var dataString = 'id='+ hit_id ;
var parent = $(this);
$(this).fadeOut(300);
$.ajax({
type: "GET",
url: "/rate/",
data: dataString,
cache: false,
success: function(html)
{
parent.html(html);
parent.fadeIn(300);
} 
});
return false;
});
});
