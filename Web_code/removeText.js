$(document).ready(function () {
    $("#myForm").on("click", ".amend_order .deleter", function () {
        $(this).closest("div").remove();
    });
    
    // Simulate one being added dynamically
    setTimeout(function () {
        var new_item = $("#template1").html();
        $("#myForm").append(new_item);
    }, 1000);
});