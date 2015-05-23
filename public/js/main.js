$(function() {
    $('#page-content').pagify({
        pages: ['home', 'about', 'signup', 'clients', 'managers'],
        default: 'home',
        animation: 'fadeIn'
    });
});
