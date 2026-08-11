bloodPressureForm = document.getElementById('bloodpressure-form')


bloodPressureForm.addEventListener('formdata', (event) => {
    const formData = event.formData;
    currentTime = new Date()
    formattedTime = currentTime.toLocaleString('en-US', {month: 'numeric', day:'numeric', year: 'numeric', hour:'numeric', minute:'numeric', second:'numeric', timeZoneName: "short"})
    formData.append('time', formattedTime)
})


