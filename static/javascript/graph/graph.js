url = `/fetch_graph_data`

const ctx = document.getElementById("dbChart").getContext('2d');
fetch(url).then(response => response.json()).then(data => {
    console.log(data.labels);
    console.log(data.systolic);
    console.log(data.diastolic);
    console.log(data.pulse);

    new Chart(ctx, {
    type: 'line',
    data: {
        labels: data.labels,
        datasets: [{
            label: 'Systolic',
            data: data.systolic,
            borderColor: 'rgb(59, 130, 246)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 2,
            tension: 0.3,
            fill: true,
            pointRadius: 3
            },
            {
            label: 'Diastolic',
            data: data.diastolic,
            borderColor: 'rgb(246, 46, 59)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 2,
            tension: 0.3,
            fill: true,
            pointRadius: 3
            },
            {
            label: 'Pulse',
            data: data.diastolic,
            borderColor: 'rgb(50, 246, 59)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 2,
            tension: 0.3,
            fill: true,
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

