var interval;


function updateStatus() {
    return $.getJSON("/status").done(response => {
        $('#time-today').html(response.today);
        $("#m1").html(response.mdHMS.charAt(0));
        $("#m2").html(response.mdHMS.charAt(1));
        $("#d1").html(response.mdHMS.charAt(2));
        $("#d2").html(response.mdHMS.charAt(3));
        $("#time-day").html(response.day);
        $("#H1").html(response.mdHMS.charAt(4));
        $("#H2").html(response.mdHMS.charAt(5));
        $("#M1").html(response.mdHMS.charAt(6));
        $("#M2").html(response.mdHMS.charAt(7));
        $("#S1").html(response.mdHMS.charAt(8));
        $("#S2").html(response.mdHMS.charAt(9));
        $("#status-room").html(response.room);
        $("#status-activity").html(response.activity);
    });
}


function update() {
    updateStatus();
}


$(document).ready(() => {
    // Disable cache
    $.ajaxSetup({cache: false});
    update();
    interval = setInterval(update, 1000);
});


function stop() {
    // For debug only
    clearInterval(interval);
}
