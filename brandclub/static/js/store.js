$(function($) {

    var slideshows = $(".slideshow");
    $.each(slideshows, function(index, element){
        var links = $(".links a", $(element));
        var slideshowId = $(element).attr('data-slideshow-id');
        blueimp.Gallery(links, {
           container: "#slide-show-carousel-"+slideshowId,
           carousel: true,
           slidesContainer:'div',
           slideClass:'slide',
            urlProperty:'href',
            fullScreen:true,
            preloadRange: 100,
        });

    });
}(jQuery));