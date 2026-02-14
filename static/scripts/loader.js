function checkStatus() {
    fetch('/scan_status')
        .then(res => res.json())
        .then(data => {
            if (data.done) {
                window.location.href = '/local';
            } else {
                setTimeout(checkStatus, 1500); 
            }
        })
        .catch(err => {
            console.error('Error checking scan status:', err);
            setTimeout(checkStatus, 2000);
        });
}

checkStatus();
