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
    medications = data['medications']
    categories = data['categories']
    console.log(categories)
    categories.forEach((category, i) => {
            newDiv = `<div id="${category.name}" class="CategoryDiv"
                                style=""><h3>${category.name}</h3></div>`
            medicationForm.insertAdjacentHTML('beforeend', newDiv)
            newDiv = document.getElementById(category.name)
            medications.forEach((med, i) => {
                if(med.category == category.name){
                    //TODO: fix delete btn class function
                    newMed =    `<div class="medBubble">
                                    <input class="form-check-input" type="checkbox" id="${med.id}" name="medication" value="${med.name} (${med.dose_mg}mg)"></input>
                                    <label for="medication">${med.name}  (${med.dose_mg}mg)</label>
                                    <a href="/delete_medication/${med.id}" class="delete-btn">delete</a>
                                </div>`
                    newDiv.insertAdjacentHTML('beforeend', newMed)
                }
            });
            addNewMedBtn = `<div style="margin: 20px;"><a style="margin: 5px;" href="add_new_medication/${category.id}" class="btn-special">add new med</a></div>`
            newDiv.insertAdjacentHTML('beforeend', addNewMedBtn)
            });

            });