<template>
  <Disclaimer v-if="showDisclaimer" @accepted="showDisclaimer = false" />
  <div id="home-app" :class="{ 'dark-mode': darkMode }">
    <div class="container">
      <!-- Sidebar -->
      <div class="sidebar">
        <h2>Enter Your Health & Lifestyle Information</h2>
        <form @submit.prevent="computeRisk" class="scrollable-form">
          
          <!-- CONTEXT CATEGORY -->
          <div class="feature-category">
            <h3 class="category-title">👤 Context</h3>
            
            <!-- Gender -->
            <div class="feature-item">
              <label>Gender *</label>
              <div class="button-group">
                <button type="button" 
                        :class="{ active: formData.Gender === 'Male' }"
                        @click="formData.Gender = 'Male'">
                  Male
                </button>
                <button type="button"
                        :class="{ active: formData.Gender === 'Female' }"
                        @click="formData.Gender = 'Female'">
                  Female
                </button>
              </div>
            </div>

            <!-- Age -->
            <div class="feature-item">
              <label>Age of respondent *</label>
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
            </div>
          </div>

          <!-- LIFESTYLE CATEGORY -->
          <div class="feature-category">
            <h3 class="category-title">🏃 Lifestyle</h3>
            
            <!-- Physical Activity -->
            <div class="feature-item">
              <label>Sports or physical activity (days per week) *</label>
              <div class="button-group multi-row">
                <button type="button" 
                        v-for="day in [0, 1, 2, 3, 4, 5, 6, 7]" 
                        :key="day"
                        :class="{ active: formData.PhysicalActivityDays === day }"
                        @click="formData.PhysicalActivityDays = day">
                  {{ day }}
                </button>
              </div>
            </div>

            <!-- Fruit -->
            <div class="feature-item">
              <label>How often eat fruit (excluding juice) *</label>
              <select v-model="formData.FruitFrequency" required>
                <option disabled value="">Select frequency</option>
                <option>Three times or more a day</option>
                <option>Twice a day</option>
                <option>Once a day</option>
                <option>Less than once a day but at least 4 times a week</option>
                <option>Less than 4 times a week but at least once a week</option>
                <option>Less than once a week</option>
                <option>Never</option>
              </select>
            </div>

            <!-- Vegetables -->
            <div class="feature-item">
              <label>How often eat vegetables or salad (excluding potatoes) *</label>
              <select v-model="formData.VegetableFrequency" required>
                <option disabled value="">Select frequency</option>
                <option>Three times or more a day</option>
                <option>Twice a day</option>
                <option>Once a day</option>
                <option>Less than once a day but at least 4 times a week</option>
                <option>Less than 4 times a week but at least once a week</option>
                <option>Less than once a week</option>
                <option>Never</option>
              </select>
            </div>

            <!-- Smoking -->
            <div class="feature-item">
              <label>Cigarette smoking behaviour *</label>
              <select v-model="formData.Smoking" required>
                <option disabled value="">Select smoking status</option>
                <option>I smoke daily, 10 or more cigarettes</option>
                <option>I smoke daily, 9 or fewer cigarettes</option>
                <option>I smoke but not every day</option>
                <option>I don't smoke now but I used to</option>
                <option>I have only smoked a few times</option>
                <option>I have never smoked</option>
              </select>
            </div>

            <!-- Alcohol -->
            <div class="feature-item">
              <label>How often drink alcohol *</label>
              <select v-model="formData.AlcoholFrequency" required>
                <option disabled value="">Select frequency</option>
                <option>Every day</option>
                <option>5-6 days a week</option>
                <option>3-4 days a week</option>
                <option>Once or twice a week</option>
                <option>2-3 times a month</option>
                <option>Once a month</option>
                <option>Less than once a month</option>
                <option>Never</option>
              </select>
            </div>

            <!-- Height -->
            <div class="feature-item">
              <label>Height (cm) *</label>
              <input v-model.number="formData.Height" 
                     type="number" 
                     placeholder="Height (90-240cm)" 
                     min="90" 
                     max="240" 
                     required />
            </div>

            <!-- Weight -->
            <div class="feature-item">
              <label>Weight (kg) *</label>
              <input v-model.number="formData.Weight" 
                     type="number" 
                     placeholder="Weight (30-400kg)" 
                     min="30" 
                     max="400" 
                     required />
            </div>
          </div>

          <!-- MEDICAL RISK FACTORS CATEGORY -->
          <div class="feature-category">
            <h3 class="category-title">🏥 Medical Risk Factors</h3>
            
            <!-- High Blood Pressure -->
            <div class="feature-item">
              <label>High blood pressure (last 12 months) *</label>
              <div class="button-group">
                <button type="button"
                        :class="{ active: formData.HighBloodPressure === false }"
                        @click="formData.HighBloodPressure = false">
                  No
                </button>
                <button type="button"
                        :class="{ active: formData.HighBloodPressure === true }"
                        @click="formData.HighBloodPressure = true">
                  Yes
                </button>
              </div>
            </div>

            <!-- Diabetes -->
            <div class="feature-item">
              <label>Diabetes (last 12 months) *</label>
              <div class="button-group">
                <button type="button"
                        :class="{ active: formData.Diabetes === false }"
                        @click="formData.Diabetes = false">
                  No
                </button>
                <button type="button"
                        :class="{ active: formData.Diabetes === true }"
                        @click="formData.Diabetes = true">
                  Yes
                </button>
              </div>
            </div>
          </div>

          <!-- ENVIRONMENTAL CATEGORY -->
          <div class="feature-category">
            <h3 class="category-title">🏘️ Environmental</h3>
            
            <!-- Noise Problems -->
            <div class="feature-item">
              <label>Problems with accommodation: noise *</label>
              <div class="button-group">
                <button type="button"
                        :class="{ active: formData.NoiseProblems === false }"
                        @click="formData.NoiseProblems = false">
                  No
                </button>
                <button type="button"
                        :class="{ active: formData.NoiseProblems === true }"
                        @click="formData.NoiseProblems = true">
                  Yes
                </button>
              </div>
            </div>
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
            <!-- Negative Factors -->
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

            <!-- Positive Factors -->
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

          <!-- Table View -->
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

          <!-- Chart View -->
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

        <!-- Empty State -->
        <div v-else class="empty-state">
          <div class="empty-icon">📋</div>
          <h3>No Analysis Yet</h3>
          <p>Fill out the form on the left and click "Analyze" to see your heart disease risk assessment.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable no-unused-vars */
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
        // Context
        Gender: '',
        AgeCategory: '',
        
        // Lifestyle
        PhysicalActivityDays: null,
        FruitFrequency: '',
        VegetableFrequency: '',
        Smoking: '',
        AlcoholFrequency: '',
        Height: '',
        Weight: '',
        
        // Medical
        HighBloodPressure: null,
        Diabetes: null,
        
        // Environmental
        NoiseProblems: null
      },
      result: null,
      shap_summary_text: '',
      whoGuidelines: {
        Gender: "Both genders should maintain healthy lifestyles.",
        Age: "Age-appropriate health monitoring is essential.",
        PhysicalActivity: "At least 150 minutes of moderate activity per week.",
        Fruit: "≥5 servings per day recommended.",
        Vegetables: "≥5 servings per day recommended.",
        Smoking: "No safe level of smoking.",
        Alcohol: "≤2 drinks/day men, ≤1 women.",
        Height: "—",
        Weight: "Maintain healthy BMI (18.5-24.9).",
        HighBloodPressure: "Control blood pressure to protect heart.",
        Diabetes: "Healthy diet and activity prevent type 2 diabetes.",
        Noise: "Chronic noise exposure may affect cardiovascular health."
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
        "Gender": build(
          "Gender",
          this.formData.Gender,
          shap.Gender,
          "👤",
          false
        ),
        "Age": build(
          "Age",
          this.formData.AgeCategory,
          shap.Age,
          "📅",
          false
        ),
        "Physical Activity": build(
          "PhysicalActivity",
          `${this.formData.PhysicalActivityDays} days/week`,
          shap.PhysicalActivityDays,
          this.formData.PhysicalActivityDays >= 3 ? "👍" : "👎",
          this.formData.PhysicalActivityDays < 3
        ),
        "Fruit Intake": build(
          "Fruit",
          this.formData.FruitFrequency,
          shap.FruitFrequency,
          this.formData.FruitFrequency.includes("Once a day") || this.formData.FruitFrequency.includes("Twice") || this.formData.FruitFrequency.includes("Three") ? "👍" : "👎",
          !this.formData.FruitFrequency.includes("day")
        ),
        "Vegetable Intake": build(
          "Vegetables",
          this.formData.VegetableFrequency,
          shap.VegetableFrequency,
          this.formData.VegetableFrequency.includes("Once a day") || this.formData.VegetableFrequency.includes("Twice") || this.formData.VegetableFrequency.includes("Three") ? "👍" : "👎",
          !this.formData.VegetableFrequency.includes("day")
        ),
        "Smoking": build(
          "Smoking",
          this.formData.Smoking,
          shap.Smoking,
          this.formData.Smoking === 'I have never smoked' ? "👍" : "👎",
          this.formData.Smoking.includes('smoke daily') || this.formData.Smoking.includes('smoke but not every day')
        ),
        "Alcohol": build(
          "Alcohol",
          this.formData.AlcoholFrequency,
          shap.AlcoholFrequency,
          this.formData.AlcoholFrequency === 'Never' || this.formData.AlcoholFrequency.includes('month') ? "👍" : "👎",
          this.formData.AlcoholFrequency === 'Every day' || this.formData.AlcoholFrequency.includes('5-6 days')
        ),
        "Height": build(
          "Height",
          `${this.formData.Height} cm`,
          shap.Height,
          "📏",
          false
        ),
        "Weight": build(
          "Weight",
          `${this.formData.Weight} kg`,
          shap.Weight,
          "⚖️",
          false
        ),
        "High Blood Pressure": build(
          "HighBloodPressure",
          this.formData.HighBloodPressure ? "Yes" : "No",
          shap.HighBloodPressure,
          this.formData.HighBloodPressure ? "👎" : "👍",
          this.formData.HighBloodPressure
        ),
        "Diabetes": build(
          "Diabetes",
          this.formData.Diabetes ? "Yes" : "No",
          shap.Diabetes,
          this.formData.Diabetes ? "👎" : "👍",
          this.formData.Diabetes
        ),
        "Noise Problems": build(
          "Noise",
          this.formData.NoiseProblems ? "Yes" : "No",
          shap.NoiseProblems,
          this.formData.NoiseProblems ? "👎" : "👍",
          this.formData.NoiseProblems
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
        "Gender": "Gender",
        "Age": "Age",
        "Physical Activity": "PhysicalActivity",
        "Fruit Intake": "Fruit",
        "Vegetable Intake": "Vegetables",
        "Smoking": "Smoking",
        "Alcohol": "Alcohol",
        "Height": "Height",
        "Weight": "Weight",
        "High Blood Pressure": "HighBloodPressure",
        "Diabetes": "Diabetes",
        "Noise Problems": "Noise"
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

    randomizeData() {
      const r = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
      const c = (arr) => arr[Math.floor(Math.random() * arr.length)];
      
      // Context
      this.formData.Gender = c(["Male", "Female"]);
      this.formData.AgeCategory = c(["18-24","25-29","30-34","35-39","40-44","45-49","50-54","55-59","60-64","65-69","70-74","75-79"]);
      
      // Lifestyle
      this.formData.PhysicalActivityDays = r(0, 7);
      this.formData.FruitFrequency = c([
        "Three times or more a day", "Twice a day", "Once a day",
        "Less than once a day but at least 4 times a week",
        "Less than 4 times a week but at least once a week",
        "Less than once a week", "Never"
      ]);
      this.formData.VegetableFrequency = c([
        "Three times or more a day", "Twice a day", "Once a day",
        "Less than once a day but at least 4 times a week",
        "Less than 4 times a week but at least once a week",
        "Less than once a week", "Never"
      ]);
      this.formData.Smoking = c([
        "I smoke daily, 10 or more cigarettes",
        "I smoke daily, 9 or fewer cigarettes",
        "I smoke but not every day",
        "I don't smoke now but I used to",
        "I have only smoked a few times",
        "I have never smoked"
      ]);
      this.formData.AlcoholFrequency = c([
        "Every day", "5-6 days a week", "3-4 days a week",
        "Once or twice a week", "2-3 times a month",
        "Once a month", "Less than once a month", "Never"
      ]);
      this.formData.Height = r(90, 240);
      this.formData.Weight = r(30, 220);
      
      // Medical
      this.formData.HighBloodPressure = Math.random() < 0.2;
      this.formData.Diabetes = Math.random() < 0.1;
      
      // Environmental
      this.formData.NoiseProblems = Math.random() < 0.3;
    },

    async computeRisk() {
      const ageMapping = {
        '18-24': 21, '25-29': 27, '30-34': 32, '35-39': 37,
        '40-44': 42, '45-49': 47, '50-54': 52, '55-59': 57,
        '60-64': 62, '65-69': 67, '70-74': 72, '75-79': 77
      };

      const apiData = {
        Gender: this.formData.Gender,
        Age: ageMapping[this.formData.AgeCategory],
        PhysicalActivityDays: this.formData.PhysicalActivityDays,
        FruitFrequency: this.formData.FruitFrequency,
        VegetableFrequency: this.formData.VegetableFrequency,
        Smoking: this.formData.Smoking,
        AlcoholFrequency: this.formData.AlcoholFrequency,
        Height: this.formData.Height,
        Weight: this.formData.Weight,
        HighBloodPressure: this.formData.HighBloodPressure,
        Diabetes: this.formData.Diabetes,
        NoiseProblems: this.formData.NoiseProblems
      };

      try {
        console.log("📊 Data prepared for backend:", apiData);
        
        // Uncomment when backend is ready:
        // const response = await axios.post("http://localhost:5000/predict", apiData);
        // this.result = response.data;
        // this.shap_summary_text = response.data.shap_summary_text;
        
        alert("✅ Data prepared successfully!\n\nCheck the console (F12) to see the formatted data.\n\nUncomment the axios.post() line when your backend is ready.");
      } catch (error) {
        console.error("❌ Error during API request:", error);
        alert("Error: " + error.message);
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
/* Base Styles */
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

/* Container */
.container {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 24px;
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Sidebar */
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
}

/* Scrollable Form */
.scrollable-form {
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 12px;
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

/* Feature Categories */
.feature-category {
  margin-bottom: 28px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  transition: all 0.3s ease;
}

.dark-mode .feature-category {
  background: #0f172a;
  border-color: #334155;
}

.category-title {
  color: #14b8a6;
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #14b8a6;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.feature-item {
  margin-bottom: 18px;
}

.feature-item:last-child {
  margin-bottom: 0;
}

.feature-item label {
  display: block;
  font-weight: 600;
  color: #475569;
  margin-bottom: 10px;
  font-size: 14px;
  text-align: left;
}

.dark-mode .feature-item label {
  color: #cbd5e1;
}

/* Input Fields */
.feature-item input,
.feature-item select {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 15px;
  transition: all 0.3s ease;
  background: white;
  color: #1e293b;
  font-weight: 500;
}

.dark-mode .feature-item input,
.dark-mode .feature-item select {
  background: #1e293b;
  color: #f1f5f9;
  border-color: #334155;
}

.feature-item input:focus,
.feature-item select:focus {
  outline: none;
  border-color: #14b8a6;
  box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.1);
}

.feature-item input::placeholder {
  color: #94a3b8;
  font-weight: 400;
}

.dark-mode .feature-item input::placeholder {
  color: #64748b;
}

/* Button Groups */
.button-group {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.button-group.multi-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}

.button-group button {
  flex: 1;
  padding: 12px 16px;
  background: white;
  color: #475569;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.2s ease;
  text-transform: none;
  letter-spacing: normal;
  margin: 0;
  min-width: 60px;
}

.dark-mode .button-group button {
  background: #1e293b;
  color: #cbd5e1;
  border-color: #334155;
}

.button-group button:hover {
  border-color: #14b8a6;
  background: #f0fdfa;
  transform: translateY(-2px);
}

.dark-mode .button-group button:hover {
  background: #134e4a;
}

.button-group button.active {
  background: linear-gradient(135deg, #14b8a6 0%, #0f766e 100%);
  color: white;
  border-color: #14b8a6;
  box-shadow: 0 4px 6px -1px rgba(20, 184, 166, 0.3);
  transform: scale(1.05);
}

.button-group button.active:hover {
  transform: scale(1.05) translateY(-2px);
}

/* Submit & Action Buttons */
button[type="submit"] {
  background: linear-gradient(135deg, #14b8a6 0%, #0f766e 100%);
  color: white;
  border: none;
  padding: 16px 24px;
  width: 100%;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 700;
  font-size: 16px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px -1px rgba(20, 184, 166, 0.3);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-top: 8px;
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
  padding: 14px 20px;
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
  transform: translateY(-1px);
}

.dark-mode button[type="button"]:hover {
  background: #1e293b;
  border-color: #475569;
}

/* Results Section */
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

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 24px;
  opacity: 0.5;
}

.empty-state h3 {
  color: #1e293b;
  font-size: 24px;
  margin-bottom: 12px;
}

.dark-mode .empty-state h3 {
  color: #f1f5f9;
}

.empty-state p {
  color: #64748b;
  font-size: 16px;
  max-width: 500px;
  margin: 0 auto;
}

.dark-mode .empty-state p {
  color: #94a3b8;
}

/* Results Layout */
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

/* Result Cards */
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

/* Risk Score Section */
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

/* Tab Navigation */
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

/* Results Container */
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

/* Impact Table */
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
  padding: 18px 20px;
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

/* Risk Level Classes */
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

/* SHAP Section */
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

/* Info Box */
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

/* Scrollbar Styles */
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

/* Responsive Design */
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
  
  .button-group.multi-row {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 480px) {
  .button-group.multi-row {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .container {
    padding: 0 12px;
  }
  
  .sidebar, .results {
    padding: 20px;
  }
}
</style>