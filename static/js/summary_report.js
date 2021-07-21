const myForm = document.forms[0];
const reportTypeRadioGroup = document.getElementsByName("report-options");
const materialGroupSelect = document.getElementById("material-group");
const materialSelect = document.getElementById("material");
const dateFromBox = document.getElementById("date-from");
const dateToBox = document.getElementById("date-to");
const resultsTable = $('#results-table');

var DateTime = luxon.DateTime; // https://moment.github.io/luxon/#/install
const ALL_VALUES_ID = 'all';

document.addEventListener('DOMContentLoaded', function() {

    // fill Date boxes
    dateFromBox.value = DateTime.now().startOf('month').toISODate();
    dateToBox.value = DateTime.now().endOf('month').toISODate();

    // Report type event listener
    function reportTypeChangeHandler(event) {
        updateReport();
    }
    Array.prototype.forEach.call(reportTypeRadioGroup, (radio) => {
        radio.addEventListener('change', reportTypeChangeHandler);
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
    console.log('updateReport');
    resultsTable.bootstrapTable('refresh');
    $('#results-table').bootstrapTable('refresh');
    console.log('refresh called');
}


function ajaxRequest(params) {
    console.log('ajaxRequest');
    const reportType = (() => {
        const val = getCheckedRadioOptionValue(reportTypeRadioGroup);
        return val;
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
        let u = new URL('http://127.0.0.1:8000/reports/get-summary/');
        let searchParams = new URLSearchParams();
        searchParams.append('resolution', reportType);
        searchParams.append('date_from', dateFrom);
        searchParams.append('date_to', dateTo);
        if (materialGroup) {
            searchParams.append('material_group', materialGroup);
        }
        if (material) {
            searchParams.append('material', material);
        }

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

function getCheckedRadioOptionValue(radioGroup) {
    for (let i = 0, length = radioGroup.length; i < length; i++) {
        if (radioGroup[i].checked) {
          return radioGroup[i].value;
        }
    }    
}
    // return document.querySelector('input[name="report-options"]:checked').value

//---------------------------
// Bootstrap Table functions
// --------------------------

function formatNumber(num) {
    return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')
}

function customViewFormatter (data) {
    console.log('customViewFormatter');
    var template = $('#reportTemplate').html()
    var view = ''
    $.each(data, function (i, row) {
      view += template
        .replace('%START_OF_PERIOD%', row.start_of_period)
        .replace('%END_OF_PERIOD%', row.end_of_period)
        .replace('%QTY_OPENING%', row.qty_opening)
        .replace('%QTY_IN%', row.qty_in)
        .replace('%QTY_OUT%', row.qty_out)
        .replace('%QTY_CLOSING%', row.qty_closing);
    })

    return `<div class="row mx-0">${view}</div>`
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

