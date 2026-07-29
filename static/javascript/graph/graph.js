url = `/fetch_graph_data`
const ctx = document.getElementById("dbChart").getContext('2d');
fetch(url).then(response => response.json()).then(data => {
    const window = 3
    labels = []
    systolic = []
    systolic_rolling = []
    diastolic = []
    diastolic_rolling = []
    pulse = []
    pulse_rolling = []

    data.forEach((element, i) => {
        const dateObj = new Date(element['created'])
        const formattedDate = new Intl.DateTimeFormat('en-US').format(dateObj)
        labels.push(formattedDate)
        systolic.push(element['systolic'])
        diastolic.push(element['diastolic'])
        pulse.push(element['pulse'])
        if (i < (parseInt(window) - 1)) {
            systolic_rolling.push(null)
            diastolic_rolling.push(null)
            pulse_rolling.push(null)
        }else{
            systolic_window_vals = systolic.slice((i - window + 1), (i + 1))
            diastolic_window_vals = diastolic.slice(i - window + 1, i + 1)
            pulse_window_vals = pulse.slice(i - window + 1, i + 1)

            systolic_rolling.push(systolic_window_vals.reduce((sum, num) => sum + num, 0) / systolic_window_vals.length)
            diastolic_rolling.push(diastolic_window_vals.reduce((sum, num) => sum + num, 0) / diastolic_window_vals.length)
            pulse_rolling.push(pulse_window_vals.reduce((sum, num) => sum + num, 0) / pulse_window_vals.length)


        }
    });

    new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Systolic',
            data: systolic,
            borderColor: 'rgb(59, 130, 246)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 1,
            tension: .3,
            fill: false,
            pointRadius: 1
            },

            {
            label: 'systolic rolling',
            data: systolic_rolling,
            borderColor: 'rgb(0, 0, 246)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 2,
            tension: 0.3,
            fill: false,
            pointRadius: 3
            },
            {
            label: 'Diastolic',
            data: diastolic,
            borderColor: 'rgb(246, 46, 59)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 1,
            tension: 0.3,
            fill: false,
            pointRadius: 1
            },
            {
            label: 'Diastolic rolling',
            data: diastolic_rolling,
            borderColor: 'rgb(246, 0, 0)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 2,
            tension: 0.3,
            fill: false,
            pointRadius: 3
            },
            {
            label: 'Pulse',
            data: pulse,
            borderColor: 'rgb(50, 246, 59)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 1,
            tension: 0.3,
            fill: false,
            pointRadius: 1
            },
            {
            label: 'Pulse rolling',
            data: pulse_rolling,
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
})
    })

