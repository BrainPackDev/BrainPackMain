$(document).ready(function() {
    var limitDays = $("#days").val();
    var sh_cookie_key = window.location.hostname + "shWebsitePopupEndDate";
    var get_dt = $.cookie(sh_cookie_key) || false;

    if (get_dt === false) {
        $("#sh_swp_model_popup").modal("show");
    } else {
        $("#sh_swp_model_popup").modal("hide");
    }
    $(".submit_btn").click(function() {
        $.cookie(sh_cookie_key, 'Model_shown', { expires: parseInt(limitDays) });
    });
});