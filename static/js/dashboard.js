
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded');
    updateStockLevels();
    updateFinancials();
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

function updateFinancials() {
    console.log('updateFinancials');
    const url = (() => {
        let u = new URL('http://127.0.0.1:8000/reports/get-financials/');
        return u;
    })();

    // make GET request
    fetch(url, {
        method: 'GET',
    })
    .then(response => response.text())
    .then(data => {
        $('#plot-content-financials').html(data);
    })
    // Catch any errors and log them to the console
    .catch(error => {
        console.log('Error:', error);
    });

}