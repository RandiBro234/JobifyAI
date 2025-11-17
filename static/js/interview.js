// ===== MODE TOGGLE =====
const voiceModeBtn = document.getElementById("voiceModeBtn");
const textModeBtn = document.getElementById("textModeBtn");
const voiceMode = document.getElementById("voiceMode");
const textMode = document.getElementById("textMode");

if (voiceModeBtn && textModeBtn) {
  voiceModeBtn.addEventListener("click", () => {
    voiceMode.classList.remove("answer-mode-hidden");
    textMode.classList.add("answer-mode-hidden");
    voiceModeBtn.classList.add("toggle-btn-active");
    textModeBtn.classList.remove("toggle-btn-active");
  });

  textModeBtn.addEventListener("click", () => {
    textMode.classList.remove("answer-mode-hidden");
    voiceMode.classList.add("answer-mode-hidden");
    textModeBtn.classList.add("toggle-btn-active");
    voiceModeBtn.classList.remove("toggle-btn-active");
  });
}

// ===== TEXT ANSWER HANDLING =====
let currentQuestionIndex = 0;

const questionText = document.getElementById("questionText");
const questionIndexText = document.getElementById("questionIndexText");
const textAnswer = document.getElementById("textAnswer");
const submitTextAnswer = document.getElementById("submitTextAnswer");

const resultCard = document.getElementById("resultCard");
const resultScore = document.getElementById("resultScore");
const resultFeedback = document.getElementById("resultFeedback");
const nextQuestionBtn = document.getElementById("nextQuestionBtn");

async function sendAnswer(answerTextValue) {
  const payload = {
    answer: answerTextValue,
    question_index: currentQuestionIndex,
  };

  const res = await fetch("/api/evaluate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await res.json();
  if (!data.success) {
    alert(data.message || "Terjadi kesalahan.");
    return;
  }

  resultScore.textContent = data.score;
  resultFeedback.textContent = data.feedback;
  resultCard.classList.remove("result-hidden");

  if (data.has_next) {
    nextQuestionBtn.style.display = "inline-flex";
    nextQuestionBtn.onclick = () => {
      currentQuestionIndex = data.next_question_index;
      questionText.textContent = data.next_question;
      questionIndexText.textContent =
        "Pertanyaan " + (currentQuestionIndex + 1) + " dari " + TOTAL_QUESTIONS;
      textAnswer.value = "";
      resultCard.classList.add("result-hidden");
    };
  } else {
    nextQuestionBtn.style.display = "none";
  }
}

if (submitTextAnswer) {
  submitTextAnswer.addEventListener("click", () => {
    const value = textAnswer.value.trim();
    if (!value) {
      alert("Jawaban teks masih kosong.");
      return;
    }
    sendAnswer(value);
  });
}

// ===== VOICE ANSWER HANDLING (opsional) =====
const micButton = document.getElementById("micButton");
const micLabel = document.getElementById("micLabel");
const voiceStatus = document.getElementById("voiceStatus");

let recognition;
let isRecording = false;
let recordedText = "";

if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.lang = "id-ID";
  recognition.continuous = false;
  recognition.interimResults = true;

  recognition.onstart = () => {
    isRecording = true;
    recordedText = "";
    micLabel.textContent = "Berhenti Rekam";
    voiceStatus.textContent = "Merekam... silakan menjawab.";
  };

  recognition.onresult = (event) => {
    let finalTranscript = "";
    for (let i = 0; i < event.results.length; i++) {
      finalTranscript += event.results[i][0].transcript + " ";
    }
    recordedText = finalTranscript.trim();
    voiceStatus.textContent = "Hasil rekaman: \"" + recordedText + "\"";
  };

  recognition.onend = () => {
    isRecording = false;
    micLabel.textContent = "Mulai Rekam";

    if (recordedText) {
      // Kirim hasil suara sebagai teks ke endpoint yang sama (text mining)
      sendAnswer(recordedText);
    } else {
      voiceStatus.textContent = "Tidak ada suara yang terekam.";
    }
  };

  recognition.onerror = (event) => {
    console.error(event.error);
    voiceStatus.textContent = "Terjadi error saat merekam suara.";
    isRecording = false;
    micLabel.textContent = "Mulai Rekam";
  };
} else {
  if (voiceStatus) {
    voiceStatus.textContent =
      "Browser Anda tidak mendukung speech recognition. Silakan gunakan mode teks.";
  }
}

if (micButton && recognition) {
  micButton.addEventListener("click", () => {
    if (!isRecording) {
      recognition.start();
    } else {
      recognition.stop();
    }
  });
}
