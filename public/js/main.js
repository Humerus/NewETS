$(function() {
    $('#page-content').pagify({
        pages: ['home', 'about', 'signup', 'clients', 'managers', 'login'],
        default: 'home',
        animation: 'fadeIn'
    });
});
