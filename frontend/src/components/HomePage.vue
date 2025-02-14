<template>
  <div id="app">
    <div class="container">
      <!-- Sidebar for Input Fields -->
      <div class="sidebar">
        <h2>Enter Measurements</h2>
        <form @submit.prevent="computeRisk">
          <!-- Weight and Height -->
          <input v-model.number="formData.Weight" type="number" placeholder="Weight (kg)*" @input="calculateBMI" required />
          <input v-model.number="formData.Height" type="number" placeholder="Height (cm)*" @input="calculateBMI" required />
          <input v-model="formData.BMI" type="number" placeholder="BMI* (auto-calculated)" readonly required />
          
          <input v-model="formData.Alcohol" placeholder="Alcohol drinking per day" required />
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

          
          <!-- Lifestyle Factors -->
          <label>Smoking*</label>
          <select v-model="formData.Smoking" required>
            <option disabled value="">Select Smoking Status</option>
            <option>Not at all</option>
            <option>Sometimes</option>
            <option>Everyday</option>
          </select>

          
          <!-- Health Conditions -->
          <h3>Check any that apply:</h3>
          <div class="checkbox-group">
            <label ><input type="checkbox" v-model="formData.Diabetes" /> Diabetes</label>
            <label><input type="checkbox" v-model="formData.Kidney" /> Kidney Disease</label>
            <label><input type="checkbox" v-model="formData.Stroke" /> Stroke</label>
          </div>

          <button type="submit">Analyze</button>
        </form>
      </div>

      <!-- Right Section for Results -->
      <div class="results">
        <h2>Prediction Results</h2>

        <div v-if="result">

          <div class="results-container">
            <div v-for="(value, key) in formattedResults" :key="key" class="result-card">
              <strong>{{ key }}</strong>: {{ value.text }}
                <div :class="value.percentage >= 0 ? 'negative' : 'positive'">
                {{ value.percentage }}%
                <span v-if="value.percentage >= 0">👎</span>
                <span v-else>👍</span>
                </div>
              </div>
            </div>

            <div class="p-6">
              <canvas  ref="barChart" style="height: 400px;"></canvas>
            </div>

          <div class="chart-container">
            <div>
              <h3>SVM Prediction</h3>
              <img :src="'data:image/png;base64,' + result.svm_pie_chart" alt="SVM Pie Chart" />
            </div>
            <div>
              <h3>XGBoost Prediction</h3>
              <img :src="'data:image/png;base64,' + result.xgb_pie_chart" alt="XGBoost Pie Chart" />
            </div>
            <div>
              <h3>Keras Prediction</h3>
              <img :src="'data:image/png;base64,' + result.keras_pie_chart" alt="Keras Pie Chart" />
            </div>
          </div>

          <!-- Display the risk summary -->
          <div class="summary">
            <h3>Risk Summary</h3>
            <p>{{ riskSummary }}</p>
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
      return {
        "Weight (kg)": { text: this.formData.Weight, percentage: this.result?.weightImpact || 0 },
        "Height (cm)": { text: this.formData.Height, percentage: this.result?.heightImpact || 0 },
        "BMI": { text: this.formData.BMI, percentage: this.result?.bmiImpact || 0 },
        "Alcohol (drinks/day)": { text: this.formData.Alcohol, percentage: this.result?.alcoholImpact || 0 },
        "Sleep (hours/day)": { text: this.formData.Sleep, percentage: this.result?.sleepImpact || 0 },
        "Exercise (min/week)": { text: this.formData.Exercise, percentage: this.result?.exerciseImpact || 0 },
        "Fruit Intake (servings/day)": { text: this.formData.Fruit, percentage: this.result?.fruitImpact || 0 },
        "Gender": { text: this.formData.Gender, percentage: this.result?.genderImpact || 0 },
        "Age Category": { text: this.formData.AgeCategory, percentage: this.result?.ageImpact || 0 },
        "Smoking": { text: this.formData.Smoking, percentage: this.result?.smokingImpact || 0 },
        "Diabetes": { text: this.formData.Diabetes ? "Yes" : "No", percentage: this.result?.diabetesImpact || 0 },
        "Kidney Disease": { text: this.formData.Kidney ? "Yes" : "No", percentage: this.result?.kidneyImpact || 0 },
        "Stroke": { text: this.formData.Stroke ? "Yes" : "No", percentage: this.result?.strokeImpact || 0 }
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

      try {
        const response = await axios.post('http://localhost:5000/predict', this.formData);
        this.result = response.data;
        this.riskSummary = this.generateRiskSummary(response.data);
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
                backgroundColor: colors,
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
/* Container with Sidebar and Results */
.container {
  display: flex;
  justify-content: space-between;
  padding: 20px;
}

/* Sidebar */
.sidebar {
  width: 30%;
  padding: 20px;
  background-color: #80d849;
  border-radius: 16px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);  
}

/* Results Section */
.results {
  width: 55%;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

/* Form Styling */
form input, form select, form button {
  display: block;
  margin: 10px auto;
  padding: 8px;
  width: 90%;
}

form label {
  display: block;
  margin: 5px 0;
}

button[type="submit"] {
  background-color: #444444;
  color: white;
  cursor: pointer;
  width: 100%;
}

button[type="submit"]:hover {
  background-color: #666666;
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
  flex-wrap: wrap; /* Wrap to the next line if space is limited */
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

.result-card {
  border: 2px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  text-align: center;
  width: 160px;
  background: #fff;
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
</style>
