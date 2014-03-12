var LOCAL_PLAYER = "VLC";

var initialized = false;
var player_state = null;
var player_time = 0;
var player_length = 0;

function watchdog(){
    if (playing()){update_player();};
    vlc_request();
}

function playing(){
    return player_state == "playing";
}

function format_time(s) {
    s = (typeof s === "undefined") ? 0 : s;
    var h = Math.floor(s/3600);
    s -= h*3600;
    var m = Math.floor(s/60);
    s -= m*60;
    return (h < 10 ? "0"+h : h)+":"+(m < 10 ? "0"+m : m)+":"+(s < 10 ? "0"+s : s); 
}

function format_progress(pos){
    return "width: " + (pos*100).toFixed(2) + "%";
}

function format_title(meta){
    if (meta.now_playing){return meta.now_playing;}
    else {return (typeof meta.title === "undefined") ? meta.filename : meta.title;};
}

function select_media(event){
    if (($(this).hasClass("active")) && ($(this).attr("data-type") == "dir")){
        vlc_request({data: {request: "browse", uri: $(this).attr("id")}});
    }
    else {
        $("#media-container > a").removeClass("active");
        $(this).addClass("active");
    };
}

function add_media(event){
    if ($("#local-media").hasClass("active")){
        var media = $("#media-container > a.active");
        if (media.length){
            event.data.request = "status";
            event.data.option = media[0].id;
            vlc_request(event);
            $("#media_browser").modal("hide")
            update_playlist(event);
        }
    }
    else if ($("#remote-media").hasClass("active")){
        var media_url = $("#media-url").val();
        if (media_url){
            event.data.request = "status";
            event.data.option = media_url;
            vlc_request(event);
            $("#media_browser").modal("hide")
            update_playlist(event);
        }
    };
}

function update_player(data){
    if (data){
        var div = $("#title");
        if (data.information){
            if (div.is(":parent")){
                var title = div.children().first();
                if (title.text() != format_title(data.information.category.meta)){
                    title.text(format_title(data.information.category.meta));
                };
            }
            else{
                var title = $("<label>");
                title.text(format_title(data.information.category.meta));
                div.append(title);
            };
        }
        else{div.empty();};

        player_state = data.state;
        player_time = data.time;
        player_length = data.length;
        
        update_toggle();

        $("#elapsed-time").text(format_time(player_time));
        $("#total-time").text(format_time(player_length));
        $("#seek-progress").attr("style", format_progress(data.position));    
        
        if ($("#playlist").hasClass("in")){vlc_request({data: {request: "playlist"}});};
        
    }
    else if (player_time < player_length){
        player_time += 1;
        $("#elapsed-time").text(format_time(player_time));
    };            
}

function update_toggle(){
    var span = $("#toggle-button").children().first();
    if (playing()){
        span.removeClass("glyphicon-play");
        span.addClass("glyphicon-pause");
    }
    else {
        span.removeClass("glyphicon-pause");
        span.addClass("glyphicon-play");
    };
}

function update_playlist(){
    $("#playlist-items").text("...");
    vlc_request({data: {request: "playlist"}});
}

function empty_playlist(event){
    vlc_request(event);
    update_playlist();
}

function toggle_playlist(event){
    if (event.type == "show"){$("#playlist-button").addClass("active");}
    else {$("#playlist-button").removeClass("active");};
}

function click_playlist(event){
    if (!$(this).hasClass("active")){vlc_request(event);};
}

function load_player(data){    
    $("#open-button").on("click", {request: "browse"}, vlc_request);
    $("#play-button").on("click", {action: "add_play"}, add_media);
    $("#enqueue-button").on("click", {action: "add_enqueue"}, add_media);

    $("#toggle-button").on("click", {request: "status", action: "toggle_pause"}, vlc_request);
    
    $("#elapsed-time").text(format_time(data.time));
    $("#total-time").text(format_time(data.length));

    if (data.random){$("#random-button").addClass("active");};
    if (data.loop){$("#loop-button").addClass("active");};
    
    $("#random-button").on("click", {request: "status", action: "random"}, vlc_request);
    $("#loop-button").on("click", {request: "status", action: "loop"}, vlc_request);
    $("#empty-button").on("click", {request: "status", action: "empty"}, empty_playlist);
    
    $("#seek-progress").attr("style", format_progress(data.position));

    $("#seek-backward-button").on("click", {request: "status", action: "seek", option: "-1%"}, vlc_request);
    $("#prev-button").on("click", {request: "status", action: "previous"}, vlc_request);
    $("#stop-button").on("click", {request: "status", action: "stop"}, vlc_request);
    $("#seek-forward-button").on("click", {request: "status", action: "seek", option: "+1%"}, vlc_request);
    $("#next-button").on("click", {request: "status", action: "next"}, vlc_request);
    
    
    $("#playlist").on("show.bs.collapse", toggle_playlist);
    $("#playlist").on("hide.bs.collapse", toggle_playlist);
    
    update_playlist();

    if (data.version){$("#version").append(LOCAL_PLAYER + " " + data.version);};
}

function load_playlist(data){
    var div = $("#playlist").children().first();
    div.empty();
    var items = data.children[0].children;
   $.each(items, function(index, item){
        var a = $("<a>", {"class": "list-group-item clearfix"});
        if (item.current){a.addClass("active");};
        var name = $("<label>");
        name.text(item.name);
        a.append(name);

       if (item.duration != -1){
            var duration = $("<label>", {"class": "pull-right"});
            duration.text(format_time(item.duration));
            a.append(duration);
        }
        a.on("click", {request: "status", action: "play", option: item.id}, click_playlist);
        div.append(a);
    });
    $("#playlist-items").text(items.length);
}

function load_browser(data){    
    $("#browser-title").text(data.element[0].path.replace("..", ""));
    var div = $("#media-container");
    div.empty();
    $.each(data.element, function(index, item){
        var a = $("<a>", {"class": "list-group-item", "id": item.uri, "data-type": item.type});
        var span = $("<span>", {"class": "glyphicon"});
        if (item.type == "dir"){
            if (item.name == ".."){span.addClass("glyphicon-folder-open");}
            else {span.addClass("glyphicon-folder-close");};
        }
        else {span.addClass("glyphicon-music");};
        a.append(span);
        a.append("\n");
        a.append(item.name);
        a.on("click", select_media);
        div.append(a);
    });
}

function vlc_request(event){
    event = (typeof event === "undefined") ? {data: {request: "status"}} : event;
    
    var jqxhr = $.ajax({url: "player", method: "POST", data: event.data});
    
    jqxhr.always(function(data, textStatus, jqXHR){
        if (!initialized){
            initialized = true; 
            load_player(data);
            setInterval(watchdog, 1000);
        };
    });
        
    jqxhr.done(function(data, textStatus, jqXHR){
        if (data.state){update_player(data);}
        else if (data.element){load_browser(data);}
        else{load_playlist(data);};
    });
    
    jqxhr.fail(function(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        show_alert(LOCAL_PLAYER, errorThrown); 
    });
}

$(document).ready(vlc_request());
