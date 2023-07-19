from bardapi import Bard
import os

token = os.environ['token']

bard = Bard(token=token)
image = open('image.jpg', 'rb').read() # (jpeg, png, webp) are supported.
# bard_answer = bard.ask_about_image('What is in the image?', image)
# bard_answer = bard.get_answer('Whats up?')
bard_answer = bard.get_answer("Give me a image of llama")['images']

print(bard_answer)