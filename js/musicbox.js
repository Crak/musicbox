function show_alert(origin, message){
    message = (typeof message === "undefined") ? "Unknown Error" : message;
    
    var div = $("<div>", {"class": "alert alert-block alert-danger fade in", "id": "active-alert"});
    var button = $("<button>", {"class": "close", "type": "button", "data-dismiss": "alert"});    
    button.append("&times;");
    div.append(button);
    
    div.append("<strong>" + origin + ": </strong>" + message);

    var container = $("#alert-container");
    container.empty();
    container.append(div);
    
    var spacer = $("#navbar-spacer");
    spacer.hide();
    $("#active-alert").on("closed.bs.alert", function(){spacer.show();});
}

function load_standby(event){
    show_alert("MUSICBOX", "The system is going to sleep!");
    $.ajax({url: "/", method: "POST", data: {request: "standby"}});
}

function update_volume(data){
    var span = $("#volume-mute-button").children().first();
    if (data.mute){
        span.removeClass("glyphicon-volume-up");
        span.addClass("glyphicon-volume-off");
    }
    else {
        span.removeClass("glyphicon-volume-off");
        span.addClass("glyphicon-volume-up");
    };
    $("#volume-progress").attr("style", "width: " + data.volume + "%");    
}

function load_sound(){
    $("#volume-mute-button").on("click", {request: "sound", action: "mute"}, sound_request);
    $("#volume-down-button").on("click", {request: "sound", action: "volume_down"}, sound_request);
    $("#volume-up-button").on("click", {request: "sound", action: "volume_up"}, sound_request);
    
    $("#standby-button").on("click", load_standby);
}

function sound_request(event){
    var jqxhr = $.ajax({url: "/", method: "POST", data: event.data});
    
    jqxhr.done(function(data, textStatus, jqXHR){
        //console.log(data);
        update_volume(data);
    });
    
    jqxhr.fail(function(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        show_alert("SOUND", errorThrown); 
    });
}

$(document).ready(load_sound());
