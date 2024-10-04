// Toggle between light and dark theme
const themeToggle = document.getElementById('theme-toggle');
const body = document.body;

themeToggle.addEventListener('click', () => {
  if (body.classList.contains('light')) {
    body.classList.replace('light', 'dark');
    themeToggle.textContent = '🌙';
  } else {
    body.classList.replace('dark', 'light');
    themeToggle.textContent = '☀️';
  }
});

// Handle prediction
document.getElementById('predictBtn').addEventListener('click', async () => {
  const age = document.getElementById('age').value;
  const gender = document.getElementById('gender').value;
  const screenTime = document.getElementById('screenTime').value;
  const familyHistory = document.getElementById('familyHistory').value;
  const outdoorTime = document.getElementById('outdoorTime').value;

  const data = {
    age: Number(age),
    gender,
    screenTime: Number(screenTime),
    familyHistory: Number(familyHistory),
    outdoorTime: Number(outdoorTime),
  };

  try {
    const response = await fetch('/api/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    const result = await response.json();
    document.getElementById('predictionResult').textContent = `Prediction: ${result.prediction}`;
  } catch (error) {
    console.error('Error:', error);
    document.getElementById('predictionResult').textContent = 'Prediction failed.';
  }
});
