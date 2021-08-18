/*
 * %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 *

 * Version: 2.0
 *
 * %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 */


/*
===========================================================
    #INDEX#
===========================================================

    --> Custom Functions
    --> Preloader Activation
    --> Meanmenu Activation
    --> Inline Background Image
    --> Header Search Form
    --> Heroslider Height
    --> Button Effect
    --> Slider Activations
        --> Heroslider Activation
        --> Text Heroslider Activation
        --> Testimonial Slider
        --> Blog Slider Activation
        --> Brand Logo Slider
        --> Portfolio Gallery Slider
        --> Blog Gallery Slider
        --> Product Details Gallery
        --> Slider Activations Initializer
    --> CounterUp Activation
    --> Wowjs Activation
    --> Popup Activations
        --> Video Pupup Activation
        --> Portfolio Image Popup Activation
        --> Portfolio Details Image Popup Activation
        --> Product Details Image Zoom Activation
        --> Popup Initializations
    --> Portfolio Filter
    --> Blog Masonry Active
    --> Range Slider Active
    --> Nice Select Active
    --> Product Quantitybox
    --> Product Details Zoom Image Change
    --> Product Details Color & Size Active
    --> Product Rating Input
    --> Different Address Form
    --> Checkout Payment Method
    --> Scroll Up Active
    --> Modal Slick Conflict
    --> Sticky Header
    --> Parallax Active
    --> Video Background Active
    --> Ajax Mailchimp
    --> Dropdown Overflow
    --> Datepicker
    --> Tooltip Activation
    --> Section Title Animation
    --> Fixed Footer
    --> Sticky Sidebar Active
    --> Ripple Js Active
    --> Dropdown Has Children
    --> Initializer

===========================================================
    #END INDEX#
===========================================================
*/



(function ($) {
    "use strict";

    $(window).on('load', function () {
        deconsult.preloaderActivation();
        deconsult.preloaderCancel();
    });

    /* Custom Functions */
    jQuery.fn.exists = function () {
        return this.length > 0;
    };

    var deconsult = {

        /* Preloader Activation */
        preloaderActivation: function () {
            $('.tm-preloader').delay(150).fadeOut('slow');
        },
        preloaderCancel: function () {
            $('.tm-preloader').find('.tm-button').on('click', function () {
                $(this).parent('.tm-preloader').fadeOut('slow');
            });
        },

        /* Meanmenu Activation */
        meanmenuActivation: function () {
            $('nav.tm-navigation').meanmenu({
                meanMenuContainer: '.tm-mobilenav',
                meanScreenWidth: '991',
                meanMenuOpen: '<i class="fa fa-bars"></i>',
                meanMenuClose: '<i class="fa fa-close"></i>'
            });
        },

        /* Inline Background Image */
        dataBgImage: function () {
            $('[data-bgimage]').each(function () {
                var imageUrl = $(this).data('bgimage');
                $(this).css({
                    'background-image': 'url(' + imageUrl + ')'
                });
            });
        },

        /* Header Search Form */
        haderSearchForm: function () {
            $('.header-searchtrigger').on('click', function (e) {
                e.preventDefault();
                $(this).find('i').toggleClass('fa-close');
                $('.header-searchbox').toggleClass('is-visible');
            });
        },

        /* Heroslider Height */
        herosliderHeight: function () {
            var headerHeight = $('.header').innerHeight();

            $('.heroslider-single').css({
                'min-height': 'calc(100vh - ' + headerHeight + 'px)',
            });
        },

        /* Button Effect */
        buttonEffect: function () {
            $('.tm-button')
                .on('mouseenter', function (e) {
                    var parentOffset = $(this).offset(),
                        relX = e.pageX - parentOffset.left,
                        relY = e.pageY - parentOffset.top;
                    $(this).find('b').css({
                        top: relY,
                        left: relX
                    });
                })
                .on('mouseout', function (e) {
                    var parentOffset = $(this).offset(),
                        relX = e.pageX - parentOffset.left,
                        relY = e.pageY - parentOffset.top;
                    $(this).find('b').css({
                        top: relY,
                        left: relX
                    });
                });
            $('[href="#"]').on('click', function () {
                return false;
            });
        },

        /* Slider Activations */
        sliderActivations: {

            /* Heroslider Activation */
            heroSliderActivation: function () {
                $('.heroslider-slider:not(.heroslider-textslider)').on('init reInit afterChange', function (event, slick, currentSlide, nextSlide) {
                    var i = (currentSlide ? currentSlide : 0) + 1;
                    $('.heroslider-slidecounter')
                        .html('<span class="current-slide">' + i + '</span><span class="total-slide">' + slick.slideCount + '</span>');
                });

                $('.heroslider-slider:not(.heroslider-textslider)').slick({
                    infinite: true,
                    autoplay: true,
                    autoplaySpeed: 7000,
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    arrows: true,
                    prevArrow: '<button class="tm-slider-arrow-prev"><i class="fa fa-angle-left"></i></button>',
                    nextArrow: '<button class="tm-slider-arrow-next"><i class="fa fa-angle-right"></i></button>',
                    dots: false,
                    draggable: false,
                    cssEase: 'ease-in-out',
                    easing: 'ease-in-out',
                    speed: 1500,
                });

                $('.heroslider-slider:not(.heroslider-textslider)').on('init beforeChange', function (event, slick, currentSlide, nextSlide) {
                    $(this).find('.slick-slide').find('.heroslider-content').css({
                        '-webkit-transform': 'translate(0) translateZ(30px)',
                        '-ms-transform': 'translate(0) translateZ(30px)',
                        'transform': 'translate(0) translateZ(30px)',
                    });
                    $(this).find('.slick-current').find('.heroslider-content').css({
                        '-webkit-transform': 'translate(300px) translateZ(30px)',
                        '-ms-transform': 'translate(300px) translateZ(30px)',
                        'transform': 'translate(300px) translateZ(30px)',
                    });
                });
            },

            /* Text Heroslider Activation */
            heroSliderTextslider: function () {
                $('.heroslider-textslider').on('init reInit afterChange', function (event, slick, currentSlide, nextSlide) {
                    var i = (currentSlide ? currentSlide : 0) + 1;
                    $('.heroslider-slidecounter')
                        .html('<span class="current-slide">' + i + '</span><span class="total-slide">' + slick.slideCount + '</span>');
                });
                $('.heroslider-textslider').slick({
                    infinite: true,
                    autoplay: true,
                    autoplaySpeed: 7000,
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    arrows: true,
                    prevArrow: '<button class="tm-slider-arrow-prev"><i class="fa fa-angle-left"></i></button>',
                    nextArrow: '<button class="tm-slider-arrow-next"><i class="fa fa-angle-right"></i></button>',
                    dots: false,
                    draggable: false,
                    cssEase: 'ease-in-out',
                    easing: 'ease-in-out',
                    speed: 1200,
                });
            },

            /* Testimonial Slider */
            testimonialSliderActivation: function () {
                $('.testimonial-slider-active').slick({
                    infinite: true,
                    autoplay: true,
                    autoplaySpeed: 5000,
                    slidesToShow: 2,
                    slidesToScroll: 1,
                    arrows: false,
                    dots: false,
                    adaptiveHeight: true,
                    speed: 1000,
                    responsive: [{
                        breakpoint: 768,
                        settings: {
                            slidesToShow: 1,
                            slidesToScroll: 1
                        }
                    }]
                });
            },

            /* Blog Slider Activation */
            blogSliderActivation: function () {
                $('.blog-slider-active').slick({
                    infinite: true,
                    autoplay: true,
                    autoplaySpeed: 5000,
                    slidesToShow: 3,
                    arrows: true,
                    prevArrow: '<button class="tm-slider-arrow-prev"><i class="fa fa-angle-left"></i></button>',
                    nextArrow: '<button class="tm-slider-arrow-next"><i class="fa fa-angle-right"></i></button>',
                    dots: false,
                    speed: 1000,
                    responsive: [{
                            breakpoint: 992,
                            settings: {
                                slidesToShow: 2,
                            }
                        },
                        {
                            breakpoint: 768,
                            settings: {
                                slidesToShow: 1,
                            }
                        }
                    ]
                });
            },

            /* Brand Logo Slider */
            brandlogoSliderActivation: function () {
                $('.brandlogo-slider').slick({
                    infinite: true,
                    autoplay: true,
                    autoplaySpeed: 5000,
                    slidesToShow: 5,
                    slidesToScroll: 2,
                    arrows: true,
                    prevArrow: '<button class="tm-slider-arrow-prev"><i class="fa fa-angle-left"></i></button>',
                    nextArrow: '<button class="tm-slider-arrow-next"><i class="fa fa-angle-right"></i></button>',
                    dots: false,
                    speed: 1000,
                    responsive: [{
                            breakpoint: 992,
                            settings: {
                                slidesToShow: 3,
                                slidesToScroll: 2,
                            }
                        },
                        {
                            breakpoint: 768,
                            settings: {
                                slidesToShow: 2,
                                slidesToScroll: 1
                            }
                        },
                        {
                            breakpoint: 420,
                            settings: {
                                slidesToShow: 1,
                                slidesToScroll: 1
                            }
                        }
                    ]
                });
            },

            /* Portfolio Gallery Slider */
            portfolioGallerySliderActivation: function () {
                $('.tm-portfoliodetails-gallery').slick({
                    infinite: false,
                    autoplay: true,
                    autoplaySpeed: 5000,
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    arrows: true,
                    prevArrow: '<button class="tm-slider-arrow-prev"><i class="fa fa-angle-left"></i></button>',
                    nextArrow: '<button class="tm-slider-arrow-next"><i class="fa fa-angle-right"></i></button>',
                    dots: false,
                });
            },

            /* Blog Gallery Slider */
            blogGallerySliderActivation: function () {
                $('.tm-blog-imageslider').slick({
                    infinite: true,
                    autoplay: true,
                    autoplaySpeed: 5000,
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    arrows: false,
                    dots: true,
                });
            },

            /* Product Details Gallery */
            productDetailsGallery: function () {
                $('.tm-prodetails-largeimages').slick({
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    arrows: false,
                    fade: true,
                    loop: false,
                    asNavFor: '.tm-prodetails-thumbnails'
                });
                $('.tm-prodetails-thumbnails').slick({
                    slidesToShow: 3,
                    slidesToScroll: 1,
                    loop: false,
                    asNavFor: '.tm-prodetails-largeimages',
                    dots: false,
                    centerMode: true,
                    arrows: true,
                    prevArrow: '<button class="tm-slider-arrow-prev"><i class="fa fa-angle-left"></i></button>',
                    nextArrow: '<button class="tm-slider-arrow-next"><i class="fa fa-angle-right"></i></button>',
                    focusOnSelect: true
                });
            },

            /* Slider Activations Initializer ( Just Remove a single line if you want to disable any slider ) */
            init: function () {
                deconsult.sliderActivations.heroSliderActivation();
                deconsult.sliderActivations.heroSliderTextslider();
                deconsult.sliderActivations.testimonialSliderActivation();
                deconsult.sliderActivations.blogSliderActivation();
                deconsult.sliderActivations.brandlogoSliderActivation();
                deconsult.sliderActivations.portfolioGallerySliderActivation();
                deconsult.sliderActivations.blogGallerySliderActivation();
                deconsult.sliderActivations.productDetailsGallery();
            }

        },

        /* CounterUp Activation */
        counterupActivation: function () {
            if ($('.odometer').length) {
                $(window).on('scroll', function () {
                    function winScrollPosition() {
                        var scrollPos = $(window).scrollTop(),
                            winHeight = $(window).height();
                        var scrollPosition = Math.round(scrollPos + (winHeight / 1.2));
                        return scrollPosition;
                    }
                    var elemOffset = $('.odometer').offset().top;
                    if (elemOffset < winScrollPosition()) {

                        $('.odometer').each(function () {
                            $(this).html($(this).data('count-to'));
                        });
                    }
                });
            }
        },

        /* Wowjs Activation */
        wowJsActive: function () {
            var wow = new WOW({
                boxClass: 'wow',
                animateClass: 'animated',
                offset: 0,
                mobile: true,
                live: true
            });
            wow.init();
        },

        /* Popup Activations */
        popupActivation: {

            /* Video Pupup Activation */
            videoPopup: function () {
                $('.tm-videobutton').lightGallery({
                    selector: 'a'
                });
            },

            /* Portfolio Image Popup Activation */
            portfolioImagePopup: function () {
                $('.tm-portfolio').lightGallery({
                    selector: '.zoom-button a',
                    thumbnail: false,
                });
            },

            /* Portfolio Details Image Popup Activation */
            portfolioDetailsImagePopup: function () {
                $('.tm-portfoliodetails-image').lightGallery({
                    selector: 'a',
                    thumbnail: false,
                });
            },

            /* Product Details Image Zoom Activation */
            productDetailsImageZoom: function () {
                $('.tm-prodetails-largeimages').lightGallery({
                    selector: 'a',
                    thumbnail: false,
                });
            },

            /* Popup Initializations */
            init: function () {
                deconsult.popupActivation.videoPopup();
                deconsult.popupActivation.portfolioImagePopup();
                deconsult.popupActivation.portfolioDetailsImagePopup();
                deconsult.popupActivation.productDetailsImageZoom();
            }
        },

        /* Portfolio Filter */
        portfolioFilter: function () {
            $('.tm-portfolio-wrapper').imagesLoaded({
                background: true
            }, function () {
                $('.tm-portfolio-wrapper').isotope({
                    itemSelector: '.tm-portfolio-item',
                    layoutMode: 'masonry',
                    masonry: {
                        columnWidth: 1,
                    }
                });
            });

            $('.tm-portfolio-buttons button').on('click', function () {
                var filterValue = $(this).attr('data-filter');
                $('.tm-portfolio-wrapper').isotope({
                    filter: filterValue
                });

                $('.tm-portfolio-buttons button').removeClass('is-active');
                $(this).addClass('is-active');
            });
        },

        /* Blog Masonry Active */
        blogMasonryActive: function () {
            $('.blog-masonry-active').masonry({
                itemSelector: '.blog-masonry-item'
            });
        },

        /* Range Slider Active */
        rangeSlider: function () {
            $('.tm-rangeslider').nstSlider({
                'left_grip_selector': '.tm-rangeslider-leftgrip',
                'right_grip_selector': '.tm-rangeslider-rightgrip',
                'value_bar_selector': '.tm-rangeslider-bar',
                'value_changed_callback': function (cause, leftValue, rightValue) {
                    $(this).parent().find('.tm-rangeslider-leftlabel').text(leftValue);
                    $(this).parent().find('.tm-rangeslider-rightlabel').text(rightValue);
                }
            });
        },

        /* Nice Select Active */
        niceSelectActive: function () {
            $('select').niceSelect();
        },

        /* Product Quantitybox */
        productQuantityBox: function () {
            $('.tm-quantitybox').append('<div class="decrement-button tm-quantitybox-button">-</i></div><div class="increment-button tm-quantitybox-button">+</div>');
            $('.tm-quantitybox-button').on('click', function () {
                var button = $(this);
                var quantityOldValue = button.parent().find('input').val();
                var quantityNewVal;
                if (button.text() == "+") {
                    quantityNewVal = parseFloat(quantityOldValue) + 1;
                } else {
                    if (quantityOldValue > 1) {
                        quantityNewVal = parseFloat(quantityOldValue) - 1;
                    } else {
                        quantityNewVal = 1;
                    }
                }
                button.parent().find('input').val(quantityNewVal);
            });
        },

        /* Product Details Color & Size Active */
        productDetailsColorSize: function () {
            $('.tm-prodetails-color ul li, .tm-prodetails-size ul li').on('click', 'span', function (e) {
                e.preventDefault();
                $(this).parent('li').addClass('is-checked').siblings().removeClass('is-checked');
            });
        },

        /* Product Rating Input */
        productRatingInput: function () {
            $('.tm-rating-input').each(function () {
                $(this).find('span').on('mouseenter', function () {
                    $('.tm-rating-input span').addClass('active');
                    $(this).nextAll('span').removeClass('active');
                });

            });
        },

        /* Different Address Form */
        differentAddressFormToggle: function () {
            $('#billform-dirrentswitch').on('change', function () {
                if ($(this).is(':checked')) {
                    $('.tm-checkout-differentform').slideDown();
                } else {
                    $('.tm-checkout-differentform').slideUp();
                }
            });
        },

        /* Checkout Payment Method */
        checkoutPaymentMethod: function () {
            $('.tm-checkout-payment input[type="radio"]').each(function () {
                if ($(this).is(':checked')) {
                    $(this).siblings('.tm-checkout-payment-content').slideDown();
                }
                $(this).siblings('label').on('click', function () {
                    $('.tm-checkout-payment input[type="radio"]').prop('checked', false).siblings('.tm-checkout-payment-content').slideUp();
                    $(this).prop('checked', true).siblings('.tm-checkout-payment-content').slideDown();
                });
            });
        },

        /* Scroll Up Active */
        scrollUpActive: function () {
            $.scrollUp({
                scrollName: 'scrollUp',
                topDistance: '300',
                topSpeed: 1000,
                animation: 'fade',
                animationInSpeed: 1000,
                animationOutSpeed: 1000,
                scrollText: '<i class="fa fa-angle-up"></i>',
                activeOverlay: false,
            });
        },

        /* Modal Slick Conflict */
        modalSlickConflict: function () {
            $('.tm-quickview-popup').on('show.bs.modal', function () {
                $('.tm-prodetails-thumbnails').slick('slickNext');
            });
        },

        /* Sticky Header */
        stickyHeader: function () {
            $(window).on('scroll', function () {
                var scrollPos = $(this).scrollTop();
                if (scrollPos > 220) {
                    $('.sticky-header').addClass('sticky-active');
                } else {
                    $('.sticky-header').removeClass('sticky-active');
                }
            });
        },

        /* Parallax Active */
        parallaxActive: function () {
            $('.tm-parallax').jarallax({
                speed: 1.15
            });
        },

        /* Video Background Active */
        videoBackgroundActive: function () {
            if ($('.tm-videobg').exists()) {
                $('.tm-videobg').YTPlayer();
            }
        },


        /* Ajax Mailchimp */
        ajaxMailchimp: function () {
            $('#tm-mailchimp-form').ajaxChimp({
                language: 'en',
                callback: mailChimpResponse,
                // ADD YOUR MAILCHIMP URL BELOW HERE!
                url: 'YOUR_MAILCHIMP_URL_HERE'
            });

            function mailChimpResponse(resp) {
                if (resp.result === 'success') {
                    $('.tm-mailchimp-success').html('' + resp.msg).fadeIn(900);
                    $('.tm-mailchimp-error').fadeOut(400);
                } else if (resp.result === 'error') {
                    $('.tm-mailchimp-error').html('' + resp.msg).fadeIn(900);
                }
            }
        },

        /* Dropdown Overflow */
        menuOverflow: function () {
            $('.tm-navigation ul li').on('mouseenter mouseleave', function (e) {
                if ($('ul', this).length) {
                    var listElem = $('ul:first', this);
                    var listElemOffset = listElem.offset();
                    var leftValue = listElemOffset.left - $('body').offset().left;
                    var widthValue = listElem.width();

                    if (listElem.find('ul').length) {
                        widthValue = listElem.width() * 2;
                    }

                    var docW = $('body').width();
                    var isEntirelyVisible = (leftValue + widthValue <= docW);

                    if (!isEntirelyVisible) {
                        $(this).addClass('overflow-element');
                    } else {
                        $(this).removeClass('overflow-element');
                    }
                }
            });
        },


        /* Datepicker */
        datepickerActivation: function () {
            $('[data-toggle="datepicker"]').datepicker();
        },


        /* Tooltip Activation */
        tooltipActivation: function () {
            $('[data-toggle="tooltip"]').tooltip();
        },


        /* Section Title Animation */
        sectionTitleAnimation: function () {
            $('.tm-section').each(function () {
                var checkStatus = $(this).find('.tm-section-title .divider').length;

                if (checkStatus) {
                    $(this).on('mouseover', function () {
                        $(this).find('.tm-section-title .divider').addClass('animateon');
                    }).on('mouseout', function () {
                        $(this).find('.tm-section-title .divider').removeClass('animateon');
                    });
                }
            });
        },

        /* Fixed Footer */
        fixedFooter: function () {
            var winWidth = $(window).width() > 991,
                checkFooter = $('.footer').hasClass('fixed-footer'),
                footerHeight = $('.footer').height();
            if (winWidth && checkFooter) {
                $('.footer').css({
                    'position': 'fixed',
                    'left': 0,
                    'bottom': 0,
                    'right': 0,
                    'width': 100 + '%',
                    'z-index': -2
                });
                $('.wrapper').css('margin-bottom', footerHeight);
            }
        },

        /* Sticky Sidebar Active */
        stickySidebarActive: function () {
            var winWidth = $(window).width();
            if (winWidth > 991) {
                $('.sticky-sidebar').stickySidebar({
                    topSpacing: 0,
                    bottomSpacing: 30
                });
            }
        },

        /* Ripple Js Active */
        rippleJsActive: function () {
            if ($('.tm-rippple-active').exists()) {
                $('.tm-rippple-active').ripples();
            }
        },

        /* Dropdown Has Children 最新最全最好的Bootstrap模板：http://www.bootstrapmb.com*/
        dropdownHasChildren: function () {
            $('.tm-navigation-dropdown ul li').each(function () {
                if ($(this).children('ul').length) {
                    $(this).addClass('has-child');
                }
            });
        },


        /* Initializer */
        init: function () {
            deconsult.meanmenuActivation();
            deconsult.dataBgImage();
            deconsult.haderSearchForm();
            deconsult.herosliderHeight();
            deconsult.buttonEffect();
            deconsult.sliderActivations.init();
            deconsult.counterupActivation();
            deconsult.wowJsActive();
            deconsult.popupActivation.init();
            deconsult.portfolioFilter();
            deconsult.blogMasonryActive();
            deconsult.rangeSlider();
            deconsult.niceSelectActive();
            deconsult.productQuantityBox();
            deconsult.productDetailsColorSize();
            deconsult.productRatingInput();
            deconsult.differentAddressFormToggle();
            deconsult.checkoutPaymentMethod();
            deconsult.scrollUpActive();
            deconsult.modalSlickConflict();
            deconsult.stickyHeader();
            deconsult.parallaxActive();
            deconsult.videoBackgroundActive();
            deconsult.ajaxMailchimp();
            deconsult.menuOverflow();
            deconsult.datepickerActivation();
            deconsult.tooltipActivation();
            deconsult.sectionTitleAnimation();
            deconsult.fixedFooter();
            deconsult.stickySidebarActive();
            deconsult.rippleJsActive();
            deconsult.dropdownHasChildren();
        }
    };

    deconsult.init();

})(jQuery);