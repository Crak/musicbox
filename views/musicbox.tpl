<!DOCTYPE html>
<html lang="en">
    <head>
        <title>{{title}}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="media/musicbox.png" rel="icon" type="image/png">
        <!-- Bootstrap -->
        <link href="bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">
        <!-- Custom styles -->
        <link href="css/musicbox.css" rel="stylesheet">
    </head>
    <body>
        <div class="navbar navbar-default navbar-fixed-top" role="navigation">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".nav-collapse">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="{{brand_url}}">{{brand}}</a>
            </div>
            <div class="collapse navbar-collapse nav-collapse">
              <ul class="nav navbar-nav">
            %for n in navs:
                % if n['active']:
            <li class="active">
                %else:
            <li>
                %end
                <a href="{{n['url']}}">{{n['name']}}</a></li>
            %end
              </ul>
                <div class="navbar-right">
                    <button type="button" class="btn btn-default navbar-btn" id="volume-mute-button">
                    %if defined('mute'):
                        <span class="glyphicon glyphicon-volume-off"></span>
                    %else:
                        <span class="glyphicon glyphicon-volume-up"></span>
                    %end
                    </button>
                    <div class="btn-group" id="volume-control">
                        <button type="button" class="btn btn-default navbar-btn"  id="volume-down-button">
                            <span class="glyphicon glyphicon-minus"></span>
                        </button>
                        <button type="button" class="btn btn-default navbar-btn disabled">
                            <div class="progress" id="volume-container">
                                <div class="progress-bar progress-bar-primary" style="width: {{volume}}%"id="volume-progress"></div>
                            </div>
                        </button>
                        <button type="button" class="btn btn-default navbar-btn"  id="volume-up-button">
                            <span class="glyphicon glyphicon-plus"></span>
                        </button>
                    </div>
                    <button type="button" class="btn btn-default navbar-btn" id="standby-button">
                        <span class="glyphicon glyphicon-flash"></span>
                    </button>
                </div>
            </div>
        </div><!-- .nav-bar -->
	<div id="navbar-spacer"><br></div>
	
        <div id="alert-container">
        </div>

        <div class="container" id="content">
        {{!base}}
        </div>
        
        <!-- jQuery -->
        <script src="js/jquery.js"></script>
        <!-- Include bootstrap plugins -->
        <script src="bootstrap/js/bootstrap.min.js"></script>
        <!-- Custom js -->
        <script src="js/musicbox.js"></script>
        <script src="js/{{script}}"></script>
    </body>
</html>