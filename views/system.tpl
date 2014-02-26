<pre class="text-center">
<span class="text-primary">{{uname}}</span>
<span class="text-success">{{uptime}}</span>
</pre>
<ul class="nav nav-tabs">
    <li class="active">
        <a href="#0" data-toggle="pill">
            <img src="media/vlc.png">
            <span>{{navs[0]['name']}}</span>
        </a>
    </li>
    <li>
        <a href="#1" data-toggle="pill">
            <img src="media/vnc.png">
            <span>{{navs[1]['name']}}</span>
        </a>
    </li>
</ul>
<div class="tab-content">
    <div class="tab-pane active" id="0">
        <div class="btn-group btn-lg pull-right">
            <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
                <span class="glyphicon glyphicon-cog"></span>
            </button>
            <ul class="dropdown-menu" role="menu">
            <li><a id="reload-vlc-button">Reload Log
                <span class="glyphicon glyphicon-refresh pull-right"></span>
            </a></li>
            <li class="divider"></li>
            <li><a id="restart-vlc-button">Restart VLC
            <span class="glyphicon glyphicon-retweet pull-right"></span>
            </a></li>
            </ul>
        </div>
        <pre class="clearfix" id="vlc-log">{{logs[0]}}</pre>
    </div><!-- .tab-pane -->
    <div class="tab-pane" id="1">
        <div class="btn-group btn-lg pull-right">
            <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
                <span class="glyphicon glyphicon-cog"></span>
            </button>
            <ul class="dropdown-menu" role="menu">
            <li><a id="reload-vnc-button">Reload Log
                <span class="glyphicon glyphicon-refresh pull-right"></span>
            </a></li>
            <li class="divider"></li>
            <li><a id="restart-vnc-button">Restart VNC
            <span class="glyphicon glyphicon-retweet pull-right"></span>
            </a></li>
            </ul>
        </div>
        <pre class="clearfix" id="vnc-log">{{logs[1]}}</pre>
    </div><!-- .tab-pane -->
</div>

%rebase musicbox **locals()
