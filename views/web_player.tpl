<canvas id="myCanvas" width="800" height="600"></canvas>
    <script>
        var canvas = document.getElementById('myCanvas');
        var context = canvas.getContext('2d');

      var imageObj = new Image();

      imageObj.onload = function() {
        context.drawImage(imageObj, 0, 0);
      };
      imageObj.src = 'media/musicbox.png';
    </script>
%rebase musicbox **locals()