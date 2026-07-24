url = `/fetch_graph_data`

const ctx = document.getElementById("dbChart").getContext('2d');
fetch(url).then(response => response.json()).then(data => {
    new Chart(ctx, {
    type: 'line',
    data: {
        labels: data.labels,
        datasets: [{
            label: 'Systolic',
            data: data.systolic,
            borderColor: 'rgb(59, 130, 246)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 1,
            tension: .3,
            fill: false,
            pointRadius: 1
            },

            {
            label: 'systolic rolling',
            data: data.systolic_rolling,
            borderColor: 'rgb(0, 0, 246)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 2,
            tension: 0.3,
            fill: false,
            pointRadius: 3
            },
            {
            label: 'Diastolic',
            data: data.diastolic,
            borderColor: 'rgb(246, 46, 59)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 1,
            tension: 0.3,
            fill: false,
            pointRadius: 1
            },
            {
            label: 'Diastolic rolling',
            data: data.diastolic_rolling,
            borderColor: 'rgb(246, 0, 0)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 2,
            tension: 0.3,
            fill: false,
            pointRadius: 3
            },
            {
            label: 'Pulse',
            data: data.pulse,
            borderColor: 'rgb(50, 246, 59)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 1,
            tension: 0.3,
            fill: false,
            pointRadius: 1
            },
            {
            label: 'Pulse rolling',
            data: data.pulse_rolling,
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

