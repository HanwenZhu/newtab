// TODO, jQuery is slow
// TODO, cache all the videos.  The videos take 2 to 3 times to go through and
// will be a major drawback if this thing were to go beyond localhost
// TODO, video is not clear.  Consider doubling width & height?

var interval;


function setup() {
    // Disable cache
    $.ajaxSetup({cache: false});
    $.getJSON('/status', response => {
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
    $.getJSON('/status', response => {
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
    if (webm) {
        $transform.attr('src', `/static/videos/${$number.text()}${target}.webm`);
    } else if (quicktime) {
        $transform.attr('src', `/static/videos/${$number.text()}${target}.mov`);
    } else {
        $number.html(target);
    }

    // TODO, in some specific version of WebKit all words seem to thicken when video is playing
    if (webm || quicktime) {
        $transform[0].load();
        $transform.one('canplay', () => {
            $transform[0].play().then(() => {
                $transform.show();
                $number.hide();
                $number.html(target);
            });
        }).one('ended', () => {
            $transform.hide();
            $number.show();
        });
    }
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
