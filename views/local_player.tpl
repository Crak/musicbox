<div class="panel panel-primary">
	<div class="panel-heading">
		<div class="text-center" id="title"></div>
		<button type="button" class="btn btn-primary " data-toggle="modal" href="#media_browser" id="open-button">
			<span class="glyphicon glyphicon-eject"></span>
		</button>
		<button type="button" class="btn btn-primary" id="toggle-button">
            <span class="glyphicon glyphicon-play"></span>
		</button>
		<label class="song-timer" id="elapsed-time"></label>
		<div class="pull-right clearfix">
			<label class="song-timer" id="total-time"></label>
			<div class="btn-group">
				<button type="button" class="btn btn-primary" data-toggle="button" id="random-button">
					<span class="glyphicon glyphicon-random"></span>
				</button>
				<button type="button" class="btn btn-primary" data-toggle="button" id="loop-button">
					<span class="glyphicon glyphicon-repeat"></span>
				</button>
			</div>
			<button type="button" class="btn btn-primary" id="empty-button">
				<span class="glyphicon glyphicon-trash"></span>
			</button>
		</div>
        <hr>
        <div class="well">
            <div class="progress progress-striped btn-block">
                <div class="progress-bar progress-bar-primary" style="width: 0%" id="seek-progress"></div>
            </div>
            <div class="btn-group btn-group-justified">
                <a class="btn btn-primary" id="prev-button">
                <span class="glyphicon glyphicon-fast-backward"></span>
                </a>
                <a class="btn btn-primary" id="stop-button">
                 <span class="glyphicon glyphicon-stop"></span>
                </a>
                <a class="btn btn-primary" id="next-button">
                 <span class="glyphicon glyphicon-fast-forward"></span>
                </a>
            </div>
        </div>
        <ul class="nav nav-pills nav-justified">
            <li class="btn btn-primary btn-lg clearfix" data-toggle="collapse" href="#playlist" id="playlist-button">
                <span class="glyphicon glyphicon-th-list pull-left"></span>
                <span class="badge-inverse pull-right" id="playlist-items"></span>
            </li>
        </ul>
	</div><!-- .panel-heading -->
    <div class="panel-body panel-collapse collapse" id="playlist">
        <div class="list-group"></div>
        <div class="text-primary text-center" data-toggle="collapse" href="#playlist">
            <span class="glyphicon glyphicon-chevron-up"></span>
        </div>
    </div><!-- .panel-body -->
	<div class="panel-footer text-primary text-center" id="version"></div>
</div>

<div class="modal fade" id="media_browser">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <label class="text-info modal-title" id="browser-title"></label>
                <button type="button" class="close" data-dismiss="modal">&times;</button>
            </div>
            <div class="modal-body list-group" id="browser-container"></div>
            <div class="modal-footer">
                <a class="btn btn-primary" id="play-button">Play</a>
                <a class="btn btn-primary" id="enqueue-button">Enqueue</a>
                <a class="btn btn-default" data-dismiss="modal">Cancel</a>
            </div>
        </div>
    </div>
</div><!-- /.modal -->

%rebase musicbox **locals()
