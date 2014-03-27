$(function($) {
    var logged_ids = []
    var links = $("#links a");
    var content_id = $("#links").attr("data-log-content-id");
    var gallery = blueimp.Gallery(links, {
       container: "#slide-show-carousel",
       carousel: true,
       slidesContainer:'div',
       slideClass:'slide',
        urlProperty:'href',
        fullScreen:true,
        closeClass: "close",
        onclose: function(){
            window.history.back();
        },
        onslideend:function(){
                var index = gallery.getIndex();
                if (logged_ids.indexOf(index)<0)   {
                    var user_unique_id = readCookie("user_unique_id");
                    call_log(content_id, window.log_info.home_device_id, user_unique_id, document.title, "Slide", '');
                    logged_ids.push(index);
                }
            }

    });
}(jQuery));