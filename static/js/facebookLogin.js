//Login Fb
var fb_login_btn_lock = false;

$('.fb-login-btn').click(function(){
    if(fb_login_btn_lock)return;
    fb_login_btn_lock = true;
    console.log('fb login');
    FB.login(function(response){
        if(response.authResponse){
            $('#login-form').append("<input type=\"test\" hidden name=\"fblogin\" value=\"1\"></input>")
            $('#login-form').submit();
        }
        console.log('fb return');
        fb_login_btn_lock = false;
    });
});
