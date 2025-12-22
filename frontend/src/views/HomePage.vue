<template>
  <Disclaimer v-if="showDisclaimer" @accepted="showDisclaimer = false" />
  <div id="home-app" :class="{ 'dark-mode': darkMode }">
    <div class="container">
      <!-- Sidebar -->
      <div class="sidebar">
        <h2>Enter Your Health & Lifestyle Information</h2>
        <form @submit.prevent="computeRisk" class="scrollable-form">
            <!-- Weight -->
            <div class="input">
              <p>Enter your weight
                <span class="tooltip-wrapper">
                  <span class="tooltip-icon">?</span>
                  <span class="tooltip-text">Your weight in kilograms (30–400)</span>
                </span>
              </p>
              <input v-model.number="formData.Weight" type="number" :placeholder="formData.Weight ? '' : 'Weight (30 - 400kg)*'" 
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
              <input v-model.number="formData.Height" type="number" :placeholder="formData.Height ? '' : 'Height (90 - 240cm)*'" 
                     @input="calculateBMI" min="90" max="240" required />
            </div>
            <!-- BMI -->
            <div class="bmi">
              <p>Calculated BMI</p>
              <input v-model="formData.BMI" type="text" :placeholder="formData.BMI ? '' : 'BMI'" readonly required />
            </div>
            <!-- Alcohol -->
            <div class="input">
              <p>Alcohol per week</p>
              <input v-model.number="formData.Alcohol" type="number" :placeholder="formData.Alcohol || formData.Alcohol === 0 ? '' : 'Alcohol (0-70)*'" min="0" max="70" required />
            </div>
            <!-- Sleep -->
            <div class="input">
              <p>Sleep (hours/day)</p>
              <input v-model.number="formData.Sleep" type="number" :placeholder="formData.Sleep || formData.Sleep === 0 ? '' : 'Sleep (0-24)*'" min="0" max="24" required />
            </div>
            <!-- Exercise -->
            <div class="input">
              <p>Exercise (minutes/week)</p>
              <input v-model.number="formData.Exercise" type="number" :placeholder="formData.Exercise || formData.Exercise === 0 ? '' : 'Exercise (0-3000)*'" min="0" max="3000" required />
            </div>
            <!-- Fruit -->
            <div class="input">
              <p>Fruit per day</p>
              <input v-model.number="formData.Fruit" type="number" :placeholder="formData.Fruit || formData.Fruit === 0 ? '' : 'Fruit (0-20)*'" min="0" max="20" required />
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
            <h3 class="conditions-label">Check any that apply:</h3>
            <div class="checkbox-group">
              <label>Diabetes<input type="checkbox" v-model="formData.Diabetes" /></label>
              <label>Kidney Disease<input type="checkbox" v-model="formData.Kidney" /></label>
              <label>Stroke<input type="checkbox" v-model="formData.Stroke" /></label>
            </div>

            <button type="submit">Analyze</button>
            <button type="button" @click="randomizeData">🔀 Randomize</button>
          </form>
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

          <!-- Table - SORTED BY IMPACT -->
          <div v-show="activeTab === 'table'" class="results-container">
            <h3>Risk Factors Analysis (Sorted by Impact)</h3>
            <table class="impact-table">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Factor</th>
                  <th>Currently</th>
                  <th>WHO Recommendation</th>
                  <th>Impact Level</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in sortedResults" :key="item.key">
                  <td class="rank-cell">{{ index + 1 }}</td>
                  <td><strong>{{ item.key }}</strong></td>
                  <td>{{ item.value.text }}</td>
                  <td class="guideline-text">{{ getGuideline(item.key) }}</td>
                  <td :class="getRiskClass(item.value.impact)">
                    {{ item.value.impact }} 
                    <span class="impact-percentage">({{ Math.abs(item.value.percentage).toFixed(1) }}%)</span>
                  </td>
                  <td :style="{
                    color: item.value.forceRed ? '#dc3545' : '#28a745',
                    fontWeight: 'bold'
                  }">
                    {{ item.value.icon }} 
                    {{ item.value.forceRed ? 'At Risk' : 'Good' }}
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
import Disclaimer from '../components/DisclaimerPopup.vue';

export default {
  name: 'HomePage',
  components: {
    Disclaimer
  },
  props: {
    darkMode: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      showDisclaimer: false,
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

    sortedResults() {
      const results = this.formattedResults;
      return Object.keys(results)
        .map(key => ({
          key: key,
          value: results[key]
        }))
        .sort((a, b) => Math.abs(b.value.percentage) - Math.abs(a.value.percentage));
    },

    negativeFactors() {
      const results = this.formattedResults;
      const entries = Object.entries(results)
        .filter(([, value]) => value.forceRed)
        .sort(([, valueA], [, valueB]) => 
          Math.abs(valueB.percentage) - Math.abs(valueA.percentage)
        );
      return Object.fromEntries(entries);
    },
    
    positiveFactors() {
      const results = this.formattedResults;
      const entries = Object.entries(results)
        .filter(([, value]) => !value.forceRed)
        .sort(([, valueA], [, valueB]) => 
          Math.abs(valueB.percentage) - Math.abs(valueA.percentage)
        );
      return Object.fromEntries(entries);
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
console.log("Calling API at:", process.env.VUE_APP_API_URL + "/predict");
console.log("Payload:", apiData);

      try {
        const response = await axios.post(`${process.env.VUE_APP_API_URL}/predict`, apiData);
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
/* Note: All styles from the document remain the same, just changed #app to #home-app */
/* and removed the dark-mode-toggle button styles since it's now in App.vue */

#home-app {
  background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 50%, #fef2f2 100%);
  min-height: 100vh;
  margin: 0;
  padding: 20px 0;
  font-family: 'Inter', 'Segoe UI', sans-serif;
  font-weight: 400;
  color: #1e293b;
  transition: all 0.3s ease;
}

#home-app.dark-mode {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  color: #f1f5f9;
}

/* All other styles remain exactly the same as in the original document... */
/* (Copy all the remaining CSS from the document here) */

h1, h2, h3, h4, h5, h6 {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  letter-spacing: -0.02em;
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

h2::before {
  font-size: 1.25rem;
}

.container {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 24px;
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 20px;
}

.sidebar {
  background: white;
  padding: 28px;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border: 1px solid #e2e8f0;
  height: fit-content;
  max-height: calc(100vh - 140px);
  position: sticky;
  top: 110px;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.dark-mode .sidebar {
  background: #1e293b;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
  border-color: #334155;
}

.sidebar h2 {
  color: #14b8a6;
  border-bottom: 3px solid #14b8a6;
  padding-bottom: 12px;
  margin-bottom: 24px;
  flex-shrink: 0;
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
}

.scrollable-form {
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 15px;
  flex: 1;
}

.scrollable-form::-webkit-scrollbar {
  width: 8px;
}

.scrollable-form::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}

.dark-mode .scrollable-form::-webkit-scrollbar-track {
  background: #0f172a;
}

.scrollable-form::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #14b8a6 0%, #0f766e 100%);
  border-radius: 10px;
}

.scrollable-form::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #0f766e 0%, #134e4a 100%);
}

form input, form select {
  width: 95%;
  padding: 12px 4px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 16px;
  transition: all 0.3s ease;
  background: white;
  margin-bottom: 16px;
  color: #1e293b;
  text-align: center;
  font-weight: 500;
}

form input::placeholder {
  color: #94a3b8;
  font-weight: 400;
  opacity: 0.7;
}

.dark-mode form input,
.dark-mode form select {
  background: #0f172a;
  color: #f1f5f9;
  border-color: #334155;
}

.dark-mode form input::placeholder {
  color: #64748b;
}

form input:focus, form select:focus {
  outline: none;
  border-color: #14b8a6;
  box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.1);
}

form input:invalid {
  border-color: #fca5a5;
  background-color: #fef2f2;
}

.dark-mode form input:invalid {
  background-color: #7f1d1d;
}

form label {
  display: block;
  font-weight: 600;
  color: #475569;
  margin-bottom: 8px;
  margin-top: 8px;
  font-size: 15px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  text-align: center;
}

.dark-mode form label {
  color: #cbd5e1;
}

.input p {
  color: #475569;
  font-weight: 600;
  margin-bottom: 8px;
  text-align: center;
  font-size: 15px;
  word-wrap: break-word;
  overflow-wrap: break-word;
  padding: 0 5px;
}

.dark-mode .input p {
  color: #cbd5e1;
}

.bmi {
  background: linear-gradient(135deg, #ccfbf1 0%, #99f6e4 100%);
  border: 2px solid #14b8a6;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  margin: 20px 0;
  transition: all 0.3s ease;
}

.dark-mode .bmi {
  background: linear-gradient(135deg, #134e4a 0%, #115e59 100%);
}

.bmi p {
  font-weight: 600;
  color: #14b8a6;
  margin-bottom: 8px;
  font-size: 13px;
  text-transform: uppercase;
}

.dark-mode .bmi p {
  color: #5eead4;
}

.bmi input {
  font-size: 32px;
  font-weight: 700;
  text-align: center;
  border: none;
  background: transparent;
  color: #0f766e;
  margin: 0;
  padding: 8px;
}

.bmi input::placeholder {
  color: #5eead4;
  opacity: 0.5;
  font-size: 24px;
}

.dark-mode .bmi input {
  color: #5eead4;
}

.dark-mode .bmi input::placeholder {
  color: #14b8a6;
  opacity: 0.5;
}

button[type="submit"] {
  background: linear-gradient(135deg, #14b8a6 0%, #0f766e 100%);
  color: white;
  border: none;
  padding: 16px 24px;
  width: 100%;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px -1px rgba(20, 184, 166, 0.3);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

button[type="submit"]:hover {
  background: linear-gradient(135deg, #0f766e 0%, #0c4a6e 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px -2px rgba(20, 184, 166, 0.4);
}

button[type="button"] {
  background: #f1f5f9;
  color: #475569;
  border: 2px solid #cbd5e1;
  padding: 16px 24px;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  margin-top: 12px;
  width: 100%;
}

.dark-mode button[type="button"] {
  background: #0f172a;
  color: #cbd5e1;
  border-color: #334155;
}

button[type="button"]:hover {
  background: #e2e8f0;
  border-color: #94a3b8;
}

.dark-mode button[type="button"]:hover {
  background: #1e293b;
  border-color: #475569;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 0 0 5% 0;
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
  border: 2px dashed #cbd5e1;
}

.dark-mode .checkbox-group {
  background: #0f172a;
  border-color: #334155;
}

.conditions-label {
  text-align: center;
  font-size: 15px;
  font-weight: 600;
  color: #475569;
  margin-top: 8px;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  word-wrap: break-word;
  overflow-wrap: break-word;
  padding: 0 5px;
}

.dark-mode .conditions-label {
  color: #cbd5e1;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: white;
  border-radius: 8px;
  border: 2px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.2s ease;
  text-transform: none;
  font-size: 15px;
  font-weight: 500;
  color: #1e293b;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.dark-mode .checkbox-group label {
  background: #1e293b;
  border-color: #334155;
  color: #f1f5f9;
}

.checkbox-group label:hover {
  border-color: #14b8a6;
  background: #f0fdfa;
}

.dark-mode .checkbox-group label:hover {
  background: #134e4a;
}

.checkbox-group input[type="checkbox"] {
  width: 24px;
  height: 24px;
  cursor: pointer;
  accent-color: #14b8a6;
  margin: 0;
}

.results {
  background: white;
  padding: 32px;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.dark-mode .results {
  background: #1e293b;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
  border-color: #334155;
}

.results h2 {
  color: #1e293b;
  font-size: 28px;
  margin-bottom: 8px;
}

.dark-mode .results h2 {
  color: #f1f5f9;
}

.results > p {
  color: #64748b;
  font-size: 16px;
  margin-bottom: 32px;
}

.dark-mode .results > p {
  color: #94a3b8;
}

.risk-score-section {
  margin: 32px 0;
  display: flex;
  justify-content: center;
}

.risk-level-badge {
  padding: 32px 48px;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  max-width: 500px;
  width: 100%;
  border: 3px solid;
  position: relative;
  overflow: hidden;
}

.risk-level-badge::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: currentColor;
}

.risk-level-badge.low {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  border-color: #10b981;
  color: #065f46;
}

.risk-level-badge.mid {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-color: #d97706;
  color: #92400e;
}

.risk-level-badge.high {
  background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%);
  border-color: #ef4444;
  color: #991b1b;
}

.risk-level-badge h3 {
  font-size: 24px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 16px;
}

.risk-score-value {
  font-size: 48px;
  font-weight: 900;
  margin: 20px 0;
  font-family: 'Inter', monospace;
}

.tab-navigation {
  display: flex;
  gap: 0;
  margin: 32px 0 0 0;
  border-bottom: 3px solid #e2e8f0;
}

.dark-mode .tab-navigation {
  border-bottom-color: #334155;
}

.tab-navigation button {
  background: transparent;
  color: #64748b;
  border: none;
  border-bottom: 3px solid transparent;
  padding: 16px 32px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
  margin-bottom: -3px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.dark-mode .tab-navigation button {
  color: #94a3b8;
}

.tab-navigation button:hover {
  color: #14b8a6;
  background: rgba(20, 184, 166, 0.05);
}

.tab-navigation button.active {
  color: #14b8a6;
  border-bottom-color: #14b8a6;
  background: rgba(20, 184, 166, 0.1);
  font-weight: 700;
}

.results-container {
  margin-top: 32px;
}

.results-container h3 {
  font-size: 22px;
  color: #1e293b;
  margin-bottom: 24px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e2e8f0;
}

.dark-mode .results-container h3 {
  color: #f1f5f9;
  border-bottom-color: #334155;
}

.impact-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-top: 20px;
  background: white;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

.dark-mode .impact-table {
  background: #0f172a;
  border-color: #334155;
}

.impact-table thead {
  background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%);
  color: white;
}

.impact-table th {
  padding: 18px 10px;
  text-align: left;
  font-weight: 700;
  text-transform: uppercase;
  font-size: 13px;
  letter-spacing: 0.1em;
  border-bottom: 3px solid #134e4a;
}

.impact-table td {
  padding: 18px 20px;
  border-bottom: 1px solid #f1f5f9;
  font-size: 15px;
  vertical-align: middle;
  color: #1e293b;
}

.dark-mode .impact-table td {
  border-bottom-color: #334155;
  color: #f1f5f9;
}

.impact-table tbody tr {
  transition: all 0.2s ease;
}

.impact-table tbody tr:hover {
  background: rgba(20, 184, 166, 0.05);
  transform: scale(1.01);
}

.dark-mode .impact-table tbody tr:hover {
  background: rgba(20, 184, 166, 0.15);
}

.impact-table tbody tr:last-child td {
  border-bottom: none;
}

.rank-cell {
  font-weight: 800;
  font-size: 18px;
  color: #14b8a6;
  text-align: center;
  width: 60px;
}

.guideline-text {
  color: #64748b;
  font-size: 13px;
  font-style: italic;
}

.dark-mode .guideline-text {
  color: #94a3b8;
}

.impact-percentage {
  display: inline-block;
  margin-left: 8px;
  font-size: 12px;
  font-weight: 700;
  opacity: 0.8;
}

.risk-level-high {
  background: linear-gradient(135deg, #cf8787 0%, #bb4949 100%);
  color: #991b1b;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 2px solid #f87171;
}

.risk-level-high::before {
  content: '⚠️';
}

.risk-level-medium {
  background: linear-gradient(135deg, #d7c88a 0%, #bca443 100%);
  color: #92400e;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 2px solid #fbbf24;
}

.risk-level-medium::before {
  content: '⚡';
}

.risk-level-low {
  background: linear-gradient(135deg, #7cc59f 0%, #3ecb89 100%);
  color: #065f46;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 2px solid #34d399;
}

.risk-level-low::before {
  content: '✓';
}

.results-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 32px;
}

.negative-factors, .positive-factors {
  padding: 24px;
  border-radius: 12px;
  border: 2px solid;
}

.negative-factors {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  border-color: #fca5a5;
}

.dark-mode .negative-factors {
  background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%);
  border-color: #dc2626;
}

.negative-factors h3 {
  color: #dc2626;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  margin-bottom: 20px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.dark-mode .negative-factors h3 {
  color: #fca5a5;
}

.positive-factors {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-color: #86efac;
}

.dark-mode .positive-factors {
  background: linear-gradient(135deg, #14532d 0%, #166534 100%);
  border-color: #22c55e;
}

.positive-factors h3 {
  color: #16a34a;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  margin-bottom: 20px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.dark-mode .positive-factors h3 {
  color: #86efac;
}

.result-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: 10px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  border: 2px solid;
  margin-bottom: 12px;
  transition: all 0.2s ease;
}

.dark-mode .result-card {
  background: #1e293b;
}

.result-card:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-positive {
  border-color: #86efac;
}

.dark-mode .card-positive {
  border-color: #22c55e;
}

.card-negative {
  border-color: #fca5a5;
}

.dark-mode .card-negative {
  border-color: #dc2626;
}

.positive-icon, .negative-icon {
  font-size: 28px;
  flex-shrink: 0;
}

.positive-icon {
  color: #16a34a;
}

.dark-mode .positive-icon {
  color: #86efac;
}

.negative-icon {
  color: #dc2626;
}

.dark-mode .negative-icon {
  color: #fca5a5;
}

.result-content {
  flex: 1;
}

.result-content strong {
  display: block;
  font-size: 15px;
  font-weight: 700;
  margin-bottom: 4px;
  color: #1e293b;
}

.dark-mode .result-content strong {
  color: #f1f5f9;
}

.result-content .positive,
.result-content .negative {
  font-size: 18px;
  font-weight: 800;
  margin-top: 8px;
}

.shap-section {
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 32px;
  margin-top: 24px;
}

.dark-mode .shap-section {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  border-color: #334155;
}

.shap-section h3 {
  color: #14b8a6;
  font-size: 24px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.shap-section h3::before {
  content: '📊';
  font-size: 28px;
}

.shap-section h4 {
  color: #1e293b;
  font-size: 18px;
  margin: 24px 0 12px 0;
  font-weight: 700;
}

.dark-mode .shap-section h4 {
  color: #f1f5f9;
}

.shap-section p {
  color: #475569;
  font-size: 16px;
  line-height: 1.7;
}

.dark-mode .shap-section p {
  color: #cbd5e1;
}

.shap-section img {
  max-width: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  margin: 20px 0;
}

.dark-mode .shap-section img {
  border-color: #334155;
}

.info-box {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border: 2px solid #93c5fd;
  border-radius: 12px;
  padding: 24px 28px;
  margin: 24px 0;
  box-shadow: 0 2px 4px rgba(37, 99, 235, 0.1);
}

.dark-mode .info-box {
  background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
  border-color: #3b82f6;
}

.info-box h5 {
  color: #2563eb;
  font-weight: 700;
  font-size: 18px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.dark-mode .info-box h5 {
  color: #93c5fd;
}

.info-box p {
  font-size: 15px;
  line-height: 1.6;
  color: #1e40af;
  margin-bottom: 12px;
}

.dark-mode .info-box p {
  color: #dbeafe;
}

.info-box ul {
  padding-left: 24px;
  margin: 16px 0;
}

.info-box li {
  font-size: 15px;
  line-height: 1.8;
  color: #1e40af;
  margin-bottom: 8px;
}

.dark-mode .info-box li {
  color: #dbeafe;
}

.info-box strong {
  font-weight: 700;
}

.tooltip-wrapper {
  position: relative;
  display: inline-block;
  margin-left: 6px;
}

.tooltip-icon {
  background: #14b8a6;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  font-size: 12px;
  font-weight: 700;
  cursor: help;
  transition: all 0.2s ease;
}

.tooltip-icon:hover {
  transform: scale(1.1);
  background: #0f766e;
}

.tooltip-text {
  visibility: hidden;
  width: 220px;
  background: #1e293b;
  color: white;
  text-align: left;
  border-radius: 8px;
  padding: 12px 14px;
  position: absolute;
  z-index: 100;
  top: 125%;
  left: 50%;
  transform: translateX(-50%);
  opacity: 0;
  transition: opacity 0.3s, visibility 0.3s;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
  font-size: 13px;
  line-height: 1.5;
}

.tooltip-text::before {
  content: '';
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 6px solid transparent;
  border-bottom-color: #1e293b;
}

.tooltip-wrapper:hover .tooltip-text {
  visibility: visible;
  opacity: 1;
}

::-webkit-scrollbar {
  width: 12px;
  height: 12px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}

.dark-mode ::-webkit-scrollbar-track {
  background: #0f172a;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #14b8a6 0%, #0f766e 100%);
  border-radius: 10px;
  border: 2px solid #f1f5f9;
}

.dark-mode ::-webkit-scrollbar-thumb {
  border-color: #1e293b;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #0f766e 0%, #134e4a 100%);
}

@media (max-width: 1024px) {
  .container {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .sidebar {
    position: relative;
    top: 0;
    max-height: none;
  }
  
  .results-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .impact-table {
    font-size: 13px;
  }
  
  .impact-table th,
  .impact-table td {
    padding: 12px 10px;
  }
  
  .risk-level-badge {
    padding: 24px 32px;
  }
  
  .risk-score-value {
    font-size: 36px;
  }
}
</style>