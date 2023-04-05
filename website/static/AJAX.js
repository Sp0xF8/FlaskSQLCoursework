$(document).ready(function() {
    $("#searchFlights").click(function() {
        $.ajax({
            url: '/search',
            type: 'get',
            contentType: 'application/json',
            data: {
                departure: $('#departure').val(),
                destination: $('#destination').val(),
            },
            success: function(response) {

                alert(response.departure)
                alert(response.destination)

                var result = '';
                
                result += `
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">` + response.departure + `</h5>
                                <br>
                                <h6 class="card-title">` + response.destination + `</h6>
                                <br>
                            </div>
                        </div>
                                
                            
                        
                        `
                
                document.getElementById('editable').innerHTML = result;
            }

        })


    })
})