$(document).ready(function() {
	$('.slider').slick({
		infinite: true,
		slidesToShow: 3,
		dots: true,
		adaptiveHeight: true,
		responsive: [ {
			breakpoint: 1170, 
			settings: {
				slidesToShow: 2
			}
		}, {
			breakpoint: 880, 
			settings: {
				slidesToShow: 1
			}
		}
		],
	})
})

$(document).ready(function() {
	$('.gallery').slick({
		infinite: true,
		slidesToShow: 3,
		dots: true,
		adaptiveHeight: true,
		responsive: [ {
			breakpoint: 1170, 
			settings: {
				slidesToShow: 2
			}
		}, {
			breakpoint: 720, 
			settings: {
				slidesToShow: 1
			}
		}
		],
	})
})

$(document).ready(function() {
	$('.reviews').slick({
		infinite: false,
		arrows: false,
		dots: true,
		slidesToShow: 3,
		step: 1,
		responsive: [ {
			breakpoint: 1070, 
			settings: {
				slidesToShow: 2
			}
		}, {
			breakpoint: 720, 
			settings: {
				slidesToShow: 1
			}
		}
		],
	})
})