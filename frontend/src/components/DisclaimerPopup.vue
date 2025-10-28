<template>
  <div class="popup-overlay">
    <div class="popup-container">
      <h2 class="popup-title">
        Welcome to <span class="highlight">Heart Disease Prediction App</span>
      </h2>
      <p class="popup-text">
        This application uses AI models to assess the risk of heart disease based on entered lifestyle habits. The result is only an estimate and not a medical diagnosis. 
      </p>
      <p class="popup-text">
        <span class="highlight">Disclaimer:</span> This application is for informational and educational purposes only.
          It is not a substitute for professional medical
                advice, diagnosis, or treatment. Always seek the advice of your
                doctor or other qualified health provider with any questions you
                may have regarding a medical treatment.
      </p>
      <p class="popup-text">
        <span class="highlight">Resources:</span> The AI model is trained based on a dataset from The USA which could have an impact on the results you recieve.
      </p>
      <p class="popup-text"> 
        No personal information is stored nor saved from your inputs or results. 
      </p>
      <div class="checkbox-container">
        <input
          type="checkbox"
          id="consent"
          v-model="checked"
        />
        <label for="consent">I have read and understood the above</label>
      </div>
      <button
        :disabled="!checked"
        class="confirm-button"
        @click="handleAccept"
      >
        I Understand
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DisclaimerPopup',
  data() {
    return {
      checked: false
    };
  },
  methods: {
    handleAccept() {
      if (this.checked) {
        this.$emit('accepted');
      }
    }
  }
};
</script>

<style scoped>
.popup-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.popup-container {
  background: white;
  padding: 30px 40px;
  border-radius: 10px;
  max-width: 700px;
  width: 90%;
  text-align: center;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
  font-family: sans-serif;
}

.popup-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
  background-color: transparent;
}

.popup-text {
  font-size: 1rem;
  margin: 0.5rem 0;
  color: #333;
  line-height: 1.4;
}

.highlight {
  color: #d32f2f;
  font-weight: bold;
}

.checkbox-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin: 20px auto 10px;
  flex-wrap: wrap;
}

.checkbox-container input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #d32f2f;
  cursor: pointer;
}

.checkbox-container label {
  font-size: 0.95rem;
  line-height: 1.3;
  cursor: pointer;
  color: #111;
}

.confirm-button {
  margin-top: 10px;
  padding: 10px 24px;
  background-color: #d32f2f;
  color: white;
  border: none;
  border-radius: 5px;
  font-weight: bold;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.confirm-button:hover:not(:disabled) {
  background-color: #b71c1c;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(211, 47, 47, 0.3);
}

.confirm-button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
  transform: none;
}
</style>