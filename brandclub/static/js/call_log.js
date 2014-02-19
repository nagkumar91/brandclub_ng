function call_log(content_id, device_id, user_unique_id, page_title, redirect_url) {
    $.post("/call_log", {
        content_id: content_id,
        device_id: device_id,
        user_unique_id: user_unique_id,
        page_title: page_title,
        redirect_url: redirect_url,
        referrer: document.referrer,
        user_agent: navigator.userAgent

    });
}