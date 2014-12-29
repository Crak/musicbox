function update_log(data){
    if (data.vlc_log){
        var pre = $("#vlc-log");
        pre.empty();
        pre.text(data.vlc_log);
    }
    if (data.vnc_log){
        var pre = $("#vnc-log");
        pre.empty();
        pre.text(data.vnc_log);
    }
}

function load_system(){
    $("#logs-button").on("click", {request: "logs", action: "full"}, system_request);
    $("#restart-vlc-button").on("click", {request: "vlc", action: "restart"}, system_request);
    $("#restart-vnc-button").on("click", {request: "vnc", action: "restart"}, system_request);
    $("#quit-button").on("click", {request: "system", action: "quit"}, system_request);
}

function system_request(event){
    var jqxhr = $.ajax({url: "/system", method: "POST", data: event.data});
    
    jqxhr.done(function(data, textStatus, jqXHR){
        //console.log(data);
        update_log(data);
    });
    
    jqxhr.fail(function(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        show_alert("SYSTEM", errorThrown); 
    });
}

$(document).ready(load_system());