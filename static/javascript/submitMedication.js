medicationForm = document.getElementById('medicationForm')


medicationForm.addEventListener('formdata', (event) => {
    const formData = event.formData;
    currentTime = new Date()
    formattedTime = currentTime.toLocaleString('en-US', {month: 'numeric', day:'numeric', year: 'numeric', hour:'numeric', minute:'numeric', second:'numeric', timeZoneName: "short"})
    formData.append('time', formattedTime)
})

url = '/fetch_medication_entries'
fetch(url).then(response => response.json()).then(data => {
    categories = []
    response = data['medications']
    response.forEach((medication, i) => {
        if (!categories.includes(medication.category)) {
            categories.push(medication.category)
        }
        });
    console.log(categories)
    categories.forEach((category, i) => {
        newDiv = document.createElement('div')
        newDiv.innerHTML = `<div className="container"
                                style="max-width: 400px; margin: 20px auto 20px; padding: 20px; border-radius: 10px; border: 1px solid grey;">`
            medicationForm.appendChild(newDiv)

            response.forEach((medication, i) => {
            newMed = document.createElement('p')
            newMed.classList.add('text-label')
            newMed.innerHTML = `<input style="margin: 5px" class="form-check-input" type="checkbox" id="${medication.id}" name="medication" value="${medication.name} (${medication.dose_mg}mg)">${medication.name}  (${medication.dose_mg}mg)</input>`
            newDiv.appendChild(newMed)
        });

            });

            });