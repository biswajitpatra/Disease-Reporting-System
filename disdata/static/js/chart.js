 //*Chart for area reports
 var ctx = document.getElementById('myChart').getContext('2d');
//  console.log(diseases_final)
 

 let length = diseases_final.disease_list.length
 let diseaseArray = []
 let diseaseCount = []
 let i =0
 while(length){
      diseaseArray.push(diseases_final.disease_list[i].disease.disease_name)
      diseaseCount.push(diseases_final.disease_list[i].report_count)
      ++i
      --length
 }
//  console.log(diseaseArray)
 var myRadarChart = new Chart(ctx, {
   type: 'bar',
   data: {
    labels: diseaseArray,
    datasets: [{
         label:'Diseases',
         backgroundColor:'rgba(0,200,132,.5)',
         borderColor:'rgba(0,200,132,1)',
         data: diseaseCount
     }]
 },
 options : {
   responsive : true,
   maintainAspectRatio :false
}
});
