<pre class="text-center">
<span class="text-primary">{{uname}}</span>
<span class="text-success">{{uptime}}</span>
</pre>
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
<pre class="clearfix" id="vlc-log">{{log}}</pre>

%rebase musicbox **locals()
