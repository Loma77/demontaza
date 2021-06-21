function openNav() {
    if (window.innerWidth > 756) {
	document.getElementById("custom-sidenav").style.width = "20%";
    }
    else {
    document.getElementById("custom-sidenav").style.width = "100%";
    }
}

function closeNav() {
	document.getElementById("custom-sidenav").style.width = "0";
}

//Slick slider
$(document).ready(function () {
	$('.slick_container').slick({
		autoplay: true,
		dots: true,
		infinite: true,
		speed: 300,
		autoplaySpeed: 5000,
		slidesToShow: 1,
		adaptiveHeight: true
	});

	$('.scrollTo').click(function(){
    $('html, body').animate({
        scrollTop: $( $(this).attr('href') ).offset().top + (-10)
    }, 1000);
    return false;
});

});
