function searchDisease(){


    let disease_name = $('#disease_name').val()
    let state_code = $("#state_code").val()
    let month = $('input[type=radio]:checked').val() 
    console.log('Search Started')
    let table, tableContent
    $.ajax({
      type:"GET",
      url:`scrap_ndres_data/${disease_name}/${month}/${state_code}`
    }).done(function(data) {
      console.log(data);
     if(data.status){

       let table = `<table class="table table-bordered table-hover mx-auto w-75 mt-5 text-center"><thead class="thead-dark"><tr>
         ${data.headers.map((tableHeader) => {
           return `<th scope="col">${tableHeader}</th>`
         }).join("")}
       </tr></thead><tbody id="tbody"></tbody></table>`
       $('#table').html(table)
       data.values.map(function(value) {

      let tableContent = `<tr>
       ${value.map((tableData) => {
           return `<td>${tableData}</td>`
         }).join("")}
      </tr>`
      $('#tbody').append(tableContent)
     })
     $('#table').append(`<div class="container"><div class="card p-3 border-danger "><div class="card-block"><p class="text-center text-secondary"><span class="text-info">Precaution</span>: ${data.precaution}</p></div></div></div>`)
     }
     else{
       $('#table').html(`<h4 class="card-text text-center text-success mt-5">No districts of ${$('#state_code option:selected').text()} in risk of <span class="text-danger">${$('#disease_name option:selected').text()}</span> for <span class="text-danger">${$('input[type=radio]:checked').siblings('.form-check-label').text()}</span></h4>`)
     }
      
    })
  }  