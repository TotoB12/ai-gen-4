const fileInput = document.getElementById("image");
const imageLabel = document.getElementById("imageLabel");

// Add an event listener to the file input
fileInput.addEventListener("change", () => {
  // Check if a file is selected
  if (fileInput.files.length > 0) {
    // Add the "file-selected" class to the label
    imageLabel.classList.add("file-selected");
  } else {
    // If no file is selected, remove the "file-selected" class
    imageLabel.classList.remove("file-selected");
  }
});

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
      messageText.appendChild(imageElement);
    
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
document.getElementById("chat-form").addEventListener("submit", function(event) {
    event.preventDefault();
    const input = document.getElementById("message");
    const message = input.value.trim();
    const image = document.getElementById("image").files[0];
    if (message.length === 0 && !image) {
        return;
    }
    let fetchOptions;
    if (image) {
        let formData = new FormData();
        formData.append("message", message);
        formData.append("history", JSON.stringify(conversationHistory));
        formData.append("image", image);
        fetchOptions = {
            method: "POST",
            body: formData
        };
    } else {
        fetchOptions = {
            method: "POST",
            body: JSON.stringify({ message: message, history: conversationHistory }),
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
    fetch("/generate", fetchOptions)
  .then(response => response.json())
  .then(data => {
    removeGeneratingMessage();
    conversationHistory.push({ role: "assistant", content: data });
    saveConversationHistory();
    addMessage(data, "bot");
  });
});
document.getElementById("clear-history").addEventListener("click", function() {
    clearHistory();
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