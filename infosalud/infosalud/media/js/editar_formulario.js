$(function() {
        $('#editar').click(function(){
            var id_user =  $('#id_medico').val()
          $.ajax({
                    url:"/editar_perfil/"+id_user,
                    type: "GET",
                    data: ({}),
                    async: false,
                    success: function(data){
                        $('#mostrar_info_perfil').html(data)
                    },
                    error:function (xhr, ajaxOptions, thrownError){
                        alert(thrownError);
                    },
                });

        });
        });
$(function() {
        $('#crear_paciente').click(function(){
            var id_user =  $('#id_medico').val()
          $.ajax({
                    url:"/crear_paciente/",
                    type: "GET",
                    data: ({}),
                    async: false,
                    success: function(data){
                        $('#mostrar_info_perfil').html(data)
                    },
                    error:function (xhr, ajaxOptions, thrownError){
                        alert(thrownError);
                    },
                });

        });
        });
  /*$('#form_perfil').live('submit', function(event) { // catch the form's submit event
          event.preventDefault(); 
          var id_email =  $('#id_email').val()
           var id_user =  $('#id_medico').val()
          $.ajax({
                    url:"/editar/"+id_user,
                    type: "POST",
                    data: id_email,
                    async: false,
                    success: function(data){
                        $('#mostrar_contenido').html(data)
                    },
                    error:function (xhr, ajaxOptions, thrownError){
                        alert(thrownError);
                    },
                });
          return false;
        });
*//*
$('#id_email').live('keypress',function () { 

    var email_user =  $('#id_email').val()
    alert(email_user)
          $.ajax({
                    url:"/verificar/"+email_user,
                    type: "GET",
                    data: ({}),
                    async: false,
                    success: function(data){
                        alert(data)
                    },
                    error:function (xhr, ajaxOptions, thrownError){
                        alert(thrownError);
                    },
                });

});*/

// Mostramos la ventana
$( '#show-modal' ).live( 'click', function( ev ) {
  $( '#modal' ).fadeIn();
  $( '#modal-background' ).fadeTo( 500, .5 );
  ev.preventDefault();
} );

// Escondemos la ventana
$( '.close-modal' ).live( 'click', function( ev ) {
  $( '#modal, #modal-background' ).fadeOut();
  ev.preventDefault();
} );

