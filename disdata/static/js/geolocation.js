
   const knowMyLocation = () => {
     
       options = {
           enableHighAccuracy:true
       }
    if(navigator.geolocation){
        navigator.geolocation.watchPosition(showPosition, error, options);
    }
    else{
        $('#user-location').html('Browser does not support geolocation')
    }
    function error(err) {
        console.warn('ERROR(' + err.code + '): ' + err.message);
      }
    function showPosition(position){

        // $('#user-location').html(`Latitude: ${position.coords.latitude} , Longitude: ${position.coords.longitude}`)

        let locationAPI = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${position.coords.latitude},${position.coords.longitude}&key=AIzaSyDI0rZJabSHwnaVtPU71KsqokaqowHSQ70` 
        // let locationAPI = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=AIzaSyDI0rZJabSHwnaVtPU71KsqokaqowHSQ70'

        $.get({
            url: locationAPI,
            success: function(data) {
                console.log(data);
                const length = data.results.length;
                // $('#location-search').attr('placeholder',`${data.results[length-3].formatted_address}`)
                $('#location-search').attr('placeholder',`${data.plus_code.compound_code.slice(7)}`)
                // $('#user-location').html(`You are currently at :${data.results[length-3].formatted_address}`);
            }
        })
    }
   }