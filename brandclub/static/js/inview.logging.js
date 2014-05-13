$(function ($) {
    $(document).ready(function () {
        $(".brandclub-widget").bind('inview', function (event, isInView, visiblePartX, visiblePartY) {
            var $this = $(this);
            var content_name = $this.data("log-content-name");
            var content_type = $this.data("log-content-type");
            var content_owner = $this.data("log-brand-name");
            var content_id = $this.data("log-content-id");
            if (isInView) {
                if (visiblePartY == 'top') {
                } else if (visiblePartY == 'bottom') {
                } else {
                    // whole part of element is visible
                    var user_unique_id = readCookie("user_unique_id");
                    call_log(content_id, window.log_info.home_device_id, user_unique_id, document.title, "card in view", "");
//                    impressionLog(content_id, content_type, content_name, content_owner);

                }
            }
        });
    });
}(jQuery));