var smoothness = 10;
var angles = new Array(smoothness).fill(null).map((element, index) => index / smoothness);

$(document).ready(() => {
    $('.cylinder').each((index, cylinder) => {
        angles.forEach(?? => {
            $(cylinder).clone().css()
        });
    });
});
