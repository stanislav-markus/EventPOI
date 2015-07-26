var image_item=$("a.image_effect");

image_item.each(function() {
	if ( $(this).find('.imagemask').length === 0 ) {
		var img_width = $(this).find('img').width();
		var img_height = $(this).find('img').innerHeight();
		var imageClass = $(this).attr("class");
		$(this).prepend('<span class="imagemask '+imageClass+'"></span>');

		var p = $(this).find('img');
		var position = p.position();
		var PosTop = parseInt(p.css("margin-top")) + position.top;
		var PosLeft = parseInt(p.css("margin-left")) + position.left;
			if (!PosLeft) {PosLeft = position.left};

		$(this).find('.imagemask').css({top: PosTop});
		$(this).find('.imagemask').css({left: PosLeft});

		$('.imagemask', this).css({width:img_width,height:img_height,backgroundPosition:'center center'});
		//for IE Browser
		if($.browser.msie){ $('.imagemask', this).css({display:'none'});}
	}
});


var image_effect= $("a.image_effect");
//ignore the shadow effect if browser IE
if ($.browser.msie) {
	image_effect.mouseover(function() {
	$(this).find('.imagemask').stop().css({
		display:"block", "z-index":"400"
	});

	}).mouseout(function() {
		$(this).find('.imagemask').stop().css({
			 display:"none","z-index":"0"
			} );
	});
} else {
	//other browsers
	image_effect.mouseover(function() {
		$(this).find('.imagemask').stop().animate({
			display:"block",
			opacity:1,
			"z-index":"400"
		}, 100);
		$(this).find('img').stop().animate({
			opacity: 0.7
		}, 200);
	}).mouseout(function() {
		$(this).find('.imagemask').stop().animate({
			display:"none",
			opacity:0,
			"z-index":"0"
		}, 100 );
		$(this).find('img').stop().animate({
			opacity: 1
		}, 300);
	});
}