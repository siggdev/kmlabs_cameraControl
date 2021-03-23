let timer = null;

const load_seconds = () => {
    fetch('/getseconds')
    .then(response => {
        return response.json()
    })
    .then(json_response => {
        window.seconds = Number(json_response.seconds);
        if(window.seconds > 0) {
            window.seconds += 3;
        }
    })
    .catch(error => {
        console.log(error);
        window.seconds = -1;
    });
};

const show_new_time = () => {
    window.seconds -= 1;
    console.log(window.seconds);

    if(window.seconds < -5)
    {
        document.getElementById('shotcounter').style.display = 'none';
        document.getElementById('noshot').style.display = 'block';
        clearInterval(window.timer);
    }
    if(window.seconds == -1) {
        console.log('loading new shot time');
        load_seconds();
    }
    if(window.seconds < 0) {
        return;
    }

    document.getElementById('shotcounter').style.display = 'block';
    document.getElementById('noshot').style.display = 'none';

    var hours = Math.floor(window.seconds / 3600);
    var minutes = Math.floor(window.seconds / 60) % 60;

    if(hours > 0)
        document.getElementById("shot-countdown").innerHTML = `${hours.toString().padStart(2, 0)}:${minutes.toString().padStart(2, 0)}:${(window.seconds%60).toString().padStart(2, 0)}`;
    else
        document.getElementById("shot-countdown").innerHTML = `${minutes.toString().padStart(2, 0)}:${(window.seconds%60).toString().padStart(2, 0)}`;
}

load_seconds();
window.seconds += 3;
window.timer = setInterval(show_new_time, 1000);