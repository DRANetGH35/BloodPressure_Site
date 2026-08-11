
async function parseResponse(){
  let systolic = []
  let diastolic = []
  let pulse = []
    url = `/fetch_graph_data`
    const response = await fetch(url)
    let data = await response.json()
  data.forEach((element, i) => {
    timestamp = new Date(element.created).getTime()
    systolicValue = element.systolic
    diastolicValue = element.diastolic
    pulseValue = element.pulse
    systolic.push([timestamp, systolicValue])
    diastolic.push([timestamp, diastolicValue])
    pulse.push([timestamp, pulseValue])
  })
  return {'systolic': systolic,
          'diastolic': diastolic,
          'pulse': pulse
  }
}

async function updateChart() {
  const data = await parseResponse()
  console.log(data.systolic)

  options = {
    series: [{
      name: "BloodPressure",
      data: await data.systolic
    },
    {
        name: "Diastolic",
        data: await data.diastolic
    },
    {
        name: "Pulse",
        data: await data.pulse
    }
    ],
    chart: {
      type: 'area',
      height: 350,
      zoom: {
        enabled: true,
        autoScaleYaxis: true
      }
    },
    dataLabels: {
      enabled: false
    },
    stroke: {
      curve: 'smooth'
    },
    xaxis: {
      type: 'datetime'
    },
    title: {
      text: 'Time Series Example',
      align: 'left'
    }

  }


  var chart = new ApexCharts(document.querySelector('#chart'), options)
  chart.render()
}

updateChart()