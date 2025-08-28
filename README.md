<h1>The current working branch is Graceland.  The main branch will be tagged and Graceland will be merged when it's ready for the main branch.</h1>


<h2>TODO:</h2>

- [ ] Connect USB Camera 1 \
https://support.myownconference.com/en/article/setting-up-and-using-an-external-usb-camera-z5o80x/
- [ ] Connect USB Camera 2 \

- [ ] Use WebRTC to pull up Camera 1

- [ ] Set up camera on headset

- [ ] Connect camera and headset to laptop via longer port

- [ ] Test hand gestures with new camera set up

- [ ] Maybe find a new gesture library as the one I'm using with WebRTC isn't working as well.

- [ ] A gesture library hosted locally

<h4>Research Links</h4>
https://webrtc.org/ \
https://github.com/AlexxIT/WebRTC \
https://www.reddit.com/r/raspberry_pi/comments/1ffkyj3/i_built_a_lowlatency_webrtc_live_camera_on_a_pi/ \
https://www.google.com/search?q=deepseek+offline&rlz=1C1UEAD_enUS1165US1166&oq=deepseek+offline&gs_lcrp=EgZjaHJvbWUqBwgAEAAYgAQyBwgAEAAYgAQyBwgBEAAYgAQyBwgCEAAYgAQyBwgDEAAYgAQyBwgEEAAYgAQyBwgFEAAYgAQyBwgGEAAYgAQyBwgHEAAYgAQyBwgIEAAYgAQyBwgJEAAYgATSAQg0NTQ4ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8 \
https://stackoverflow.com/questions/24514936/how-can-i-serve-npm-packages-using-flask \
https://pypi.org/project/Flask-Fanstatic/ \
https://www.fanstatic.org/en/latest/intro.html \
https://www.google.com/search?q=deepseek+offline&rlz=1C1UEAD_enUS1165US1166&oq=deepseek+offline&gs_lcrp=EgZjaHJvbWUqBwgAEAAYgAQyBwgAEAAYgAQyBwgBEAAYgAQyBwgCEAAYgAQyBwgDEAAYgAQyBwgEEAAYgAQyBwgFEAAYgAQyBwgGEAAYgAQyBwgHEAAYgAQyBwgIEAAYgAQyBwgJEAAYgATSAQg0NTQ4ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8 \
https://cdn.jsdelivr.net/npm/@mediapipe/hands/

<h2>What is SERINDA?</h2>
Sophisticated Engaging Rider Interface Near-eye Digital Assistant or SERINDA.<br/><br/>
It's a Mixed Reality Intelligent Personal Assistant using Python3, Flask, HTML/CSS/JS, and OpenCV.  It was originally supposed to be for HMD on a motorcycle.  It is now, more of an HMD for daily life.

I have not tried this with Project North Star.  I have used this on Mad Gaze Glow and my own headset.

---
<h2>How To Startup SERINDA</h2>
I still have some work to do with the installers and requirements.txt - aka merging the two together.  There are libraries
that will be needed for Mac and Linux variants.  There are some notes in the installers/python3Installs.sh file.  You will
need to install OpenCV.

python3 startup.py

when running startup.py the server will start up in the terminal and open the url in an instance of chrome.  Then the page will keep attempting to connect until it can connect to the server

---
<h2>Integrations</h2>

Python 3.8 is an interpreted language.  That means it's not faster for some code.  Or maybe you have code already written
in Java, Groovy, Rust, or C that you would like to use.  Here are some options for you.

<b>Java</b> or <b>Groovy</b> - The Gradle build will compile both and put them in the build directory.  The <i>serinda.props</i> file
contains the location of the builds.  You can place groovy and java files into the src/main/groovy/ directory then run
<i>gradle compileJava compileGroovy</i> and they'll be built to the build directory.  In <i>main.py</i> at the bottom in
<i>main</i> is an example of how to use the compiled files and call them from Python.  You will need to install jpype1 
with <i>pip3 install jpype1</i> and then add <i>import jpype1</i> in the main file.
<br/><br/>
<b>Rust</b> - by default when the server starts up it compiles any Rust files in the <i>src/rust/src</i> directory into
a shared object (so) or DLL depending on your system.  The library is copied from the <i>target/release</i> directory to the 
<i>build</i> directory.  There is a test in <i>TESTS/rust</i> that demonstrates calling DLL functions from Python.
<br/><br/>
<b>C</b> - if you want to use C shared objects (so) or DLLs you may also compile C with the compileC shell script.  This
only works on non-windows machines.  I don't use C so I am not spending the time to get the compiler to work on Windows.
These work the same as Rust from Python.  There is an example in the <i>TESTS/cFuncs</i> directory.

---
<h2>How It Works</h2>
<b>Voice control</b> - There are intentions you create in the <i>intents/serindaCommands.ini</i> file.  They follow the 
JSGF format that CMU Sphinx does.  The basics of natural language understanding (NLU) is that you say something and then
those are mapped to intentions.  For example, "show grid on camera 1".  The intention is to show the grid then apply it 
to camera 1.  The intention is simply mapped as "showGrid".  The speech is processed and intention determined.  Then in
the plugins they check to see if the intention is mapped to them and if they are then the command is processed.  You can
see how this works in the <i>OpenCVPlugin.py</i>.
<br/><br/>
Currently, the commands come from the browser and are processed in Python.  Eventually, they will be processed on the 
backend and then sent to the server.
<br/><br/>
Simply say "Okay Bob Show Grid on Camera 1" and a green grid should appear.  There are a few other commands that are 
available.  Some you can test via the menu in the upper left corner of the webpage.  Not all of them work.  More plugins
are added often.
<br/><br/>
Plugins follow the structure in the serinda/plugin/TestPlugin directory.  They have to have a menu.html, template.html, 
javascript.js, commands.yml, and <name>Plugin.py file.  The menu.html is automatically added to the menu list.  The 
javascript.js is automatically added to the page.  The commands.yml is not currently used, but if you enable SNIPs then 
it will get combined into a large intent file that is used.  I'll be adding commands.ini file so each of the plugins will
have their own ini that is combined into a single ini.  For now, just use the intents/serindaCommands.ini file.  Plugins 
are not automatically accessible to use.  You'll need to open PluginManager.py and import the plugin python file then add
it to the plugin list.  After that everything is automatic for the page.  All commands go through processIntent and setCommand.
This process is constantly evolving.  However, it should make it quick work to add your own plugin to test or remove existing
plugins.
<br/><br/>
Since this is intended to be used as a Mixed Reality headset we do not need to display the actual camera image.  If you 
want to test a plugin and view the actual camera image with OpenCV go to the videocamera.py file and the return statement
of get_frame will have an <i>if True:</i> line.  I'll probably change this to a property for the files so it's easier to 
change.  However, simply change the True to False then restart the server.  The idea is that when you're looking through 
the viewscreen at the AR world and you want to detect a face you don't want to see what the camera sees you only want to 
see what OpenCV has detected.
<br/><br/>
This project does require a LeapMotion if you want to do any interaction with AR elements (to make it MR).  OpenCV gesture
work is ongoing.  This project uses the LeapJS, leap-widgets, and leapOrbitControls projects to interact with the ThreeJs
items.

---
<h2>Special Thanks</h2>
I started learning OpenCV about 5 years ago thanks to Adrian at PyImageSearch.  His tutorials are always easy to follow and the information is invaluable.

Here are just a few of the tutorials I followed to build this application:
https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/ 

---
<h2>Licensing</h2>
I have attempted to document where code comes from if I didn't write it from scratch.  To this extent the code has comments
that contain links to StackOverflow pages, github projects, and more.  That doesn't mean I copied wholesale.  It simply 
means I drew inspiration from somewhere.  It doesn't exclude copy and paste.  I'll be adding the specific licensing as I
document more of the system.

I chose the MIT license because I think if you want to use any of the code for any reason in your work, for any reason,
then you are free to do so.  I would like a snippet of recognition by name or by project.  But it's yours to do with as
you please and, as always, we're not responsible for anything you do with this code nor are held liable for anything this
code does.  use at your own risk.

Some libraries are licensed under LGPL2, LGPL3, MIT, BSD - I have attempted to list all of those here.

The Triton work is licensed under Creative Commons Attribution-NonCommercial-ShareAlike

Any code from PyImageSearch is licensed here - https://www.pyimagesearch.com/faqs/

All LeapMotion code is licensed by the repo (I'll be adding more info on those later) otherwise it's licensed under
https://www.ultraleap.com/vr-controller-mount-pricing-and-licensing/

---
### TODO List
 ln -s ~/.pyenv/versions/3.8.20/bin/python python3
- update installs so that numpy doesn't break
- set a setting so that you can say whether or not you have a raspberry pi - that way Rasspy can or can't be used

There are only a few "basic" items that need to be done in order for this to be fully functional as a base for adding 
plugins, optimizing code, etc.  Once these items are completed I'd consider SERINDA ready for prime testing.
<br/><br/>
1) OpenCV and WebGL to have the same camera perspective.  For now, I'm working on using OpenCV to adjust the camera 
perspective of WebGL so they match.  Then ThreeJS elements placed in a scene will have the same look as if they were real.
This also means that if an object 10 feet away has a HUD element then that will look like it's 10 feet away.
<br/><br/>
2) Simultaneous Location and Mapping (SLAM) and Visual Odometry (VO or VIO).<br/>
I have successfully integrated a 9DOF sensor with the HMD.  There are tweaks to make, but the data works pretty well for 
adjusting the camera view in ThreeJs.  I am working on integrating some version of SLAM (OpenVSLAM, ORB SLAM 2, ORB SLAM 3, idk).
I'll also use a flavor of homography for a few elements since this is primarily going to be used indoors.  I'd like to
have SLAM implemented and then remove the DOF sensor or use the DOF sensor to add more precision.<br/><br/>
3) Object Detection and Object Recognition<br/>
This is part of the HUD integration.  If I have an object that it detects and I want a specific HUD to overlay then I first 
need the object to be detected.  There are many datasets out there for this from YOLO, Tiny YOLO, and more.  There is 
more to this and will require some data be passed back to the front end for it to be used to display ThreeJs elements.
<br/><br/>
4) Interactive HUD elements<br/>
This isn't difficult.  I have some that are in my experimental box still.  Some of this will be solved when 1 and 3 are 
done then I'll add these experiments so users can interact with them.  Some are tied to real objects like a hand or wrist.
Some are tied to the display like a HUD in a game would be.  And others are tied to objects like in 3 above.  This also
means adding some sort of 3D GUI.
<br/><br/>
5) Dynamic loading of scenes and objects<br/>
This can be done independent of the other items.  The user needs to be able to 
CRUD 3D objects and then assign them to specific items and then those elements only display when those items are in view.
For example, if I have a chair and I want a price to display over it.  I need to identify that it's a chair and what type
of chair.  Then assign 3D elements to display in the HUD for that chair.  When that type of chair comes into view then
the HUD I've chosen will display.  When the chair is no longer visible after x amount of time, then that HUD object is 
removed from active memory.  In the future this could be used for items like walking into a furniture store and the store 
sends the data to your HMD then as you're walking around you can see prices, maybe virtual items that you can "try out" in
your own home, etc.  In the context of scenes, this could be like for a game.  You could create an AR game that's mapped
to your house.  When you go to certain areas maybe med packs are there or hidden compartments.
<br/><br/>
6) Audio<br/>
VOX controls work ok.  They're not great and if the browser is taxed then they don't work well at all.  Speech playback 
sometimes works; you never know when it will work.  In order to be able to continue with the IPA portion and make this
something fully functional the VOX portion (TTS and STT) need to work better.  Specifically this is referring to only
the TTS and STT portions not the Rhasspy nor SNIPs intents.

- install depthai
- figure out what packages I still need to install to update the python packages and still startup the server
- figure out why audio isn't working
- wink nlp? https://winkjs.org/wink-nlp/ instead of SNIPS?
- Why can't I use the latest libraries?  Is it because one package hasn't been updated?
- ffmpeg -i "http://10.255.255.254:8000/camera/mjpeg"-an output.mp4
- LLAMA3
	ollama run llama3.2-vision

	localhost:11434

	pip install unstructured[docx] langchain langchainhub langchain_community langchain-chroma

	curl -fsSL https://ollama.com/install.sh | sh
	https://ollama.com/download/linux
	https://ollama.com/download/OllamaSetup.exe

	curl http://localhost:11434/api/chat -d '{
	  "model": "llama3.2-vision",
	  "messages": [
		{ "role": "user", "content": "What are God Particles?" }
	  ],
	  "stream": false
	}'

	check=$(curl -s -w "%{http_code}\n" -L "${localhost}${11434}/" -o /dev/null)
	if [[ $check == 200 || $check == 403 ]]
	then
		# Service is online
		echo "Service is online"
		exit 0
	else
		# Service is offline or not working correctly
		echo "Service is offline or not working correctly"
		#exit 1
	fi

# TROUBLESHOOTING

## REGEX
To find pip versions and remove them from the requirements file 
[=>~]=[0-9]{1,4}\.[0-9]{1,2}(\.[0-9]{1,4})?(\.[a-zA-Z0-9]{1,10})?
 
## could not load library libcudnn_ops_infer.so.8 
pip install torch==2.3.1 torchaudio==2.3.1 torchvision==0.18.1 --index-url https://download.pytorch.org/whl/cu118
export LD_LIBRARY_PATH=`python3 -c 'import os; import nvidia.cublas.lib; import nvidia.cudnn.lib; import torch; print(os.path.dirname(nvidia.cublas.lib.__file__) + ":" + os.path.dirname(nvidia.cudnn.lib.__file__) + ":" + os.path.dirname(torch.__file__) +"/lib")'`

## OPENAPI KEY
https://platform.openai.com/api-keys

## PYTTSX3
https://stackoverflow.com/questions/29615235/pyttsx-no-module-named-engine
https://puneet166.medium.com/how-to-added-more-speakers-and-voices-in-pyttsx3-offline-text-to-speech-812c83d14c13

## SNIPS
https://snips-nlu.readthedocs.io/en/latest/installation.html
with latest python

snips
snips-nlu
snips-nlu-metrics
snips-nlu-parsers
snips-nlu-utils
snips_nlu_en
