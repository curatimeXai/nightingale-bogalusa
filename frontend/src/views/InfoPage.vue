<template>
  <div class="info-page">
    <div class="info-content">
      <h1>About the Service</h1>
      <p>
        This application uses AI models to assess the risk of heart disease based on entered lifestyle habits and personal information such as BMI.
        The result is only an estimate and not a medical diagnosis. 
        <br><br>
        <strong>
          Always seek the advice of your doctor or other qualified 
          health provider with any questions you may have regarding a medical treatment.
        </strong>
        <br><br>
      </p>
      <h1>Use of AI and personal information</h1>
      <p>
        The AI model is trained based on a dataset from the website Kaggle called "Indicators of Heart Disease".
        The participants were all US residents,and uses your personal input only for making predictions — not for training.
        
        <br><br>
        No personal information is stored nor saved from your inputs or results. 
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "InfoPage",
};
</script>

<style scoped>
.info-page {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f4f4f4;
  padding: 20px;
}

.info-content {
  max-width: 800px;
  padding: 20px;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: left;
}

h1 {
  text-align: center;
  font-size: 1.5rem;
  margin-bottom: 20px;
}

p {
  line-height: 1.6;
  font-size: 1rem;
}
</style>