let db;

// Initialize the IndexedDB and load stored videos when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const videoUpload = document.getElementById('videoUpload');
    const videoList = document.getElementById('videoList');
    const analyzeButton = document.getElementById('analyzeButton');

    // Open or create the IndexedDB database
    const request = indexedDB.open('FitnessTrackerDB', 1);

    request.onupgradeneeded = (event) => {
        db = event.target.result;
        if (!db.objectStoreNames.contains('videos')) {
            db.createObjectStore('videos', { keyPath: 'id', autoIncrement: true });
        }
    };

    request.onsuccess = (event) => {
        db = event.target.result;
        loadVideosFromDB();  // Load videos from IndexedDB into the library
    };

    request.onerror = (event) => {
        console.error('Error opening IndexedDB:', event.target.errorCode);
    };

    // Handle video upload
    videoUpload.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const videoURL = URL.createObjectURL(file);
            saveVideoToDB(videoURL);
        }
    });

    analyzeButton.addEventListener('click', () => {
        if (videoList.children.length > 0) {
            // Redirect to suggestions page
            window.location.href = 'suggestions.html';
        } else {
            alert('Please upload a video first.');
        }
    });

    // Function to save a video URL to IndexedDB
    function saveVideoToDB(videoURL) {
        const transaction = db.transaction(['videos'], 'readwrite');
        const videoStore = transaction.objectStore('videos');
        videoStore.add({ videoURL });
        displayVideo(videoURL);  // Immediately display the new video in the library
    }

    // Function to load videos from IndexedDB and display them
    function loadVideosFromDB() {
        const transaction = db.transaction(['videos'], 'readonly');
        const videoStore = transaction.objectStore('videos');
        const request = videoStore.getAll();

        request.onsuccess = () => {
            request.result.forEach((video) => {
                displayVideo(video.videoURL);
            });
        };
    }

    // Function to display a video in the video library
    function displayVideo(videoURL) {
        const videoElement = document.createElement('video');
        videoElement.src = videoURL;
        videoElement.controls = true;
        videoElement.width = 300;
        videoList.appendChild(videoElement);
    }
});

