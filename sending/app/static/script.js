let questions = [
    {
        question: "Have you ever visited a therapist or attended a mental health seminar?",
        options: ["Nope, never!", "Yes, I have!"],
        encoded: [0, 1]
    },
    {
        question: "How would you rate the quality of your sleep lately?",
        options: [
            "I barely sleep at all!", 
            "Poor, I struggle to get enough rest.",
            "Fair, I sleep, but not great.",
            "Good, but with some restless nights.",
            "Very good, I mostly sleep well.",
            "Excellent, I sleep like a baby!"
        ],
        encoded: [0, 1, 2, 3, 4, 5]
    },
    {
        question: "Imagine you’re climbing a mountain which represents your daily life. How often do you feel out of breath?",
        options: [
            "I’m at the bottom, breathing easy.", 
            "I’m starting to feel a bit out of breath.",
            "I'm halfway up, needing some breaks.", 
            "I’m getting close to the top, breathless.",
            "Near the peak, and I’m gasping for air!", 
            "At the top, completely out of breath!"
        ],
        encoded: [0, 1, 2, 3, 4, 5]
    },
    {
        question: "Which of these environments matches the level of noise around you most of the time?",
        options: [
            "It’s as quiet as a library.", 
            "It’s fairly quiet, like a small park.",
            "It’s a bit noisy, like a café.", 
            "It’s noisy, like a busy street.",
            "It’s very noisy, like a construction site.", 
            "It’s as loud as a concert, I can’t hear myself think!"
        ],
        encoded: [0, 1, 2, 3, 4, 5]
    },
    {
        question: "Look at these homes. Which one feels most like your current living situation?",
        options: [
            "I’m living in a shack, barely managing.", 
            "I’m in a small, rundown home, struggling.",
            "My home is modest but okay.", 
            "I have a comfortable home, no complaints.",
            "My living conditions are quite good.", 
            "I’m living in luxury, like a mansion!"
        ],
        encoded: [0, 1, 2, 3, 4, 5]
    },
    {
        question: "How safe do you feel in your daily life?",
        options: [
            "I constantly feel unsafe.", 
            "I feel unsafe often.",
            "I sometimes feel unsafe.", 
            "I mostly feel safe.",
            "I feel safe almost all the time.", 
            "I always feel completely safe."
        ],
        encoded: [0, 1, 2, 3, 4, 5]
    },
    {
        question: "You’re a Sims character. How well are your basic needs (food, water, shelter) being met?",
        options: [
            "My needs are in the red, I'm barely surviving!", 
            "I’m struggling, my hunger meter is low.",
            "I’m managing, but it's not easy.", 
            "My needs are mostly met, life is okay.",
            "I’m thriving, my needs are well taken care of.", 
            "I'm living the dream, everything is perfect!"
        ],
        encoded: [0, 1, 2, 3, 4, 5]
    },
    {
        question: "Imagine you’re in an RPG in a shooting game. How’s your ‘academic XP’ progression?",
        options: [
            "I’m stuck at Level 1, failing all quests.", 
            "I’m trying, but struggling to level up.",
            "Gaining XP slowly, but I’m not a top player.", 
            "I’m levelling up at a good pace, doing well!",
            "I’m a top-tier player, acing most challenges!", 
            "I’m the hero of the game, I’ve mastered everything!"
        ],
        encoded: [0, 1, 2, 3, 4, 5]
    },
    {
        question: "You’re carrying a backpack. How heavy is it with your current study load?",
        options: [
            "It’s empty, I have no work to do!", 
            "It’s light, not much in there at all.",
            "It’s getting heavier, but still manageable.", 
            "It’s heavy, but I can still carry it.",
            "It’s very heavy, I’m struggling to keep up!", 
            "It’s crushing me, I can’t take another step!"
        ],
        encoded: [0, 1, 2, 3, 4, 5]
    },
    {
        question: "You’re in a co-op game with your teacher. How’s the teamwork going?",
        options: [
            "We’re not even on the same team. It’s bad.", 
            "Barely playing together, communication is poor.",
            "It’s okay, but we need better teamwork.", 
            "We’re working well together most of the time!",
            "Great teamwork, we’re in sync!", 
            "We’re unstoppable, best team ever!"
        ],
        encoded: [0, 1, 2, 3, 4, 5]
    },
    {
        question: "Your future career is like a treasure map. How worried are you about finding the treasure?",
        options: [
            "Not at all, I know exactly where I’m headed!", 
            "A little, but I’m confident I’ll find it.",
            "Occasionally, I wonder if I’m on the right path.", 
            "Often, I’m worried about getting lost.",
            "Very often, I feel like the treasure might be out of reach.", 
            "Constantly, I’m lost and don’t know where to go!"
        ],
        encoded: [0, 1, 2, 3, 4, 5]
    },
    {
        question: "Imagine you’re a player in a team-based game. How strong is your support squad?",
        options: [
            "I’m playing solo, no teammates.", 
            "I have one or two weak teammates.",
            "I have some decent teammates, but not enough.", 
            "I’ve got a strong team that’s always there for me!"
        ],
        encoded: [0, 1, 2, 3]
    },
    {
        question: "How much pressure do you feel from others, like this group?",
        options: [
            "I feel no pressure from others.", 
            "I feel a little pressure, but I manage well.",
            "Moderate pressure, but nothing overwhelming.", 
            "I feel pressured quite often.",
            "I’m under a lot of pressure from my peers.", 
            "Constantly pressured, it’s overwhelming!"
        ],
        encoded: [0, 1, 2, 3, 4, 5]
    },
    {
        question: "How many extracurricular badges have you earned, like this character?",
        options: [
            "I haven’t earned any badges yet.", 
            "I’ve earned one or two badges.",
            "I’ve earned a few badges, not many.", 
            "I’ve earned several badges.",
            "I’ve earned most of the badges available.", 
            "I’ve earned all the badges, I’m a star player!"
        ],
        encoded: [0, 1, 2, 3, 4, 5]
    },
    {
        question: "Do you face issues regarding bullying or ragging?",
        options: [
            "I’ve never experienced bullying.", 
            "I’ve rarely encountered bullying.",
            "Occasionally, I face mild bullying.", 
            "Bullying happens sometimes, and it affects me.",
            "I frequently deal with bullying, and it causes significant stress.", 
            "I’m constantly bullied, and it severely affects my life."
        ],
        encoded: [0, 1, 2, 3, 4, 5]
    },
    {
        question: "In the past couple of weeks, how often have you felt down, depressed, or hopeless?",
        options: [
            "I have not felt this way at all",
            "I felt this way on a few days",
            "I felt this way on most days",
            "I felt this way every day",
            "I felt this way all the time"
        ],
        encoded: [1, 2, 3, 4, 5]
    }
];
let currentQuestion = 0;
let responses = new Array(questions.length).fill(null);

function displayMessage() {
    const message = "Hey, I am Serenity! I will help you to analyze your stress level and manage stress.";
    const startButtonText = "Okay, Fine!";
    
    const chatBox = document.getElementById("chat-box");
    const messageElement = document.createElement('div');
    const startButton = document.createElement('button');
    
    messageElement.className = 'bot-message';
    startButton.className = 'start-button';
    
    messageElement.textContent = message;
    startButton.textContent = startButtonText;
    
    startButton.onclick = function () {
        chatBox.innerHTML = ''; // Clear the initial message and button
        displayQuestion(); // Start displaying questions after clicking the button
    };
    
    chatBox.appendChild(messageElement);
    chatBox.appendChild(startButton);
}

function displayQuestion() {
    const question = questions[currentQuestion];
    const chatBox = document.getElementById("chat-box");
    
    // Display question
    const questionElement = document.createElement("div");
    questionElement.className = "bot-message";
    questionElement.textContent = question.question;
    chatBox.appendChild(questionElement);
    
    // Display options as buttons
    question.options.forEach((option, index) => {
        const button = document.createElement("button");
        button.textContent = option;
        button.className = "option-button";
        button.onclick = () => selectOption(index);
        chatBox.appendChild(button);
    });
    
    // Scroll to bottom of chat
    chatBox.scrollTop = chatBox.scrollHeight;
}

function selectOption(index) {
    const question = questions[currentQuestion];
    const chatBox = document.getElementById("chat-box");
    
    // Remove the option buttons after selection
    const buttons = chatBox.querySelectorAll(".option-button");
    buttons.forEach(button => button.remove());
    
    // Display user's selected option
    const userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.textContent = question.options[index];
    chatBox.appendChild(userMessage);
    
    // Store the encoded value
    responses[currentQuestion] = question.encoded[index];
    
    currentQuestion++;
    
    // If there are more questions, display the next one
    if (currentQuestion < questions.length) {
        setTimeout(displayQuestion, 500); // Delay to mimic conversation
    } else {
        // All questions answered, submit the responses
        setTimeout(submitResponses, 500);
    }
    
    // Scroll to bottom of chat
    chatBox.scrollTop = chatBox.scrollHeight;
}

function submitResponses() {
    const chatBox = document.getElementById("chat-box");
    
    // Display thank you message
    const thankYouMessage = document.createElement("div");
    thankYouMessage.className = "thank-you-message";
    thankYouMessage.textContent = "Thank you for answering all the questions! Processing your responses...";
    chatBox.appendChild(thankYouMessage);
    
    // Send responses to the server
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ responses: responses })
    })
    .then(response => response.json())
    .then(data => {
        displayResults(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function displayResults(data) {
    const chatBox = document.getElementById("chat-box");
    
    // Display stress level message
    const stressMessage = document.createElement("div");
    stressMessage.className = "bot-message";
    stressMessage.textContent = data.stress_level;
    chatBox.appendChild(stressMessage);
    
    // Display guidelines
    if (data.guidelines && data.guidelines.length > 0) {
        data.guidelines.forEach(guideline => {
            const guidelineMessage = document.createElement("div");
            guidelineMessage.className = "guidelines-message";
            guidelineMessage.textContent = guideline;
            chatBox.appendChild(guidelineMessage);
        });
    }
    
    // Scroll to bottom of chat
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Start by displaying the initial message
displayMessage();
