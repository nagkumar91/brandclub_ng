function call_log(content_id, device_id, user_unique_id, page_title, user_action, redirect_url) {
    var data_to_be_sent = {
        content_id: content_id,
        device_id: device_id,
        user_unique_id: user_unique_id,
        page_title: page_title,
        redirect_url: redirect_url,
        referrer: document.referrer,
        user_agent: navigator.userAgent,
        device_height: $(window).height(),
        device_width: $(window).width(),
        user_action: user_action

    };
    $.ajax({
        type: "POST",
        url: "/call_log/",
        data: data_to_be_sent,
        dataType: 'json',
        success: function(data){
//            console.log(data);
        }
    });
}