
async function areaReport(data={}) {
    const response = await fetch('/area_summary_api',{
        method: 'POST',
        body: JSON.stringify(data)
    })
    return response.json()

}


areaReport({`pincode:'${pincode}'`})
    .then(data => {
        console.log(data)
    })