document.getElementById('continueButton').addEventListener('click', function() {
    document.getElementById('slide1').classList.add('hidden');
    document.getElementById('slide2').classList.remove('hidden');
});

document.getElementById('backButtonSlide2').addEventListener('click', function() {
    document.getElementById('slide2').classList.add('hidden');
    document.getElementById('slide1').classList.remove('hidden');
});

document.getElementById('uploadButton').addEventListener('click', function() {
    alert("This will take you to the next page to upload your zip file."); // Placeholder action
    // Implement the code to show the next slide here when ready
});