function getKey() {
    var apiKey = localStorage.getItem('apiKey');
    if (Boolean(apiKey)) {
        return apiKey;
    }
    return '';
}
function storeKey(apiKey) {
    var storedKey = getKey();
    if (apiKey == storedKey) {
        // keys are the same, stop function
        return;
    }
    // keys are different, save to storage
    localStorage.setItem('apiKey', apiKey);
}
function setKeyFormInput(inputId) {
    var apiKey = getKey();
    $("#" + inputId).val(apiKey);
}
