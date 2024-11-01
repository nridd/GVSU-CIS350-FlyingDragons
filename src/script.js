let db;
document.addEventListener('DOMContentLoaded', () => {
    // Open IndexedDB
    const request = indexedDB.open('FitnessTrackerDB', 1);

    request.onupgradeneeded = (e) => {
        db = e.target.result;
        if (!db.objectStoreNames.contains('videos')) {
            db.createObjectStore('videos', { keyPath: 'id', autoIncrement: true });
        }
    };

    request.onsuccess = (e) => {
        db = e.target.result;
        loadVideosFromDB();
    };

    request.onerror = (e) => {
        console.error('Error opening IndexedDB:', e.target.errorCode);
    };

    const videoUpload = document.getElementById('videoUpload');
    videoUpload.addEventListener('change', handleVideoUpload);
});

function handleVideoUpload(event) {
    const files = event.target.files;
    const transaction = db.transaction(['videos'], 'readwrite');
    const videoStore = transaction.objectStore('videos');

    for (let i = 0; i < files.length; i++) {
        const videoFile = files[i];
        const videoURL = URL.createObjectURL(videoFile);
        videoStore.add({ videoURL });
        addVideoToLibrary(videoURL);
    }
}

function loadVideosFromDB() {
    const transaction = db.transaction(['videos'], 'readonly');
    const videoStore = transaction.objectStore('videos');
    const request = videoStore.getAll();

    request.onsuccess = () => {
        request.result.forEach((video) => {
            addVideoToLibrary(video.videoURL);
        });
    };
}

function addVideoToLibrary(videoURL) {
    const videoElement = document.createElement('video');
    videoElement.src = videoURL;
    videoElement.controls = true;
    videoElement.width = 200;
    videoList.appendChild(videoElement);
}
