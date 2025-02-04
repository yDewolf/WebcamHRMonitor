<h1>Webcam Heart Rate Monitor</h1>
<p>This is a really simple Webcam based heart rate monitor, that uses gaussians and color magnification to calculate the heart rate</p>
<h2>Disclaimer: This is very unaccurate and most of the code for calculations aren't mine!</h2>
<p>If you want to learn more about this method of monitoring heart rate, you can go to: <a href="https://github.com/giladoved/webcam-heart-rate-monitor/tree/master">Giladoved's Repository</a> where most of the calculations code is taken from.</h3>
<p>Also you should read about the method in the original <a href="https://people.csail.mit.edu/mrub/evm/">paper</a> from MIT Computer Science & Artificial Intelligence Lab</p>
<h1>How to use it</h1>
<p>This program is meant to be used in OBS Studio, but you can pretty much use it anywhere.</p>
<ol>
  <li>
    Download the zip file from the releases tab
  </li>
  <li>
    Extract the folder and run start_http.bat or run the main.exe file, running the start_http.bat will open a tab on your browser with the HR monitor
  </li>
  <li>
    On OBS, add a new <b>browser</b> element. Set its URL to: http://127.0.0.1:8000 (or localhost:8000), set the width to 300 and the height to 100
  </li>
</ol>
<p>With that you should be good to go!</p>
<p>
  By default <b>CameraIndex</b> is set to <b>2</b> (Usually OBS Virtual Camera), but you can change it in the <b>config.ini</b> file by changing the <b>CameraIndex</b> field.<br>
  By setting it to 0 it should use the default camera of your computer
</p>
