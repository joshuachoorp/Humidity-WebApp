document.addEventListener('DOMContentLoaded', function () {
    const submitForm = document.getElementById('submitForm');
    const fileInput = document.getElementById('fileInput');
    const selectBox = document.getElementById('selectBox');

    submitForm.addEventListener('submit', async function (event) {
        event.preventDefault(); // Prevent the default form submission

        // Check if a file is selected
        if (fileInput.files.length === 0) {
            alert('Please select a CSV file before submitting.');
            return;
        }
        // Access the selected file using fileInput.files[0]
        const selectedFile = fileInput.files[0];
        const selectedRegion = selectBox.value;

        // You can add your validation logic here
        try {
            const validationResult = await readAndValidateCSV(selectedFile,selectedRegion);
            if (validationResult == false) {
               
                return;
            }
            else{
                // If validation passes, submit the form programmatically
                
                fileInput.value = ''; // Reset the file input
                selectBox.value = ''; // Reset the select box
                resetFormData();
                submitForm.submit();
            }

        } catch (error) {
            console.error('An error occurred during validation:', error);
            alert('Invalid file format or content. Please check your CSV file.');
        }
    });
});

async function readAndValidateCSV(file,region) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = function (e) {
            const data = new Uint8Array(e.target.result);
            const workbook = XLSX.read(data, { type: 'array' });

            // Assuming the first sheet is the one you want to read
            const firstSheetName = workbook.SheetNames[0];
            const firstSheet = workbook.Sheets[firstSheetName];

            // Extract the headers from the first row of the Excel file
            const firstRow = XLSX.utils.sheet_to_json(firstSheet, { header: 1 })[0];
            const dataStartIndex = 1; // Change this index if needed
            const headersFromBOnwards = firstRow.slice(dataStartIndex);
            console.log('First row from Excel:', headersFromBOnwards);

            // Define the expected column headers
            const expectedHeaders = [
                'Mean Temperature (°C)',
                'Maximum Temperature (°C)',
                'Lowest Temperature (°C)',
                'Mean Wind Speed (km/h)',
                'Max Wind Speed (km/h)'
            ];
            console.log('Expected Headers:', expectedHeaders);
            // Check if the first row matches the expected headers
            const headersMatch = expectedHeaders.every(header => headersFromBOnwards.includes(header));

            if (headersMatch) {
                console.log('Column headers match the expected format.');
                sendDataToServer(file,region);
                resolve(true); // Resolve the Promise if validation passes
            } else {
                console.log('Column headers do not match the expected format.');
                reject(false); // Reject the Promise if validation fails
            }
        };

        reader.onerror = function (e) {
            console.error('An error occurred while reading the file:', e);
            reject(false); // Reject the Promise if an error occurs
        };

        reader.readAsArrayBuffer(file);
    });
}
let formData = new FormData();
function resetFormData() {
    formData = new FormData();
}
function sendDataToServer(file,region) {
    resetFormData();
    formData.append('file', file);
    formData.append('region',region)
    console.log(file)

    fetch('/process-csv', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log('Data received from the server:', data);
    });
}
