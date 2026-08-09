/**
 * AI Smart Civic Services — Main Interactive Frontend Logic
 */

(function () {
  'use strict';

  // --- Theme Toggle Engine ---
  function initTheme() {
    const savedTheme = localStorage.getItem('civic_theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeToggleIcon(savedTheme);
  }

  function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('civic_theme', newTheme);
    updateThemeToggleIcon(newTheme);
    showToast(`Switched to ${newTheme} mode`, 'info');
  }

  function updateThemeToggleIcon(theme) {
    const btn = document.getElementById('theme-toggle-btn');
    if (btn) {
      btn.innerHTML = theme === 'dark' ? '☀️' : '🌙';
    }
  }

  // --- Toast Notification Engine ---
  window.showToast = function (message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    let icon = 'ℹ️';
    if (type === 'success') icon = '✅';
    if (type === 'error') icon = '⚠️';
    
    toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  };

  // --- AI Chatbot Engine ---
  function initChatbot() {
    const fab = document.getElementById('chatbot-fab');
    const window = document.getElementById('chatbot-window');
    const closeBtn = document.getElementById('chatbot-close');
    const sendBtn = document.getElementById('chatbot-send');
    const input = document.getElementById('chatbot-input');
    const messages = document.getElementById('chatbot-messages');

    if (!fab || !window) return;

    fab.addEventListener('click', () => {
      window.classList.toggle('open');
      if (window.classList.contains('open') && input) input.focus();
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', () => window.classList.remove('open'));
    }

    function appendMessage(sender, text) {
      const bubble = document.createElement('div');
      bubble.className = `chat-bubble ${sender}`;
      bubble.textContent = text;
      messages.appendChild(bubble);
      messages.scrollTop = messages.scrollHeight;
    }

    function handleSend() {
      const text = input.value.trim();
      if (!text) return;

      appendMessage('user', text);
      input.value = '';

      // Instant AI Assistant Bot Responses
      setTimeout(() => {
        let reply = "I'm CivicBot, your AI assistant! How can I help you report or track a civic issue today?";
        const lower = text.toLowerCase();
        if (lower.includes('report') || lower.includes('file') || lower.includes('complaint')) {
          reply = "You can submit a complaint via the 'Submit Issue' button. Uploading photos helps our AI route it faster!";
        } else if (lower.includes('status') || lower.includes('track') || lower.includes('my')) {
          reply = "Check your 'My Dashboard' to view real-time status updates and department action timelines.";
        } else if (lower.includes('emergency') || lower.includes('urgent') || lower.includes('fire')) {
          reply = "CRITICAL: For life-threatening emergencies, please dial emergency services (911/112) immediately.";
        }
        appendMessage('bot', reply);
      }, 600);
    }

    if (sendBtn && input) {
      sendBtn.addEventListener('click', handleSend);
      input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
      });
    }
  }

  // --- File Dropzone & Live Photo Upload Preview ---
  function initDropzone() {
    const dropzone = document.getElementById('file-dropzone');
    const fileInput = document.getElementById('file-input');
    const previewGrid = document.getElementById('file-preview-grid');

    if (!dropzone || !fileInput) return;

    dropzone.addEventListener('click', () => fileInput.click());

    ['dragenter', 'dragover'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
      });
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
      });
    });

    dropzone.addEventListener('drop', (e) => {
      const files = e.dataTransfer.files;
      fileInput.files = files;
      handleFiles(files);
    });

    fileInput.addEventListener('change', () => {
      handleFiles(fileInput.files);
    });

    function handleFiles(files) {
      if (!previewGrid) return;
      previewGrid.innerHTML = '';
      Array.from(files).forEach(file => {
        if (!file.type.startsWith('image/')) return;
        const reader = new FileReader();
        reader.onload = (e) => {
          const img = document.createElement('img');
          img.src = e.target.result;
          img.className = 'file-preview-item';
          previewGrid.appendChild(img);
        };
        reader.readAsDataURL(file);
      });
    }
  }

  // --- Live Client-Side AI Form Preview ---
  function initAIFormPreview() {
    const descField = document.getElementById('complaint-description');
    const aiPreviewBox = document.getElementById('ai-preview-box');
    const aiCat = document.getElementById('ai-preview-category');
    const aiPrio = document.getElementById('ai-preview-priority');

    if (!descField || !aiPreviewBox) return;

    descField.addEventListener('input', () => {
      const text = descField.value.trim();
      if (text.length > 15) {
        aiPreviewBox.style.display = 'block';
        const lower = text.toLowerCase();
        
        if (lower.includes('water') || lower.includes('pipe') || lower.includes('leak')) {
          if (aiCat) aiCat.textContent = 'Water Supply';
          if (aiPrio) { aiPrio.textContent = 'HIGH'; aiPrio.className = 'badge badge-high'; }
        } else if (lower.includes('fire') || lower.includes('hazard') || lower.includes('collapse') || lower.includes('electric')) {
          if (aiCat) aiCat.textContent = 'Public Safety';
          if (aiPrio) { aiPrio.textContent = 'CRITICAL'; aiPrio.className = 'badge badge-critical'; }
        } else if (lower.includes('garbage') || lower.includes('trash') || lower.includes('waste')) {
          if (aiCat) aiCat.textContent = 'Sanitation';
          if (aiPrio) { aiPrio.textContent = 'MEDIUM'; aiPrio.className = 'badge badge-medium'; }
        } else {
          if (aiCat) aiCat.textContent = 'Roads & Infrastructure';
          if (aiPrio) { aiPrio.textContent = 'MEDIUM'; aiPrio.className = 'badge badge-medium'; }
        }
      } else {
        aiPreviewBox.style.display = 'none';
      }
    });
  }

  // --- Live Table Filtering ---
  function initTableFilter() {
    const searchInput = document.getElementById('table-search-input');
    const filterSelect = document.getElementById('table-filter-select');
    const table = document.querySelector('table.data-table');

    if (!searchInput || !table) return;

    function filterRows() {
      const query = searchInput.value.toLowerCase();
      const category = filterSelect ? filterSelect.value.toLowerCase() : '';
      const rows = table.querySelectorAll('tbody tr');

      rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const matchesQuery = text.includes(query);
        const matchesCategory = !category || text.includes(category);
        row.style.display = (matchesQuery && matchesCategory) ? '' : 'none';
      });
    }

    searchInput.addEventListener('input', filterRows);
    if (filterSelect) filterSelect.addEventListener('change', filterRows);
  }

  // Initialize on DOM load
  document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initChatbot();
    initDropzone();
    initAIFormPreview();
    initTableFilter();

    const themeBtn = document.getElementById('theme-toggle-btn');
    if (themeBtn) themeBtn.addEventListener('click', toggleTheme);
  });

})();
