
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded');
    updateStockLevels();
    updateWeeklyFinancials();
    updateSummaryFinancials();
});

function updateStockLevels() {
    console.log('updateStockLevels');
    const url = (() => {
        let u = new URL('http://127.0.0.1:8000/reports/get-stock-levels/');
        return u;
    })();

    // make GET request
    fetch(url, {
        method: 'GET',
    })
    .then(response => response.text())
    .then(data => {
        $('#plot-content-stock-levels').html(data);
    })
    // Catch any errors and log them to the console
    .catch(error => {
        console.log('Error:', error);
    });

}

function updateWeeklyFinancials() {
    console.log('updateWeeklyFinancials');
    const url = (() => {
        let u = new URL('http://127.0.0.1:8000/reports/get-weekly-financials/');
        return u;
    })();

    // make GET request
    fetch(url, {
        method: 'GET',
    })
    .then(response => response.text())
    .then(data => {
        $('#plot-content-weekly-financials').html(data);
    })
    // Catch any errors and log them to the console
    .catch(error => {
        console.log('Error:', error);
    });

}

function updateSummaryFinancials() {
    console.log('updateSummaryFinancials');
    const url = (() => {
        let u = new URL('http://127.0.0.1:8000/reports/get-summary-financials/');
        return u;
    })();

    // make GET request
    fetch(url, {
        method: 'GET',
    })
    .then(response => response.text())
    .then(data => {
        $('#plot-content-summary-financials').html(data);
    })
    // Catch any errors and log them to the console
    .catch(error => {
        console.log('Error:', error);
    });

}