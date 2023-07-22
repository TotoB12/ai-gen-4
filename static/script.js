const fileInput = document.getElementById("image");
const imageLabel = document.getElementById("imageLabel");

fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) {
    const file = fileInput.files[0];
    const maxSizeInBytes = 10 * 1024 * 1024;
    
    if (file.size > maxSizeInBytes) {
      alert("File size exceeds the allowed limit of 10MB. Please select a smaller file.");
      
      fileInput.value = null;
      imageLabel.classList.remove("file-selected");
    } else {
      imageLabel.classList.add("file-selected");
    }
  } else {
    imageLabel.classList.remove("file-selected");
  }
});

function getBase64Image(imageFile) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(imageFile);
    reader.onloadend = () => {
      const base64Data = reader.result.split(',')[1];
      resolve(base64Data);
    };
    reader.onerror = error => reject(error);
  });
}


async function uploadImageToImgur(imageFile) {
  return getBase64Image(imageFile)
    .then(base64Image => {
      var myHeaders = new Headers();
      myHeaders.append("Authorization", "Client-ID 6a8a51f3d7933e1");

      var formdata = new FormData();
      formdata.append("image", base64Image);

      var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: formdata,
        redirect: 'follow'
      };

      return fetch("https://api.imgur.com/3/image", requestOptions)
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            console.log(data.data.link);
            return data.data.link;
          } else {
            const errorReason = data.data ? data.data.error : "Unknown error";
            console.error("Failed to upload image to Imgur. Reason:", errorReason);
            throw new Error("Failed to upload image to Imgur. Reason: " + errorReason);
          }
        })
        .catch(error => {
          console.error('Error uploading image:', error);
          return null;
        });
    })
    .catch(error => {
      console.error('Error converting image to base64:', error);
      return null;
    });
}

function redirectToImage() {
  var imageSource = this.src;
  window.open(imageSource, '_blank')
}

document.addEventListener("DOMContentLoaded", function() 
{
  let conversationHistory = [];
  
  function loadConversationHistory() {
    const storedHistory = localStorage.getItem("conversationHistory");
    if (storedHistory) 
    {
      conversationHistory = JSON.parse(storedHistory);
      conversationHistory.forEach(message => {
        addMessage(message.content, message.role === "user" ? "user" : "bot");
      });
    } 
    else 
    {
      displayWelcomeMessage();
    }
}
  
function clearHistory() 
{
  const chatContainer = document.getElementById("chat-container");
  chatContainer.innerHTML = '';
  conversationHistory = [];
  localStorage.removeItem("conversationHistory");
  displayWelcomeMessage();
}

document.getElementById("clear-history").addEventListener("click", function() {
    clearHistory();
});

function saveConversationHistory() 
{
  localStorage.setItem("conversationHistory", JSON.stringify(conversationHistory));
}

    
function addMessage(message, sender, additionalClass) 
{
  const chatContainer = document.getElementById("chat-container");
  const messageElement = document.createElement("div");
  messageElement.className = `message ${sender}-message ${additionalClass}`;
  
  var imageRegex = /\[(http.*?)\]/g;
  var codeSnippetRegex = /```(\w+)\n([\s\S]*?)\n```/g;
  var regex = new RegExp(imageRegex.source + "|" + codeSnippetRegex.source, "g");
  // console.log(regex);
  
  let lastIndex = 0;
  let match;
  
  let messageText = document.createElement("pre");
  messageText.style.whiteSpace = "pre-wrap";
  messageText.style.fontFamily = "'Roboto', sans-serif";
  messageText.style.whiteSpace = "pre-wrap";
  messageText.className = "message-text";
  
  // first layer match : detect if it's a code embed or image link
  while ((match = regex.exec(message)) !== null) {
    console.log('code embed or image link detected !');
    // console.log(match[0])
    // console.log(match[1])
    // console.log(match[2])
    
    const plainText = message.substring(lastIndex, match.index);
    const escapedText = plainText.replace(/</g, "&lt;").replace(/>/g, "&gt;");
    messageText.insertAdjacentHTML("beforeend", escapedText);
    
    // if it's an image link
    if (match[1]) 
    {
      console.log('the match is an image ! ' + match[1]);
      const imageLink = match[1];
      const imageElement = document.createElement("img");
      imageElement.src = imageLink;
      imageElement.style.width = "50%";
      imageElement.onclick = redirectToImage;
      const imageContainer = document.createElement("div");
      imageContainer.className = "image-container";
      imageContainer.appendChild(imageElement);
      console.log(imageElement);
      messageText.appendChild(imageContainer); /* imageElement */
    
    // if it's a code embed
    } else if ((codeMatch = codeSnippetRegex.exec(match[0])) !== null) {
      console.log('match code');
      const language = codeMatch[1];
      const code = codeMatch[2];
      const codeElement = document.createElement("code");
      codeElement.className = language;
      codeElement.classList.add('code');
      codeElement.textContent = code;
      hljs.highlightElement(codeElement);
      const codeContainer = document.createElement("pre");
      codeContainer.appendChild(codeElement);
      messageText.appendChild(codeContainer);
    }
      
    console.log('--- next match ---')
    lastIndex = regex.lastIndex;
    
  }

  const remainingText = message.substring(lastIndex);
  const escapedRemainingText = remainingText.replace(/</g, "&lt;").replace(/>/g, "&gt;");
  messageText.insertAdjacentHTML("beforeend", escapedRemainingText);
  
  messageElement.appendChild(messageText);
  chatContainer.appendChild(messageElement);
  chatContainer.scrollTop = chatContainer.scrollHeight;
  
}
    
function displayWelcomeMessage() {
    const welcomeMessage = "Hello! I'm TotoB12. How can I help you today?";
    addMessage(welcomeMessage, "bot");
}
function displayGeneratingMessage() {
  const generatingMessage = "Generating response";
  addMessage(generatingMessage, "bot", "generating-message");
  const dotsContainer = document.createElement("span");
  dotsContainer.className = "dots-animation";
  const dot1 = document.createElement("span");
  dot1.textContent = ".";
  const dot2 = document.createElement("span");
  dot2.textContent = ".";
  const dot3 = document.createElement("span");
  dot3.textContent = ".";
  dotsContainer.appendChild(dot1);
  dotsContainer.appendChild(dot2);
  dotsContainer.appendChild(dot3);
  const messageElement = document.querySelector(".generating-message .message-text");
  messageElement.appendChild(dotsContainer);
  return generatingMessage;
}
function removeGeneratingMessage() {
  const chatContainer = document.getElementById("chat-container");
  const generatingMessageElement = chatContainer.querySelector(".generating-message");
  if (generatingMessageElement) {
    chatContainer.removeChild(generatingMessageElement);
  }
}
document.getElementById("chat-form").addEventListener("submit", async function(event) {
    event.preventDefault();
    const input = document.getElementById("message");
    let message = input.value.trim();
    const image = document.getElementById("image").files[0];
    if (message.length === 0 && !image) {
        return;
    }
    let fetchOptions;
    let imageUrl;

  document.getElementById("image").value = null;
  imageLabel.classList.remove("file-selected");
  input.value = "";
  input.style.height = "";
  input.focus();

    if (image) {
        try {
            imageUrl = await uploadImageToImgur(image);
        } catch (error) {
            console.error("Error uploading image:", error);
        }

        if (imageUrl) {
            formData = JSON.stringify({ message: message += `\n\n[${imageUrl}]`, history: conversationHistory, image: imageUrl });
            fetchOptions = {
                method: "POST",
                body: formData,
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            };
        }
    } else {
        formData = JSON.stringify({ message: message, history: conversationHistory });
        fetchOptions = {
            method: "POST",
            body: formData,
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        };
    }

    addMessage(message, "user");
    conversationHistory.push({ role: "user", content: message });
    saveConversationHistory();
    document.getElementById("image").value = null;
    imageLabel.classList.remove("file-selected");
    input.value = "";
    input.style.height = "";
    input.focus();
    const generatingMessage = displayGeneratingMessage();
    const additionalClass = (generatingMessage === "Generating response...") ? "generating-message" : "";
    if (fetchOptions) {
        try {
            const response = await fetch("/generate", fetchOptions);
            const data = await response.json();
            removeGeneratingMessage();
            conversationHistory.push({ role: "assistant", content: data });
            saveConversationHistory();
            addMessage(data, "bot");
        } catch (error) {
            console.error("Error fetching response:", error);
        }
    }
});


function adjustTextareaHeight(textarea) {
    textarea.style.height = "auto";
    const maxHeight = window.innerHeight * 0.3;
    const newHeight = Math.min(textarea.scrollHeight, maxHeight);
    textarea.style.height = newHeight + "px";
    if (textarea.value.trim().length === 0 || textarea.value.split("\n").length === 1) {
        textarea.style.height = "";
    }
}
document.getElementById("message").addEventListener("blur", function() {
  adjustTextareaHeight(this);
});
document.getElementById("message").addEventListener("input", function() {
    adjustTextareaHeight(this);
});
document.getElementById("message").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        if (!event.shiftKey) {
            event.preventDefault();
            document.getElementById("chat-form").dispatchEvent(new Event("submit"));
        }
    }
});
loadConversationHistory();
adjustTextareaHeight(document.getElementById("message"));
});
