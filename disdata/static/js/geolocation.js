$(document).ready(() => {
    
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(showPosition);
    }
    else{
        $('#user-location').html('Not supporting')
    }

    function showPosition(position){

        // $('#user-location').html(`Latitude: ${position.coords.latitude} , Longitude: ${position.coords.longitude}`)

        let locationAPI = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${position.coords.latitude},${position.coords.longitude}&key=AIzaSyDI0rZJabSHwnaVtPU71KsqokaqowHSQ70` 
        // let locationAPI = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=AIzaSyDI0rZJabSHwnaVtPU71KsqokaqowHSQ70'

        $.get({
            url: locationAPI,
            success: function(data) {
                console.log(data);
                $('#user-location').html(`You are currently at :${data.results[7].formatted_address}`);
            }
        })
    }
})