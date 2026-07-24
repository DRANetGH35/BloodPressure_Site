const bloodPressureTable = document.getElementById('blood-pressure-table')

page_num = 1
const USFormatter = new Intl.DateTimeFormat('en-US', {
  dateStyle: 'short',
  timeStyle: 'medium'
});




url = `fetch_table_data/${page_num}`
fetch(url).then(response => response.json()).then(data => {
        response = data['data']
        console.log(response)
        for (i=0; i<response.length; i++){
            entry = response[i]
            let newRow = bloodPressureTable.insertRow();

            let timeCell = newRow.insertCell(0);

            let systolicCell = newRow.insertCell(1);
            let diastolicCell = newRow.insertCell(2);
            let pulseCell = newRow.insertCell(3);
            let noteCell = newRow.insertCell(4);

            let timeCreated = new Date(entry.created)
            timeCell.textContent = timeCreated.toLocaleString('en-US');
            systolicCell.textContent = entry.systolic;
            diastolicCell.textContent = entry.diastolic;
            pulseCell.textContent = entry.pulse;
            noteCell.textContent = entry.notes;
        }
    })