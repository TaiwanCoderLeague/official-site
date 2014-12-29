//Login Fb
var fb_login_btn_lock = false;

$('#fb_login_btn').click(function(){
    if(fb_login_btn_lock)return;
    fb_login_btn_lock = true;
    console.log('fb login');
    FB.login(function(response){
        if(response.authResponse){
            $('login_form').append("<input type=\"test\" hidden name=\"fblogin\" value=\"1\"></input>")
            $('login_form').submit();
        }
        console.log('fb return');
        fb_login_btn_lock = false;
    });
});