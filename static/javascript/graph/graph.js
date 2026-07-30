const TimeSelect = document.getElementById('time-select')
const WindowSelect = document.getElementById('window-select')
const ctx = document.getElementById("dbChart").getContext('2d');
TimeSelect.addEventListener('change', updateGraph)
WindowSelect.addEventListener('change', updateGraph)

async function ParseResponse(window){
    let response_data
    window = 30
    url = `/fetch_graph_data`
    labels = []
    systolic = []
    systolic_rolling = []
    diastolic = []
    diastolic_rolling = []
    pulse = []
    pulse_rolling = []
    const response = await fetch(url)
    const data = await response.json()
    data.forEach((element, i) => {
        const dateObj = new Date(element['created'])
        const formattedDate = new Intl.DateTimeFormat('en-US').format(dateObj)
        labels.push(formattedDate)
        systolic.push(element['systolic'])
        diastolic.push(element['diastolic'])
        pulse.push(element['pulse'])
        systolic_rolling = RollingAverageOf(systolic, window)
        diastolic_rolling = RollingAverageOf(diastolic, window)
        pulse_rolling = RollingAverageOf(pulse, window)

        response_data = {
        "labels": labels,
        "systolic": systolic,
        "systolic_rolling": systolic_rolling,
        "diastolic": diastolic,
        "diastolic_rolling": diastolic_rolling,
        "pulse": pulse,
        "pulse_rolling": pulse_rolling
    }
    }

    )
    return response_data

}

function RollingAverageOf(data, window){
    let rolling_values = []
    data.forEach((element, i) => {
        if (i < (parseInt(window) - 1)) {
            rolling_values.push(null)
        }else{
            window_vals = data.slice((i - window + 1), (i + 1))
            rolling_values.push(window_vals.reduce((sum, num) => sum + num, 0) / window_vals.length)
        }
    })
    return rolling_values
}

async function updateGraph(){
    window = 30
    const existingChart = Chart.getChart("dbChart")
    if (existingChart){
        existingChart.destroy();
    }


    const response = await ParseResponse(window)
    let cfg = {
    type: 'line',
    data: {
        labels: response.labels,
        datasets: [{
            label: 'Systolic',
            data: response.systolic,
            borderColor: 'rgb(59, 130, 246)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 1,
            tension: .3,
            fill: false,
            pointRadius: 1
            },

            {
            label: 'systolic rolling',
            data: response.systolic_rolling,
            borderColor: 'rgb(0, 0, 246)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 2,
            tension: 0.3,
            fill: false,
            pointRadius: 3
            },
            {
            label: 'Diastolic',
            data: response.diastolic,
            borderColor: 'rgb(246, 46, 59)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 1,
            tension: 0.3,
            fill: false,
            pointRadius: 1
            },
            {
            label: 'Diastolic rolling',
            data: response.diastolic_rolling,
            borderColor: 'rgb(246, 0, 0)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 2,
            tension: 0.3,
            fill: false,
            pointRadius: 3
            },
            {
            label: 'Pulse',
            data: response.pulse,
            borderColor: 'rgb(50, 246, 59)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 1,
            tension: 0.3,
            fill: false,
            pointRadius: 1
            },
            {
            label: 'Pulse rolling',
            data: response.pulse_rolling,
            borderColor: 'rgb(0, 246, 0)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 2,
            tension: 0.3,
            fill: false,
            pointRadius: 3
            }
        ]
    },
    options:{
        responsive: true,
        plugins: {
            legend: { display: true
        },
        scales: {
            y: {
                beginAtZero: false
            }
        }
    }
}
}
    new Chart(ctx, cfg)
}

updateGraph()


