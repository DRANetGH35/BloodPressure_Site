const bloodPressureTable = document.getElementById('blood-pressure-table')
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
    bloodPressureTable.innerHTML = ""
    page_num = pageNumInput.value;
    url = `/admin/fetch_users/${page_num}`
    fetch(url).then(response => response.json()).then(data => {
        response = data['data']
        for (i=0; i<response.length; i++){
            user = response[i]
            let newRow = bloodPressureTable.insertRow();

            let nameCell = newRow.insertCell(0);
            let emailCell = newRow.insertCell(1);
            let codeCell = newRow.insertCell(2);
            let verifiedCell = newRow.insertCell(3);
            let adminCell = newRow.insertCell(4);
            let btnCell = newRow.insertCell(5);
            nameCell.classList.add('nameCell')
            emailCell.classList.add('emailCell')
            codeCell.classList.add('codeCell')
            verifiedCell.classList.add('verifiedCell')
            adminCell.classList.add('adminCell')
            btnCell.classList.add('btnCell')

            nameCell.textContent = user.name
            emailCell.textContent = user.email
            codeCell.textContent = user.verification_code
            verifiedCell.textContent = user.verified
            adminCell.textContent = user.is_admin
            btnCell.innerHTML = `<a class='delete-btn' href=/admin/login_as/${user.id}>Login as<a>`;
        }
    })
}
changePage()

