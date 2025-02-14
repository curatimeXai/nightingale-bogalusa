<template>
  <div id="app">
    <nav>
      <button @click="activeTab = 'measurements'">Enter Measurements</button>
      <button @click="activeTab = 'goal'">Select Risk Percentage Goal</button>
      <button @click="activeTab = 'frozen'">Frozen Measures</button>
    </nav>

    <div v-if="activeTab === 'measurements'">
      <h2>Enter Measurements</h2>
      <form @submit.prevent="computeRisk">
        <!-- Gender Dropdown -->
        <label>Gender*</label>
        <select v-model="formData.Gender" required>
          <option disabled value="">Select Gender</option>
          <option>Male</option>
          <option>Female</option>
        </select>

        <!-- Age Category Dropdown -->
        <label>Age Category*</label>
        <select v-model="formData.AgeCategory" required>
          <option disabled value="">Select Age Range</option>
          <option>18-24</option>
          <option>25-29</option>
          <option>30-34</option>
          <option>35-39</option>
          <option>40-44</option>
          <option>45-49</option>
          <option>50-54</option>
          <option>55-59</option>
          <option>60-64</option>
          <option>65-69</option>
          <option>70-74</option>
          <option>75-79</option>
        </select>

        <!-- Weight and Height for BMI Calculation -->
        <input v-model.number="formData.Weight" type="number" placeholder="Weight (kg)*" @input="calculateBMI" required />
        <input v-model.number="formData.Height" type="number" placeholder="Height (cm)*" @input="calculateBMI" required />

        <!-- Automatically Calculated BMI -->
        <input v-model="formData.BMI" type="number" placeholder="BMI* (auto-calculated)" readonly required />

        <!-- Smoking Dropdown -->
        <label>Smoking*</label>
        <select v-model="formData.Smoking" required>
          <option disabled value="">Select Smoking Status</option>
          <option>Not at all</option>
          <option>Sometimes</option>
          <option>Everyday</option>
        </select>

        <input v-model="formData.Alcohol" placeholder="Alcohol drinking per day" required />
        <input v-model="formData.Sleep" type="number" placeholder="Sleep (hours per day)*" required />
        <input v-model="formData.Exercise" type="number" placeholder="Exercise (minutes per week)*" required />
        <input v-model="formData.Fruit" placeholder="Fruit intake (servings per day)*" required />

        <h3>Select the ones which apply to you:</h3>
        <label><input type="checkbox" v-model="formData.Diabetes" /> Do you have diabetes?</label>
        <label><input type="checkbox" v-model="formData.Kidney" /> Do you have a kidney disease?</label>
        <label><input type="checkbox" v-model="formData.Stroke" /> Have you had a stroke before?</label>

        <button type="submit">Compute Risk Percentage</button>
      </form>
    </div>

    <div v-if="activeTab === 'goal'">
      <h2>Select Risk Percentage Goal</h2>
      <!-- Add goal selection UI here -->
    </div>

    <div v-if="activeTab === 'frozen'">
      <h2>Frozen Measures</h2>
      <!-- Add frozen measures UI here -->
    </div>

    <div v-if="result">
      <h2>Prediction Results</h2>
      
      <!-- Display the pie charts -->
      <div>
        <h3>SVM Prediction</h3>
        <img :src="'data:image/png;base64,' + result.svm_pie_chart" alt="SVM Pie Chart"/>
      </div>
      
      <div>
        <h3>XGBoost Prediction</h3>
        <img :src="'data:image/png;base64,' + result.xgb_pie_chart" alt="XGBoost Pie Chart"/>
      </div>
      
      <div>
        <h3>Keras Prediction</h3>
        <img :src="'data:image/png;base64,' + result.keras_pie_chart" alt="Keras Pie Chart"/>
      </div>

      <!-- Display the risk summary -->
      <div>
        <h3>Risk Summary</h3>
        <p>{{ riskSummary }}</p>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'App',
  data() {
    return {
      activeTab: 'measurements',
      formData: {
        Gender: '',
        AgeCategory: '',  // Now using AgeCategory instead of Age
        Weight: '',
        Height: '',
        BMI: '',
        Smoking: '',
        Alcohol: '',
        Sleep: '',
        Exercise: '',
        Fruit: '',
        Diabetes: false,
        Kidney: false,
        Stroke: false
      },
      result: null,
      riskSummary: ''  // Add riskSummary property
    };
  },
  methods: {
    calculateBMI() {
      if (this.formData.Weight && this.formData.Height) {
        const heightInMeters = this.formData.Height / 100;
        this.formData.BMI = (this.formData.Weight / (heightInMeters ** 2)).toFixed(2);
      }
    },
    async computeRisk() {
      // Mapping the selected Age Category to the numeric value for backend
      const ageMapping = {
        '18-24': 21, '25-29': 27, '30-34': 32, '35-39': 37,
        '40-44': 42, '45-49': 47, '50-54': 52, '55-59': 57,
        '60-64': 62, '65-69': 67, '70-74': 72, '75-79': 77
      };
      
      // Ensure correct format for AgeCategory
      this.formData.Age = ageMapping[this.formData.AgeCategory];

      try {
        const response = await axios.post('http://localhost:5000/predict', this.formData);
        this.result = response.data;

        // Generate the risk summary based on model outputs
        this.riskSummary = this.generateRiskSummary(response.data);
      } catch (error) {
        console.error("There was an error making the API request:", error);
      }
    },
    generateRiskSummary(data) {
      let summary = 'Based on the model predictions, here is your heart disease risk: \n\n';

      // Assuming the predictions are probabilities between 0 and 1
      const svmRisk = (data.svm_prediction * 100).toFixed(2);
      const xgbRisk = (data.xgb_prediction * 100).toFixed(2);
      const kerasRisk = (data.keras_prediction * 100).toFixed(2);

      summary += `SVM model suggests you have a ${svmRisk}% risk of heart disease.\n`;
      summary += `XGBoost model suggests you have a ${xgbRisk}% risk of heart disease.\n`;
      summary += `Keras model suggests you have a ${kerasRisk}% risk of heart disease.`;

      return summary;
    }
  }
};
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin: 20px;
}
nav button {
  margin: 5px;
  padding: 10px;
  background-color: #f0f0f0;
  border: none;
  cursor: pointer;
}
nav button:hover {
  background-color: #a04747;
}
form input, form select, form button {
  display: block;
  margin: 10px auto;
  padding: 8px;
  width: 80%;
}
form label {
  display: block;
  margin: 5px 0;
}
button[type="submit"] {
  background-color: #444444;
  color: white;
  cursor: pointer;
}
button[type="submit"]:hover {
  background-color: #666666;
}
</style>
