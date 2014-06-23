$(function ($) {
    if (document.cookie.indexOf("user_unique_id=") == -1) {
        $.ajax({
            url: "/create_user_id/",
            success: function (result) {
                var date = new Date();
                var days = 365;
                var name = "user_unique_id";
                date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
                var expires = "; expires=" + date.toGMTString();
                var user_id = result['user_id'];
                document.cookie = name + "=" + user_id + expires + "; path=/";
                $.get("/create_user/").success(function (data) {
                    console.log("User created");
                    console.log(data);
                });

            }
        });
    }
}(jQuery));