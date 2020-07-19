function report_verify(formId) {
    let form = document.getElementById(formId);
    const data = new URLSearchParams(new FormData(form));

    $(`#${formId} input`)

    fetch('/report_verify/', {
        method: 'post',
        credentials: 'include',
        body: data,
    })
    .then((value) => {
        return value.text()
    })
    .then((res) => {
        console.log(res);
    })
}