$(function() {
    $('#page-content').pagify({
        pages: ['home', 'about', 'signup', 'clients', 'managers', 'login', 'driverclient'],
        default: 'home',
        animation: 'fadeIn',
        onChange: function(name){
          var capitalized = name.substr(0, 1).toUpperCase() + name.substr(1);
          $(document).prop('title', 'NewETS · ' + capitalized);
        }
    });
});

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname + "=" + cvalue + "; " + expires; //+ ";domain=.example.com;path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name) === 0) return c.substring(name.length, c.length);
    }
    return "";
}
