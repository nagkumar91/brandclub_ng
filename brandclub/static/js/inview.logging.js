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
                    impressionLog(content_id, content_type, content_name, content_owner);

                }
            }
        });
    });
}(jQuery));

function impressionLog(content_id, content_type, content_name, content_owner) {
    _paq.push(["setDocumentTitle", document.domain + "/" + document.title]);
    _paq.push(["setCookieDomain", window.log_info.cookie_domain]);
    _paq.push(["setDomains", [window.log_info.cookie_domain]]);
    _paq.push(['setCustomVariable', 1, "store_name", window.log_info.home_store_name, "visit"]);
    _paq.push(['setCustomVariable', 2, "mac_address", window.log_info.mac_id, "visit"]);
    _paq.push(['setCustomVariable', 3, "device_id", window.log_info.home_device_id, "visit"]);
    _paq.push(['setCustomVariable', 4, "store_brand", window.log_info.home_brand_name, "visit"]);
    _paq.push(['setCustomVariable', 5, "cluster_name", window.log_info.home_cluster_name, "visit"]);
    _paq.push(['setCustomVariable', 1, "content_id", content_id, "page"]);
    _paq.push(['setCustomVariable', 2, "content_type", content_type, "page"]);
    _paq.push(['setCustomVariable', 3, "content_name", content_name, "page"]);
    _paq.push(['setCustomVariable', 4, "content_brand", content_owner, "page"]);
    _paq.push(['setCustomVariable', 5, "log_type", "impression", "page"]);
    _paq.push(["appendToTrackingUrl", 'city=' + window.log_info.home_city_name]);
    _paq.push(["appendToTrackingUrl", 'country=in']);
    _paq.push(["trackPageView", content_owner]);
    _paq.push(["enableLinkTracking"]);
}