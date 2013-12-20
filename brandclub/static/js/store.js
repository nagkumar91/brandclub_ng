$(function($) {
    $("#store-map").popover({
        placement : 'bottom',
        title : 'Store Location',
        html: true,
        content: function () {
            return '<a target="_blank" href="'+$(this).data('store-map')+'"><img class="img-responsive" src="' + $(this).data('store-map')+'" /></a>';
        }
    });


}(jQuery));