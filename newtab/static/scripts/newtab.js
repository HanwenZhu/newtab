// TODO, jQuery is slow
// TODO, video is not clear.  Consider doubling width & height?
// TODO, support other browsers?

var interval;


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
    $.getJSON('/status').done(response => {
        $('#time-today').html(response.today);
        $('#m1 > .number').html(response.mdHMS.charAt(0));
        $('#m2 > .number').html(response.mdHMS.charAt(1));
        $('#d1 > .number').html(response.mdHMS.charAt(2));
        $('#d2 > .number').html(response.mdHMS.charAt(3));
        $('#time-day').html(response.day);
        $('#H1 > .number').html(response.mdHMS.charAt(4));
        $('#H2 > .number').html(response.mdHMS.charAt(5));
        $('#M1 > .number').html(response.mdHMS.charAt(6));
        $('#M2 > .number').html(response.mdHMS.charAt(7));
        $('#S1 > .number').html(response.mdHMS.charAt(8));
        $('#S2 > .number').html(response.mdHMS.charAt(9));
        $('#status-room').html(response.room);
        $('#status-activity').html(response.activity);
    });
}


function updateStatus() {
    $.getJSON('/status').done(response => {
        $('#time-today').html(response.today);
        manimTransform($('#m1'), response.mdHMS.charAt(0));
        manimTransform($('#m2'), response.mdHMS.charAt(1));
        manimTransform($('#d1'), response.mdHMS.charAt(2));
        manimTransform($('#d2'), response.mdHMS.charAt(3));
        $('#time-day').html(response.day);
        manimTransform($('#H1'), response.mdHMS.charAt(4));
        manimTransform($('#H2'), response.mdHMS.charAt(5));
        manimTransform($('#M1'), response.mdHMS.charAt(6));
        manimTransform($('#M2'), response.mdHMS.charAt(7));
        manimTransform($('#S1'), response.mdHMS.charAt(8));
        manimTransform($('#S2'), response.mdHMS.charAt(9));
        $('#status-room').html(response.room);
        $('#status-activity').html(response.activity);
    });
}


function manimTransform($element, target) {
    var $number = $element.find('.number');
    var $transform = $element.find('video.transform');

    if ($number.text() === target) {
        return;
    }

    // We need videos with an alpha channel for transparency.
    // I found that *.mov and *.webm work.
    // Newest Safari does not accept WebM (although WebM should be supported
    // as per the HTML5 <video> standard).  But (since it's Apple's) it supports
    // Quicktime's *.mov.
    // Chrome does support WebM.  It (reasonably) doesn't support *.mov.
    var webm = $transform[0].canPlayType('video/webm');
    var quicktime = $transform[0].canPlayType('video/quicktime');

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
