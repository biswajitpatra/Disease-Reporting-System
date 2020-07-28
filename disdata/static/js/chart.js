let length = diseases_final.disease_list.length
let diseaseArray = []
let diseaseCount = []
let diseaseLevel = []
let travelFeedback = []
let i =0
if(diseases_final.max_warn === 'success'){
    travelFeedback.push(10, 90)
}
else if(diseases_final.max_warn === 'warning'){
    travelFeedback.push(40, 60)
}
else{
    travelFeedback.push(90, 10)
}
while(length){
     diseaseArray.push(diseases_final.disease_list[i].disease.disease_name)
     diseaseCount.push(diseases_final.disease_list[i].report_count)
     diseaseLevel.push(diseases_final.disease_list[i].disease_level)
     ++i
     --length
}
//doughnut chart
var doughnut = document.getElementById('doughnut');
var doughnutConfig = new Chart(doughnut, {
    type: 'doughnut',
    data: {
        labels: diseaseArray,
        datasets: [{
            label: '# of data',
            data: diseaseLevel,
            backgroundColor: ['rgba(0, 230, 118, 1)', 'rgba(255, 206, 86, 1)', 'rgba(255,99,132,1)', 'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)'],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true, // Instruct chart js to respond nicely.
        maintainAspectRatio: true, // Add to prevent default behaviour of full-width/height 
    }
});
//pie chart
var pie = document.getElementById('pie');
var doughnutConfig = new Chart(pie, {
    type: 'pie',
    data: {
        labels:['Cancelled', 'Went'],
        datasets: [{
            label: '# of data',
            data: travelFeedback,
            backgroundColor: ['rgba(246, 26, 104,1)', 'rgba(0, 230, 118, 1)'],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true, // Instruct chart js to respond nicely.
        maintainAspectRatio: true, // Add to prevent default behaviour of full-width/height 
    }
});
//bar chart

var bar = document.getElementById('bar');
var barConfig = new Chart(bar, {
    type: 'bar',
    data: {
        labels: diseaseArray,
        datasets: [{
            label: '# of data',
            data: diseaseCount,
            backgroundColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)', 'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)', 'rgba(225, 50, 64, 1)', 'rgba(255, 159, 64, 1)'],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        },
        responsive: true, // Instruct chart js to respond nicely.
        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height 
    }
})