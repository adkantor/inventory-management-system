const pdfButton = document.getElementById("pdf-button");

document.addEventListener('DOMContentLoaded', function() {
    pdfButton.addEventListener('click', (event) => {
        onPdfButtonClicked(event);
    });

    // update button
    updatePdfButton();
});

function updatePdfButton() {
    const pdfExists = (parseInt(pdfButton.dataset.pdfExists) == 1 ? true : false);
    const uuid = pdfButton.dataset.uuid
    if (pdfExists) {
        pdfButton.innerHTML = 'Open PDF';
        pdfButton.className = 'btn btn-primary btn-sm mx-3';
        pdfButton.setAttribute('href', `${uuid}/pdf`);
    } else {
        pdfButton.innerHTML = 'Create PDF';
        pdfButton.className = 'btn btn-success btn-sm mx-3';
    }
}


function onPdfButtonClicked(event) {
    const pdfExists = (parseInt(pdfButton.dataset.pdfExists) == 1 ? true : false);
    const uuid = pdfButton.dataset.uuid
    if (pdfExists) {
        // do nothing, link href handles pdf opening
    } else {
        // generate pdf
        event.preventDefault();

        const csrftoken = getCookie('csrftoken');
        fetch(`generate/${uuid}`, {
            method: 'PATCH',
            headers: { "X-CSRFToken": csrftoken },
            credentials: 'same-origin'
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw response;
            }
        })
        .then(doc => {
            // update button data attribute
            pdfButton.dataset.pdfExists = "1"
            updatePdfButton();
            // open pdf in new tab
            window.open(`${uuid}/pdf`, '_blank').focus();
        })
        // Catch any errors and log them to the console
        .catch(error => {
            console.log('Error:', error);
        });
    }
}


// The following function are copying from 
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
