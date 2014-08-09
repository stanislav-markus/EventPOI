var BaseMap = {};
BaseMap.limit = 20;
BaseMap.points = [];
BaseMap.userPoints = {};
BaseMap.map = null;
BaseMap.markers = [];
BaseMap.infoWindow = null;
BaseMap.pointSlider = null;


var UserPage = {};
UserPage.limit = 5;


$.extend({
    getUrlVars: function(){
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
    },
        getUrlVar: function(name){
        return $.getUrlVars()[name];
    }
});


function photoHandlers() {

    $('#avatar_upload').fileupload({
        dataType : 'json',
        autoUpload : false,
        add : function(e, data) {
            data.formData = $("#avatar_form").serializeArray();
            data.submit();
            var files = data.files;
            if (files && files[0]) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    $('#avatar_href').attr('href',  e.target.result);
                    $('#avatar_img').attr('src', e.target.result);
                }
                reader.readAsDataURL(files[0]);
            }
            handlePhotoInput(files);
        }
    });


    function handlePhotoInput(files) {
        if (files && files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('#photo_preview').attr('src', e.target.result);
                $('#upload_zone').css('display', 'none');
                $('#photo_preview').css('display', 'block');
            }
            reader.readAsDataURL(files[0]);
        }
    }

    $('#photo_upload').on('change', function(evt) {
        var files = evt.target.files;
        handlePhotoInput(files);
    });

    $('#photo_upload').on('drop', function(evt) {
        var files = evt.originalEvent.dataTransfer.files;
        handlePhotoInput(files);
    });

    $('#photo_upload').on("dragenter", function(evt) {
        $('#upload_zone').css({
            'border': '5px dashed rgb(137, 150, 243)',
            'opacity': '0.4',
        });
    });

    $('#photo_upload').on("dragleave", function(evt) {
        $('#upload_zone').css({
            'border': '5px dashed #fff',
            'opacity': '1',
        });
    });

}


function userPoiTemplate(from, to) {

    UserPage.from = from;
    UserPage.to = to;

    var allow_to_remove = '';
    var user_pois = $('#user_pois');
    user_pois.empty();
    owner = user_pois.attr('owner');
    user = user_pois.attr('user');
    points = BaseMap.userPoints[owner];

    if (!points) {
        return;
    }

    if (to < points.length) {
        $('.next_page').css('visibility', 'visible');
        var next = true;
    } else {
        $('.next_page').css('visibility', 'hidden');
        var next = false;
    }
    if (from > 0) {
        $('.prev_page').css('visibility', 'visible');
        var prev = true;
    } else {
        $('.prev_page').css('visibility', 'hidden');
        var prev = false;
    }


    $('#user_pois').bind('mousewheel', function(e) {
        if (e.originalEvent.wheelDelta / 120 > 0) {
            if (prev) {
                $('#user_pois').unbind('mousewheel');
                userPoiTemplate(from - UserPage.limit, from);
            }
        } else {
            if (next) {
                $('#user_pois').unbind('mousewheel');
                userPoiTemplate(to, to + UserPage.limit);
            }
        }
    });


    $('.next_page').click(function() {
        $('.next_page').off('click');
        userPoiTemplate(to, to + UserPage.limit);
    });

    $('.prev_page').click(function() {
        $('.prev_page').off('click');
        userPoiTemplate(from - UserPage.limit, from);
    });

    
    $.each(points.slice(from, to), function(i, point) {
        point = point[0];
        var date = new Date(point.date).toDateString();
        if (owner == user) {
            allow_to_remove = '\
                <a id="' + point.id + '" class="poi_remove" href="#">\
                    <span class="glyphicon glyphicon-trash"></span>\
                </a>';
        }
        var template = '<ul id="poi_' + point.id + '" class="media-list">\
            <li class="media bg-warning">\
                <p class="p_media"><span class="frame alignleft">\
                <a class="pull-left image_effect zoom" href="' + point.photo.image + '" rel="prettyPhoto[userGallery]"\
                    title="' +
                        '&lt;a href=&#x27;/profile/' + point.user.username.toLowerCase() + '/&#x27; &gt;' +
                        '&lt;img class=&#x27;img-circle avatar left&#x27; src=&#x27;' + point.user.avatar_url + '&#x27;&gt;' +
                        '&lt;a class=&#x27;photo_title&#x27 href=&#x27/' + point.slug + '/&#x27;&gt;' +
                        point.name +
                        '&lt;/a&gt;' +
                        '&lt;br /&gt;' +
                        '&lt;span class=&#x27;glyphicon glyphicon-user&#x27;&gt;&lt;/span&gt; ' +
                        '&lt;a href=&#x27;/profile/' + point.user.username.toLowerCase() + '/&#x27;&gt;' +
                        point.user.username +
                        '&lt;/a&gt;&lt;br /&gt;' +
                        '&lt;p class=&#x27;photo_description&#x27;&gt;' + point.description + '&lt;/p&gt;' +
                        '">\
                    <img class="img-thumbnail" src="' + point.photo.thumbnail_url + '" width="100%">\
                </a>\
                </span></p>\
                <div class="media-body">\
                    <h4 class="media-heading media_heigth"><a href="/' + point.slug + '/">' + point.name + '</a></h4>'
                    + allow_to_remove +
                    '<br /><br />\
                    <div>\
                        <i class="glyphicon glyphicon-eye-open"></i>\
                        <span>' + point.photo.view_count + '</span>\
                    </div>\
                    <div>\
                        <i class="glyphicon glyphicon-time"></i>\
                        <span>' + date + '</span>\
                    </div>\
                </div>\
            </li>\
        </ul>'

        user_pois.append(template);
    });
    hideTitles();
    $.getScript('/static/js/hover.js');
    refreshPrettyPhoto();

}


function fixtures() {

    $.ajaxSetup({
        cache: true
    });

    $(".scrollable_detail").mCustomScrollbar();

    $('#text_area').elastic();

    var username = $('#nav_username').text();
    if(username.length > 10) {
        username = username.substring(0,10);
        $('#nav_username').html('<span class="glyphicon glyphicon-user"></span>' + username + '...');
    }

    var showChar = 100;
    var ellipsestext = "...";
    var moretext = "more";
    var lesstext = "less";
    $('.more').each(function() {
        var content = $(this).html();
 
        if(content.length > showChar) {
 
            var c = content.substr(0, showChar);
            var h = content.substr(showChar-1, content.length - showChar);
 
            var html = c + '<span class="moreellipses">' + ellipsestext+ '&nbsp;</span><span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<a href="" class="morelink">' + moretext + '</a></span>';
 
            $(this).html(html);
        }
 
    });
 
    $(".morelink").click(function(){
        if($(this).hasClass("less")) {
            $(this).removeClass("less");
            $(this).html(moretext);
        } else {
            $(this).addClass("less");
            $(this).html(lesstext);
        }
        $(this).parent().prev().toggle();
        $(this).prev().toggle();
        return false;
    });

}


function refreshPrettyPhoto() {
    $("a[rel^='prettyPhoto']").prettyPhoto();
}


$('#show_comments').click(function () {
    $('#poi_edit_group .preview').slideUp('slow');
    $('#poi_edit_group .comments').slideDown('slow');
});

$('#hide_comments').click(function() {
    $('#poi_edit_group .comments').slideUp('slow');
    $('#poi_edit_group .preview').slideDown('slow');
    return false;
});


$('#add_comment').click(function() {
    var form = $('#comment_form');
    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr);
            if ( $(xhr).find('.errorlist').length > 0 ) {
                var form_div = form.find('.form-group');
                if ( form_div.find('.errorlist').length == 0 ) {
                    form_div.append($(xhr).find('.errorlist'));
                }
            } else {
                window.location.href ="";
            }
        }
    });
    return false;
});


$('.view_count.like a').click(function() {
    var poi_id = $(this).attr('id');
    var like_count = $('.view_count.like span').text();
    console.log(like_count);
    like_count++;
    var data = JSON.stringify({"like_count": like_count});
    $.ajax({
        dataType: "json",
        contentType: 'application/json',
        data: data,
        type: 'PUT',
        url: '/api/v1/poi/' + poi_id + '/',
        success: function(response) {
            $('.view_count.like span').text(like_count);
        }
    });
    return false;
});


$(document).on('click', '.poi_remove', function() {
    var poi_id = $(this).attr('id');
    $.ajax({
        dataType: "json",
        type: 'DELETE',
        url: '/api/v1/poi/' + poi_id + '/',
        success: function(response) {
            $("#poi_" + poi_id).css('display', 'none');
            $("#user_poi_count").html(parseInt($('#user_poi_count').html(), 10) - 1);
            $.when(BaseMap.getPOIs()).done(function() {
                BaseMap.filterSlider(BaseMap.map.getBounds());
                userPoiTemplate(UserPage.from, UserPage.from + UserPage.limit);
            });
        }
    });
    return false;
});


function searcPlace() {

    var markers = [];

    var input = (document.getElementById('pac-input'));
    BaseMap.map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    var searchBox = new google.maps.places.SearchBox((input));

    
    google.maps.event.addListener(searchBox, 'places_changed', function() {
        var places = searchBox.getPlaces();

        if (places.length == 0) {
          return;
        }
        for (var i = 0, marker; marker = markers[i]; i++) {
          marker.setMap(null);
        }

        markers = [];
        var bounds = new google.maps.LatLngBounds();
        for (var i = 0, place; place = places[i]; i++) {
            var image = {
                url: place.icon,
                size: new google.maps.Size(71, 71),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(17, 34),
                scaledSize: new google.maps.Size(25, 25)
            };

            var marker = new google.maps.Marker({
                map: BaseMap.map,
                icon: image,
                title: place.name,
                position: place.geometry.location
            });

            markers.push(marker);

            bounds.extend(place.geometry.location);
        }

        BaseMap.map.fitBounds(bounds);
    });
    google.maps.event.addListener(BaseMap.map, 'bounds_changed', function() {
        var bounds = BaseMap.map.getBounds();
        searchBox.setBounds(bounds);
    });    
}


function getPosition() {
    navigator.geolocation.getCurrentPosition(function(position) {
        var location = new google.maps.LatLng(position.coords.latitude,
                                        position.coords.longitude);
        BaseMap.map.setCenter(location);
        new google.maps.Marker({
            position: location, 
            map: BaseMap.map
        });
        BaseMap.map.setOptions({draggableCursor: null, zoom: 10});
    });
}


BaseMap.init = function(lat, lon) {

    fixtures();
    photoHandlers();

    var center = new google.maps.LatLng(16.959626, -5.991012);
    var options = {
        'zoom': 3,
        'minZoom': 3,
        'center': center,
        'mapTypeId': google.maps.MapTypeId.ROADMAP
    };

    BaseMap.map = new google.maps.Map(document.getElementById('map'), options);

    if (lat && lon) {
        var center = new google.maps.LatLng(lat, lon);
        BaseMap.map.setOptions({center: center, zoom: 10});
        if (window.location.pathname == '/poi/add/') {
            new google.maps.Marker({position: center, map: BaseMap.map});
        }
    }

    $('#my_location').click(function() {
        getPosition();
        return false;
    });

    searcPlace();

    BaseMap.infoWindow = new google.maps.InfoWindow();

    BaseMap.pointSlider = $('.items.gallery');


    google.maps.event.addListener(BaseMap.map, "bounds_changed", function() {
        if (BaseMap.points.length === 0) {
            $.when(BaseMap.getPOIs()).done(function() {
                BaseMap.filterSlider(BaseMap.map.getBounds());
                userPoiTemplate(0, UserPage.limit);
            });
        } else {
            BaseMap.filterSlider(BaseMap.map.getBounds());
        }
    }); 



    $('#add_marker').click(function() {
        $('#add_poi').addClass('active');
        BaseMap.map.setOptions({draggableCursor: 'crosshair'});
        google.maps.event.addListener(BaseMap.map, 'click', function(event) {
            BaseMap.placeMarker(event.latLng);
        });
        return false;
    });

};


$('#edit_poi').click(function() {
    $(this).off('click');
    $('#poi_edit_group').load('update/', function () {
        photoHandlers();
        fixtures();
    });
    return false;
});


BaseMap.clearOverlays = function() {
    for (var i = 0; i < BaseMap.markers.length; i++ ) {
        BaseMap.markers[i].setMap(null);
    }
    BaseMap.markers.length = 0;
}


BaseMap.getPOIs = function() {
    BaseMap.clearOverlays();
    return $.ajax({
        dataType: "json",
        url: '/pois/',
        success: function(response) {
            BaseMap.showMarkers(response.objects);
        }
    });
}


BaseMap.filterSlider = function(bounds) {
    var count = 0;
    var points = [];
    for (var i=0; i<BaseMap.points.length; i++) {
        var point = BaseMap.points[i];
        var latLng = new google.maps.LatLng(point.latitude,
            point.longitude);
        if (bounds.contains(latLng)) {
            points.push(point);
            count++;
            if (count > BaseMap.limit) {
                break;
            }
        }
    }
    BaseMap.showSlider(points);
}


BaseMap.getSlider = function(bounds) {
    var bbox = bounds.toUrlValue();
    $.ajax({
        dataType: "json",
        url: '/api/v1/poi/?bbox=' + bbox,
        success: function(response) {
            BaseMap.showSlider(response.objects);
        }
    });
}


function hideTitles() {
    $(".image_effect").each(function() {
        this._title = this.title;
        this.onmouseover = function() { 
            this.title = '';
        }
        this.onmouseout = function() { 
            this.title = this._title;
        }
        this.onclick = function() { 
            this.title = this._title;
        }
    });
}

function repairTitles() {
    $(".image_effect").each(function() {
        this.title = this._title;
    });
}

// < - &lt;
// > - &gt;
// ' - &#x27;

BaseMap.showSlider = function(points) {
    BaseMap.pointSlider.empty();
    for (var i=0; i<points.length; i++) {
        var point = points[i];
        BaseMap.pointSlider.append('<div><p><span class="frame alignleft">' +
        '<a id="slider_tooltip" class="image_effect zoom" href="'
        + point.photo.display_url +
        '" rel="prettyPhoto[gallery]" title="' +
        '&lt;a href=&#x27;/profile/' + point.user.username.toLowerCase() + '/&#x27; &gt;' +
        '&lt;img class=&#x27;img-circle avatar left&#x27; src=&#x27;' + point.user.avatar_url + '&#x27;&gt;' +
        '&lt;div class=&#x27;tooltip_slider&#x27;&gt;' +
        '&lt;a class=&#x27;photo_title&#x27 href=&#x27/' + point.slug + '/&#x27;&gt;' +
        point.name +
        '&lt;/a&gt;' +
        '&lt;br /&gt;' +
        '&lt;span class=&#x27;glyphicon glyphicon-user&#x27;&gt;&lt;/span&gt; ' +
        '&lt;a href=&#x27;/profile/' + point.user.username.toLowerCase() + '/&#x27;&gt;' +
        point.user.username +
        '&lt;/a&gt;&lt;br /&gt;' +
        '&lt;p class=&#x27;photo_description&#x27;&gt;' + point.description + '&lt;/p&gt;' +
        '&lt;/div&gt;' +
        '"><img class="slider_thumbnails" src="'
        + point.photo.thumbnail_url + '" title="' + point.name +
        '"/></a></span></p></div>');
    }
    $.getScript('/static/js/hover.js');
    hideTitles();
    $("a[id^='slider_tooltip']").tooltip({ effect: 'slide'});
    repairTitles();
    refreshPrettyPhoto();
    $(".scrollable").scrollable();
}


BaseMap.placeMarker = function (location) {
    var marker = new google.maps.Marker({
        position: location, 
        map: BaseMap.map
    });
    BaseMap.map.setOptions({draggableCursor: null});
    google.maps.event.clearListeners(BaseMap.map, 'click');
    window.location.href = "/poi/add/?lat=" + location.lat() + "&lon=" + location.lng();
}


BaseMap.showMarkers = function(points) {
    BaseMap.points = points;

    BaseMap.markers = [];
    BaseMap.userPoints = [];
    for (var i=0; i<points.length; i++) {
        var point = points[i];

        if(!BaseMap.userPoints[point.user.username]) {
            BaseMap.userPoints[point.user.username] = [];
        }
        BaseMap.userPoints[point.user.username].push([point]);

        var titleText = point.name;
            if (titleText == '') {
              titleText = 'No title';
            }

            var item = document.createElement('DIV');
            var title = document.createElement('A');
            title.href = '#';
            title.className = 'title';
            title.innerHTML = titleText;

        var latLng = new google.maps.LatLng(point.latitude,
            point.longitude);
        var imageUrl = 'http://chart.apis.google.com/chart?cht=mm&chs=24x32&chco=' +
            'FFFFFF,008CFF,000000&ext=.png';
        var markerImage = new google.maps.MarkerImage(imageUrl,
            new google.maps.Size(24, 32));
        var marker = new google.maps.Marker({
            position: latLng,
            icon: markerImage
        });
        var fn = BaseMap.markerClickFunction(point, latLng);
        google.maps.event.addListener(marker, 'click', fn);
        google.maps.event.addDomListener(title, 'click', fn);
        BaseMap.markers.push(marker);


    }
    var markerCluster = new MarkerClusterer(BaseMap.map, BaseMap.markers);
}

BaseMap.markerClickFunction = function(point, latlng) {
  return function(e) {
    e.cancelBubble = true;
    e.returnValue = false;
    if (e.stopPropagation) {
      e.stopPropagation();
      e.preventDefault();
    }
    var title = point.name;
    var url = point.photo.image;
    var fileurl = point.photo.preview_url;

    var infoHtml = '<div class="info gallery"><h3>' +
        '<a href="/' + point.slug + '/">' + title + '</a>' +
        '</h3><div class="info-body">' +
        '<p><span class="frame alignleft">' +
        '<a class="image_effect zoom" href="' + url + '" rel="prettyPhoto" title="' +
        '&lt;a href=&#x27;/profile/' + point.user.username.toLowerCase() + '/&#x27; &gt;' +
        '&lt;img class=&#x27;img-circle avatar left&#x27; src=&#x27;' + point.user.avatar_url + '&#x27;&gt;' +
        '&lt;a class=&#x27;photo_title&#x27 href=&#x27/' + point.slug + '/&#x27;&gt;' +
        point.name +
        '&lt;/a&gt;' +
        '&lt;br /&gt;' +
        '&lt;span class=&#x27;glyphicon glyphicon-user&#x27;&gt;&lt;/span&gt; ' +
        '&lt;a href=&#x27;/profile/' + point.user.username.toLowerCase() + '/&#x27;&gt;' +
        point.user.username +
        '&lt;/a&gt;&lt;br /&gt;' +
        '&lt;p class=&#x27;photo_description&#x27;&gt;' + point.description + '&lt;/p&gt;' +
        '"><img src="'
        + fileurl +
        '" alt="'
        + title +
        '" class="info-img"/></a></span></p></div>' +
        '<span class="glyphicon glyphicon-user"/></span> <a href="/profile/'
         + point.user.username.toLowerCase() + '/" >' + point.user.username +
        '</a></div></div>';

    BaseMap.infoWindow.setContent(infoHtml);
    BaseMap.infoWindow.setPosition(latlng);
    BaseMap.infoWindow.open(BaseMap.map);
    hideTitles();
    $.getScript('/static/js/hover.js');
    refreshPrettyPhoto();
  };
};