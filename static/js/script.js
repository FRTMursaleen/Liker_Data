(function($) {
    "use strict";

    // Windows load

    $(window).on("load", function() {

        // Site loader 

        $(".loader-inner").fadeOut();
        $(".loader").delay(200).fadeOut("slow");

    });


    // Scroll to

    $('a.scroll').smoothScroll({
        speed: 800,
        offset: -93
    });



    // Nav setup

    $(window).scroll(function() {

        var blockNav = $('.block-nav'),
            navOuterHeight = blockNav.outerHeight(),
            outerBlock = $('.block-outer-nav'),
            blockTop = $('.block-top');
        if (blockNav.length) {
            var position = 200;
            if ($(window).scrollTop() > position) {
                blockNav.removeClass('slideIn animated');
                blockNav.addClass('sticky-nav slideIn animation');
                outerBlock.css({
                    height: navOuterHeight
                });
                blockTop.addClass('active');
            } else if ($(this).scrollTop() <= position) {
                blockNav.removeClass('sticky-nav slideIn animation');
                blockTop.removeClass('active');
            }
        };

    });


    // Slider

    $('.main-slider').flexslider({
        animation: "fade",
        slideshow: true,
        directionNav: false,
        controlNav: true,
        pauseOnAction: false,
        animationSpeed: 1000
    });


    // Hero resize

    function mainHeroResize() {
        $(".main-slider .slides li").css('height', $(window).height() - 300);
    }

    $(function() {
            mainHeroResize()
        }),
        $(window).resize(function() {
            mainHeroResize()
        });


    // Play video button


    $('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
        disableOn: 700,
        type: 'iframe',
        mainClass: 'mfp-fade',
        removalDelay: 160,
        preloader: false,

        fixedContentPos: false
    });


    // Mobile menu

    var mobileBtn = $('.mobile-but');
    var nav = $('.main-nav ul');
    var navHeight = nav.height();

    $(mobileBtn).on("click", function() {
        $(".toggle-mobile-but").toggleClass("active");
        nav.slideToggle();
        $('.main-nav li a').addClass('mobile');
        return false;


    });

    $(window).resize(function() {
        var w = $(window).width();
        if (w > 320 && nav.is(':hidden')) {
            nav.removeAttr('style');
            $('.main-nav li a').removeClass('mobile');
        }

    });

    $('.main-nav li a').on("click", function() {
        if ($(this).hasClass('mobile')) {
            nav.slideToggle();
            $(".toggle-mobile-but").toggleClass("active");
        }

    });


    // Setup gradient background

    var granimInstance = new Granim({
        element: '.facts',
        direction: 'diagonal',
        opacity: [.98, .98],
        isPausedWhenNotInView: true,
        states: {
            "default-state": {
                gradients: [
                    ['#ffc845', '#bf3654'],
                    ['#f58770', '#bf3654']
                ],
                transitionSpeed: 2000
            }
        }
    });

    var granimInstance = new Granim({
        element: '.ticker',
        direction: 'diagonal',
        opacity: [.98, .98],
        isPausedWhenNotInView: true,
        states: {
            "default-state": {
                gradients: [
                    ['#ffc845', '#bf3654'],
                    ['#f58770', '#bf3654']
                ],
                transitionSpeed: 2000
            }
        }
    });


    // Append images as css background

    $('.background-img').each(function() {
        var path = $(this).children('img').attr('src');
        $(this).css('background-image', 'url("' + path + '")').css('background-position', 'initial');
    });



    //wrap select currency converter

    $('.cryptonatorwidget select').each(function() {
        var $select = $(this);
        $select.wrap('<div class=" block-select"></div>');

    });


    //Instagram setup

    var instaFeed = new Instafeed({
        get: 'user',
        userId: '6965103190',
        accessToken: '6965103190.1740e6f.ccdf9896d9bb45409caa4d8428937e1e',
        limit: 6,
        resolution: 'standard_resolution',
        template: '<li class="col-sm-4 col-xs-4"><a href="{{link}}"><img src="{{image}}"/></a></li>'
    });
    instaFeed.run();


    //Twitter setup

    var twitterConfig = {
        "id": '347821849301897217',
        "domId": 'twitter-feed',
        "maxTweets": 2,
        "enableLinks": true,
        "showUser": false,
        "showTime": false,
        "lang": 'en'
    };
    twitterFetcher.fetch(twitterConfig);


    //Search form setup

    var btn = $('.block-helpers.icons li ul li:last-child a');
    var searchForm = {

        container: $('.block-search-form'),


        config: {
            effect: 'slideToggle',
            speed: '300'
        },

        init: function(config) {

            $.extend(this.config, config);
            btn.on('click', this.show);

        },

        show: function() {


            var sf = searchForm,
                container = sf.container,
                config = sf.config;

            if (container.is(':hidden')) {

                searchForm.close.call(container);
                searchForm.container[config.effect](config.speed);

            }
        },

        close: function() {

            var $this = $(this);

            if ($this.find('span.search-close').length) return;

            document.onkeydown = function(e) {
                e = e || window.event;
                if (e.keyCode == 27) {

                    $this[searchForm.config.effect](searchForm.config.effect.speed);
                }
            };

            $('<span class=close-search></span>')
                .prependTo($this)
                .on('click', function() {
                    $this[searchForm.config.effect](searchForm.config.effect.speed);
                })
        }
    };

    searchForm.init({
        effect: 'fadeToggle',
        speed: '300'
    });


})(jQuery);




//Map location setup

function initializeMap() {



    var styles = [{


                "elementType": "geometry",
                "stylers": [{
                    "color": "#f5f5f5"
                }]
            },
            {
                "elementType": "labels.icon",
                "stylers": [{
                    "visibility": "off"
                }]
            },
            {
                "elementType": "labels.text.fill",
                "stylers": [{
                    "color": "#616161"
                }]
            },
            {
                "elementType": "labels.text.stroke",
                "stylers": [{
                    "color": "#f5f5f5"
                }]
            },
            {
                "featureType": "administrative.land_parcel",
                "elementType": "labels.text.fill",
                "stylers": [{
                    "color": "#bdbdbd"
                }]
            },
            {
                "featureType": "poi",
                "elementType": "geometry",
                "stylers": [{
                    "color": "#eeeeee"
                }]
            },
            {
                "featureType": "poi",
                "elementType": "labels.text.fill",
                "stylers": [{
                    "color": "#757575"
                }]
            },
            {
                "featureType": "poi.park",
                "elementType": "geometry",
                "stylers": [{
                    "color": "#e5e5e5"
                }]
            },
            {
                "featureType": "poi.park",
                "elementType": "labels.text.fill",
                "stylers": [{
                    "color": "#9e9e9e"
                }]
            },
            {
                "featureType": "road",
                "elementType": "geometry",
                "stylers": [{
                    "color": "#ffffff"
                }]
            },
            {
                "featureType": "road.arterial",
                "elementType": "labels.text.fill",
                "stylers": [{
                    "color": "#757575"
                }]
            },
            {
                "featureType": "road.highway",
                "elementType": "geometry",
                "stylers": [{
                    "color": "#dadada"
                }]
            },
            {
                "featureType": "road.highway",
                "elementType": "labels.text.fill",
                "stylers": [{
                    "color": "#616161"
                }]
            },
            {
                "featureType": "road.local",
                "elementType": "labels.text.fill",
                "stylers": [{
                    "color": "#9e9e9e"
                }]
            },
            {
                "featureType": "transit.line",
                "elementType": "geometry",
                "stylers": [{
                    "color": "#e5e5e5"
                }]
            },
            {
                "featureType": "transit.station",
                "elementType": "geometry",
                "stylers": [{
                    "color": "#eeeeee"
                }]
            },
            {
                "featureType": "water",
                "elementType": "geometry",
                "stylers": [{
                    "color": "#c9c9c9"
                }]
            },
            {
                "featureType": "water",
                "elementType": "labels.text.fill",
                "stylers": [{
                    "color": "#9e9e9e"
                }]
            }
        ],

        lat = 39.148352,
        lng = -84.443999,




        customMap = new google.maps.StyledMapType(styles, {
            name: 'Styled Map'
        }),


        mapOptions = {
            zoom: 14,
            scrollwheel: false,
            disableDefaultUI: true,
            draggable: true,
            center: new google.maps.LatLng(lat, lng),
            mapTypeControlOptions: {
                mapTypeIds: [google.maps.MapTypeId.ROADMAP]
            }
        },
        map = new google.maps.Map(document.getElementById('map'), mapOptions),
        myLatlng = new google.maps.LatLng(lat, lng),




        marker = new google.maps.Marker({
            position: myLatlng,
            map: map,
            icon: {
                url: 'img/marker.png',
                scaledSize: new google.maps.Size(40, 40)
            }
        });




    map.mapTypes.set('map_style', customMap);
    map.setMapTypeId('map_style');



    var transitLayer = new google.maps.TransitLayer();
    transitLayer.setMap(map);


}