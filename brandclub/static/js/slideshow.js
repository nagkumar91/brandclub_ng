$(function($) {
    var links = $("#links a");
    var content_id = $("#links").attr("data-log-content-id");
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
        },
        onslidecomplete: function(){
                var user_unique_id = readCookie("user_unique_id");
                call_log(content_id, window.log_info.home_device_id, user_unique_id, document.title, "Slide", '');
        }
    });
}(jQuery));