import os
from bardapi import Bard
from flask import Flask, jsonify, render_template, request, session
import re
from PIL import Image
import numpy as np
import urllib.request
import imageio

app = Flask(__name__)
app.secret_key = os.urandom(24)
token = os.environ['token']
cutoff = 0.35

def trim_data(data):
    if len(data) > 5000:
        data = data[:5000]
    return data

with open("system_card.txt", "r") as file:
    system = file.read()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    bard = Bard(token=token)
    data = request.get_json()
    # print(data)
    conversation = str(data["history"]) + str(data["message"])
    messages = str(system) + trim_data(conversation)

    ai_gen = bard.get_answer(messages)

    ai_message = ai_gen['content']

    if ai_gen["images"]:

        images = ai_gen["images"]
        link_list = ai_gen["links"]
        links = [link for link in link_list if "https://lh3.googleusercontent.com/" in link or "http://t0.gstatic.com/" in link]
        print(images)
        print(links)
      
        image_links = list(links) #use links or ai_gen["images"]
        bracket_contents = re.findall(r'\[(.*?)\]', ai_message)
        for bracket in bracket_contents:
            number_images = re.search(r'^(\d+)', bracket)
            if number_images:
                number_images = int(number_images.group())
                bracket_replacement = " ".join(["[" + image_links.pop(0) + "]" for _ in range(number_images)])
                ai_message = ai_message.replace(f"[{bracket}]", bracket_replacement, 1)
            else:
                ai_message = ai_message.replace(f"[{bracket}]", "[" + image_links.pop(0) + "]", 1)

    # make it print the "raw" new text
    print(ai_message)

    return jsonify(ai_message)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)
