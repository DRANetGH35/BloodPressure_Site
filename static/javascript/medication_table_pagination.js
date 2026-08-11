const medicationTable = document.getElementById('medication_table')
const pageUpBtn = document.getElementById('page-up')
const pageDownBtn = document.getElementById('page-down')
const pageNumInput = document.getElementById('page-num-input')

pageNumInput.addEventListener('change', changePage)
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
    medicationTable.innerHTML = ""
    page_num = pageNumInput.value;
    url = `fetch_medication_table_data/${page_num}`
    fetch(url).then(response => response.json()).then(data => {
        response = data['data']
        for (i=0; i<response.length; i++){
            entry = response[i]
            let newRow = medicationTable.insertRow();

            let timeCell = newRow.insertCell(0);
            let medListCell = newRow.insertCell(1);
            let btnCell = newRow.insertCell(2);

            timeCell.classList.add('timeCell');
            medListCell.classList.add('medListCell');
            let timeCreated = new Date(entry.created);
            timeCell.textContent = timeCreated.toLocaleString('en-US');


            let medList = JSON.parse(entry.medication.replace(/'/g, '"'))

            medListCell.innerHTML = `<div class="tooltip">List..
                                        <span id="tooltip_${i}" class="tooltiptext"></span>
                                        </div>`;
            medList.forEach((element) => {
                let tooltip = document.getElementById(`tooltip_${i}`)
                tooltip.innerHTML = tooltip.innerHTML += `<br><p>${element}</p>`
            });
            btnCell.innerHTML = `<a class='delete-btn' href=/delete_medication_entry/${entry.id}>delete<a>`;
        }
    })
}
changePage()

