<template>
  <div v-if="show" class="disclaimer-overlay">
    <div class="disclaimer-box">
      <h2>Important information</h2>
      <p>
        This application uses AI models to assess the risk of heart disease based on entered lifestyle habits.
        The result is only an estimate and not a medical diagnosis. 
        <br><br>
        <strong>Always seek the advice of your doctor or other qualified 
        health provider with any questions you may have regarding a medical treatment.
        </strong> 
        <br><br>
        The AI model is trained based on a dataset from the website Kaggle called "Indicators of Heart Disease".
        The participants were all US residents,and uses your personal input only for making predictions — not for training.

        <br><br>
        No personal information is stored nor saved from your inputs or results.
      </p>

      <div class="form-check mt-3">
        <input
          type="checkbox"
          id="dontShowAgain"
          v-model="dontShowAgain"
        />
        <label for="dontShowAgain">Don't show again</label>
      </div>

      <button class="btn btn-primary" @click="acceptDisclaimer">I accept</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      show: true,
      dontShowAgain: false
    };
  },
  created() {
    const accepted = localStorage.getItem("disclaimerAccepted");
    if (accepted === "true") {
      this.show = false;
    }
  },
  methods: {
    acceptDisclaimer() {
    this.$emit("accepted", this.dontShowAgain);
    this.show = false;
    }
  }
};
</script>

<style scoped>
.disclaimer-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0,0,0,0.75);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.disclaimer-box {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  max-width: 600px;
  text-align: center;
}
</style>
