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

                
                
                var result = '';

                result += `<div style="text-align:center; width:100%;">`

                
                var x = 0;
                while(x < parseInt(response[999].index)) {
                    result += `
                            <div class="card text-center mb-3 flightCard" >
                                <div class="card-header">
                                    <h5 class="card-title">` + response[x].departure + `</h5>
                                    <h5 class="card-title">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-down" viewBox="0 0 16 16">
                                            <path fill-rule="evenodd" d="M8 1a.5.5 0 0 1 .5.5v11.793l3.146-3.147a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 .708-.708L7.5 13.293V1.5A.5.5 0 0 1 8 1z"/>
                                        </svg>  
                                    </h5>
                                    <h5 class="card-title">` + response[x].destination + `</h5>
                                </div>
                                <div class="card-body bodyFlightCard">
                                    <div class="card" style="width: 46%; display:inline-block;">
                                        <div class="card-body">
                                            <p class="card-text" style="margin:0; padding:0;">Takeoff</p>
                                            <p class="card-text" style="margin:0; padding:0;">` + response[x].departure_time + `</p>
                                            <hr style="width:70%; margin:auto;">
                                            <p class="card-text" style="margin:0; padding:0;">Landing</p>
                                            <p class="card-text" style="margin:0; padding:0;">` + response[x].arrival_time + `</p>
                                        </div>
                                    </div>
                                    <div class="card" style="width: 46%;display:inline-block;">
                                        <div class="card-body">
                                            <p class="card-text" style="margin:0; padding:0;">Price</p>
                                            <p class="card-text" style="margin:0; padding:0;">£` + response[x].price + `</p>
                                            <hr style="width:70%; margin:auto;">
                                            <p class="card-text" style="margin:0; padding:0;">Total Seats</p>
                                            <p class="card-text" style="margin:0; padding:0;">` + response[x].arrival_time + `</p>
                                        </div>
                                    </div>

                                    <form action="/booking" method="GET">
                                        <input type="date" class="form-control" name="flight_date" required>
                                        <input type="hidden" name="flightID" value="` + response[x].flight_id + `">
                                        <input type="hidden" name="action" value="selectFlight">
                                        <button class="btn btn-primary w-50" type="submit">Book</button>
                                    </form>
                                </div>
                            </div>
                        `
                    x++;
                }
                 

                result += `</div>`

                
                document.getElementById('editable').innerHTML = result;
            }

        })
    });
})