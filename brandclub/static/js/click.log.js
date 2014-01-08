function logAndRedirect(tag, redirect_url)   {
    var $this = $(tag);
    var content_name = $this.data("log-content-name");
    var content_type = $this.data("log-content-type");
    var content_owner = $this.data("log-brand-name");
    var content_id = $this.data("log-content-id");
//    console.log(tag);
//    console.log(content_name);
//    console.log(content_type);
//    console.log(content_owner);
//    console.log(content_id);
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
    _paq.push(['setCustomVariable', 5, "log_type", "click", "page"]);
    _paq.push(["appendToTrackingUrl", 'city='+window.log_info.home_city_name]);
    _paq.push(["appendToTrackingUrl", 'country=in']);
    _paq.push(["trackPageView"]);
    _paq.push(["enableLinkTracking"]);
    setTimeout(function(){
        window.location.href = redirect_url;
    }, 600);
}