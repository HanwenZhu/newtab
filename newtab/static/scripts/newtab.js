// TODO, jQuery is slow
// TODO, video is not clear.  Consider doubling width & height?
// TODO, support other browsers?

var interval;

// To avoid DOM lookup
var $timeToday, $timeDay, $statusRoom, $statusActivity, $mdHMS;

// We need videos with an alpha channel for transparency.
// I found that *.mov and *.webm work.
// Newest Safari does not accept WebM (although WebM should be supported
// as per the HTML5 <video> standard).  But (since it's Apple's) it supports
// Quicktime's *.mov.
// Chrome does support WebM.  It (reasonably) doesn't support *.mov.
var videoElement = $('<video></video>')[0];
var webm = videoElement.canPlayType('video/webm');
var quicktime = videoElement.canPlayType('video/quicktime');
var extension = webm ? '.webm' : quicktime ? '.mov' : null;

var videoPool = new Array(10).fill(null).map(item => new Array(10).fill(null));


function fetchVideo(from, to, callback) {
    // As was discussed, the best practice is to cache individual videos.
    // This will be implemented by appending new videos into an array.
    // There is the alternative of having a long video cached and jumping to
    // individual timestamps, but it is not efficient for this task since
    // 01, 12, ..., 90 are used predominantly.

    if (videoPool[from][to] !== null) {
        return videoPool[from][to];
    }

    var $video = $('<video class="transform" src="/static/videos/' +
                   `${from}${to}${extension}" preload="auto" muted ` +
                   'playsinline disablepictureinpicture>');
    $video[0].load();
    videoPool[from][to] = $video;
    return $video;
}


function setup() {
    // Disable cache
    $.ajaxSetup({cache: false});

    $timeToday = $('#time-today');
    $timeDay = $('#time-day');
    $statusRoom = $('#status-room');
    $statusActivity = $('#status-activity');
    $mdHMS = $('.mdHMS');
    $.getJSON('/status').done(response => {
        $timeToday.html(response.today);
        $timeDay.html(response.day);
        $statusRoom.html(response.room);
        $statusActivity.html(response.activity);
        $mdHMS.each((index, digit) => {
            number = parseInt(response.mdHMS.charAt(index));
            $(digit).html(number);
            digit.number = number;
        });
    });
}


function updateStatus() {
    $.getJSON('/status').done(response => {
        $timeToday.html(response.today);
        $timeDay.html(response.day);
        $statusRoom.html(response.room);
        $statusActivity.html(response.activity);
        $mdHMS.each((index, digit) => {
            manimTransform($(digit), response.mdHMS.charAt(index));
        });
    });
}


function manimTransform($element, target) {
    target = parseInt(target);
    if ($element[0].number === target) {
        return;
    }

    if (!webm && !quicktime) {
        $element[0].number = target;
        $element.html(target);
        return;
    }

    var $video = fetchVideo($element[0].number, target);
    $video.one('ended', () => {
        $element.html(target);
    })[0].play().then(() => {
        $element.html($video);
        $element[0].number = target;
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
