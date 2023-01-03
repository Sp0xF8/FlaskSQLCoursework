$(document).ready(function() {
    $('#form').on('submit', function(event) {


        $.ajax({
            data : {
                destination : $('#destination').val(),
                departing : $('#departing').val()
        },
            type : 'POST',
            url : '/process'
    })
    .done(function(data) {
        
    });


        event.preventDefault();
        
});