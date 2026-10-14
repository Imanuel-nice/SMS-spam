// ==========================================================================
// SpamFree JavaScript Logic
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const messageInput = document.getElementById('message-input');
  const analyzeBtn = document.getElementById('analyze-btn');
  const clearBtn = document.getElementById('clear-btn');
  const sampleBtns = document.querySelectorAll('.pill-btn');
  const resultsPanel = document.getElementById('results-panel');
  const verdictBadge = document.getElementById('verdict-badge');
  const scoreBar = document.getElementById('score-bar');
  const scoreText = document.getElementById('score-text');
  const signalsList = document.getElementById('signals-list');

  // Sample Data
  const samples = {
    spam: "URGENT! You have won a $1,000 Walmart Gift Card. Go to http://bit.ly/claim-prize NOW to claim. Valid today only!",
    ham: "Hey, are we still meeting for lunch at 12:30 PM today? Let me know when you're leaving."
  };

  // Sample Pill Event Handler
  sampleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const type = btn.getAttribute('data-sample');
      if (samples[type]) {
        messageInput.value = samples[type];
      }
    });
  });

  // Clear Input Event Handler
  clearBtn.addEventListener('click', () => {
    messageInput.value = '';
    resetResults();
  });

  // Analyze Button Event Handler
  analyzeBtn.addEventListener('click', () => {
    const text = messageInput.value.trim();
    
    if (!text) {
      alert('Please enter or paste a message to analyze.');
      return;
    }

    analyzeMessage(text);
  });

  // Analysis Handler Placeholder (Extend with real backend API or ML model logic)
  function analyzeMessage(text) {
    resultsPanel.classList.remove('card-hidden');

    // Rule-based dummy score calculation for demonstration layout
    let score = 0;
    const detectedSignals = [];

    const lowerText = text.toLowerCase();

    // Urgent keywords
    if (/urgent|win|winner|claimed|gift card|valid today|act now/i.test(lowerText)) {
      score += 45;
      detectedSignals.push('Contains promotional or urgent phrasing');
    }

    // Links / Shorteners
    if (/http[s]?:\/\/|bit\.ly|tinyurl/i.test(lowerText)) {
      score += 40;
      detectedSignals.push('Contains suspicious external link or shortened URL');
    }

    // Currency symbols / Numbers
    if (/\$|\b\d{3,}\b/i.test(lowerText)) {
      score += 15;
      detectedSignals.push('Contains dollar amounts or numerical incentives');
    }

    score = Math.min(score, 100);

    // Update UI
    scoreBar.style.width = `${score}%`;
    scoreText.textContent = `${score}%`;

    if (score >= 50) {
      verdictBadge.textContent = 'SPAM DETECTED';
      verdictBadge.className = 'verdict-badge spam';
      scoreBar.style.backgroundColor = 'var(--danger)';
    } else {
      verdictBadge.textContent = 'LIKELY SAFE';
      verdictBadge.className = 'verdict-badge safe';
      scoreBar.style.backgroundColor = 'var(--success)';
    }

    // Render signals
    signalsList.innerHTML = '';
    if (detectedSignals.length > 0) {
      detectedSignals.forEach(signal => {
        const li = document.createElement('li');
        li.textContent = `• ${signal}`;
        signalsList.appendChild(li);
      });
    } else {
      const li = document.createElement('li');
      li.textContent = '• No obvious risk indicators found.';
      signalsList.appendChild(li);
    }
  }

  function resetResults() {
    resultsPanel.classList.add('card-hidden');
    verdictBadge.textContent = 'Pending';
    verdictBadge.className = 'verdict-badge';
    scoreBar.style.width = '0%';
    scoreText.textContent = '0%';
    signalsList.innerHTML = '<li>No analysis performed yet.</li>';
  }
});