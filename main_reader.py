import pytesseract 
import PIL
from PIL import Image
import pyautogui
import pyttsx3
from pyttsx3.drivers import sapi5
import pathlib
import wavio
import sounddevice as sd
import speech_recognition as sr
import pynput
from pynput.mouse import Controller, Button
import keyboard 
import wave
import sys
import os 
import time 

global b_ 
b_ = []

class reader:

    def crop_image(input_image, output_image, start_x, start_y, width, height):
        
        p = pathlib.Path(__file__).parent.absolute()
        z = str(p).split('/')
        z[0].replace("\\","//")
# here we crop the image so that we focus only in the text of the stories and we can ignore the rest 
# of the peripherical text( from the url for example ) 
        input_img = Image.open(input_image)
        box = (start_x, start_y, start_x + width, start_y + height)
        output_img = input_img.crop(box)
        output_img.save(z[0]+'\\'+output_image +".png")

        return z[0]+'\\'+output_image +".png"

    def capture(pic_name):
# here we get the current file directory to save the printed images
        p = pathlib.Path(__file__).parent.absolute()
        z = str(p).split('/')
# thats the directory to be used 
        z[0].replace("\\","//")
# then we format the file format
# we just capture the screen 
        myScreenshot = pyautogui.screenshot()
        directory = z[0]+"\{x}.png".format(x=pic_name)
        myScreenshot.save(directory)
# this format works well on my computer , there's a need for more tests 
# in order to see if this kind of crop will work 
        c = reader.crop_image(directory,'cropped_{z}'.format(z=pic_name),500,70,350,690)
        return c 
        

    def read(dir,lang='por'):
# here we get the tesseract excutable
# the main objective here is to find the tesseract itself instead of the need to pass the path for it 
# because of the acessbility i didnt figure out an way in which we can really make this configuration 
# one of the stuff i tought was that maybe we can make a file find that will crawl to the tesseract file and extract 
# the path of it but i still need to test this possibility  

# here we find the tesseract path # 
        try:
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
        except:
            exe = 'tesseract.exe'
            for root, dirs, files in os.walk(r"C:\Program Files (x86)"):
                for name in files:
                    if name == exe:
                        pth = os.path.abspath(os.path.join(root, name))
            z = str(pth).split('/')
            z[0].replace("\\","//")
            pytesseract.pytesseract.tesseract_cmd = z[0]        
# we open the image
        image = Image.open(dir)
# here we extract the text 
        phrase = pytesseract.image_to_string(image, lang=lang)
        return phrase 
    
    def normalize(text):
# here we normalize the text , and then we can make sense of the text
# usually if we only synthetize the text purely the voice is too slow 
# but if we remove the wait times and some useless punctuation then we can get something more valuable
        p_text = text.split("\n")
        norm_text = " ".join(p_text)
        return norm_text

    def synth_text(phrase):
# then we synth the phrase 
        engine = pyttsx3.init()
        engine.setProperty('rate', 355)
        engine.say(phrase)
        engine.runAndWait()

    def run(name):
        dir = reader.capture(name)
        f = reader.read(dir)
        n_t = reader.normalize(f)
        reader.synth_text(n_t)


class command:
# here we start to process the pics's text and transform it into sound
    def start():
        engine = pyttsx3.init()
        engine.setProperty('rate', 355)
        engine.say("processando um instante")
        engine.runAndWait()
# here then the mouse is stepped to the point where it pause the stories pic 
        mouse = Controller()
        mouse.position = (643, 273)
        mouse.press(Button.left)
        reader.run("test_it")
        b_.append(1)
        mouse.release(Button.left)
# here we establish an barrier to start the process step 
    def init():
        engine = pyttsx3.init()
        engine.setProperty('rate', 355)
        engine.say("Aperte control + y para ler a foto")
        engine.runAndWait()

if __name__ == '__main__':

    print('iniciando....')
    command.init()
    while True :
# we run the app 
        print('running...')
        if len(b_) != 0:
# after the read of the image the list get one value and then the system stops
           print("encerrando...")
           try:
               engine = pyttsx3.init()
               engine.setProperty('rate', 355)
               engine.say("Encerrando")
               engine.stop()
               sys.exit()
           except:
# for now there's the exception almost all time 
# then the mouse is unpressed and the system stops
               mouse = Controller()
               mouse.release(Button.left)
               sys.exit()
        else:
# after one click the system will read the picture 
# and then make it stops 
            keyboard.add_hotkey('ctrl + y',command.start) 
        pass