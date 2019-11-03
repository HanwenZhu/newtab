// TODO, jQuery is slow

var interval;

// To avoid DOM lookup
var $timeToday, $timeDay, $statusRoom, $statusActivity, $mdHMS;


function setup() {
    // Disable cache
    $.ajaxSetup({cache: false});

    $timeToday = $('#time-today');
    $timeDay = $('#time-day');
    $statusRoom = $('#status-room');
    $statusActivity = $('#status-activity');
    $mdHMS = $('.mdHMS');

    update();
}


function updateStatus() {
    $.getJSON('/status').done(response => {
        $timeToday.html(response.today);
        $timeDay.html(response.day);
        $statusRoom.html(response.room);
        $statusActivity.html(response.activity);
        $mdHMS.each((index, digit) => {
            digit.innerHTML = response.mdHMS.charAt(index);
        });
    });
}


function update() {
    updateStatus();
}


$(document).ready(() => {
    setup();
    interval = setInterval(update, 1000);
});


function stopInterval() {
    // For debug only
    clearInterval(interval);
}
