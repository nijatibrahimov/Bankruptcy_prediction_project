// script.js
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("prediction-form");
  const resultEl = document.getElementById("result");

  // Loading indicator
  const loadingEl = document.createElement("div");
  loadingEl.textContent = "Predicting...";
  loadingEl.style.display = "none";
  loadingEl.style.fontWeight = "bold";
  loadingEl.style.marginTop = "15px";
  loadingEl.style.textAlign = "center";
  loadingEl.style.fontSize = "24px";

  form.appendChild(loadingEl);

  // Helper: show result or error
  function displayMessage(message, isError = false) {
    resultEl.textContent = message;
    resultEl.style.color = isError ? "#e74c3c" : "#27ae60";
    resultEl.style.fontSize = "24px";
    resultEl.style.marginBottom = "60px";
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    loadingEl.style.display = "block";
    displayMessage(""); // clear previous

    try {
      // Build JSON payload from form
      const formData = new FormData(form);
      const payload = {};

      for (let [key, value] of formData.entries()) {
        if (key === "company_name") {
          payload[key] = value; // keep company_name as string
        } else {
          payload[key] = parseFloat(value); // numeric conversion
        }
      }

      // Validate all numeric inputs
      for (let key in payload) {
        if (key !== "company_name" && isNaN(payload[key])) {
          throw new Error(`Invalid number in field: ${key}`);
        }
      }

      // Call Flask backend /predict endpoint
      const response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errText = await response.text();
        throw new Error(`Server error: ${response.status} — ${errText}`);
      }

      const data = await response.json();

      // ✅ Display explanatory message instead of raw 0/1
      if (data.message) {
        displayMessage(`Result: ${data.message}`);
      } else {
        displayMessage(`Prediction result: ${data.prediction}`);
      }

    } catch (error) {
      console.error("Prediction failed:", error);
      displayMessage(`Error: ${error.message}`, true);
    } finally {
      loadingEl.style.display = "none";
    }
  });
});

// 1. LENIS INITIALIZATION
const lenis = new Lenis({
  duration: 1.2,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  smooth: true,
});

function raf(time) {
  lenis.raf(time);
  requestAnimationFrame(raf);
}
requestAnimationFrame(raf);

// 2. STARS ANIMATION LOGIC
(function () {
  let container = document.getElementById('star-container');
  container.innerHTML = '';

  const count = 300;
  const stars = [];

  for (let i = 0; i < count; i++) {
    const s = document.createElement('div');
    s.className = 'star';

    const x = Math.random() * 100;
    const y = Math.random() * 100;

    const isStatic = Math.random() < 0.3;
    const z = isStatic ? 0 : 0.2 + Math.random() * 0.6;
    const size = isStatic ? 1 + Math.random() : 1 + Math.random() * 2;

    s.style.left = x + '%';
    s.style.top = y + '%';
    s.style.width = size + 'px';
    s.style.height = size + 'px';

    s.style.setProperty('--duration', (2 + Math.random() * 4) + 's');
    s.style.animationDelay = (Math.random() * 5) + 's';

    container.appendChild(s);
    stars.push({ el: s, initialY: y, speed: z });
  }

  lenis.on('scroll', ({ scroll, velocity }) => {
    const stretch = Math.max(1, Math.min(1 + Math.abs(velocity) * 0.15, 4));

    stars.forEach(star => {
      if (star.speed === 0) {
        star.el.style.transform = 'scaleY(1)';
        return;
      }

      let pos = (star.initialY - (scroll * star.speed * 0.05)) % 100;
      if (pos < 0) pos += 100;

      star.el.style.top = pos + '%';
      star.el.style.transform = `scaleY(${stretch})`;
    });
  });
})();