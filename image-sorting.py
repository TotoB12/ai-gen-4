# Importing necessary libraries
from PIL import Image
import numpy as np
import urllib.request
import imageio

images = ['https://www.akc.org/wp-content/uploads/2021/07/Cavalier-King-Charles-Spaniel-laying-down-indoors.jpeg', 'https://i.natgeofe.com/n/4f5aaece-3300-41a4-b2a8-ed2708a0a27c/domestic-dog_thumb_3x4.jpg', 'https://cdn-prod.medicalnewstoday.com/content/images/articles/322/322868/golden-retriever-puppy.jpg', 'https://hips.hearstapps.com/hmg-prod/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg?crop=0.752xw:1.00xh;0.175xw,0&resize=1200:*']

links = ['https://lh3.googleusercontent.com/bip/APOwr81W3j3jCWFQGeAMuYIwZpmVWKiV3rpsNg7HJBpa4oqKvD2l-YH1Co7rT1UobzdxqxPeZG8XuBfo9h3owwTndGHIaKMnUu-oapXywj1rTmyGkJ8f9Cw5FFoFUj0pWCa9iL_T2z81cGQm8mrwV80r82N_kEkLFq7PRDeTT79jCksDQLu-hdPMmFIS0RPG6vVsc2MAkAQFGrfFWPaPhmwv3Hxc3xZQE7Q0Yq_BF1g0X3fUUw=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr82og3Bex0fVfSKvph3VoqZG3nKTXvmrdmNbFzau38JbPMqQj6HC5dZH--WF52oBEC126LbxricQCg87tHd3-0tXavFMJiH_VCIELmNuV6Ig1ah02v8fgN-r2VuL7903vaAZbq6g1deLMnNsXkZK9SpqR_yi7DwhiD2Vyxc=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr82bQR5xLFc4wWMo1hHQxrCx4Ie61cnfNCt9VYDcy4QFdXHCQp049XoP9EqfQNsuMyXxMiWMYzDBBGO8IlPNaZ4Jx8vecmBURczjJIxjjEpJ7uB3Cc3yzeNhPa6DMfkz4fWuuQPDW97r1ZESXYHWAmOD0oMKs9RFCmDOmIrld_2JGjPqkF6r-w=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr82wQ6Oy5ABg1-D0wi0KzSdo29wtbd_-lg-tFinFb9zDZDUYQpjJU4FF-CqnnfRMRK7AUw-dBDE6oriKkmwcUC6gwSe2l0h1rdSBtEtehB-_Dhl_WPtkdEV0ajDq1OoJ_c6rg9Hb-VP_NVXVeqMm_GVc0LdcaQZOUNhKuE7jfzRvlK8C37o_Q9w=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr81W3j3jCWFQGeAMuYIwZpmVWKiV3rpsNg7HJBpa4oqKvD2l-YH1Co7rT1UobzdxqxPeZG8XuBfo9h3owwTndGHIaKMnUu-oapXywj1rTmyGkJ8f9Cw5FFoFUj0pWCa9iL_T2z81cGQm8mrwV80r82N_kEkLFq7PRDeTT79jCksDQLu-hdPMmFIS0RPG6vVsc2MAkAQFGrfFWPaPhmwv3Hxc3xZQE7Q0Yq_BF1g0X3fUUw=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr82og3Bex0fVfSKvph3VoqZG3nKTXvmrdmNbFzau38JbPMqQj6HC5dZH--WF52oBEC126LbxricQCg87tHd3-0tXavFMJiH_VCIELmNuV6Ig1ah02v8fgN-r2VuL7903vaAZbq6g1deLMnNsXkZK9SpqR_yi7DwhiD2Vyxc=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr82bQR5xLFc4wWMo1hHQxrCx4Ie61cnfNCt9VYDcy4QFdXHCQp049XoP9EqfQNsuMyXxMiWMYzDBBGO8IlPNaZ4Jx8vecmBURczjJIxjjEpJ7uB3Cc3yzeNhPa6DMfkz4fWuuQPDW97r1ZESXYHWAmOD0oMKs9RFCmDOmIrld_2JGjPqkF6r-w=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr82wQ6Oy5ABg1-D0wi0KzSdo29wtbd_-lg-tFinFb9zDZDUYQpjJU4FF-CqnnfRMRK7AUw-dBDE6oriKkmwcUC6gwSe2l0h1rdSBtEtehB-_Dhl_WPtkdEV0ajDq1OoJ_c6rg9Hb-VP_NVXVeqMm_GVc0LdcaQZOUNhKuE7jfzRvlK8C37o_Q9w=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr81W3j3jCWFQGeAMuYIwZpmVWKiV3rpsNg7HJBpa4oqKvD2l-YH1Co7rT1UobzdxqxPeZG8XuBfo9h3owwTndGHIaKMnUu-oapXywj1rTmyGkJ8f9Cw5FFoFUj0pWCa9iL_T2z81cGQm8mrwV80r82N_kEkLFq7PRDeTT79jCksDQLu-hdPMmFIS0RPG6vVsc2MAkAQFGrfFWPaPhmwv3Hxc3xZQE7Q0Yq_BF1g0X3fUUw=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr82og3Bex0fVfSKvph3VoqZG3nKTXvmrdmNbFzau38JbPMqQj6HC5dZH--WF52oBEC126LbxricQCg87tHd3-0tXavFMJiH_VCIELmNuV6Ig1ah02v8fgN-r2VuL7903vaAZbq6g1deLMnNsXkZK9SpqR_yi7DwhiD2Vyxc=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr82bQR5xLFc4wWMo1hHQxrCx4Ie61cnfNCt9VYDcy4QFdXHCQp049XoP9EqfQNsuMyXxMiWMYzDBBGO8IlPNaZ4Jx8vecmBURczjJIxjjEpJ7uB3Cc3yzeNhPa6DMfkz4fWuuQPDW97r1ZESXYHWAmOD0oMKs9RFCmDOmIrld_2JGjPqkF6r-w=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr82wQ6Oy5ABg1-D0wi0KzSdo29wtbd_-lg-tFinFb9zDZDUYQpjJU4FF-CqnnfRMRK7AUw-dBDE6oriKkmwcUC6gwSe2l0h1rdSBtEtehB-_Dhl_WPtkdEV0ajDq1OoJ_c6rg9Hb-VP_NVXVeqMm_GVc0LdcaQZOUNhKuE7jfzRvlK8C37o_Q9w=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr81W3j3jCWFQGeAMuYIwZpmVWKiV3rpsNg7HJBpa4oqKvD2l-YH1Co7rT1UobzdxqxPeZG8XuBfo9h3owwTndGHIaKMnUu-oapXywj1rTmyGkJ8f9Cw5FFoFUj0pWCa9iL_T2z81cGQm8mrwV80r82N_kEkLFq7PRDeTT79jCksDQLu-hdPMmFIS0RPG6vVsc2MAkAQFGrfFWPaPhmwv3Hxc3xZQE7Q0Yq_BF1g0X3fUUw=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr82og3Bex0fVfSKvph3VoqZG3nKTXvmrdmNbFzau38JbPMqQj6HC5dZH--WF52oBEC126LbxricQCg87tHd3-0tXavFMJiH_VCIELmNuV6Ig1ah02v8fgN-r2VuL7903vaAZbq6g1deLMnNsXkZK9SpqR_yi7DwhiD2Vyxc=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr82bQR5xLFc4wWMo1hHQxrCx4Ie61cnfNCt9VYDcy4QFdXHCQp049XoP9EqfQNsuMyXxMiWMYzDBBGO8IlPNaZ4Jx8vecmBURczjJIxjjEpJ7uB3Cc3yzeNhPa6DMfkz4fWuuQPDW97r1ZESXYHWAmOD0oMKs9RFCmDOmIrld_2JGjPqkF6r-w=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr82wQ6Oy5ABg1-D0wi0KzSdo29wtbd_-lg-tFinFb9zDZDUYQpjJU4FF-CqnnfRMRK7AUw-dBDE6oriKkmwcUC6gwSe2l0h1rdSBtEtehB-_Dhl_WPtkdEV0ajDq1OoJ_c6rg9Hb-VP_NVXVeqMm_GVc0LdcaQZOUNhKuE7jfzRvlK8C37o_Q9w=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr81W3j3jCWFQGeAMuYIwZpmVWKiV3rpsNg7HJBpa4oqKvD2l-YH1Co7rT1UobzdxqxPeZG8XuBfo9h3owwTndGHIaKMnUu-oapXywj1rTmyGkJ8f9Cw5FFoFUj0pWCa9iL_T2z81cGQm8mrwV80r82N_kEkLFq7PRDeTT79jCksDQLu-hdPMmFIS0RPG6vVsc2MAkAQFGrfFWPaPhmwv3Hxc3xZQE7Q0Yq_BF1g0X3fUUw=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr82og3Bex0fVfSKvph3VoqZG3nKTXvmrdmNbFzau38JbPMqQj6HC5dZH--WF52oBEC126LbxricQCg87tHd3-0tXavFMJiH_VCIELmNuV6Ig1ah02v8fgN-r2VuL7903vaAZbq6g1deLMnNsXkZK9SpqR_yi7DwhiD2Vyxc=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr82bQR5xLFc4wWMo1hHQxrCx4Ie61cnfNCt9VYDcy4QFdXHCQp049XoP9EqfQNsuMyXxMiWMYzDBBGO8IlPNaZ4Jx8vecmBURczjJIxjjEpJ7uB3Cc3yzeNhPa6DMfkz4fWuuQPDW97r1ZESXYHWAmOD0oMKs9RFCmDOmIrld_2JGjPqkF6r-w=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr82wQ6Oy5ABg1-D0wi0KzSdo29wtbd_-lg-tFinFb9zDZDUYQpjJU4FF-CqnnfRMRK7AUw-dBDE6oriKkmwcUC6gwSe2l0h1rdSBtEtehB-_Dhl_WPtkdEV0ajDq1OoJ_c6rg9Hb-VP_NVXVeqMm_GVc0LdcaQZOUNhKuE7jfzRvlK8C37o_Q9w=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr81W3j3jCWFQGeAMuYIwZpmVWKiV3rpsNg7HJBpa4oqKvD2l-YH1Co7rT1UobzdxqxPeZG8XuBfo9h3owwTndGHIaKMnUu-oapXywj1rTmyGkJ8f9Cw5FFoFUj0pWCa9iL_T2z81cGQm8mrwV80r82N_kEkLFq7PRDeTT79jCksDQLu-hdPMmFIS0RPG6vVsc2MAkAQFGrfFWPaPhmwv3Hxc3xZQE7Q0Yq_BF1g0X3fUUw=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr82og3Bex0fVfSKvph3VoqZG3nKTXvmrdmNbFzau38JbPMqQj6HC5dZH--WF52oBEC126LbxricQCg87tHd3-0tXavFMJiH_VCIELmNuV6Ig1ah02v8fgN-r2VuL7903vaAZbq6g1deLMnNsXkZK9SpqR_yi7DwhiD2Vyxc=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr82bQR5xLFc4wWMo1hHQxrCx4Ie61cnfNCt9VYDcy4QFdXHCQp049XoP9EqfQNsuMyXxMiWMYzDBBGO8IlPNaZ4Jx8vecmBURczjJIxjjEpJ7uB3Cc3yzeNhPa6DMfkz4fWuuQPDW97r1ZESXYHWAmOD0oMKs9RFCmDOmIrld_2JGjPqkF6r-w=w250-h200-p', 'https://lh3.googleusercontent.com/bip/APOwr82wQ6Oy5ABg1-D0wi0KzSdo29wtbd_-lg-tFinFb9zDZDUYQpjJU4FF-CqnnfRMRK7AUw-dBDE6oriKkmwcUC6gwSe2l0h1rdSBtEtehB-_Dhl_WPtkdEV0ajDq1OoJ_c6rg9Hb-VP_NVXVeqMm_GVc0LdcaQZOUNhKuE7jfzRvlK8C37o_Q9w=w250-h200-p']

links = links[:len(images)]
cutoff = 0.2

# Compute the Chi-Squared distance
def chi_squared_distance(hist1, hist2):
    return 0.5 * np.sum((hist1 - hist2) ** 2 / (hist1 + hist2 + 1e-10))

def same(url0, url1):
  with urllib.request.urlopen(url0) as url:
      img1 = Image.open(url)

  with urllib.request.urlopen(url1) as url:
      img2 = Image.open(url)

  # Resize and crop the images
  img1 = img1.resize((200, 200))
  img1 = img1.crop((0, 0, 100, 100))
  
  img2 = img2.resize((200, 200))
  img2 = img2.crop((0, 0, 100, 100))
  
  # Convert the images to arrays
  img1_array = np.array(img1)
  img2_array = np.array(img2)
  
  # Calculate histograms
  hist1, _ = np.histogramdd(img1_array.reshape(-1, 3), bins=(8, 8, 8), range=[(0, 256), (0, 256), (0, 256)])
  hist2, _ = np.histogramdd(img2_array.reshape(-1, 3), bins=(8, 8, 8), range=[(0, 256), (0, 256), (0, 256)])
  
  # Normalize the histograms
  hist1 /= np.sum(hist1)
  hist2 /= np.sum(hist2)

  chi = chi_squared_distance(hist1, hist2)
  print(chi)

  if chi < cutoff:
    print('images are similar')
    return True
  else:
    print('images are not similar')
    return False

# Create a copy of the links list to be able to remove elements from it
links_copy = links.copy()

# Create an empty list to store the rearranged links
rearranged_links = []

# Iterate over each image
for image in images:
    # Iterate over each link in the copy of the links list
    for link in links_copy:
        # If the image and the link are the same
        if same(image, link):
            # Add the link to the rearranged links list
            rearranged_links.append(link)
            # Remove the link from the copy of the links list
            links_copy.remove(link)
            # Stop the loop as the match is found
            break

# Print the rearranged links
print(rearranged_links)