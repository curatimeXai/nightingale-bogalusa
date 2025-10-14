<template>
  <Disclaimer />
  <div id="app">
    <div class="container">
      <!-- Sidebar -->
      <div class="sidebar">
        <h2>Enter Your Health & Lifestyle Information</h2>
        <div class="scrollable-content">
          <form @submit.prevent="computeRisk">
            <!-- Weight -->
            <div class="input">
              <p>Enter your weight
                <span class="tooltip-wrapper">
                  <span class="tooltip-icon">?</span>
                  <span class="tooltip-text">Your weight in kilograms (30–400)</span>
                </span>
              </p>
              <input v-model.number="formData.Weight" type="number" placeholder="Weight (30 - 400kg)*" 
                     @input="calculateBMI" min="30" max="400" required />
            </div>
            <!-- Height -->
            <div class="input">
              <p>Enter your height
                <span class="tooltip-wrapper">
                  <span class="tooltip-icon">?</span>
                  <span class="tooltip-text">Your height in centimeters (90–240)</span>
                </span>
              </p>
              <input v-model.number="formData.Height" type="number" placeholder="Height (90 - 240cm)*" 
                     @input="calculateBMI" min="90" max="240" required />
            </div>
            <!-- BMI -->
            <div class="bmi">
              <p>Calculated BMI</p>
              <input v-model="formData.BMI" type="number" placeholder="BMI" readonly required />
            </div>
            <!-- Alcohol -->
            <div class="input">
              <p>Alcohol per week</p>
              <input v-model="formData.Alcohol" type="number" placeholder="Alcohol (0-70)*" min="0" max="70" required />
            </div>
            <!-- Sleep -->
            <div class="input">
              <p>Sleep (hours/day)</p>
              <input v-model="formData.Sleep" type="number" placeholder="Sleep (0-24)*" min="0" max="24" required />
            </div>
            <!-- Exercise -->
            <div class="input">
              <p>Exercise (minutes/week)</p>
              <input v-model="formData.Exercise" type="number" placeholder="Exercise (0-3000)*" min="0" max="3000" required />
            </div>
            <!-- Fruit -->
            <div class="input">
              <p>Fruit per day</p>
              <input v-model="formData.Fruit" type="number" placeholder="Fruit (0-20)*" min="0" max="20" required />
            </div>

            <!-- Gender -->
            <label>Gender *</label>
            <select v-model="formData.Gender" required>
              <option disabled value="">Select Gender</option>
              <option>Male</option>
              <option>Female</option>
            </select>

            <!-- Age -->
            <label>Age Category *</label>
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

            <!-- Smoking -->
            <label>Smoking *</label>
            <select v-model="formData.Smoking" required>
              <option disabled value="">Select Smoking Status</option>
              <option>Not at all</option>
              <option>Sometimes</option>
              <option>Every day</option>
            </select>

            <!-- Conditions -->
            <h3>Check any that apply:</h3>
            <div class="checkbox-group">
              <label>Diabetes<input type="checkbox" v-model="formData.Diabetes" /></label>
              <label>Kidney Disease<input type="checkbox" v-model="formData.Kidney" /></label>
              <label>Stroke<input type="checkbox" v-model="formData.Stroke" /></label>
            </div>

            <button type="submit">Analyze</button>
            <button type="button" @click="randomizeData">🔀 Randomize</button>
          </form>
        </div>
      </div>

      <!-- Results -->
      <div class="results">
        <h2>Heart Disease Risk Prediction Results</h2>
        <p>Based on your health data, here's how your lifestyle factors contribute to your risk</p>

        <div v-if="result">
          <div class="results-layout">
            <!-- Negative -->
            <div class="negative-factors">
              <h3>🛑 Negative Factor</h3>
              <div class="factors-column">
                <div v-for="(value, key) in negativeFactors" :key="key" class="result-card card-negative">
                  <i class="bi bi-hand-thumbs-down-fill negative-icon"></i>
                  <div class="result-content">
                    <strong>{{ key }}</strong>: {{ value.text }}
                    <div class="negative">{{ Math.abs(value.percentage).toFixed(2) }}%</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Positive -->
            <div class="positive-factors">
              <h3>✅ Favorable Factor</h3>
              <div class="factors-column">
                <div v-for="(value, key) in positiveFactors" :key="key" class="result-card card-positive">
                  <i class="bi bi-hand-thumbs-up-fill positive-icon"></i>
                  <div class="result-content">
                    <strong>{{ key }}</strong>: {{ value.text }}
                    <div class="positive">{{ Math.abs(value.percentage).toFixed(2) }}%</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Risk Score Section -->
          <div class="risk-score-section" v-if="result && result.risk_assessment">
            <div class="risk-level-badge" :class="result.risk_assessment.level.toLowerCase()">
              <h3>{{ result.risk_assessment.level }}</h3>
              <div class="risk-score-value">
                Risk Score: {{ (result.risk_assessment.score * 100).toFixed(1) }}%
              </div>
              <p>{{ result.risk_assessment.description }}</p>
            </div>
          </div>

          <!-- Tab Navigation -->
          <div class="tab-navigation">
            <button 
              :class="{ active: activeTab === 'table' }" 
              @click="activeTab = 'table'">
              📊 Table View
            </button>
            <button 
              :class="{ active: activeTab === 'chart' }" 
              @click="activeTab = 'chart'">
              📈 Impact Chart
            </button>
          </div>

          <!-- Table -->
          <div v-show="activeTab === 'table'" class="results-container">
            <h3>Explaining Heart Disease Predictions Through Feature Importance</h3>
            <table class="impact-table">
              <thead>
                <tr>
                  <th>Factor</th>
                  <th>Currently</th>
                  <th>Recommendation WHO</th>
                  <th>Risk level</th>
                  <th>State</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(value, key) in formattedResults" :key="key">
                  <td><strong>{{ key }}</strong></td>
                  <td>{{ value.text }}</td>
                  <td>{{ getGuideline(key) }}</td>
                  <td :class="getRiskClass(value.impact)">{{ value.impact }}</td>
                  <td :style="{
                    color: value.forceRed ? '#dc3545' : '#28a745',
                    fontWeight: 'bold'
                  }">
                    {{ value.icon }} 
                    {{ value.forceRed ? 'unwell' : 'good health' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- SHAP Chart -->
          <div v-show="activeTab === 'chart'" v-if="isValidBase64(result.shap_plot) || shap_summary_text" class="shap-section">
            <h3>What Affected Your Results Most</h3>

            <div v-if="isValidBase64(result.shap_plot)">
              <img :src="'data:image/png;base64,' + result.shap_plot" alt="SHAP Impact Chart" />
            </div>

            <!-- Info Box -->
            <div class="info-box">
              <h5>📊 How This Chart Works</h5>
              <p>This chart shows which health factors had the biggest effect on your heart disease risk.</p>
              <ul>
                <li><strong>Green bars</strong> = lower your risk</li>
                <li><strong style="color:#dc3545;">Red bars</strong> = increase your risk</li>
                <li>The longer the bar, the more important the effect</li>
              </ul>
              <p>
                Even if you don't have a condition like stroke or kidney disease, it may still appear. 
                That's because your good health (not having it) helped lower your risk — and the model shows that.
              </p>
            </div>

            <div v-if="shap_summary_text">
              <h4>Main Risk Factors Identified</h4>
              <p>{{ shap_summary_text }}</p>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'App',
  data() {
    return {
      activeTab: 'table',
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
      shap_summary_text: '',
      whoGuidelines: {
        BMI: "18.5 – 24.9 kg/m² is healthy.",
        Alcohol: "≤2 drinks/day men, ≤1 women.",
        Sleep: "7–9 hours per night.",
        Exercise: "At least 150 min/week.",
        Fruit: "≥5 servings per day.",
        Smoking:"No safe level of smoking.",
        Diabetes:"Healthy diet and activity prevent type 2 diabetes.",
        Kidney:"Control blood pressure/sugar to protect kidneys.",
        Stroke:"Control BP, cholesterol, avoid smoking."
      }
    };
  },
  computed: {
    formattedResults() {
      if (!this.result || !this.result.shap_impact) return {};
      const shap = this.result.shap_impact;

      const build = (label, value, shapVal, icon, forceRed) => {
        return {
          text: value,
          percentage: shapVal ?? 0,
          icon,
          forceRed,
          impact: this.getRiskLevel(Math.abs(shapVal ?? 0), shapVal ?? 0)
        };
      };

      return {
        "BMI (normal between 18.5 - 24.9)": build(
          "BMI",
          this.formData.BMI,
          shap.BMI,
          this.formData.BMI >= 18.5 && this.formData.BMI <= 24.9 ? "👍" : "👎",
          this.formData.BMI >= 25 || this.formData.BMI < 18.5
        ),

        "Alcohol (drinks/week)": build(
          "Alcohol",
          this.formData.Alcohol,
          shap.Alcohol,
          this.formData.Alcohol <= 3 ? "👍" : "👎",
          this.formData.Alcohol > 4
        ),

        "Sleep (hours/day)": build(
          "Sleep",
          this.formData.Sleep,
          shap.Sleep,
          (this.formData.Sleep >= 6 && this.formData.Sleep <= 10) ? "👍" : "👎",
          !(this.formData.Sleep >= 6 && this.formData.Sleep <= 10)
        ),

        "Exercise (min/week)": build(
          "Exercise",
          this.formData.Exercise,
          shap.Exercise,
          this.formData.Exercise > 150 ? "👍" : "👎",
          this.formData.Exercise <= 150
        ),

        "Fruit Intake (servings/day)": build(
          "Fruit",
          this.formData.Fruit,
          shap.Fruit,
          this.formData.Fruit >= 5 ? "👍" : "👎",
          this.formData.Fruit < 5
        ),

        "Smoking": build(
          "Smoking",
          this.formData.Smoking,
          shap.Smoking,
          this.formData.Smoking === 'Not at all' ? "👍" : "👎",
          this.formData.Smoking === 'Every day' || this.formData.Smoking === 'Sometimes'
        ),

        "Diabetes": build(
          "Diabetes",
          this.formData.Diabetes ? "Yes" : "No",
          shap.Diabetes,
          this.formData.Diabetes ? "👎" : "👍",
          this.formData.Diabetes
        ),

        "Kidney Disease": build(
          "Kidney",
          this.formData.Kidney ? "Yes" : "No",
          shap.Kidney,
          this.formData.Kidney ? "👎" : "👍",
          this.formData.Kidney
        ),

        "Stroke": build(
          "Stroke",
          this.formData.Stroke ? "Yes" : "No",
          shap.Stroke,
          this.formData.Stroke ? "👎" : "👍",
          this.formData.Stroke
        )
      };
    },

    negativeFactors() {
      const f = {};
      Object.keys(this.formattedResults).forEach(k => {
        if (this.formattedResults[k].forceRed) f[k] = this.formattedResults[k];
      });
      return f;
    },
    positiveFactors() {
      const f = {};
      Object.keys(this.formattedResults).forEach(k => {
        if (!this.formattedResults[k].forceRed) f[k] = this.formattedResults[k];
      });
      return f;
    }
  },
  methods: {
    getGuideline(key) {
      const map = {
        "BMI (normal between 18.5 - 24.9)": "BMI",
        "Alcohol (drinks/week)": "Alcohol",
        "Sleep (hours/day)": "Sleep",
        "Exercise (min/week)": "Exercise",
        "Fruit Intake (servings/day)": "Fruit",
        "Smoking": "Smoking",
        "Diabetes": "Diabetes",
        "Kidney Disease": "Kidney",
        "Stroke": "Stroke"
      };
      return this.whoGuidelines[map[key]] || "—";
    },
    getRiskLevel(value, shapVal) {
      if (shapVal <= 0) return "risk-level-low";
      if (value >= 5) return "risk-level-high";
      if (value >= 2) return "risk-level-medium";
      return "risk-level-low";
    },

    getRiskClass(impact) {
      return impact;
    },
    calculateBMI() {
      if (this.formData.Weight && this.formData.Height) {
        const h = this.formData.Height / 100;
        this.formData.BMI = (this.formData.Weight / (h * h)).toFixed(2);
      }
    },
    randomizeData() {
      const r = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
      const c = (arr) => arr[Math.floor(Math.random() * arr.length)];
      this.formData.Weight = r(30, 220);
      this.formData.Height = r(90, 240);
      this.calculateBMI();
      this.formData.Alcohol = r(0, 35);
      this.formData.Sleep = r(0, 24);
      this.formData.Exercise = r(0, 300);
      this.formData.Fruit = r(0, 5);
      this.formData.Gender = c(["Male", "Female"]);
      this.formData.AgeCategory = c(["18-24","25-29","30-34","35-39","40-44","45-49","50-54","55-59","60-64","65-69","70-74","75-79"]);
      this.formData.Smoking = c(["Not at all", "Sometimes", "Every day"]);
      this.formData.Diabetes = Math.random() < 0.2;
      this.formData.Kidney = Math.random() < 0.1;
      this.formData.Stroke = Math.random() < 0.05;
    },
    async computeRisk() {
      const ageMapping = {
        '18-24': 21, '25-29': 27, '30-34': 32, '35-39': 37,
        '40-44': 42, '45-49': 47, '50-54': 52, '55-59': 57,
        '60-64': 62, '65-69': 67, '70-74': 72, '75-79': 77
      };
      this.formData.Age = ageMapping[this.formData.AgeCategory];

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
        const response = await axios.post("http://localhost:5000/predict", apiData);
        this.result = response.data;
        this.shap_summary_text = response.data.shap_summary_text;
        console.log("SHAP Impact:", response.data.shap_impact);
        console.log("API Response:", response.data);
      } catch (error) {
        console.error("Error during API request:", error);
      }
    },
    isValidBase64(base64) {
      return typeof base64 === 'string' && 
             (base64.startsWith('iVBORw0KGgo') || base64.length > 0);
    }
  }
};
</script>

<style scoped>
/* Full Page Background */
body, #app {
  background-color: #c53030;
  height: 100vh;
  margin: 0;
  margin-top: 110px;
  padding-top: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Roboto', sans-serif;
  font-weight: 400;
}

/* Fonts */
h1, h2, h3, h4, h5, h6 {
  font-family: 'Montserrat';
  font-weight: 600;
  color: #c53030;
}
h1, h2 {
  font-family: 'Montserrat';
  font-size: larger;
  color: #c53030;
}
input, textarea, button, label {
  font-family: 'Roboto', sans-serif;
}

/* Layout Styles */
.container {
  display: flex;
  height: 95vh;
  width: 100%;
  gap: 20px;
}

/* Sidebar (White Background) */
.sidebar {
  width: 30vw;
  background-color: white;
  color: red;
  padding: 20px;
  overflow-y: auto;
  height: 92vh;
  border-radius: 16px;
  border-color: red;
  margin-left: 20px;
  margin-top: 20px;
}

/* Tooltip CSS in sidebar */
.tooltip-wrapper {
  position: relative;
  display: inline-block;
  margin-left: 8px;
}

.tooltip-icon {
  background-color: #333;
  color: #fff;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  font-size: 12px;
  cursor: pointer;
}

.tooltip-text {
  visibility: hidden;
  width: 200px;
  background-color: rgba(0,0,0,0.95);
  color: #fff;
  text-align: left;
  border-radius: 6px;
  padding: 12px 10px;
  min-height: 40px;
  box-sizing: border-box;
  position: absolute;
  z-index: 10;
  top: 200%;
  right: 0;
  transform: translateY(-50%);
  opacity: 0;
  transition: opacity 0.3s;
  white-space: normal;
}

.tooltip-wrapper:hover .tooltip-text {
  visibility: visible;
  opacity: 1;
}

/* Results Section (White Background) */
.results {
  flex-grow: 1;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  height: 92vh;
  margin-right: 20px;
  margin-top: 20px;
}

/* Layout pour séparer les facteurs positifs et négatifs */
.results-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.negative-factors, .positive-factors {
  padding: 15px;
  border-radius: 10px;
}

.negative-factors {
  background-color: #fff5f5;
  border: 1px solid #fed7d7;
}

.positive-factors {
  background-color: #f0fff4;
  border: 1px solid #c6f6d5;
}

.negative-factors h3 {
  color: #e53e3e;
  text-align: center;
  margin-bottom: 15px;
}

.positive-factors h3 {
  color: #38a169;
  text-align: center;
  margin-bottom: 15px;
}

.factors-column {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* Risk Score Section */
.risk-score-section {
  margin: 30px 0;
  display: flex;
  justify-content: center;
}

.risk-level-badge {
  padding: 20px 40px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  max-width: 400px;
  width: 100%;
}

.risk-level-badge.low {
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  border: 2px solid #28a745;
}

.risk-level-badge.medium {
  background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
  border: 2px solid #e3ac05ff;
}

.risk-level-badge.high {
  background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
  border: 2px solid #dc3545;
}

.risk-level-badge h3 {
  font-size: 24px;
  margin-bottom: 10px;
  color: #333;
}

.risk-score-value {
  font-size: 32px;
  font-weight: bold;
  margin: 15px 0;
  color: #c53030;
}

.risk-level-badge p {
  font-size: 16px;
  color: #555;
  margin-top: 10px;
}

/* Tab Navigation Styling */
.tab-navigation {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin: 30px 0 20px 0;
  border-bottom: 2px solid #e1e1e1;
  padding-bottom: 10px;
}

.tab-navigation button {
  background-color: #f8f9fa;
  color: #495057;
  border: 2px solid #dee2e6;
  padding: 12px 24px;
  border-radius: 8px 8px 0 0;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
  width: auto;
}

.tab-navigation button:hover {
  background-color: #e9ecef;
  transform: translateY(-2px);
}

.tab-navigation button.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
  font-weight: 600;
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
}

form label {
  display: block;
  margin: 5px 0;
}

.input input:invalid {
  background-color: #ffa2a2;
}

.input ::placeholder {
  color: #515152;
}

.bmi {
  color: black;
  font-weight: bold;
  margin: 20px auto;
}
.bmi input {
  width: 60%;
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
  gap: 20px;
  flex-wrap: wrap;
  justify-content: center;
}

/* Checkbox label css */
.checkbox-group label {
  display: flex;
  flex-direction: column; 
  align-items: center; 
  text-align: center; 
  gap: 5px;
  padding: 5px;
  border: 2px dashed #a02121;
  border-radius: 20px;
  width: 30%;
}

/* Checkboxes styling */
.checkbox-group input[type="checkbox"] {
  appearance: none;
  width: 30px;
  height: 30px;
  border: 2px solid #555;
  border-radius: 50%;
  display: inline-block;
  position: relative;
}

.checkbox-group input[type="checkbox"]:checked {
  background-color: #4CAF50;
  border-color: #4CAF50;
}

.checkbox-group input[type="checkbox"]:checked::after {
  content: '✔';
  color: white;
  font-size: 16px;
  font-weight: bold;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
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
  width: 100%;
  background: #fff;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
}

/* Results Cards borders */
.card-positive {
  border-color: green;
  background-color: #d4f8d4;
}

.card-negative {
  border-color: red;
  background-color: #f8d4d4;
}

.card-neutral {
  border-color: black;
  background-color: #f0f0f0;
}

/* Results Cards text */
.result-card .positive {
  color: green;
  font-weight: bold;
}

.result-card .negative {
  color: red;
  font-weight: bold;
}

.result-card .neutral {
  color: black;
  font-weight: bold;
}

/* Results Cards icons */
.icon-up i {
  font-size: 30px;
  margin: 5px;
  display: block;
}

.positive-icon {
  color: green;
}

.negative-icon {
  color: red;
}

.neutral-icon {
  color: rgb(65, 65, 65);
}

.p-6 {
  width: 100%;
  max-width: 800px;
  height: 400px;
}

/* Scrollable Content */
.scrollable-content {
  max-height: 80vh;
  overflow-y: visible;
  position: relative;
  padding-right: 10px;
  z-index: 1;
}

/* Scrollbar Styling */
.scrollable-content::-webkit-scrollbar {
  width: 10px;
}
.scrollable-content::-webkit-scrollbar-track {
  background: whitesmoke;
}
.scrollable-content::-webkit-scrollbar-thumb {
  background: #c53030;
  border-radius: 10px;
}
.scrollable-content::-webkit-scrollbar-thumb:hover {
  background: #a02121;
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

/* Table */
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

.risk-level-high {
  color: #dc3545;
  background-color: #f8d7da;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: bold;
}

.risk-level-medium {
  color: #6f5401ff;
  background-color: #fff3cd;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: bold;
}

.risk-level-low {
  color: #28a745;
  background-color: #d4edda;
  padding: 0px 8px;
  border-radius: 4px;
  font-weight: bold;
}

.impact-table td {
  vertical-align: middle;
  padding: 12px 15px;
}

/* Risk summary */
.risk-summary {
  background-color: #e7f3fe; 
  border: 1px solid #bcdff1;
  border-radius: 5px;
  padding: 20px;
  margin-top: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.risk-summary h3 {
  color: #0d6efd;
  margin-bottom: 10px;
}

.risk-summary p {
  font-size: 16px;
  line-height: 1.5;
  color: #212529;
}

.risk-summary .highlight {
  font-weight: bold;
  color: #dc3545;
}

/* SHAP Section */
.shap-section {
  background-color: #f9f9fc;
  border: 1px solid #dcdde1;
  border-radius: 12px;
  padding: 24px;
  margin-top: 20px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.shap-section h3 {
  color: green;
  font-size: 30px;
  margin-bottom: 16px;
}

.shap-section h4 {
  color: green;
  font-size: large;
  margin-top: 20px;
  margin-bottom: 10px;
}

.shap-section p {
  color: red;
  font-size: 30px;
  line-height: 1.6;
}

.shap-section img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin-bottom: 16px;
  border: 1px solid #e1e1e1;
}

/* Info Box */
.info-box {
  background-color: #ffffff; 
  border-radius: 10px;
  padding: 20px 25px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  font-family: 'Segoe UI', sans-serif;
  color: #212529;
  margin-top: 20px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.info-box h5 {
  color: #007BFF;
  font-weight: 600;
  font-size: 20px;
  margin-bottom: 15px;
}

.info-box p {
  font-size: 16px;
  line-height: 1.5;
  margin-bottom: 12px;
}

.info-box ul {
  padding-left: 20px;
  margin-bottom: 12px;
}

.info-box li {
  font-size: 16px;
  line-height: 1.4;
  margin-bottom: 8px;
}

.info-box strong {
  color: #28a745;
}

/* Risk Assessment */
.risk-assessment {
  margin: 20px 0;
}

.risk-level {
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.risk-level.low {
  background-color: #d4edda;
  border-left: 4px solid #28a745;
}

.risk-level.medium {
  background-color: #fff3cd;
  border-left: 4px solid #e3ac05ff;
}

.risk-level.high {
  background-color: #f8d7da;
  border-left: 4px solid #dc3545;
}

/* Lifestyle Factors */
.lifestyle-factors {
  margin-top: 30px;
}

.factors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px;
}

.factor-card {
  background: white;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.factor-card.warning {
  border-left: 4px solid #dc3545;
}

.factor-card.good {
  border-left: 4px solid #28a745;
}

.factor-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.factor-icon {
  font-size: 24px;
}

.factor-content .value {
  font-weight: 600;
  color: #333;
  margin: 5px 0;
}

.factor-content .impact {
  color: #666;
  font-size: 14px;
  margin: 5px 0;
}

.factor-content .recommendation {
  color: #007bff;
  font-size: 13px;
  font-style: italic;
  margin: 5px 0;
}

/* Responsive design */
@media (max-width: 768px) {
  .results-layout {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .container {
    flex-direction: column;
    height: auto;
  }
  
  .sidebar, .results {
    width: 90%;
    margin: 10px auto;
  }

  .tab-navigation {
    flex-direction: column;
    gap: 5px;
  }

  .tab-navigation button {
    width: 100%;
    border-radius: 8px;
  }

  .factors-grid {
    grid-template-columns: 1fr;
  }
}
</style>