// ?Outbreak Graphs
let length = outbreak_json.length
let diseaseArray = []
let infectionCount = []
let diseaseLevel = []
let deaths = []
let i =0

while(length){
    diseaseArray.push(outbreak_json[i].disease__disease_name)
    infectionCount.push(outbreak_json[i].infected)
    deaths.push(outbreak_json[i].death)
    diseaseLevel.push(outbreak_json[i].disease__morbidity)
    ++i
    --length
}

//doughnut chart
var doughnut = document.getElementById('doughnut-outbreak');
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
var pie = document.getElementById('pie-outbreak');
var doughnutConfig = new Chart(pie, {
    type: 'pie',
    data: {
        labels:diseaseArray,
        datasets: [{
            label: '# of data',
            data: deaths,
            backgroundColor: ['rgba(246, 26, 104,1)', 'rgba(0, 230, 118, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)', 'rgba(75, 192, 192, 1)'],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true, // Instruct chart js to respond nicely.
        maintainAspectRatio: true, // Add to prevent default behaviour of full-width/height 
    }
});

//bar chart
var bar = document.getElementById('bar-outbreak');
var barConfig = new Chart(bar, {
    type: 'bar',
    data: {
        labels: diseaseArray,
        datasets: [{
            label: '# of data',
            data: infectionCount,
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

// ? Current Diseases Graphs
let diseaseLength = diseases_final.disease_list.length
let currentDiseaseArray = []
let currentInfectionArray = []
let currentDiseaseLevel = []
let currentDeaths = []
let j=0
while(diseaseLength){
    currentDiseaseArray.push(diseases_final.disease_list[j].disease.disease_name)   
    currentInfectionArray.push(diseases_final.disease_list[j].report_count)
    currentDiseaseLevel.push(diseases_final.disease_list[j].disease_level)
    currentDeaths.push(diseases_final.disease_list[j].death_count)
    ++j
    --diseaseLength
}
//doughnut chart
var doughnut = document.getElementById('doughnut-disease');
var doughnutConfig = new Chart(doughnut, {
    type: 'doughnut',
    data: {
        labels: currentDiseaseArray,
        datasets: [{
            label: '# of data',
            data: currentDiseaseLevel,
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
var pie = document.getElementById('pie-disease');
var doughnutConfig = new Chart(pie, {
    type: 'pie',
    data: {
        labels:currentDiseaseArray,
        datasets: [{
            label: '# of data',
            data: currentDeaths,
            backgroundColor: ['rgba(246, 26, 104,1)', 'rgba(0, 230, 118, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)', 'rgba(75, 192, 192, 1)'],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true, // Instruct chart js to respond nicely.
        maintainAspectRatio: true, // Add to prevent default behaviour of full-width/height 
    }
});

//bar chart
var bar = document.getElementById('bar-disease');
var barConfig = new Chart(bar, {
    type: 'bar',
    data: {
        labels: currentDiseaseArray,
        datasets: [{
            label: '# of data',
            data: currentInfectionArray,
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