 //*Chart for area reports
 var ctx = document.getElementById('myChart').getContext('2d');
 var myRadarChart = new Chart(ctx, {
   type: 'bar',
   data: {
     labels: ['Running', 'Swimming', 'Eating', 'Cycling'],
     datasets: [{
         label:'Disease1',
         backgroundColor:'rgba(0,200,132,.5)',
         borderColor:'rgba(0,200,132,1)',
         data: [20, 10, 4, 2]
     }]
 },
 options : {
   responsive : true,
   maintainAspectRatio :false
}
});
