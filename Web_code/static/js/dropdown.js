//Javascript for drop down checkbox menu
$('.dropdown-menu').on('click', function(e) {
if($(this).hasClass('dropdown-menu-form')) {
    e.stopPropagation();
}
});