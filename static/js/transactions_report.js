const myForm = document.forms[0];
const transactionTypeInCheckbox = document.getElementById("transaction-type-in");
const transactionTypeOutCheckbox = document.getElementById("transaction-type-out");
const materialGroupSelect = document.getElementById("material-group");
const materialSelect = document.getElementById("material");
const dateFromBox = document.getElementById("date-from");
const dateToBox = document.getElementById("date-to");
// const resultsTable = document.getElementById('results-table');
const resultsTable = $('#results-table');

var DateTime = luxon.DateTime; // https://moment.github.io/luxon/#/install
const ALL_VALUES_ID = 'all';

document.addEventListener('DOMContentLoaded', function() {

    // fill Date boxes
    dateFromBox.value = DateTime.now().startOf('month').toISODate();
    dateToBox.value = DateTime.now().endOf('month').toISODate();

    // Type IN event listener
    transactionTypeInCheckbox.addEventListener('change', (event) => {
        updateReport();
    });

    // Type OUT event listener
    transactionTypeOutCheckbox.addEventListener('change', (event) => {
        updateReport();
    });

    // Material Group change event listener
    materialGroupSelect.addEventListener('change', (event) => {
        populateMaterialSelect(materialGroupSelect.value);
        updateReport();
    });

    // Material change event listener
    materialSelect.addEventListener('change', (event) => {
        // update material group selection
        materialGroupSelect.value = materialSelect.options[materialSelect.selectedIndex].getAttribute('data-groupid')
        updateReport();
    });

    // DateFrom event listener
    dateFromBox.addEventListener('change', (event) => {
        const dateFrom = DateTime.fromISO(dateFromBox.value).startOf('day')
        // check if box content is a valid date
        if (dateFrom.isValid) {
            updateReport();
        }
    });

    // DateTo event listener
    dateToBox.addEventListener('change', (event) => {
        const dateTo = DateTime.fromISO(dateToBox.value).endOf('day')
        // check if box content is a valid date
        if (dateTo.isValid) {
            updateReport();
        }
    });

    // DateFrom 'Enter key' event listener
    dateFromBox.addEventListener('keyup', (event) => {
        event.preventDefault();
        if (event.key === 'Enter') {
            if (myForm.reportValidity()) {
                updateReport();
            }
        }
    });

    // DateTo 'Enter key' event listener
    dateToBox.addEventListener('keyup', (event) => {
        event.preventDefault();
        if (event.key === 'Enter') {
            if (myForm.reportValidity()) {
                updateReport();
            }
        }
    });

    // Bootstrap-table event listeners
    resultsTable.on('click-row.bs.table', (e, row, element, field) => {
        const uuid = row.id;
        const url = `../../inventories/transactions/${uuid}`;
        window.open(url, '_blank'); // open in new tab
      })

    // Populate Material Group select
    populateMaterialGroupSelect();
    // Populate Material select
    populateMaterialSelect(materialGroupSelect.value);
    // update report with initial values
    updateReport();

});


function populateMaterialGroupSelect() {
    // initialize select object
    initializeSelect(materialGroupSelect, ALL_VALUES_ID, 'All Material Groups');
    // Fetch material groups from server
    fetch(`/reports/get-material-groups/`)
    .then(response => response.json())
    .then(data => {
        // add options to select object
        data.forEach(function(element) {
            addOptionsToSelect(materialGroupSelect, element.id, element.name)
        });
    });
}


function populateMaterialSelect(materialGroupId) {
    // initialize select object
    initializeSelect(materialSelect, ALL_VALUES_ID, 'All Materials', 'groupid', ALL_VALUES_ID);
    // Fetch materials from server
    fetch(`/reports/get-materials/${materialGroupId}`)
    .then(response => response.json())
    .then(data => {
        // add options to select object
        data.forEach(function(element) {
            addOptionsToSelect(materialSelect, element.id, element.name, 'groupid', element.material_group_id)
        });
    });
}


// clears the referred select object and adds the first element
function initializeSelect(selectObject, firstOptionValue='', firstOptionHTML = '----------', dataIdentifier=undefined, dataValue=undefined) {
    // clear existing options
    selectObject.options.length = 0;
    // add first (no-selection) element
    let opt = document.createElement('option');
    opt.value = firstOptionValue;
    opt.innerHTML = firstOptionHTML;
    if (dataIdentifier !== undefined && dataValue !== undefined) {
        opt.setAttribute(`data-${dataIdentifier}`, dataValue)
    }
    selectObject.appendChild(opt);
}


// adds an option to the referred select object
function addOptionsToSelect(selectObject, optionValue, optionHTML, dataIdentifier, dataValue) {
    let opt = document.createElement('option');
    opt.value = optionValue;
    opt.innerHTML = optionHTML;
    if (dataIdentifier !== undefined && dataValue !== undefined) {
        opt.setAttribute(`data-${dataIdentifier}`, dataValue)
    }  
    selectObject.appendChild(opt);
}


function updateReport() {
    resultsTable.bootstrapTable('refresh');
}


function ajaxRequest(params) {
    
    // Returns array of transaction types. Returns [''] if none of types is checked.
    const transactionTypes = (() => {
        const values = ['IN', 'OUT', ''];
        const mask = [transactionTypeInCheckbox.checked, transactionTypeOutCheckbox.checked, !(transactionTypeInCheckbox.checked || transactionTypeOutCheckbox.checked)];
        return values.filter((d, ind) => mask[ind]);
    })();
    
    const materialGroup = (() => {
        const val = materialGroupSelect.value;
        if (val === ALL_VALUES_ID) {
            return;
        } else {
            return val;
        }
    })();

    const material = (() => {
        const val = materialSelect.value;
        if (val === ALL_VALUES_ID) {
            return;
        } else {
            return val;
        }
    })();

    const dateFrom = (() => {
        const val = DateTime.fromISO(dateFromBox.value).startOf('day').toISO()
        return val;
    })();

    const dateTo = (() => {
        const val = DateTime.fromISO(dateToBox.value).endOf('day').toISO()
        return val;
    })();

    const url = (() => {
        let u = new URL('http://127.0.0.1:8000/reports/get-transactions/');
        let searchParams = new URLSearchParams();
        searchParams.append('date_from', dateFrom);
        searchParams.append('date_to', dateTo);
        if (materialGroup) {
            searchParams.append('material_group', materialGroup);
        }
        if (material) {
            searchParams.append('material', material);
        }
        transactionTypes.forEach(t => searchParams.append('transaction_types', t))

        u.search = searchParams.toString();
        return u;
    })();

    // make GET request
    fetch(url, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(transactions => {
        params.success(transactions)
    })
    // Catch any errors and log them to the console
    .catch(error => {
        console.log('Error:', error);
    });

  }


//---------------------------
// Bootstrap Table functions
// --------------------------

function formatNumber(num) {
    return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')
}


// function customSort(sortName, sortOrder, data) {
//     var order = sortOrder === 'desc' ? -1 : 1
//     data.sort(function (a, b) {
//         var aa = +((a[sortName] + '').replace(/[^\d]/g, ''))
//         var bb = +((b[sortName] + '').replace(/[^\d]/g, ''))
//         if (aa < bb) {
//             return order * -1
//         }
//         if (aa > bb) {
//             return order
//         }
//         return 0
//     })
// }

