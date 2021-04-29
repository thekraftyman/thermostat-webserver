function getKey(): string {
    var apiKey: string = localStorage.getItem( 'apiKey' );
    if (Boolean( apiKey )) {
        return apiKey;
    }
    return '';
}

function setKey( apiKey: string ) {
    var storedKey: string = getKey();

    if ( apiKey == storedKey ) {
        // keys are the same, stop function
        return ;
    }

    // keys are different, save to storage
    localStorage.setItem( 'apiKey', apiKey );
}

function setKeyFormInput( inputId: string ) {
    var apiKey: string = getKey();
    $(`#${inputId}`).val( apiKey );
}
