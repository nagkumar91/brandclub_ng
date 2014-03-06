$(function($){

});
function validate_free_internet_form()  {
    var name_field = $("#user_name");
    if(validate_name($(name_field).val()))  {
        $(name_field).removeClass("has-error");
        var user_name = $(name_field).val();
        var user_phone_field = $("#user_phone");
        if(validate_phone_number($(user_phone_field).val())){
            $(user_phone_field).removeClass("has-error")
            var phone_number = $(user_phone_field).val();
            var user_code_field = $("#user_code");
            if(validate_code($(user_code_field).val())) {
                var fi_code = $(user_code_field).val();
                $.ajax({
                    type: 'POST',
                    url: '/authorize_free_internet/',
                    data: {
                        'user_name': user_name,
                        'user_phone': phone_number,
                        'user_code': fi_code
                    },
                    dataType: "JSON",
                    success: function(data){
                        console.log(data);
                        console.log(data['success']);
                        if(data['success']){
                            var success_html = '<h6>Enjoy Free Internet.</h6>';
                            $("#error-message-container").empty().append(success_html);
                            $.ajax({
                                type: 'POST',
                                url: "/activate_free_internet.php",
                                data: {
                                    'user_name': user_name,
                                    'user_phone': phone_number,
                                    'user_code': fi_code
                                },
                                dataType: "JSON",
                                success: function(data){
                                    var redirect_html = '<h6>Click <span class="redirect-span" onclick="redirect_free_internet()">here</span> to continue.</h6>';
                                    $("#error-message-container").append(redirect_html);
                                },
                                error: function()   {
                                    var err_msg = "<h6>Sorry. Some error occured.</h6>";
                                    $("#error-message-container").append(err_msg);
                                    redirect_free_internet();
                                }
                            });
                        }
                        else    {
                            var error_html = '<h6>'+data['reason']+'</h6>';
                            $("#error-message-container").empty().append(error_html);
                        }
                    }
                });
            }
            else    {
                $(user_code_field).addClass("has-error").focus();
            }
        }
        else    {
            $(user_phone_field).addClass("has-error").focus();
        }
    }
    else    {
        $(name_field).addClass("has-error").focus();
    }

}

function validate_name(text)    {
    if (/^[a-zA-Z]*[a-zA-Z]+[a-zA-Z]*$/.test(text))
        return true;
    return false;
}


function validate_phone_number(phone) {
    if (phone.length != 10 || !$.isNumeric(phone)) {
        return false;
    }
    return true;
}

function validate_code(text)    {
    if(text.length == 6 && /^[a-zA-Z0-9]*$/.test(text))    {
        return true;
    }
    return false;
}

function redirect_free_internet()   {
    window.location.href='http://google.com'

}