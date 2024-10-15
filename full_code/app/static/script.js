let questions = [];
let currentQuestion = 0;
let responses = [];

// Utility function to handle fetch requests
async function fetchQuestions(url) {
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) throw new Error('Network response was not ok');
    questions = await response.json(); // Assign the received data to 'questions'
    console.log(questions); // Log the questions for confirmation
  } catch (error) {
    console.error("Error:", error);
    alert("Failed to load questions. Please try again later."); // User-friendly error message
  }
}

// Initialize chat
function initChat() {
  fetchQuestions("http://localhost:5000/chat-bot.html/questions");
  setTimeout(() => {
    responses = new Array(questions.length).fill(null);
    displayMessage();
  }, 1000);
}

// Restart chat
function restartChat() {
  currentQuestion = 0;
  responses.fill(null); // Reset responses
  updateProgressBar();
  document.getElementById("chat-box").innerHTML = "";
  displayMessage();
}

document.getElementById("reload-btn").addEventListener("click", restartChat);
window.onload = initChat;

// Display initial message
function displayMessage() {
  const message = "Hey, I am Serenity! I will help you to analyze your stress level and manage stress.";
  const chatBox = document.getElementById("chat-box");

  const messageElement = document.createElement("li");
  messageElement.className = "chat incoming";
  messageElement.innerHTML = `<span class="material-symbols-outlined">smart_toy</span><p>${message}</p>`;
  chatBox.appendChild(messageElement);

  const startButton = document.createElement("button");
  startButton.className = "start-button";
  startButton.textContent = "Okay, Fine!";
  startButton.onclick = () => {
    chatBox.innerHTML = ""; // Clear chat box for new questions
    displayQuestion();
  };

  chatBox.appendChild(startButton);
}

function updateProgressBar() {
  const progressBar = document.getElementById("progress-bar");
  const currentProgress = (currentQuestion / questions.length) * 100; // Ensure max is 100%
  progressBar.style.width = currentProgress + "%";
}

function displayQuestion() {
  const question = questions[currentQuestion];
  const chatBox = document.getElementById("chat-box");

  const questionElement = document.createElement("li");
  questionElement.className = "chat incoming";
  questionElement.innerHTML = `<span class="material-symbols-outlined">smart_toy</span><p>${question.question}</p>`;
  chatBox.appendChild(questionElement);

  question.options.forEach((option, index) => {
    const button = document.createElement("button");
    button.textContent = option;
    button.className = "option-button";
    button.onclick = () => selectOption(index);
    chatBox.appendChild(button);
  });

  chatBox.scrollTop = chatBox.scrollHeight;
  updateProgressBar();
}

function selectOption(index) {
  const chatBox = document.getElementById("chat-box");
  const question = questions[currentQuestion];

  const userMessage = document.createElement("li");
  userMessage.className = "chat outgoing";
  userMessage.innerHTML = `<p>${question.options[index]}</p>`;
  chatBox.appendChild(userMessage);

  responses[currentQuestion] = question.encoded[index];
  currentQuestion++;

  // Delay the next question to enhance user experience
  setTimeout(() => {
    if (currentQuestion < questions.length) {
      displayQuestion();
    } else {
      submitResponses();
    }
  }, 500);
}

async function submitResponses() {
  const chatBox = document.getElementById("chat-box");
  const thankYouMessage = document.createElement("li");
  thankYouMessage.className = "chat incoming";
  thankYouMessage.innerHTML = `<span class="material-symbols-outlined">smart_toy</span><p>Thank you for answering all the questions! Processing your responses...</p>`;
  chatBox.appendChild(thankYouMessage);

  // Delay before submitting responses
  setTimeout(async () => {
    try {
      const response = await fetch("/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ responses: responses }),
      });
      if (!response.ok) throw new Error('Network response was not ok');
      const data = await response.json();
      displayResults(data);
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to submit responses. Please try again later."); // User-friendly error message
    }
  }, 1000);
}

function displayResults(data) {
  const chatBox = document.getElementById("chat-box");
  chatBox.innerHTML = ""; // Clear chat for results

  const finalResultContainer = document.createElement("div");
  finalResultContainer.className = "final-result";

  const stressMessage = document.createElement("p");
  stressMessage.innerText = `Your Stress Level: ${data.stress_level}`;
  
  // Set color based on stress level
  const colorMap = {
    "Minimal": "#28a745",
    "Moderate": "#ff9800",
    "High": "#dc3545"
  };
  stressMessage.style.color = colorMap[data.stress_level] || "#28a745"; // Default color
  finalResultContainer.style.border = `2px solid ${stressMessage.style.color}`; // Border color matches stress level

  finalResultContainer.appendChild(stressMessage);

  if (data.guidelines && data.guidelines.length > 0) {
    const guidelinesHeading = document.createElement("h3");
    guidelinesHeading.innerText = "Guidelines for You:";
    finalResultContainer.appendChild(guidelinesHeading);

    data.guidelines.forEach((guideline) => {
      const guidelineMessage = document.createElement("p");
      guidelineMessage.innerText = guideline;
      finalResultContainer.appendChild(guidelineMessage);
    });
  }

  chatBox.appendChild(finalResultContainer);
  chatBox.scrollTop = chatBox.scrollHeight; 
}
