const TimeSelect = document.getElementById('time-select')
const WindowSelect = document.getElementById('window-select')
const SystolicCheck = document.getElementById('systolic-check')
const DiastolicCheck = document.getElementById('diastolic-check')
const PulseCheck = document.getElementById('pulse-check')

const ctx = document.getElementById("dbChart").getContext('2d');
TimeSelect.addEventListener('change', updateGraph)
WindowSelect.addEventListener('change', updateGraph)
SystolicCheck.addEventListener('click', updateGraph)
DiastolicCheck.addEventListener('click', updateGraph)
PulseCheck.addEventListener('click', updateGraph)

async function ParseResponse(rolling_window, days){
    let response_data
    url = `/fetch_graph_data`
    labels = []
    systolic = []
    diastolic = []
    pulse = []
    const response = await fetch(url)
    let data = await response.json()
    data = timeLimit(data, days)
    data.forEach((element, i) => {
        const dateObj = new Date(element['created'])
        const formattedDate = new Intl.DateTimeFormat('en-US').format(dateObj)
        labels.push(formattedDate)
        if (SystolicCheck.checked){systolic.push(element['systolic'])}
        if (DiastolicCheck.checked){diastolic.push(element['diastolic'])}
        if (PulseCheck.checked){pulse.push(element['pulse'])}

    })
    if (rolling_window !== 0){
        if (SystolicCheck.checked){systolic_rolling = RollingAverageOf(systolic, rolling_window)}else{systolic_rolling=null}
        if (DiastolicCheck.checked){diastolic_rolling = RollingAverageOf(diastolic, rolling_window)}else{diastolic_rolling=null}
        if (PulseCheck.checked){pulse_rolling = RollingAverageOf(pulse, rolling_window)}else{pulse_rolling=null}
        }
    response_data = {
        "labels": labels,
        "systolic": systolic,
        "systolic_rolling": systolic_rolling,
        "diastolic": diastolic,
        "diastolic_rolling": diastolic_rolling,
        "pulse": pulse,
        "pulse_rolling": pulse_rolling
    }
    return response_data

}

function timeLimit(data, days){
    new_data = []
    const cutoffDate = new Date(Date.now() - days * 24 * 60 * 60 * 1000) //days x hours x mins x seconds x ms

    data.forEach((entry, i) => {
        entryDate = Date.parse(entry.created)
        if (entryDate > cutoffDate){
            new_data.push(entry)
        }
    })
    return new_data
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

    const existingChart = Chart.getChart("dbChart")
    if (existingChart){
        existingChart.destroy();
    }

    rolling_window = WindowSelect.value
    days = TimeSelect.value
    const response = await ParseResponse(rolling_window, days)
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
    },
    scales: {
            x: {
                grid: {
                    color: 'rgba(255, 255, 255, .5)',
                    linewidth: 1
                }
            },
            y: {
                grid: {
                    color: 'rgba(255, 255, 255, .5)'
                },
                beginAtZero: false
            }
    }
}
}
    new Chart(ctx, cfg)
}

updateGraph()


