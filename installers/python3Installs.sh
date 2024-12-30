python3 -m pip install -r ./requirements.txt
python3 -m snips_nlu download en
python3 -m textblob.download_corpora


#python -m pip install numpy==1.21.1
#python -m pip install tensorboard==2.14.0

# sudo apt-get install python3-venv
# python3 -m pip install --user virtualenv

# python3 -m venv serinda

# source ./serinda/bin/activate
pip install setuptools-rust

pip3 install flask
pip3 install flask_cors

pip3 install setuptools_rust

pip3 install SpeechRecognition
pip3 install textblob
pip3 install googletrans
pip3 install imutils
pip3 install opencv-python

#
pip3 install pyzbar
pip3 install jpype1

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


pip3 install pyttsx3

# for working with java style properties files
# https://github.com/mgood/jprops/blob/master/README.rst
pip3 install jprops


# http://cmake.org install or apt-get or brew
pip3 install dlib

# for autoscraping sites
pip3 install autoscraper

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



#NLU - rhasspy is preferred over snips
pip3 install snips_nlu

#install en language pack
python3 -m snips_nlu download en

# rhasspy uses JSGF where snips has it's own
# also available for NLU is alter NLU engine which has it's own server - I have chosen not to use it because of the additional server running
pip3 install rhasspy-nlu

# for the 9DOF sensors
pip3 install adafruit-circuitpython-fxos8700
pip3 install adafruit-circuitpython-fxas21002c

# so we can use python and directly connect to the 9DOF sensor via windows 10
# https://github.com/tino/pyFirmata
pip3 install pyfirmata

pip3 install setuptools-rust
pip3 install scikit-learn
pip3 install cython

#install en language pack
#pip3 install textblob
#pip3 install snips_nlu
python3 -m snips_nlu download en
python3 -m textblob.download_corpora

pip3 install flask
pip3 install nlu
pip3 install numpy~=1.19.4
#pywinauto~=0.6.8
pip3 install matplotlib~=3.3.3
pip3 install pyttsx3~=2.90
pip3 install autoscraper~=1.1.10
pip3 install Jinja2~=2.11.2
pip3 install jprops~=2.0.2
pip3 install imutils~=0.5.3
pip3 install dlib~=19.21.1
pip3 install pyzbar~=0.1.8
pip3 install textblob~=0.15.3
pip3 install googletrans~=3.0.0
pip3 install wheel
pip3 install twine
pip3 install setuptools
pip3 install zbar-py
pip3 install markupsafe==2.0.1
pip3 install PyAutoGUI~=0.9.50
pip3 install websockets
pip3 install rhasspy-nlu

