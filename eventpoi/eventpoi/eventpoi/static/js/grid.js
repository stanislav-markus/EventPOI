var temp = "<a href='{img_href}'><div class='cell' style='width:{width}px; height: {height}px; background-image: url({index})'></div></a>";
var w = 110, h = 85, html = '';
$('.gallery-photo a').each(function() {
	img_href = $(this).attr('href');
	img_display_url = $(this).find('img').attr('src');
	html += temp.replace(/\{height\}/g, h).replace(/\{width\}/g, w).replace("{index}", img_display_url).replace("{img_href}", img_href);
});
$("#freewall").html(html);


$('#all-photos').hide();

var wall = new freewall("#freewall");
wall.reset({
	selector: '.cell',
	animate: true,
	cellW: 110,
	cellH: 85,
	onResize: function() {
		wall.refresh();
	}
});
wall.fitWidth();
// for scroll bar appear;
$(window).trigger("resize");