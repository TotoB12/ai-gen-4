import os
# from bardapi import Bard
from gemini import Gemini
from flask import Flask, jsonify, render_template, request
import re
import urllib.request
import imageio
import random
import base64
import requests
import json
import os, shutil

app = Flask(__name__)
app.secret_key = os.urandom(24)

proxies = {
  'http': '104.45.128.122:80'
}

folder = 'img'
def clear():
  for filename in os.listdir(folder):
      file_path = os.path.join(folder, filename)
      try:
          if os.path.isfile(file_path) or os.path.islink(file_path):
              os.unlink(file_path)
          elif os.path.isdir(file_path):
              shutil.rmtree(file_path)
      except Exception as e:
          print('Failed to delete %s. Reason: %s' % (file_path, e))

def trim_data(data):
    if len(data) > 47000:
        data = data[:47000]
    return data

with open("system_card.txt", "r") as file:
    system = file.read()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST", "GET"])
def generate():
    # token = os.environ[random.choice(['token', 'token1'])]
    # token = os.environ['token']
    # print(token)
    data = request.get_json()
    try:
      # bard = Bard(token=token)    
      cookies = {
        "__Secure-1PSIDCC" : os.environ['token'],
      }
      GeminiClient = Gemini(cookies=cookies)
      print(data)
      conversation = str(data["history"]) + str(data["message"])
      messages = str(system) + trim_data(conversation)
  
      if 'image' in request.get_json():
          print(data["image"])
          print("yay")
  
          image = requests.get(data["image"]).content
          # ai_gen = bard.ask_about_image(messages, image)
          ai_gen = None
          ai_message = ai_gen['content']
  
      else:
          # ai_gen = bard.get_answer(messages)
          ai_gen = GeminiClient.generate_content(messages)
          ai_message = ai_gen['content']
  
      if ai_gen["images"] and any(image.strip() for image in ai_gen["images"]):
          images = ai_gen["images"]
          link_list = ai_gen["links"]
          links = [link for link in link_list if "https://lh3.googleusercontent.com/" in link or "http://t0.gstatic.com/" in link]
          print(images)
          print(links)
  
          if len(list(images)) == 1:
            links = [list(images)[0]]
        
          image_links = list(ai_gen["images"]) #use links or ai_gen["images"]
          bracket_contents = re.findall(r'\[(.*?)\]', ai_message)
          for bracket in bracket_contents:
              number_images = re.search(r'^(\d+)', bracket)
              if number_images:
                  number_images = int(number_images.group())
                  bracket_replacement = "\n" + " ".join(["[" + image_links.pop(0) + "]" for _ in range(number_images)])
                  ai_message = ai_message.replace(f"[{bracket}]", bracket_replacement, 1)
              else:
                  ai_message = ai_message.replace(f"[{bracket}]", "\n[" + image_links.pop(0) + "]", 1)
  
    except Exception as e:
      print(e)
      if str(data["message"]) == "really" or str(data["message"]) == "seriously" or str(data["message"]) == "really?" or str(data["message"]) == "seriously?":
        ai_message = "yes"
      else:
        ai_message = "Error. Please kill me."

    # make it print the "raw" new text
    print(ai_message)

    return jsonify(ai_message)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)
