const bloodPressureTable = document.getElementById('blood-pressure-table')
const pageUpBtn = document.getElementById('page-up')
const pageDownBtn = document.getElementById('page-down')
const pageNumInput = document.getElementById('page-num-input')

pageNumInput.addEventListener('keyup', changePage)
pageUpBtn.addEventListener('click', pageUp)
pageDownBtn.addEventListener('click', pageDown)

function pageUp() {
    pageNumInput.value = parseInt(pageNumInput.value) + 1
    changePage()
}
function pageDown(){
    if (pageNumInput.value > 1){
        pageNumInput.value = parseInt(pageNumInput.value) - 1
    }
    changePage()
}

function changePage(){
    bloodPressureTable.innerHTML = ""
    page_num = pageNumInput.value;
    url = `fetch_table_data/${page_num}`
    fetch(url).then(response => response.json()).then(data => {
        response = data['data']
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
}
changePage()

