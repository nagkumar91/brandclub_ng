$(document).ready(function () {

    if($("#email_id").length==0)   {
        $(".offer").show();
        $(".form").hide();
    }
    else    {
        $(".offer").hide();
        $(".form").show();
    }
});
function no_number_or_mail() {
    $(".email_div").addClass("has-error");
    $("#phone_number").focus();
    return;
}
function show_offer() {
    $(".offer").show();
    $(".form").hide();
}
function validate_and_submit() {
    var user_name = $("#user_name").val();
    var email = $("#email_id").val();
    var phone_number = $("#phone_number").val();
    var offer = $("#offer").val();
    if (user_name == "") {
        if ($(".user_name_div").hasClass("has-error")) {
        }
        else {
            $(".user_name_div").addClass("has-error");
            $('<label class="label_for_name" for="user_name">This field is mandatory</label>').insertBefore("#user_name");
        }
        $("#user_name").focus();
        return;
    }
    else {
        $(".label_for_name").remove();
        $(".user_name_div").removeClass("has-error").addClass("has-success");
    }
    if (email == "" && phone_number == "") {
        no_number_or_mail();
        return;
    }
    else {
        if (validate_phone_number(phone_number) || validate_email(email)) {
            var data = {"user_name": user_name, "phone_number": phone_number, "email_id": email, "offer": offer};
            $.ajax({
                url: "/authenticateUserForOffer/",
                data: data,
                success: function () {
                    show_offer();
                },
                fail: function () {
                    console.log("Ajax incomplete")
                }
            });
        }
        else
            no_number_or_mail();
    }
}
function validate_phone_number(phone) {
    if (phone.length != 10 || !$.isNumeric(phone)) {
        return false;
    }
    return true;
}
function validate_email(email) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    if (email.length > 3 && emailReg.test(email)) {
        return true;
    }
    return false;
}
