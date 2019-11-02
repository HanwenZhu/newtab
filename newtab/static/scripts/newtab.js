// TODO, jQuery is slow
// TODO, video is not clear.  Consider doubling width & height?
// TODO, support other browsers?

var interval;

var $time_today, $time_day, $status_room, $status_activity, $mdHMS;

// We need videos with an alpha channel for transparency.
// I found that *.mov and *.webm work.
// Newest Safari does not accept WebM (although WebM should be supported
// as per the HTML5 <video> standard).  But (since it's Apple's) it supports
// Quicktime's *.mov.
// Chrome does support WebM.  It (reasonably) doesn't support *.mov.
var videoElement = $('<video></video>')[0];
var webm = videoElement.canPlayType('video/webm');
var quicktime = videoElement.canPlayType('video/quicktime');


function fetchCachedVideo(filename, callback) {
    // As was discussed, the best practice is to cache individual videos.
    // There is the alternative of having a long video cached and jumping to
    // individual timestamps, but it is not efficient for this task since
    // 01, 12, ..., 90 are used predominantly.

    // Safari doesn't cache by default!
    // Actually, using base64 is slower on locally hosted pages.
    if (navigator.vendor !== 'Apple Computer, Inc.' || ['localhost', '127.0.0.1', '0.0.0.0'].includes(window.location.hostname)) {
        setTimeout(() => callback(`/static/videos/${filename}`), 0);
        return;
    }

    var dataURL = localStorage.getItem(filename);
    if (dataURL) {
        setTimeout(() => callback(dataURL), 0);
    } else {
        $.ajax(`/static/videos/${filename}`, {
            method: 'GET',
            cache: true,
            xhrFields: {
                responseType: 'blob'
            }
        }).done(response => {
            var fileReader = new FileReader();
            fileReader.onloadend = () => {
                dataURL = fileReader.result;
                localStorage.setItem(filename, dataURL);
                callback(dataURL);
            };
            fileReader.readAsDataURL(response);
        });
    }
}


function setup() {
    // Disable cache
    $.ajaxSetup({cache: false});

    $time_today = $('#time-today');
    $time_day = $('#time-day');
    $status_room = $('#status-room');
    $status_activity = $('#status-activity');
    $mdHMS = $('.mdHMS')
    $.getJSON('/status').done(response => {
        $time_today.html(response.today);
        $time_day.html(response.day);
        $status_room.html(response.room);
        $status_activity.html(response.activity);
        $mdHMS.each((index, digit) => {
            $(digit).find('.number').html(response.mdHMS.charAt(index));
        });
    });
}


function updateStatus() {
    $.getJSON('/status').done(response => {
        $time_today.html(response.today);
        $time_day.html(response.day);
        $status_room.html(response.room);
        $status_activity.html(response.activity);
        $mdHMS.each((index, digit) => {
            manimTransform($(digit), response.mdHMS.charAt(index));
        });
    });
}


function manimTransform($element, target) {
    var $number = $element.find('.number');
    var $transform = $element.find('video.transform');

    if ($number.html() === target) {
        return;
    }

    if (!webm && !quicktime) {
        $number.html(target);
        return;
    }

    fetchCachedVideo(`${$number.text()}${target}` + (webm ? '.webm' : '.mov'), dataURL => {
        $transform.attr('src', dataURL);
        $transform[0].load();
        $transform.one('canplay', () => {
            $transform[0].play().then(() => {
                $transform.show(0, () => {
                    $number.hide(0, () => {
                        $number.html(target);
                    });
                });
            });
        }).one('ended', () => {
            $number.show(0, () => {
                $transform.hide(0);
            });
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
