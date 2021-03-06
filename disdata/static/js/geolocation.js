
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
                const pincode = data.results[0].address_components.filter(d => d.types.includes('postal_code'))[0].long_name
                const district = data.results[0].address_components.filter(d => d.types.includes('administrative_area_level_2'))[0].long_name
                console.log(pincode);
                console.log(district);
                // $("#pincode-field").val(pincode)
                // $('#location-search').html(`${data.plus_code.compound_code.slice(7)}`)
                let userLocation = {
                    id:pincode,
                    text:`${district}, ${pincode}`
                }
                $("#optionList").append(new Option(userLocation.text, userLocation.id, false, true))
                // $('#optionList').html(`${district}, ${pincode}`)
            }
        })
    }
   }

   function searchLocation() {
       pincode = $('#optionList').val();
       window.location = `/area/${pincode}`
   }
  