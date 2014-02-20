$(function($) {

    var slideshows = $(".slideshow");
    $.each(slideshows, function(index, element){
        var links = $(".links a", $(element));
        var slideshowId = $(element).attr('data-slideshow-id');
        var content_id = $(element).attr('data-log-content-id');
        blueimp.Gallery(links, {
           container: "#slide-show-carousel-"+slideshowId,
           carousel: true,
           slidesContainer:'div',
           slideClass:'slide',
            urlProperty:'href',
            fullScreen:true,
            preloadRange: 100,
            onslidecomplete: function(){
                var user_unique_id = readCookie("user_unique_id");
                call_log(content_id, window.log_info.home_device_id, user_unique_id, document.title, "Slide", '');
            }
        });

    });
    $(document).ready(function(){
        var videos = $('video');
        $(videos).each(function(index){
            videos[index].addEventListener('play', video_play_listener, false)
        });
    });
    function video_play_listener(){
        var content_id = $(this).attr('data-log-content-id');
        var user_unique_id = readCookie("user_unique_id");
        call_log(content_id, window.log_info.home_device_id, user_unique_id, document.title, "Video Play", '');
    }
}(jQuery));