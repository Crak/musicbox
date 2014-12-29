<div class="btn-group btn-lg pull-right clear-fix">
    <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
        <span class="glyphicon glyphicon-cog"></span>
    </button>
    <ul class="dropdown-menu" role="menu">
    <li><a id="logs-button">Full Logs
        <span class="glyphicon glyphicon-list-alt pull-right"></span>
    </a></li>
    <li><a id="restart-vlc-button">Restart VLC
        <span class="glyphicon glyphicon-refresh pull-right"></span>
    </a></li>
    <li><a id="restart-vnc-button">Restart VNC
        <span class="glyphicon glyphicon-refresh pull-right"></span>
    </a></li>
    <li class="divider"></li>
    <li><a id="quit-button">Quit Server
    <span class="glyphicon glyphicon-off pull-right"></span>
    </a></li>
    </ul>
</div>
<pre class="text-center">
<span class="text-primary">{{uname}}</span>
<span class="text-success">{{uptime}}</span>
</pre>
<!-- Nav tabs -->
<div class="panel panel-primary">
    <ul class="nav nav-pills nav-justified" role="tablist">
        <li role="presentation" class="active">
            <a href="#vlc" role="tab" data-toggle="tab">VLC</a>
        </li>
        <li role="presentation">
            <a href="#vnc" role="tab" data-toggle="tab">VNC</a>
        </li>
    </ul>
</div>
<!-- Tab panes -->
<div class="tab-content">
    <div role="tabpanel" class="tab-pane active" id="vlc">
        <pre id="vlc-log">{{logs[0]}}</pre>
    </div>
    <div role="tabpanel" class="tab-pane" id="vnc">
        <pre id="vnc-log">{{logs[1]}}</pre>
    </div>
</div>

%rebase musicbox **locals()
