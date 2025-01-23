# About the Application

This flask app uses multiple tools to serve as a voice chatbot. Vosk is used to convert audio to text. this text is then fed to Llama using python library nexusraven. The output of this intent classfication is used to interact with a dummy database to let user see their bank details or transfer funds.

# How to run

download and unzip model inside source/model 

link : https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip

$pip install -r requirements

(There might be other requirements, please install accordingly)

After installing dependencies, inside /source run :

$python app.js

Example username and account number you can use to test = 

account no. 123 \\
username : Shashwat


account no. 69 \\
username : Amruta

Please note that llama instance we are using is running in a workstation at college using llama2:13b model.

The front end is run by jquery.

The back-end is flask.

Audio transcription is done with vosk.

Text intent classificaiton is done by llama2.



