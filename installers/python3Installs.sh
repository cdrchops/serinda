pip3 install flask
pip3 install flask_cors

# rust install for use with snips
# windows may require a different installer
# https://www.rust-lang.org/tools/install
# add %USERPROFILE%\.cargo\bin to windows environment variables
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

pip3 install setuptools_rust

pip3 install snips_nlu

#install en language pack
python3 -m snips_nlu download en
pip3 install SpeechRecognition
pip3 install textblob
pip3 install googletrans
pip3 install imutils
pip3 install opencv-python

#sudo apt-get install libzbar0
pip3 install pyzbar
pip3 install jpype1
#sudo apt-get install default-jdk
#sudo apt-get install curl

#https://nlu.johnsnowlabs.com/
#pip3 install nlu
#pip3 install pyspark==2.4.7


pip3 install pandas
pip3 install seaborn
#xls
pip3 install xlrd
pip3 install pyyaml h5py

#if command line tools for xcode are not installed
#xcode-select --install

# for windows
# https://stackoverflow.com/questions/52283840/i-cant-install-pyaudio-on-windows-how-to-solve-error-microsoft-visual-c-14
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# download the wheel matching your Python version
# then pip3 install <whl name>

# for linux
# sudo apt-get install portaudio19-dev
# python-pyaudio python3-pyaudio
# pip3 install pyaudio
#pip3 install PyAudio # fix for debian

pip3 install pyttsx3

# for working with java style properties files
# https://github.com/mgood/jprops/blob/master/README.rst
pip3 install jprops

pip3 install wolframclient

# http://cmake.org install or apt-get or brew
pip3 install dlib

# for autoscraping sites
pip3 install autoscraper

#sudo apt install python3-dev python3-pip python3-venv
#sudo apt-get install software-properties-common

# tensorflow 2 currently only supports up to python3.8 so you may need to downgrade your python3
# https://stackoverflow.com/questions/43743509/how-to-make-python3-command-run-python-3-6-instead-of-3-5
#which python3
#sudo apt-get install python3.8
# sudo ln -sfn /usr/bin/python3.8 python3
pip3 install tensorflow

# for tensorflow datasets
pip3 install tensorflow_datasets

# for tensorflow probabilities
pip3 install tensorflow_probability

pip3 install numpy
pip3 install opencv-contrib-python # ==4.1.0.25  >= 4.1.0.25
pip3 install sklearn
pip3 install imutils

sudo apt-get install -y build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
git clone https://github.com/opencv/opencv.git
cd ..
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_GSTREAMER=ON -D WITH_FFMPEG=ON ../opencv
make -j8
sudo make install

#pip3 install --user flask-cors
#pip3 install --user pyzbar

# use snips or rhasspy for NLU
# rhasspy uses JSGF where snips has it's own
# also available for NLU is alter NLU engine which has it's own server - I have chosen not to use it because of the additional server running
pip3 install rhasspy-nlu

# for the 9DOF sensors
pip3 install adafruit-circuitpython-fxos8700
pip3 install adafruit-circuitpython-fxas21002c

# so we can use python and directly connect to the 9DOF sensor via windows 10
# https://github.com/tino/pyFirmata
pip3 install pyfirmata