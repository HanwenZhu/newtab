// TODO, jQuery is slow

var interval;

// For short-period checks
var tick = 0;

// For long-period checks
var lastWeatherCheck = 0;

// To avoid DOM lookup
var $timeToday, $timeDay, $locationRoom, $locationActivity, $mdHMS,
    $weather;


function setup() {
    // Disable cache
    $.ajaxSetup({cache: false});

    $timeToday = $('#time-today');
    $timeDay = $('#time-day');
    $locationRoom = $('#location-room');
    $locationActivity = $('#location-activity');
    $mdHMS = $('.mdHMS');

    $weather = $('#weather');

    update();
}


function updateClock() {
    $.getJSON('/clock').done(response => {
        $timeToday.html(response.today);
        $timeDay.html(response.day);
        $locationRoom.html(response.room);
        $locationActivity.html(response.activity);
        $mdHMS.each((index, digit) => {
            digit.innerHTML = response.mdHMS.charAt(index);
        });
    });
}


function updateWeather() {
    $.getJSON('/weather').done(response => {
        $weather.html(response);
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
}


$(document).ready(() => {
    setup();
    interval = setInterval(update, 1000);
});


function stopInterval() {
    // For debug only
    clearInterval(interval);
}
