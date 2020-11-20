
var setMainMargin = function() {
    var marginSize = $('.menu-bar').width();
    var mainContent = $('.main-content-wrapper');
    mainContent.css('margin-left', marginSize)
};


$(document).ready(function() {

    $(window).resize(function() {
        setMainMargin();
    });

    $('.year-selector-item').click(function() {
        $('.selected').toggleClass('selected');
        $(this).toggleClass('selected');

        var field_name = $('.analysis-content-container .heading-container span').html();
        var year = $(this).html();
        var data = { 'field': field_name, 'year': year };

        $.ajax({
            url: '/',
            method: 'GET',
            data: data,
            success: function(res) {
                $('.field-analysis-ajax-wrap').html(res['analysis']);
                $('.results-ajax-wrap').html(res['results']);
            }
        });
    });

    setMainMargin();
});
