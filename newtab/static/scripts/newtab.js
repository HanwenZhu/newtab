// TODO, jQuery is slow

var interval;

// For short-period checks
var tick = 0;

// For long-period checks
var lastWeatherCheck = 0;
var lastWifiCheck = 0;

// To avoid DOM lookup
var $timeDate, $timeTime;
var $timeToday, $timeDay, $locationRoom, $locationActivity;
var $weather;


function setup() {
    // Disable cache
    $.ajaxSetup({cache: false});

    $timeDate = $('#time-date');
    $timeTime = $('#time-time');

    $timeToday = $('#time-today');
    $timeDay = $('#time-day');
    $locationRoom = $('#location-room');
    $locationActivity = $('#location-activity');

    $weather = $('#weather');

    update();
}


function updateClock() {
    // Mon Jan 1
    $.getJSON('/clock/strftime/%a%20%b%20%-d').done(response => {
        $timeDate.html(response);
    });

    // 00:00:00
    $.getJSON('/clock/strftime/%H:%M:%S').done(response => {
        $timeTime.html(response);
    });

    $.getJSON('/clock/school').done(response => {
        $timeToday.html(response.today);
        $timeDay.html(response.day);
        $locationRoom.html(response.room);
        $locationActivity.html(response.activity);
    });
}


function updateWeather() {
    $.getJSON('/weather').done(response => {
        $weather.html(response);
    });
}


function updateWifi() {
    // TODO: display
    $.getJSON('/wifi/wifi').done(response => {
        if (response === 'STUWIRELESS' || response === 'SJWIRELESS') {
            $.getJSON('/wifi/login').done(response => {
                if (response) {
                    console.log('Logged in: ', response);
                }
            });
        }
    });
}


function update() {
    if (tick % 1 == 0) {
        updateClock();
    }
    tick++;

    var now = Date.now();
    if (now - lastWeatherCheck > 1800000) {
        updateWeather();
        lastWeatherCheck = now;
    }
    if (now - lastWifiCheck > 1800000) {
        updateWifi();
        lastWifiCheck = now;
    }
}


$(document).ready(() => {
    setup();
    interval = setInterval(update, 1000);
});


function stopInterval() {
    // For debug only
    clearInterval(interval);
}
