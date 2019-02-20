//site_static/site/js/location_detail.js
jQuery(function($) {
    function show_best_images() {
        $('img.img-full-width').each(function() {
            var $img = $(this);
            if ($img.width() > 1024) {
                $img.attr('src', $img.data('large-src'));
            } else if ($img.width() > 468) {
                $img.attr('src', $img.data('medium-src'));
            } else {
                $img.attr('src', $img.data('small-src'));
            }
        });
    }

    function show_map() {
        var $map = $('#map');
        var latitude = parseFloat($map.data('latitude'));
        var longitude = parseFloat($map.data('longitude'));
        var latlng = new google.maps.LatLng(latitude, longitude);
        var map = new google.maps.Map($map.get(0), {
            zoom: 15,
            center: latlng
        });
        var marker = new google.maps.Marker({
            position: latlng,
            map: map
        });
    }

    show_best_images();
    show_map();
    $(window).on('resize', show_best_images);
});
