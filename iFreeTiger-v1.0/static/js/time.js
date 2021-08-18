$(function() {
	var bannerSlider = new Slider($('.banner_tabs'), {
		time: 5000,
		delay: 400,
		event: 'hover',
		auto: true,
		mode: 'fade',
		controller: $('.bannerCtrl'),
		activeControllerCls: 'active'
	});
	$('.banner_tabs .left').click(function() {
		bannerSlider.prev()
	});
	$('.banner_tabs .right').click(function() {
		bannerSlider.next()
	});
})