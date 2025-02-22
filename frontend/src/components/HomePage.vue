
<template>
  <div id="app">
    <div class="container">
      <!-- Sidebar for Input Fields -->
      <div class="sidebar">
        <h2>Enter Measurements</h2>
        <div class="scrollable-content">
          <form @submit.prevent="computeRisk">
            
            <input v-model.number="formData.Weight" type="number" placeholder="Weight (kg)*" @input="calculateBMI" required />
            <input v-model.number="formData.Height" type="number" placeholder="Height (cm)*" @input="calculateBMI" required />
            <input v-model="formData.BMI" type="number" placeholder="BMI* (auto-calculated)" readonly required />

            <input v-model="formData.Alcohol" placeholder="Alcohol drinking per week" required />
            <input v-model="formData.Sleep" type="number" placeholder="Sleep (hours per day)*" required />
            <input v-model="formData.Exercise" type="number" placeholder="Exercise (minutes per week)*" required />
            <input v-model="formData.Fruit" placeholder="Fruit intake (servings per day)*" required />

          <!-- Gender Dropdown -->
          <label>Gender*</label>
          <select v-model="formData.Gender" required>
            <option disabled value="">Select Gender</option>
            <option>Male</option>
            <option>Female</option>
          </select>

           
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

           
            <label>Smoking*</label>
            <select v-model="formData.Smoking" required>
              <option disabled value="">Select Smoking Status</option>
              <option>Not at all</option>
              <option>Sometimes</option>
              <option>Everyday</option>
            </select>

            
            <h3>Check any that apply:</h3>
            <div class="checkbox-group">
              <label><input type="checkbox" v-model="formData.Diabetes" /> Diabetes</label>
              <label><input type="checkbox" v-model="formData.Kidney" /> Kidney Disease</label>
              <label><input type="checkbox" v-model="formData.Stroke" /> Stroke</label>
            </div>

            <button type="submit">Analyze</button>
          </form>
        </div>
      </div>

     
      <div class="results">
        <h2>Prediction Results</h2>
        <div class="scrollable-content">
          <div v-if="result">
            <div class="results-container">
             <div v-for="(value, key) in formattedResults" :key="key" class="result-card">
                <div class="icon-up">
                  <span v-if="value.percentage >= 0">👎</span>
                  <span v-else>👍</span>
                </div>

                <div class="result-content">
                  <strong>{{ key }}</strong>: {{ value.text }}
                  <div :class="value.percentage >= 0 ? 'negative' : 'positive'">
                  {{ value.percentage.toFixed(2) }}%
                </div>
              </div>

                
            </div>
         </div>

         <div class="results-container">
            <h3>Feature Impact</h3>
            <table class="impact-table">
              <thead>
                <tr>
                  <th>Feature</th>
                  <th>Value</th>
                  <th>Impact (%)</th>
                  <th>Color</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(value, key) in formattedResults" :key="key">
                  <td><strong>{{ key }}</strong></td>
                  <td>{{ value.text }}</td>
                  <td>{{ value.percentage.toFixed(2) }}%</td>
                  
                  <td :style="{ color: value.forceRed ? 'red' : (value.percentage < 0 ? 'green' : 'red'), fontWeight: 'bold' }">
                  {{ value.icon }} {{ value.forceRed || value.percentage >= 0 ? 'Red' : 'Green' }}
                </td>
                </tr>
              </tbody>
            </table>
          </div>



            <!-- SHAP Feature Importance Plot -->
            <div v-if="isValidBase64(result.shap_plot)">
            <h3>SHAP Feature Importance</h3>
            <img :src="'data:image/png;base64,' + result.shap_plot" alt="SHAP Plot" />
            </div>

            <div class="p-6">
              <canvas ref="barChart" style="height: 400px;"></canvas>
            </div>

            <div class="chart-container">
              <div v-if="isValidBase64(result.svm_pie_chart)">
                <h3>SVM Prediction</h3>
                <img :src="'data:image/png;base64,' + result.svm_pie_chart" alt="SVM Pie Chart" />
              </div>
              <!-- XGBoost Pie Chart -->
              <div v-if="isValidBase64(result.xgb_pie_chart)">
                <h3>XGBoost Prediction</h3>
                <img :src="'data:image/png;base64,' + result.xgb_pie_chart" alt="XGBoost Pie Chart" />
              </div>
              <!-- Keras Pie Chart -->
              <div v-if="isValidBase64(result.keras_pie_chart)">
                <h3>Keras Prediction</h3>
                <img :src="'data:image/png;base64,' + result.keras_pie_chart" alt="Keras Pie Chart" />
              </div>
            </div>
            
            
            <!--
            <div class="summary">
              <h3>Risk Summary</h3>
              <p>{{ riskSummary }}</p>
            </div>
          -->
            <!-- Risk Prediction Summary Section -->
            <div class="risk-summary">
              <h3>🩺 Risk Prediction Summary</h3>
              <h4>🔍 SHAP Feature Importance</h4>
              <ul>
                <li><strong>Major Contributors:</strong> Sleep duration, Kidney Disease, Fruit Intake</li>
                <li><strong>Other Factors:</strong> Alcohol consumption, Smoking, Exercise, Gender, Diabetes, Stroke, BMI, Age</li>
              </ul>

              <h4>📊 Model Predictions Comparison</h4>
              <div>
                <strong>SVM Model:</strong>
                <p>High Risk: {{ (result.svm_prediction * 100).toFixed(2) }}%</p>
                <p>No Risk: {{ (1 - result.svm_prediction) * 100 }}%</p>
                <p>🛑 Most conservative model, predicting the lowest risk percentage.</p>
              </div>
              <div>
                <strong>XGBoost Model:</strong>
                <p>High Risk: {{ (result.xgb_prediction * 100).toFixed(2) }}%</p>
                <p>No Risk: {{ (1 - result.xgb_prediction) * 100 }}%</p>
                <p>🚨 Most aggressive in identifying high-risk individuals.</p>
              </div>
              <div>
                <strong>Keras Model:</strong>
                <p>High Risk: {{ (result.keras_prediction * 100).toFixed(2) }}%</p>
                <p>No Risk: {{ (1 - result.keras_prediction) * 100 }}%</p>
                <p>⚖️ Balanced approach between sensitivity and specificity.</p>
              </div>
            </div>


          </div>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
import axios from 'axios';
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);
export default {
  name: 'App',
  data() {
    return {
      formData: {
        Gender: '',
        AgeCategory: '',
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
      chart: null,
      riskSummary: ''
    };
  },
  computed: {
    formattedResults() {
      if (!this.result || !this.result.shap_impact) {
      console.log("No results found in computed property");
      return {};
    }
    console.log("SHAP Impact Data:", this.result.shap_impact);
      return {
        "Weight (kg)": { text: this.formData.Weight, percentage: this.result.shap_impact?.Weight ?? 0,icon: (this.result.shap_impact?.Weight ?? 0) < 0 ? "👍" : "👎" },
        "Height (cm)": { text: this.formData.Height, percentage: this.result.shap_impact?.Height ?? 0,icon: (this.result.shap_impact?.Height ?? 0) < 0 ? "👍" : "👎" },
        "BMI": { text: this.formData.BMI, percentage: this.result.shap_impact?.BMI ?? 0,icon: (this.result.shap_impact?.BMI ?? 0) < 0 ? "👍" : "👎" },
        "Alcohol (drinks/week)": { text: this.formData.Alcohol, percentage: this.result.shap_impact?.Alcohol ?? 0,icon: (this.result.shap_impact?.Alcohol ?? 0) < 0 ? "👍" : "👎"},
        "Sleep (hours/day)": { text: this.formData.Sleep, percentage: this.result.shap_impact?.Sleep ?? 0,icon: (this.result.shap_impact?.Sleep ?? 0) < 0 ? "👍" : "👎" },
        "Exercise (min/week)": { text: this.formData.Exercise, percentage: this.result.shap_impact?.Exercise ?? 0,icon: (this.result.shap_impact?.Exercise ?? 0) < 0 ? "👍" : "👎" },
        "Fruit Intake (servings/day)": { text: this.formData.Fruit, percentage: this.result.shap_impact?.Fruit ?? 0,icon: (this.result.shap_impact?.Fruit ?? 0) < 0 ? "👍" : "👎" },
        "Gender": { text: this.formData.Gender, percentage: this.result.shap_impact?.Gender ?? 0, icon: (this.result.shap_impact?.Gender?? 0) < 0 ? "👍" : "👎" },
        "Age Category": { text: this.formData.AgeCategory, percentage: this.result.shap_impact?.Age ?? 0,icon: this.result.shap_impact.Age < 0 ? "👍" : "👎" },
        "Smoking": { text: this.formData.Smoking, percentage: this.result.shap_impact?.Smoking?? 0,icon: (this.result.shap_impact?.Smoking ?? 0) < 0 ? "👍" : "👎" },
        "Diabetes": { text: this.formData.Diabetes ? "Yes" : "No", percentage: this.result.shap_impact?.Diabetes ?? 0,icon: (this.result.shap_impact?.Diabetes ?? 0) < 0 ? "👍" : "👎" },
        "Kidney Disease": { text: this.formData.Kidney ? "Yes" : "No", percentage: this.result.shap_impact?.Kidney ?? 0 ,icon: (this.result.shap_impact?.Kidney ?? 0) < 0 ? "👍" : "👎"},
        "Stroke": { text: this.formData.Stroke ? "Yes" : "No", percentage: this.result.shap_impact?.Stroke ?? 0 ,icon: (this.result.shap_impact?.Stroke ?? 0) < 0 ? "👍" : "👎",forcedRed:true}
      };
    }
    
  },
  methods: {
    calculateBMI() {
      if (this.formData.Weight && this.formData.Height) {
        const heightInMeters = this.formData.Height / 100;
        this.formData.BMI = (this.formData.Weight / (heightInMeters ** 2)).toFixed(2);
      }
    },
    async computeRisk() {
      const ageMapping = {
        '18-24': 21, '25-29': 27, '30-34': 32, '35-39': 37,
        '40-44': 42, '45-49': 47, '50-54': 52, '55-59': 57,
        '60-64': 62, '65-69': 67, '70-74': 72, '75-79': 77
      };

      this.formData.Age = ageMapping[this.formData.AgeCategory];
      // Prepare the data object to be sent to the backend
      const apiData = {
        Weight: this.formData.Weight,
        Height: this.formData.Height,
        BMI: this.formData.BMI,
        Alcohol: this.formData.Alcohol,
        Sleep: this.formData.Sleep,
        Exercise: this.formData.Exercise,
        Fruit: this.formData.Fruit,
        Gender: this.formData.Gender,
        Age: this.formData.Age,
        Smoking: this.formData.Smoking,
        Diabetes: this.formData.Diabetes,
        Kidney: this.formData.Kidney,
        Stroke: this.formData.Stroke
      };

      try {
        const response = await axios.post('http://localhost:5000/predict', apiData);
        this.result = response.data;
        this.riskSummary = this.generateRiskSummary(response.data);
        console.log(this.formattedResults);
        // Debugging - Check if SHAP data is coming correctly
        console.log("SHAP Impact:", response.data.shap_impact);
        console.log("API Response:", response.data); // Debugging
    
      } catch (error) {
        console.error("There was an error making the API request:", error);
      }
    },
    generateRiskSummary(data) {
      return `
        SVM model: ${ (data.svm_prediction * 100).toFixed(2) }% risk.
        XGBoost model: ${ (data.xgb_prediction * 100).toFixed(2) }% risk.
        Keras model: ${ (data.keras_prediction * 100).toFixed(2) }% risk.
      `;
    },
    isValidBase64(base64) {
      // Ensure the base64 string starts with 'data:image/png;base64,'
      return typeof base64 === 'string' && base64.startsWith('iVBORw0KGgo') || base64.length > 0;
    },
    // Helper function to determine if the result is positive
    isPositiveResult(key, value) {
      switch(key) {
        case 'BMI':
          return value >= 18 && value <= 24;
        case 'Alcohol (drinks/day)':
          return value > 2;
        case 'Sleep (hours/day)':
          return value >= 6 && value <= 9;
        case 'Smoking':
          return value === 'No';
        case 'Diabetes':
          return value === 'No';
        case 'Kidney Disease':
          return value === 'No';
        case 'Stroke':
          return value === 'No';
        case 'Exercise (min/week)':
          return value >= 60 && value <= 120;
        default:
          return false;
      }
    },

    // Modify renderChart function to use positive result logic
    renderChart() {
      if (this.chart) {
        this.chart.destroy(); // Destroy previous instance before re-rendering
      }

      const chartElement = this.$refs.barChart;
      if (chartElement) {
        const ctx = chartElement.getContext("2d");

        const labels = Object.keys(this.formattedResults);
        const values = Object.values(this.formattedResults).map(item => item.percentage);
        // Check values before rendering
    console.log("Labels:", labels);
    console.log("Values:", values);

    if (labels.length === 0 || values.length === 0) {
      console.error("No data to render on the chart");
      return;
    }

        const colors = values.map((val, index) => {
          // Check if the result is positive based on the key and value
          const label = labels[index];
          const value = this.formattedResults[label].text;
          return this.isPositiveResult(label, value) ? "rgba(75, 192, 75, 0.7)" : "rgba(255, 99, 132, 0.7)"; // Green for positive, Red for negative
        });

        this.chart = new Chart(ctx, {
          type: "bar",
          data: {
            labels: labels,
            datasets: [
              {
                label: "Impact Percentage",
                data: values,
                backgroundColor: values.map((val) => (val >= 0 ? "rgba(255, 99, 132, 0.7)" : "rgba(75, 192, 75, 0.7)")),
                borderColor: colors.map(c => c.replace("0.7", "1")),
                borderWidth: 1
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,
                ticks: {
                  callback: function (value) {
                    return value + "%";
                  }
                }
              }
            }
          }
        });
      } else {
        console.error("Canvas element is not available.");
      }
    }
  },
  watch: {
    formattedResults: {
      handler() {
        this.$nextTick(() => {
         this.renderChart();
        
        });
      },
      deep: true
    }
  },
  mounted() {
    this.$nextTick(() => {
      console.log('Mounted hook called');
    if (this.$refs.barChart) {
      console.log('Canvas element found:', this.$refs.barChart);
      this.renderChart();
    } else {
      console.error('Canvas element is not available');
    }
    });
  }
};
</script>


<style scoped>

/* Full Page Background */
body, #app {
  background-color: #c53030; /* Red background */
  height: 100vh;
  margin: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}
/* Container with Sidebar and Results */
/* Layout Styles */
.container {
  display: flex;
  height: 95vh;
  width: 100%;
  /*max-width: 1400px;*/
  gap:20px;
  
  
}

/* Sidebar (White Background) */
.sidebar {
  width: 30%;
  background-color: #ffffff; /* White */
  color: red;
  padding: 20px;
  overflow-y: auto;
  height: 92vh;
  border-radius: 16px;
  border-color: red;

  margin-left: 20px;
  margin-top:20px;
  
  
}
/* Results Section (White Background) */
.results {
  flex-grow: 1;
  padding: 20px;
  background-color: #ffffff; /* White */
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  height: 92vh;
  margin-right: 20px;
  margin-top:20px;
  
}


/* Form Styling */
form input, form select, form button {
  display: flex;
  flex-direction: column;
  margin: 10px auto;
  padding: 8px;
  width: 90%;  
  border-radius: 16px;
  border-color: #a02121;
  justify-content: space-between;
  
  /*flex: 2; 
  padding: 8px;
  width: 40%;
  border-radius: 16px;
  border: 2px solid #a02121;*/
}

form label {
  display: block;
  margin: 5px 0;
  
}

button[type="submit"] {
  background-color: #c53030; 
  color: white;
  border: none;
  padding: 10px;
  width: 50%;
  border-radius: 16px;
  cursor: pointer;
}

button[type="submit"]:hover {
  background-color: #a02121;
}

/* Pie Chart Display */
.chart-container {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
}

.chart-container div {
  text-align: center;
  margin: 10px;
}

img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
}

/* Summary Section */
.summary {
  margin-top: 20px;
  padding: 10px;
  background: #e9f7ef;
  border-left: 5px solid #2ecc71;
}
.checkbox-group {
  display: flex;
  gap: 15px;
  flex-wrap: wrap; 
  
}

.checkbox-group label {
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.results-container {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  justify-content: center;
}

/* Results Cards */
.result-card {
  border: 2px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  text-align: center;
  width: 160px;
  background: #fff;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
}

.result-card .positive {
  color: green;
  font-weight: bold;
}

.result-card .negative {
  color: red;
  font-weight: bold;
}


.p-6 {
  width: 100%;
  max-width: 800px;
  height: 400px;
}
/* Layout Styles */
.container {
  display: flex;
  height: 100vh;
}



/* Scrollable Content */
.scrollable-content {
  max-height: 80vh;
  overflow-y: auto;
  padding-right: 10px;
}

/* Scrollbar Styling */
.scrollable-content::-webkit-scrollbar {
  width: 10px;
}
.scrollable-content::-webkit-scrollbar-track {
  background:whitesmoke;
}
.scrollable-content::-webkit-scrollbar-thumb {
  background: #c53030;
  border-radius: 10px;
}
.scrollable-content::-webkit-scrollbar-thumb:hover {
  background: #a02121;
}

/* Results Cards */
.result-card {
  background-color: white;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 10px;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
}

/* Positive & Negative Colors */
.negative {
  color: red;
}
.positive {
  color: green;
}

/* Button Styling */
button {
  background-color: white;
  color: #c53030;
  border: none;
  padding: 10px;
  width: 100%;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background-color: #f8d7da;
}
/*Table*/
.impact-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  overflow: hidden;
}

.impact-table th, 
.impact-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.impact-table thead {
  background-color: #007bff;
  color: white;
  text-transform: uppercase;
  font-weight: bold;
}

.impact-table tbody tr:hover {
  background-color: rgba(0, 123, 255, 0.1);
}

.impact-table td {
  font-size: 16px;
}

.impact-table td:nth-child(4) {
  font-weight: bold;
}
/* risk summary*/
.risk-summary {
  background-color: #e7f3fe; /* Light blue background for the summary */
  border: 1px solid #bcdff1; /* Slightly darker border for emphasis */
  border-radius: 5px; /* Rounded corners */
  padding: 20px; /* Padding inside the box */
  margin-top: 20px; /* Space above the summary */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
}

.risk-summary h3 {
  color: #0d6efd; /* Blue color for the heading */
  margin-bottom: 10px; /* Space below the heading */
}

.risk-summary p {
  font-size: 16px; /* Font size for the text */
  line-height: 1.5; /* Line height for better readability */
  color: #212529; /* Dark text color */
}

.risk-summary .highlight {
  font-weight: bold; /* Bold text for key phrases */
  color: #dc3545; /* Red color for high-risk warnings */
}

</style>
