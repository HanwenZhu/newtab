// TODO, jQuery is slow

var interval;

// For short-period checks
var tick = 0;

// For long-period checks
var lastWeatherCheck = 0;
var lastWifiCheck = 0;

// To avoid DOM lookup
var $timeDate, $timeTime;
var $schoolToday, $schoolClasses;
var $weatherTemperature, $weatherEmoji;

// Element templates
// Note that we can't use <span> with display: block or <div> with display: flex
// for (-webkit-)background-clip: text on Safari
// This is a documented bug: https://bugs.webkit.org/show_bug.cgi?id=169125
var $schoolClass = $('<div></div>').addClass('school-class');
var $schoolRecess = $('<span></span>').addClass('school-recess');
var unfinishedColor;
var finishedColor;


function setup() {
    // Disable cache
    $.ajaxSetup({cache: false});

    $timeDate = $('#time-date');
    $timeTime = $('#time-time');

    $schoolToday = $('#school-today');
    $schoolClasses = $('#school-classes');

    $weatherTemperature = $('#weather-temperature');
    $weatherEmoji = $('#weather-emoji');

    unfinishedColor = $('body').css('color');
    finishedColor = unfinishedColor.replace(')', ', 0.5)').replace('rgb', 'rgba');

    update();
}


function updateClock() {
    // Mon Jan 1
    $.getJSON('/clock/strftime/%a%20%b%20%-d').done(response => {
        $timeDate.text(response);
    });

    // 00:00:00
    $.getJSON('/clock/strftime/%H:%M:%S').done(response => {
        $timeTime.text(response);
    });

    $.getJSON('/clock/school').done(response => {
        $schoolToday.text(response.today);
        if (response.school) {
            $schoolClasses.empty();
            var progressPercent = response.progress * 100;
            var backgroundImage = `linear-gradient(to right, ${finishedColor} 0%, ${finishedColor} ${progressPercent}%, ${unfinishedColor} ${progressPercent}%)`;
            response.classes.forEach((className, index) => {
                var $thisClass = $schoolClass.clone().text(className);

                if (index === response.classIndex && !response.started) {
                    $schoolRecess.clone().css({
                        backgroundImage: backgroundImage
                    }).appendTo($schoolClasses);
                    $thisClass.css({
                        backgroundColor: unfinishedColor
                    });
                } else if (index === response.classIndex && response.started) {
                    $thisClass.css({
                        backgroundImage: backgroundImage
                    });
                } else if (index < response.classIndex) {
                    $thisClass.css({
                        backgroundColor: finishedColor
                    });
                } else if (index > response.classIndex) {
                    $thisClass.css({
                        backgroundColor: unfinishedColor
                    });
                }

                $thisClass.appendTo($schoolClasses);
            });
        }
    });
}


function updateWeather() {
    $.getJSON('/weather').done(response => {
        [temperature, emoji] = response.split(' ');
        $weatherTemperature.text(temperature);
        $weatherEmoji.text(emoji);
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
