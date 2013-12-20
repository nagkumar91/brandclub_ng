$(function($) {
    var links = $("#links a");
    blueimp.Gallery(links, {
       container: "#slide-show-carousel",
       carousel: true
    });
}(jQuery));