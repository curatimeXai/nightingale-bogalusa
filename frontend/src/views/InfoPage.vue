<template>
  <div class="info-page">
    <div class="info-content">
      <h1>About the AI Model</h1>
      <p>
        This application uses AI models to assess the risk of heart disease based on entered lifestyle habits.
        The result is only an estimate and not a medical diagnosis. 
        <br><br>
        Always seek the advice of your doctor or other qualified 
        health provider with any questions you may have regarding a medical treatment.
        <br><br>
        The AI model is trained based on a dataset from
        The USA which could have an impact on the results you receive.
        <br><br>
        No personal information is stored from your inputs. 
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
  background-color: #f4f4f4; /* Choose any background color you prefer */
  padding: 20px;
}

.info-content {
  max-width: 800px; /* Adjust based on how wide you want your text block */
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: left; /* This will keep the text aligned to the left */
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