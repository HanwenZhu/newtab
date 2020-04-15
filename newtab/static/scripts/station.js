var smoothness = 12;
var angles = new Array(smoothness).fill(null).map((element, index) => index / smoothness);

$(document).ready(() => {
    $('.cylinder').each((index, cylinder) => {
        angles.forEach(angle => {
            var diameter = $(cylinder).width();
            var facetWidth = diameter * Math.tan(Math.PI / smoothness);
            $('<div></div>').addClass('abs-center facet').css({
                width: `${facetWidth}px`,
                transform: `rotateY(${angle}turn) translateZ(${diameter / 2}px)`,
                background: 'linear-gradient(to right, red, blue)'
            }).appendTo($(cylinder));
        });
    });
});
