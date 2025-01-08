function processFile() {
    const fileInput = document.getElementById('file');
    const keyInput = document.getElementById('key');
    const modeSelect = document.getElementById('mode');
    const resultDisplay = document.getElementById('result');
    
    const file = fileInput.files[0];
    const key = parseInt(keyInput.value);
    const mode = modeSelect.value;

    if (!file) {
        resultDisplay.textContent = "Please select a file!";
        return;
    }
    
    if (isNaN(key) || key <= 0) {
        resultDisplay.textContent = "Please enter a valid encryption key!";
        return;
    }
    
    // Prepare form data
    const formData = new FormData();
    formData.append('file', file);
    formData.append('key', key);
    formData.append('mode', mode);
    
    const exten = file.name.split('.').pop().toLowerCase();
    if(exten==='txt' || exten === 'pdf'){

        
        // Send file to Python backend (Flask or FastAPI)
        fetch('http://127.0.0.1:5000/process', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        // Create a link to download the processed file
        const downloadLink = document.createElement('a');
        downloadLink.href = URL.createObjectURL(blob);

        
        const extension = file.name.split('.').pop().toLowerCase();
        
        if (extension === 'txt') {
            downloadLink.download = "output.txt";  // Set the file name for text files
        } else if (extension === 'pdf') {
            downloadLink.download = "output.pdf";  // Set the file name for PDF files
        }
        // downloadLink.download = mode + "_output.pdf";  // Set the file name
        downloadLink.click();
        resultDisplay.textContent = `${mode.charAt(0).toUpperCase() + mode.slice(1)} operation completed!`;
    })
    .catch(error => {
        console.error(error);
        resultDisplay.textContent = "An error occurred!";
    });
    }else{
        resultDisplay.textContent = "Invalid File Format";
        
    }
}
