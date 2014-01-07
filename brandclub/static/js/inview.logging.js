$(function($) {
    $(".brandclub-widget").bind('inview', function(event, isInView, visiblePartX, visiblePartY) {
        var $this = $(this);
        if (isInView) {
//            console.log("Element now visible in the viewport");
//            console.log($this);
            // element is now visible in the viewport
            if (visiblePartY == 'top') {
                // top part of element is visible
            } else if (visiblePartY == 'bottom') {
                // bottom part of element is visible
            } else {
                console.log("whole part of element is visible");
                console.log($this);
                // whole part of element is visible
            }
        } else {
        // element has gone out of viewport
        }
    });
}(jQuery));