document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please upload a file!');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();

    if (response.ok) {
        const imagesDiv = document.getElementById('images');
        imagesDiv.innerHTML = `
            <p><b>ECCV 16 Output:</b></p>
            <img src="${result.eccv16}" alt="ECCV 16 Output">
            <p><b>SIGGRAPH 17 Output:</b></p>
            <img src="${result.siggraph17}" alt="SIGGRAPH 17 Output">
        `;
    } else {
        alert(result.error || 'Something went wrong');
    }
});
