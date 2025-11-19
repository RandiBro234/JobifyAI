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

// ===== GLOBAL STATE =====
let currentQuestionIndex = 0;

const questionText = document.getElementById("questionText");
const questionIndexText = document.getElementById("questionIndexText");

const textAnswer = document.getElementById("textAnswer");
const submitTextAnswer = document.getElementById("submitTextAnswer");

const resultCard = document.getElementById("resultCard");
const resultScore = document.getElementById("resultScore");
const resultFeedback = document.getElementById("resultFeedback");
const nextQuestionBtn = document.getElementById("nextQuestionBtn");

const finalResultCard = document.getElementById("finalResultCard");
const finalAvgScore = document.getElementById("finalAvgScore");
const finalOverallFeedback = document.getElementById("finalOverallFeedback");

// ===== FUNGSI KIRIM JAWABAN KE BACKEND =====
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

  // Tampilkan hasil per pertanyaan
  resultScore.textContent = data.score;
  resultFeedback.textContent = data.feedback;
  resultCard.classList.remove("result-hidden");

  // Jika masih ada pertanyaan berikutnya
  if (data.has_next) {
    nextQuestionBtn.style.display = "inline-flex";
    nextQuestionBtn.onclick = () => {
      currentQuestionIndex = data.next_question_index;
      questionText.textContent = data.next_question;
      questionIndexText.textContent =
        "Pertanyaan " + (currentQuestionIndex + 1) + " dari " + TOTAL_QUESTIONS;
      if (textAnswer) textAnswer.value = "";
      resultCard.classList.add("result-hidden");
      // sembunyikan ringkasan kalau sebelumnya kelihatan (harusnya tidak, tapi jaga-jaga)
      if (finalResultCard) finalResultCard.classList.add("result-hidden");
    };
  } else {
    // Tidak ada pertanyaan berikutnya: sesi selesai
    nextQuestionBtn.style.display = "none";

    if (data.is_finished && finalResultCard) {
      if (data.final_avg_score !== null && data.final_avg_score !== undefined) {
        finalAvgScore.textContent = data.final_avg_score.toFixed(2);
      } else {
        finalAvgScore.textContent = "-";
      }
      finalOverallFeedback.textContent = data.overall_feedback || "";
      finalResultCard.classList.remove("result-hidden");
    }
  }
}

// ===== HANDLING MODE TEKS =====
if (submitTextAnswer) {
  submitTextAnswer.addEventListener("click", () => {
    const value = (textAnswer.value || "").trim();
    if (!value) {
      alert("Jawaban teks masih kosong.");
      return;
    }
    sendAnswer(value);
  });
}

// ===== HANDLING MODE SUARA (Speech Recognition) =====
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
    if (voiceStatus)
      voiceStatus.textContent = "Merekam... silakan menjawab.";
  };

  recognition.onresult = (event) => {
    let finalTranscript = "";
    for (let i = 0; i < event.results.length; i++) {
      finalTranscript += event.results[i][0].transcript + " ";
    }
    recordedText = finalTranscript.trim();
    if (voiceStatus)
      voiceStatus.textContent = 'Hasil rekaman: "' + recordedText + '"';
  };

  recognition.onend = () => {
    isRecording = false;
    micLabel.textContent = "Mulai Rekam";

    if (recordedText) {
      sendAnswer(recordedText);
    } else {
      if (voiceStatus) voiceStatus.textContent = "Tidak ada suara yang terekam.";
    }
  };

  recognition.onerror = (event) => {
    console.error(event.error);
    if (voiceStatus)
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
