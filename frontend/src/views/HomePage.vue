
<template>
  <Disclaimer />
  <div id="app">
  
    <div class="container">
      <!-- Sidebar for Input Fields -->
      <div class="sidebar">
        <h2>Enter Your Health & Lifestyle Information</h2>
        <div class="scrollable-content">
          <form @submit.prevent="computeRisk">
            <!-- Form questions with user inputs that includes limited value ranges -->
            <div class="input">
             <p>Enter your weight
               <span class="tooltip-wrapper">
                 <span class="tooltip-icon">?</span>
                 <span class="tooltip-text">Your weight in kilograms (used to calculate BMI). Acceptable inputs limited between 30 - 400</span>
                </span>
              </p>
              <input v-model.number="formData.Weight" type="number" placeholder="Weight ( 30 - 400 kg max)*" @input="calculateBMI" min="30" max="400" required />
            </div>
            <div class="input">
              <p>Enter your height
                <span class="tooltip-wrapper">
                 <span class="tooltip-icon">?</span>
                 <span class="tooltip-text">Your height in centimeters (used to calculate BMI). Acceptable inputs limited between 90 - 240</span>
                </span>
              </p>
              <input v-model.number="formData.Height" type="number" placeholder="Height (90 - 240 cm max)*" @input="calculateBMI" min="90" max="240" required />
            </div>
            <div class="bmi">
              <p>Calculated BMI
                <span class="tooltip-wrapper">
                 <span class="tooltip-icon">?</span>
                 <span class="tooltip-text">This displays BMI based on what height and weight you entered. NOTE: BMI can not differentiate between bodyfat and muscle mass</span>
                </span>
              </p>
              <input v-model="formData.BMI" type="number" placeholder="BMI* (auto-calculated)" readonly required />
            </div>
            <div class="input">
              <p>How many drinks of alcohol do you consume per week?
                <span class="tooltip-wrapper">
                 <span class="tooltip-icon">?</span>
                 <span class="tooltip-text">Average amount of units of alcohol you consume in a week. Max limit set at 70</span>
                </span>
              </p>
              <input v-model="formData.Alcohol" placeholder="Alcohol drinking per week (70 max)*" type="number" min="0" max="70" required />
            </div>
            <div class="input">
              <p>How many hours of sleep do you get per 24 hours?
                <span class="tooltip-wrapper">
                 <span class="tooltip-icon">?</span>
                 <span class="tooltip-text">Average amount of hours you sleep in a day</span>
                </span>
              </p>
              <input v-model="formData.Sleep" type="number" placeholder="Sleep (hours per day)*" min="0" max="24" required />
            </div>
            <div class="input">
              <p>How many minutes do you exercise per week?
                <span class="tooltip-wrapper">
                 <span class="tooltip-icon">?</span>
                 <span class="tooltip-text">Amount of minutes you exercise on an average week including activities like cycling, hiking, walking etc. Max limit set att 3000 (50 hours)</span>
                </span>
              </p>
              <input v-model="formData.Exercise" type="number" placeholder="Exercise (minutes per week, 3000 max)*" min="0" max="3000" required />
            </div>
            <div class="input">
              <p>How many fruits do you eat per day?
                <span class="tooltip-wrapper">
                 <span class="tooltip-icon">?</span>
                 <span class="tooltip-text">Amount of fruits you eat on average everyday. Max limit set at 20</span>
                </span>
              </p>
              <input v-model="formData.Fruit" placeholder="Fruit intake (servings per day, 20 max)*" min="0" max="20" required />
            </div>

          <!-- Gender Dropdown -->
          <label>Gender *</label>
          <select v-model="formData.Gender" required>
            <option disabled value="">Select Gender</option>
            <option>Male</option>
            <option>Female</option>
          </select>

           
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

           
            <label>Smoking *</label>
            <select v-model="formData.Smoking" required>
              <option disabled value="">Select Smoking Status</option>
              <option>Not at all</option>
              <option>Sometimes</option>
              <option>Everyday</option>
            </select>

            
            <h3>Check any that apply:  
              <span class="tooltip-wrapper">
                <span class="tooltip-icon">?</span>
                <span class="tooltip-text">Check one or multiple boxes if you have experienced any of these</span>
              </span>
            </h3>
            <div class="checkbox-group">
              <label>Diabetes<input type="checkbox" v-model="formData.Diabetes" /></label>
              <label>Kidney Disease<input type="checkbox" v-model="formData.Kidney" /></label>
              <label>Stroke<input type="checkbox" v-model="formData.Stroke" /></label>
            </div>

            <button type="submit">Analyze</button>
            <button type="submit" @click="randomizeData">🔀 Randomize</button>
          </form>
        </div>
      </div>

     
      <div class="results">
        <h2>Heart Disease Risk Prediction Results</h2>
        <p>Based on your health data, here's how your lifestyle factors contribute to your risk</p>
        <div class="scrollable-content">
          <div v-if="result">
            <div class="results-container">
             <div v-for="(value, key) in formattedResults" :key="key" class="result-card" :class="{
              'card-negative': value.forceRed ,
              'card-positive': !value.forceRed 
              //'card-neutral': !value.forceRed && !value.forcedRed && value.percentage === 0
             }">
              <div class="icon-up">
                <i v-if="value.forceRed " class="bi bi-hand-thumbs-down-fill negative-icon"></i>
               <!-- <i v-else-if="value.percentage === 0" class="bi bi-slash-circle neutral-icon"></i>-->
                <i v-else class="bi bi-hand-thumbs-up-fill positive-icon"></i>  
              </div>
             
                <div class="result-content">
                  <strong>{{ key }}</strong>: {{ value.text }}
                  <div :class="{
                        'negative': value.forceRed ,
                        'positive': !value.forceRed  ,
                       // 'positive': !value.forceRed && !value.forcedRed && value.percentage < 0,
                       // 'neutral': !value.forceRed && !value.forcedRed && value.percentage === 0
                      }">
                    {{ value.percentage.toFixed(2) }}%
                  </div>
              </div>             
            </div>
          </div>

         <div class="results-container">
            <h3>Explaining Heart Disease Predictions Through Feature Importance</h3>
            <table class="impact-table">
              <thead>
                <tr>
                  <th>Feature</th>
                  <th>
                   
                    <span class="tooltip-wrapper"> WHO Recommendation / Guidance 
                    <span class="tooltip-icon">*</span>
                    <span class="tooltip-text">These are benchmarks recommended by the World Health Organization (WHO) for a healthy lifestyle.</span>
                    </span>
                  </th>
                  <th>Value</th>
                  <th>Impact (%)</th>
                  <th>Effect</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(value, key) in formattedResults" :key="key">
                  <td><strong>{{ key }}</strong></td>
                  <td>{{ getGuideline (key)  }}</td>
                  <td>{{ value.text }}</td>
                  <td>{{ value.percentage.toFixed(2) }}%</td>
                  <!--
                  <td :style="{ 
                    color: value.forceRed 
                      ? 'red' 
                     // : value.percentage === 0 
                     //   ? 'black' 
                        : value.percentage <= 0 
                          ? 'green' 
                          : 'red',
                    fontWeight: 'bold' 
                  }">
                  {{ value.icon }} 
                  {{ value.percentage === 0 ? 'Neutral' : (value.forceRed || value.percentage > 0 ? 'Negative' : 'Positive') }}
                 {{  value.forceRed ? 'Negative':'Positive'}}
                </td>-->
                                <td :style="{
                  color: value.forceRed ? 'red' : 'green',
                  fontWeight: 'bold'
                }">
                  {{ value.icon }} 
                  {{ value.forceRed ? 'Negative' : 'Positive' }}
                </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-if="isValidBase64(result.shap_plot) || shap_summary_text" class="shap-section">
            <h3>What Affected Your Results Most</h3>

            <div v-if="isValidBase64(result.shap_plot)">
              <img :src="'data:image/png;base64,' + result.shap_plot" alt="SHAP Impact Chart" />
            </div>

            <div class="info-box">
              <h5>📊 How This Chart Works</h5>
              <p>
                This chart shows which health factors had the biggest effect on your heart disease risk. 
              </p>
              <ul>
                <li><strong>Green bars</strong> = lower your risk</li>
                <li><strong style="color:#dc3545;">Red bars</strong> = increase your risk</li>
                <li>The longer the bar, the more important the effect</li>
              </ul>
              <p>
                Even if you don't have a condition like stroke or kidney disease, it may still appear. That's because your good health (not having it) helped lower your risk — and the model shows that.
              </p>
            </div>


            <div v-if="shap_summary_text">
              <h4>Main Risk Factors Identified</h4>
              <p>{{ shap_summary_text }}</p>
            </div>
          </div>


          <!-- SHAP Feature Importance Plot 
         
          <div v-if="isValidBase64(result.shap_plot)">
                <h3>SHAP Feature Importance</h3>
                <img :src="'data:image/png;base64,' + result.shap_plot" alt="SHAP Impact Chart" />
                
          </div>
          
          <div v-if="shap_summary_text">
            <h4>Summary of Risk Factors</h4>
            <p>{{ shap_summary_text }}</p>
          </div>-->
              <!--
              <div class="p-6">
                <canvas ref="barChart" style="height: 400px;"></canvas>
              </div>
                
              <div class="chart-container">
                <div v-if="isValidBase64(result.svm_pie_chart)">
                  <h3>SVM Prediction</h3>
                  <img :src="'data:image/png;base64,' + result.svm_pie_chart" alt="SVM Pie Chart" />
                </div>
              --> 
              <!-- XGBoost Pie Chart -->
               <!--
              <div v-if="isValidBase64(result.xgb_pie_chart)">
                <h3>XGBoost Prediction</h3>
                <img :src="'data:image/png;base64,' + result.xgb_pie_chart" alt="XGBoost Pie Chart" />
              </div>-->
           
              <!-- Keras Pie Chart-->
               <!--
              <div v-if="isValidBase64(result.keras_pie_chart)">
                <h3>Keras Prediction</h3>
                <img :src="'data:image/png;base64,' + result.keras_pie_chart" alt="Keras Pie Chart" />
              </div>
            </div>-->
         
            
            <!--
            <div class="summary">
              <h3>Risk Summary</h3>
              <p>{{ riskSummary }}</p>
            </div>
          -->
            <!-- Risk Prediction Summary Section
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
               -->

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
      whoGuidelines: {
      BMI: "18.5 – 24.9 kg/m² is considered healthy. Over 25 is overweight; over 30 is obese.",
      Alcohol: "Limit to ≤2 standard drinks/day for men, ≤1 for women. Avoid binge drinking.",
      Sleep: "7–9 hours of sleep per night for adults recommended .",
      Exercise: " At least 150 min of moderate  activity/week.",
      Fruit: "At least 400grams or 5 servings /day",
      Smoking:"No level of smoking is safe",
      Diabetes:" Maintain a healthy diet, regular physical activity, and a healthy weight to prevent type 2 diabetes",
      Kidney:"Manage blood pressure and blood sugar to prevent kidney disease. Avoid smoking and excessive alcohol.",
      Stroke:"Manage blood pressure, reduce cholesterol, and avoid smoking to lower stroke risk.",
      
    },
      result: null,
      chart: null,
      riskSummary: '',
      shap_summary_text:'',
    };
  },
  computed: {
    formattedResults() {
  if (!this.result || !this.result.shap_contrib_pp || !this.result.shap_share_percent) {
    return {};
  }
  const contrib = this.result.shap_contrib_pp;         // signé, en points
  const share   = this.result.shap_share_percent;      // % (somme ≈ 100)

  return {
    "BMI (normal entre 18.5 - 24.9)": {
      text: this.formData.BMI,
      percentage: contrib?.BMI ?? 0,   // <- utilisé pour le graphe (signé, en points)
      share: share?.BMI ?? 0,          // <- % pour le tableau
      icon: this.formData.BMI < 18.5 ? "👎" : (this.formData.BMI <= 24.9 ? "👍" : "👎"),
      forceRed: this.formData.BMI >= 25 || this.formData.BMI < 18.5
    },
    "Alcohol (drinks/week)": {
      text: this.formData.Alcohol,
      percentage: contrib?.Alcohol ?? 0,
      share: share?.Alcohol ?? 0,
      icon: this.formData.Alcohol <= 3 ? "👍" : "👎",
      forceRed: contrib?.Alcohol > 0
    },
    "Sleep (hours/day)": {
      text: this.formData.Sleep,
      percentage: contrib?.Sleep ?? 0,
      share: share?.Sleep ?? 0,
      icon: (this.formData.Sleep >= 6 && this.formData.Sleep <= 10) ? "👍" : "👎",
      forceRed: !(this.formData.Sleep >= 6 && this.formData.Sleep <= 10)
    },
    "Exercise (min/week)": {
      text: this.formData.Exercise,
      percentage: contrib?.Exercise ?? 0,
      share: share?.Exercise ?? 0,
      icon: this.formData.Exercise > 150 ? "👍" : "👎",
      forceRed: this.formData.Exercise <= 150
    },
    "Fruit Intake (servings/day)": {
      text: this.formData.Fruit,
      percentage: contrib?.Fruit ?? 0,
      share: share?.Fruit ?? 0,
      icon: this.formData.Fruit >= 5 ? "👍" : "👎",
      forceRed: this.formData.Fruit < 5
    },
    "Smoking": {
      text: this.formData.Smoking,
      percentage: contrib?.Smoking ?? 0,
      share: share?.Smoking ?? 0,
      icon: this.formData.Smoking === 'Not at all' ? "👍" : "👎",
      forceRed: this.formData.Smoking !== 'Not at all'
    },
    "Diabetes": {
      text: this.formData.Diabetes ? "Yes" : "No",
      percentage: contrib?.Diabetes ?? 0,
      share: share?.Diabetes ?? 0,
      icon: this.formData.Diabetes ? "👎" : "👍",
      forceRed: !!this.formData.Diabetes
    },
    "Kidney Disease": {
      text: this.formData.Kidney ? "Yes" : "No",
      percentage: contrib?.Kidney ?? 0,
      share: share?.Kidney ?? 0,
      icon: this.formData.Kidney ? "👎" : "👍",
      forceRed: !!this.formData.Kidney
    },
    "Stroke": {
      text: this.formData.Stroke ? "Yes" : "No",
      percentage: contrib?.Stroke ?? 0,
      share: share?.Stroke ?? 0,
      icon: this.formData.Stroke ? "👎" : "👍",
      forceRed: !!this.formData.Stroke
    },
    "Age": {
      text: this.formData.Age,
      percentage: contrib?.Age ?? 0,
      share: share?.Age ?? 0,
      icon: this.formData.Age ? "👎" : "👍",
      forceRed: contrib?.Age > 0
    },
  };
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
    calculateBMI() {
      if (this.formData.Weight && this.formData.Height) {
        const heightInMeters = this.formData.Height / 100;
        this.formData.BMI = (this.formData.Weight / (heightInMeters ** 2)).toFixed(2);
      }
    },

    /* Function for randomlize button*/
    randomizeData() {
      const randomBetween = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
      const randomChoice = (arr) => arr[Math.floor(Math.random() * arr.length)];

      this.formData.Weight = randomBetween(30, 220);// Between 30kg-220kg
      this.formData.Height = randomBetween(90, 240);// between 90cm -240cm
      this.calculateBMI();
      this.formData.Alcohol = randomBetween(0, 35);// max to 35 times per week
      this.formData.Sleep = randomBetween(0, 24); // between 0 -24h per day
      this.formData.Exercise = randomBetween(0, 300); // between 0-300 minutes/weekly
      this.formData.Fruit = randomBetween(0, 5);// max to 5 times per days
      this.formData.Gender = randomChoice(["Male", "Female"]);
      this.formData.AgeCategory = randomChoice(["18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79"]);
      this.formData.Smoking = randomChoice(["Not at all", "Sometimes", "Everyday"]);
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
        this.shap_summary_text =response.data.shap_summary_text;
        console.log("SHAP Summary:",response.data.shap_summary_text);
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
          return value >= 18.5 && value <= 24.9;
        case 'Alcohol (drinks/week)':
          return value <= 3;
        case 'Sleep (hours/day)':
          return value >= 6 && value <= 10;
        case 'Smoking':
          return value === 'Not at all';
        case 'Diabetes':
          return value === 'No';
        case 'Kidney Disease':
          return value === 'No';
        case 'Stroke':
          return value === 'No';
        case 'Exercise (min/week)':
          return value >150;
        case 'Fruit Intake (servings/day)':
          return value >= 5  ;
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
  color :	#c53030;
 
}
h1,h2 {
  font-family: 'Montserrat';
  font-size: larger;
  color :	#c53030;
}
input, textarea, button, label {
  font-family: 'Roboto', sans-serif;
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
  width: 30vw;
  background-color: white;
  color: red;
  padding: 20px;
  overflow-y: auto;
  height: 92vh;
  border-radius: 16px;
  border-color: red;
  margin-left: 20px;
  margin-top:20px;
}

/* Tooltip CSS in sidebar*/
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
.bmi input{
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
  width: 160px;
  background: #fff;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
}

/* Results Cards borders*/
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

/* Results Cards text*/
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
/* Layout Styles */
.container {
  display: flex;
  height: 100vh;
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
  background:whitesmoke;
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
  font: size 30px;;
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

</style>

