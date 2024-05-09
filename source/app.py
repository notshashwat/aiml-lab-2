import vosk
import wave
import os
import uuid
import librosa
import soundfile as sf
from flask import Flask, flash, request, redirect
import random
import string
import ollama
import re
client = ollama.Client(host="http://10.10.2.148:11434")



def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def classify_intent(q):
    
    response = client.chat(model='nexusraven', messages=[{
        'role':'user',
        'content':
        """
        Function:
            def GET_BALANCE():
                Fetches balance data from database about the current user. 
                Args : 
                    None
                Returns : 
                    The balance, name and account number of the current user.
        
        Function:
            def TRANSFER( target_account, amount):
                Transfer the funds of amount from the current user to user belong to acc_no2
                Arguments : 
                    Person : the person you want to trasnfer the money to.
                Returns : 
                    Success or failure in transaction.

        Function: 
            def Other():    
                This function is called when chit chat done by the user.
                Arguments : 
                    None
                Returns :
                    Information about the app and pleasentaries

                
        
        Return only the function name that will be called followed by word Call:
        User query : \n
        """ + q
    }])
    
    print(response)
    
    ans = re.split(' |\(', response["message"]["content"].strip())[1]
    print(ans)

    # split("(")[0].split("Call: ")[0]
    
    return ans
    

dummy_db = {
        "123" : {"name":"Shashwat",
        "acc_no":123,
        "balance":19000},

        "69" :  {"name":"Amruta",
        "acc_no":69,
        "balance":-10}
    }
    


UPLOAD_FOLDER = 'files'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def root():
    return app.send_static_file('index.html')

    



def transcribe_audio(audio_file_path):
    """
    A module to transcribe from audio to text.
    Args:
        audio_file_path: path to .wav file
    Retuer:
        text: the recognized text from audio
    """

   

    model_path = "model/vosk-model-small-en-us-0.15"
    vosk.SetLogLevel(-1)  # Suppress Vosk log messages
    model = vosk.Model(model_path)
    recognizer = vosk.KaldiRecognizer(model, 16000)

    x,_ = librosa.load(audio_file_path, sr=16000)
    sf.write('tmp.wav', x, 16000)
    wf = wave.open('tmp.wav','rb')
    # wf = wave.open(audio_file_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        exit(1)

    # Process audio
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()

    result = recognizer.FinalResult()
    # format
    # { "text": "I am the recognized text" }
    result = eval(result)["text"]
    return result


@app.route('/get-details', methods=['POST'])
def get_details():
    request_data = request.get_json()
    acc_no = request_data["acc_no"]
    return dummy_db[acc_no]

@app.route('/get-users', methods=['POST'])
def get_users():
    request_data = request.get_json()
    #authorization steps
    auth = id_generator()
    return auth

@app.route('/transfer-money', methods=['POST'])
def transfer_money():
    request_data = request.get_json()
    acc_no1 = request_data["acc_no1"]
    acc_no2 = request_data["acc_no2"]
    amount = request_data["amount"]

    if(int(dummy_db[acc_no1]['balance'])< int(amount) ):
        return "Insufficient balance"
    if(acc_no2 not in dummy_db ):
        return "Account number does not exist!"
    
    dummy_db[acc_no1]['balance']-=int(amount)
    dummy_db[acc_no2]['balance']+=int(amount)
    
    
    return "Successful Transaction"


@app.route('/send-record', methods=['POST'])
def send_record():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    # file_name = str(uuid.uuid4()) + ".mp3"
    file_name = "audiofile.mp3"
    # full_file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    file.save(file_name)

    transcribed_text = transcribe_audio(file_name)
    print("text" ,transcribed_text)
    intent = classify_intent(transcribed_text)
    print("intent:", intent)
    return intent



    # return '<h1>Success</h1>'


if __name__ == '__main__':

    app.run()
    # print(transcribe_audio("audiofile.mp3"))
