$(function($) {
    var links = $("#links a");
    blueimp.Gallery(links, {
       container: "#slide-show-carousel",
       carousel: true,
       slidesContainer:'div',
       slideClass:'slide',
        urlProperty:'href',
        fullScreen:true,
        closeClass: "close",
        onclose: function(){
            window.history.back();
        }
    });
}(jQuery));