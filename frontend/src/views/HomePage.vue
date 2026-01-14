<template>
  <Disclaimer v-if="showDisclaimer" @accepted="showDisclaimer = false" />
  <div id="home-app" :class="{ 'dark-mode': darkMode }">
    <div class="container">
      <!-- Sidebar -->
      <div class="sidebar">
        <h2> Enter Your Health & Lifestyle Information</h2>
        <form @submit.prevent="computeRisk" class="scrollable-form">
          
          <!-- CONTEXT CATEGORY -->
          <div class="feature-category">
            <h3 class="category-title"> Context</h3>
            
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
            <h3 class="category-title"> Lifestyle</h3>
            
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
          
          <!-- BMI Display -->
          <div v-if="calculatedBMI" class="bmi-display">
            <h4>📊 Your BMI</h4>
            <div class="bmi-value" :class="bmiCategory.class">
              {{ calculatedBMI }}
            </div>
            <div class="bmi-category">{{ bmiCategory.label }}</div>
          </div>

          <!-- MEDICAL RISK FACTORS CATEGORY -->
          <div class="feature-category">
            <h3 class="category-title"> Medical Risk Factors</h3>
            
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
            <h3 class="category-title"> Environmental</h3>
            
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

          <button type="submit"> Analyze</button>
          <button type="button" @click="randomizeData"> Randomize</button>
        </form>
      </div>

      <!-- Results -->
      <div class="results">
        <h2> Heart Disease Risk Prediction Results</h2>
        <p>Based on your health data, here's how your lifestyle factors contribute to your risk</p>

        <div v-if="result">
          <div class="results-layout">
            <!-- Negative Factors -->
            <div class="negative-factors">
              <h3>🛑 Negative Factors</h3>
              <div class="factors-column">
                <div v-for="(value, key, index) in negativeFactors" 
                     :key="key" 
                     class="result-card card-negative"
                     :style="{ animationDelay: `${index * 0.15}s` }">
                  <i class="bi bi-hand-thumbs-down-fill negative-icon"></i>
                  <div class="result-content">
                    <strong>{{ key }}</strong>: {{ value.text }}
                    <div class="negative">{{ value.percentage.toFixed(2) }}%</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Positive Factors -->
            <div class="positive-factors">
              <h3>✅ Favorable Factors</h3>
              <div class="factors-column">
                <div v-for="(value, key, index) in positiveFactors" 
                     :key="key" 
                     class="result-card card-positive"
                     :style="{ animationDelay: `${index * 0.15}s` }">
                  <i class="bi bi-hand-thumbs-up-fill positive-icon"></i>
                  <div class="result-content">
                    <strong>{{ key }}</strong>: {{ value.text }}
                    <div class="positive">{{ value.percentage.toFixed(2) }}%</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Risk Score Section -->
          <div class="risk-score-section" v-if="result && result.risk !== undefined">
            <div class="risk-level-badge" :class="getRiskLevelClass(result.risk)">
              <div class="risk-badge-icon">{{ getRiskIcon(result.risk) }}</div>
              <h3>{{ getRiskLevelLabel(result.risk) }}</h3>
              <div class="risk-score-value">
                {{ (result.risk * 100).toFixed(1) }}%
              </div>
              <p>{{ getRiskDescription(result.risk) }}</p>
            </div>
          </div>

          <!-- Tab Navigation -->
          <div class="tab-navigation">
            <button 
              :class="{ active: activeTab === 'table' }" 
              @click="activeTab = 'table'">
              📋 Table View
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
                    <span class="impact-percentage">({{ item.value.percentage > 0 ? '+' : '' }}{{ item.value.percentage.toFixed(1) }}%)</span>
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
          <div v-show="activeTab === 'chart'" class="shap-section">
            <h3> Interactive Risk Analysis</h3>

            <!-- Interactive Chart -->
            <div class="interactive-chart-container">
              <canvas ref="riskChart"></canvas>
            </div>

            <div v-if="isValidBase64(result.shap_plot)">
              <h4>Detailed SHAP Analysis</h4>
              <img :src="'data:image/png;base64,' + result.shap_plot" alt="SHAP Impact Chart" />
            </div>

            <!-- Info Box -->
            <div class="info-box">
              <h5>ℹ️ How This Chart Works</h5>
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
import Chart from 'chart.js/auto';

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
      riskChartInstance: null,
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
        BMI: "Maintain healthy BMI (18.5-24.9).",
        HighBloodPressure: "Control blood pressure to protect heart.",
        Diabetes: "Healthy diet and activity prevent type 2 diabetes.",
        Noise: "Chronic noise exposure may affect cardiovascular health."
      }
    };
  },
  computed: {
    calculatedBMI() {
      if (this.formData.Height && this.formData.Weight) {
        const heightInMeters = this.formData.Height / 100;
        const bmi = this.formData.Weight / (heightInMeters * heightInMeters);
        return bmi.toFixed(1);
      }
      return null;
    },

    bmiCategory() {
      const bmi = parseFloat(this.calculatedBMI);
      if (!bmi) return { label: '', class: '' };
      if (bmi < 18.5) return { label: 'Underweight', class: 'bmi-underweight' };
      if (bmi < 25) return { label: 'Normal weight', class: 'bmi-normal' };
      if (bmi < 30) return { label: 'Overweight', class: 'bmi-overweight' };
      return { label: 'Obese', class: 'bmi-obese' };
    },

    formattedResults() {
      if (!this.result || !this.result.shap_impact) return {};
      const shap = this.result.shap_impact;

      const build = (label, value, shapVal) => {
        const actualShapVal = shapVal ?? 0;
        const absValue = Math.abs(actualShapVal);
        
        // Déterminer si c'est un facteur de risque basé UNIQUEMENT sur shapVal
        const isRiskFactor = actualShapVal > 0;
        
        return {
          text: value,
          percentage: actualShapVal,
          icon: isRiskFactor ? "👎" : "👍",
          forceRed: isRiskFactor,
          impact: this.getRiskLevel(absValue, actualShapVal)
        };
      };

      return {
        "Gender": build(
          "Gender",
          this.formData.Gender,
          shap.Gender
        ),
        "Age": build(
          "Age",
          this.formData.AgeCategory,
          shap.Age
        ),
        "Physical Activity": build(
          "PhysicalActivity",
          `${this.formData.PhysicalActivityDays} days/week`,
          shap.PhysicalActivityDays
        ),
        "Fruit Intake": build(
          "Fruit",
          this.formData.FruitFrequency,
          shap.FruitFrequency
        ),
        "BMI": build(
          "BMI",
          this.calculatedBMI ? `${this.calculatedBMI}` : "—",
          shap.BMI
        ),
        "Vegetable Intake": build(
          "Vegetables",
          this.formData.VegetableFrequency,
          shap.VegetableFrequency
        ),
        "Smoking": build(
          "Smoking",
          this.formData.Smoking,
          shap.Smoking
        ),
        "Alcohol": build(
          "Alcohol",
          this.formData.AlcoholFrequency,
          shap.AlcoholFrequency
        ),
        "High Blood Pressure": build(
          "HighBloodPressure",
          this.formData.HighBloodPressure ? "Yes" : "No",
          shap.HighBloodPressure
        ),
        "Diabetes": build(
          "Diabetes",
          this.formData.Diabetes ? "Yes" : "No",
          shap.Diabetes
        ),
        "Noise Problems": build(
          "Noise",
          this.formData.NoiseProblems ? "Yes" : "No",
          shap.NoiseProblems
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
  watch: {
    result() {
      if (this.result && this.activeTab === 'chart') {
        this.$nextTick(() => {
          this.renderRiskChart();
        });
      }
    },
    activeTab(newTab) {
      if (newTab === 'chart' && this.result) {
        this.$nextTick(() => {
          this.renderRiskChart();
        });
      }
    }
  },
  beforeUnmount() {
    if (this.riskChartInstance) {
      this.riskChartInstance.destroy();
    }
  },

  methods: {
    renderRiskChart() {
      if (!this.$refs.riskChart) return;
      
      if (this.riskChartInstance) {
        this.riskChartInstance.destroy();
      }

      const ctx = this.$refs.riskChart.getContext('2d');
      const sortedData = this.sortedResults.slice(0, 10);
      const labels = sortedData.map(item => item.key);
      
      const negativeValues = sortedData.map(item => 
        item.value.forceRed ? Math.abs(item.value.percentage) : 0
      );
      
      const positiveValues = sortedData.map(item => 
        !item.value.forceRed ? Math.abs(item.value.percentage) : 0
      );

      this.riskChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Risk Increasing',
              data: negativeValues,
              backgroundColor: 'rgba(239, 68, 68, 0.85)',
              borderColor: '#dc2626',
              borderWidth: 2,
              borderRadius: 8,
              barThickness: 25,
              categoryPercentage: 0.9,
              barPercentage: 0.85
            },
            {
              label: 'Risk Reducing',
              data: positiveValues.map(v => -v),
              backgroundColor: 'rgba(34, 197, 94, 0.85)',
              borderColor: '#16a34a',
              borderWidth: 2,
              borderRadius: 8,
              barThickness: 25,
              categoryPercentage: 0.9,
              barPercentage: 0.85
            }
          ]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          interaction: {
            mode: 'nearest',
            intersect: true,
          },
          plugins: {
            legend: {
              display: true,
              position: 'top',
              labels: {
                font: { size: 14, weight: '600' },
                padding: 20,
                usePointStyle: true,
                pointStyle: 'rectRounded',
                boxWidth: 15,
                boxHeight: 15
              }
            },
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.9)',
              padding: 14,
              cornerRadius: 10,
              titleFont: { size: 14, weight: 'bold' },
              bodyFont: { size: 13 },
              callbacks: {
                label: function(context) {
                  let label = context.dataset.label || '';
                  let value = Math.abs(context.parsed.x);
                  return label + ': ' + value.toFixed(2) + '%';
                }
              }
            }
          },
          scales: {
            x: {
              stacked: false,
              grid: { 
                display: true,
                color: 'rgba(0, 0, 0, 0.05)',
                lineWidth: 1
              },
              ticks: {
                callback: function(value) {
                  return Math.abs(value) + '%';
                },
                font: { size: 12, weight: '600' }
              },
              title: {
                display: true,
                text: 'Impact on Risk (%)',
                font: { size: 14, weight: 'bold' },
                padding: 10
              }
            },
            y: {
              stacked: false,
              grid: { display: false },
              ticks: {
                font: { size: 13, weight: '600' },
                padding: 15,
                autoSkip: false
              },
              afterFit: function(scale) {
                scale.width = 180;
              }
            }
          },
          layout: {
            padding: {
              left: 10,
              right: 30,
              top: 10,
              bottom: 10
            }
          }
        }
      });
    },

    getGuideline(key) {
      const map = {
        "Gender": "Gender",
        "Age": "Age",
        "BMI": "BMI",
        "Physical Activity": "PhysicalActivity",
        "Fruit Intake": "Fruit",
        "Vegetable Intake": "Vegetables",
        "Smoking": "Smoking",
        "Alcohol": "Alcohol",
        "High Blood Pressure": "HighBloodPressure",
        "Diabetes": "Diabetes",
        "Noise Problems": "Noise"
      };
      return this.whoGuidelines[map[key]] || "—";
    },

    getRiskLevel(value, shapVal) {
      // Si shapVal est positif, c'est un facteur de RISQUE (augmente le risque)
      // Si shapVal est négatif, c'est un facteur PROTECTEUR (diminue le risque)
      if (shapVal > 0) {
        // Facteur de risque - rouge/orange selon l'intensité
        if (value >= 5) return "risk-level-high";
        if (value >= 2) return "risk-level-medium";
        return "risk-level-medium";
      } else {
        // Facteur protecteur - toujours vert (bon pour la santé)
        return "risk-level-low";
      }
    },

    getRiskLevelClass(risk) {
      const riskPercent = risk * 100;
      if (riskPercent < 10) return 'low';
      if (riskPercent < 30) return 'mid';
      return 'high';
    },

    getRiskIcon(risk) {
      const riskPercent = risk * 100;
      if (riskPercent < 10) return '✅';
      if (riskPercent < 30) return '⚠️';
      return '🚨';
    },

    getRiskLevelLabel(risk) {
      const riskPercent = risk * 100;
      if (riskPercent < 10) return 'Low Risk';
      if (riskPercent < 30) return 'Medium Risk';
      return 'High Risk';
    },

    getRiskDescription(risk) {
      const riskPercent = risk * 100;
      if (riskPercent < 10) return 'Your heart disease risk is low. Keep maintaining healthy habits!';
      if (riskPercent < 30) return 'Your risk is moderate. Consider improving key lifestyle factors.';
      return 'Your risk is elevated. Consult a healthcare professional for personalized advice.';
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
        "Gender": this.formData.Gender,
        "Age of respondent, calculated": ageMapping[this.formData.AgeCategory],
        "Do sports or other physical activity, how many of last 7 days": this.formData.PhysicalActivityDays,
        "How often eat fruit, excluding drinking juice": this.formData.FruitFrequency,
        "How often eat vegetables or salad, excluding potatoes": this.formData.VegetableFrequency,
        "Cigarette smoking behaviour": this.formData.Smoking,
        "How often drink alcohol": this.formData.AlcoholFrequency,
        "Height of respondent (cm)": this.formData.Height,
        "Weight of respondent (kg)": this.formData.Weight,
        "Health problems, last 12 months: high blood pressure": this.formData.HighBloodPressure ? "Marked" : "Not marked",
        "Health problems, last 12 months: diabetes": this.formData.Diabetes ? "Marked" : "Not marked",
        "Problems with accomodation: noise": this.formData.NoiseProblems ? "Marked" : "Not marked"
      };

      try {
        const response = await axios.post("https://bogalusabackend.nightingaleheart.com/predict",apiData,);
        
        const data = response.data;
        
        console.log("📥 Data received from backend:", data);
        data.shap_impact = mapBackendToFrontend(data.feature_impacts_percent);

        this.result = data;
        
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

function mapBackendToFrontend(raw) {
  return {
    Gender: raw["Gender"],
    Age: raw["Age of respondent, calculated"],
    PhysicalActivityDays: raw["Do sports or other physical activity, how many of last 7 days"],
    FruitFrequency: raw["How often eat fruit, excluding drinking juice"],
    VegetableFrequency: raw["How often eat vegetables or salad, excluding potatoes"],
    Smoking: raw["Cigarette smoking behaviour"],
    AlcoholFrequency: raw["How often drink alcohol"],
    BMI: raw["BMI"],
    HighBloodPressure: raw["Health problems, last 12 months: high blood pressure"],
    Diabetes: raw["Health problems, last 12 months: diabetes"],
    NoiseProblems: raw["Problems with accomodation: noise"]
  };
}

</script>

<style scoped>
/* Base Styles */
/* ===== BASE STYLES ===== */
/* ===== BASE STYLES ===== */
#home-app {
	background: #e0e5ec;
	min-height: 100vh;
	margin: 0;
	padding: 20px 0;
	font-family: "Inter", "Segoe UI", sans-serif;
	color: #5a6f88;
	transition: all 0.3s ease;
}

#home-app.dark-mode {
	background: #2c3e50;
	color: #ecf0f1;
}

h2,
h3,
h4 {
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

/* ===== CONTAINER ===== */
.container {
	display: grid;
	grid-template-columns: 400px 1fr;
	gap: 24px;
	max-width: 1600px;
	margin: 0 auto;
	padding: 0 20px;
}

/* ===== SIDEBAR - NEUMORPHIC ===== */
.sidebar {
	background: #e0e5ec;
	padding: 28px;
	border-radius: 40px;
	box-shadow:
		10px 10px 20px rgba(184, 197, 214, 0.8),
		-10px -10px 20px rgba(255, 255, 255, 0.9);
	height: fit-content;
	max-height: calc(100vh - 140px);
	position: sticky;
	top: 110px;
	display: flex;
	flex-direction: column;
}

.dark-mode .sidebar {
	background: #2c3e50;
	box-shadow:
		10px 10px 20px rgba(0, 0, 0, 0.3),
		-10px -10px 20px rgba(255, 255, 255, 0.05);
}

.sidebar h2 {
	color: #5a6f88;
	text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.5);
	padding-bottom: 12px;
	margin-bottom: 24px;
	border-bottom: 2px solid #667eea;
}

.dark-mode .sidebar h2 {
	color: #ecf0f1;
	text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

/* ===== SCROLLABLE FORM ===== */
.scrollable-form {
	overflow-y: auto;
	padding-right: 12px;
	flex: 1;
}

.scrollable-form::-webkit-scrollbar {
	width: 8px;
}

.scrollable-form::-webkit-scrollbar-track {
	background: #e0e5ec;
	border-radius: 10px;
}

.scrollable-form::-webkit-scrollbar-thumb {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	border-radius: 10px;
}

/* ===== FEATURE CATEGORIES - INSET ===== */
.feature-category {
	margin-bottom: 28px;
	padding: 20px;
	background: #e0e5ec;
	border-radius: 25px;
	box-shadow:
		inset 5px 5px 10px rgba(184, 197, 214, 0.5),
		inset -5px -5px 10px rgba(255, 255, 255, 0.3);
}

.dark-mode .feature-category {
	background: #2c3e50;
	box-shadow:
		inset 5px 5px 10px rgba(0, 0, 0, 0.3),
		inset -5px -5px 10px rgba(255, 255, 255, 0.05);
}

.category-title {
	color: #667eea;
	font-size: 16px;
	margin-bottom: 20px;
	padding-bottom: 10px;
	border-bottom: 2px solid #667eea;
	text-transform: uppercase;
	letter-spacing: 0.05em;
}

/* ===== FEATURE ITEMS ===== */
.feature-item {
	margin-bottom: 18px;
}

.feature-item label {
	display: block;
	font-weight: 600;
	color: #5a6f88;
	margin-bottom: 10px;
	font-size: 14px;
}

.dark-mode .feature-item label {
	color: #cbd5e1;
}

/* ===== INPUTS - INSET NEUMORPHIC ===== */
.feature-item input,
.feature-item select {
	width: 100%;
	padding: 12px 16px;
	border: none;
	border-radius: 15px;
	font-size: 15px;
	background: #e0e5ec;
	color: #5a6f88;
	font-weight: 500;
	box-shadow:
		inset 3px 3px 6px rgba(184, 197, 214, 0.5),
		inset -3px -3px 6px rgba(255, 255, 255, 0.5);
	transition: all 0.3s ease;
}

.dark-mode .feature-item input,
.dark-mode .feature-item select {
	background: #2c3e50;
	color: #ecf0f1;
	box-shadow:
		inset 3px 3px 6px rgba(0, 0, 0, 0.3),
		inset -3px -3px 6px rgba(255, 255, 255, 0.05);
}

.feature-item input:focus,
.feature-item select:focus {
	outline: none;
	box-shadow:
		inset 5px 5px 10px rgba(184, 197, 214, 0.6),
		inset -5px -5px 10px rgba(255, 255, 255, 0.6),
		0 0 0 3px rgba(102, 126, 234, 0.2);
}

/* ===== BUTTON GROUPS ===== */
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
	background: #e0e5ec;
	color: #5a6f88;
	border: none;
	border-radius: 15px;
	cursor: pointer;
	font-weight: 600;
	font-size: 14px;
	box-shadow:
		5px 5px 10px rgba(184, 197, 214, 0.8),
		-5px -5px 10px rgba(255, 255, 255, 0.9);
	transition: all 0.2s ease;
}

.dark-mode .button-group button {
	background: #2c3e50;
	color: #cbd5e1;
	box-shadow:
		5px 5px 10px rgba(0, 0, 0, 0.3),
		-5px -5px 10px rgba(255, 255, 255, 0.05);
}

.button-group button:hover {
	transform: translateY(-2px);
}

.button-group button.active {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: white;
	box-shadow:
		inset 3px 3px 6px rgba(0, 0, 0, 0.3),
		inset -3px -3px 6px rgba(255, 255, 255, 0.2),
		0 0 0 2px rgba(102, 126, 234, 0.5);
	transform: scale(0.98);
}

.dark-mode .button-group button.active {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: white;
	box-shadow:
		inset 4px 4px 8px rgba(0, 0, 0, 0.5),
		inset -4px -4px 8px rgba(255, 255, 255, 0.1),
		0 0 0 3px rgba(102, 126, 234, 0.6),
		0 0 20px rgba(102, 126, 234, 0.4);
	transform: scale(0.98);
}

/* ===== BMI DISPLAY ===== */
.bmi-display {
	background: #e0e5ec;
	border-radius: 25px;
	padding: 20px;
	margin: 20px 0;
	text-align: center;
	box-shadow:
		8px 8px 16px rgba(184, 197, 214, 0.8),
		-8px -8px 16px rgba(255, 255, 255, 0.9);
}

.dark-mode .bmi-display {
	background: #2c3e50;
	box-shadow:
		8px 8px 16px rgba(0, 0, 0, 0.3),
		-8px -8px 16px rgba(255, 255, 255, 0.05);
}

.bmi-display h4 {
	color: #667eea;
	font-size: 16px;
	margin-bottom: 12px;
	text-transform: uppercase;
}

.bmi-value {
	font-size: 42px;
	font-weight: 900;
	margin: 12px 0;
}

.bmi-category {
	font-size: 16px;
	font-weight: 600;
	margin-top: 8px;
	text-transform: uppercase;
}

.bmi-underweight {
	color: #f59e0b;
}
.bmi-normal {
	color: #10b981;
}
.bmi-overweight {
	color: #f59e0b;
}
.bmi-obese {
	color: #ef4444;
}

/* ===== SUBMIT BUTTONS ===== */
button[type="submit"] {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: white;
	border: none;
	padding: 16px 24px;
	width: 100%;
	border-radius: 25px;
	cursor: pointer;
	font-weight: 700;
	font-size: 16px;
	box-shadow:
		8px 8px 16px rgba(184, 197, 214, 0.8),
		-8px -8px 16px rgba(255, 255, 255, 0.9);
	text-transform: uppercase;
	margin-top: 8px;
	transition: all 0.3s ease;
}

button[type="submit"]:hover {
	transform: translateY(-3px);
	box-shadow:
		10px 10px 20px rgba(184, 197, 214, 0.9),
		-10px -10px 20px rgba(255, 255, 255, 1);
}

button[type="submit"]:active {
	transform: scale(0.98);
	box-shadow:
		inset 5px 5px 10px rgba(0, 0, 0, 0.2),
		inset -5px -5px 10px rgba(255, 255, 255, 0.1);
}

button[type="button"] {
	background: #e0e5ec;
	color: #5a6f88;
	border: none;
	padding: 14px 20px;
	border-radius: 25px;
	cursor: pointer;
	font-weight: 600;
	box-shadow:
		6px 6px 12px rgba(184, 197, 214, 0.8),
		-6px -6px 12px rgba(255, 255, 255, 0.9);
	margin-top: 12px;
	width: 100%;
	transition: all 0.3s ease;
}

.dark-mode button[type="button"] {
	background: #2c3e50;
	color: #cbd5e1;
	box-shadow:
		6px 6px 12px rgba(0, 0, 0, 0.3),
		-6px -6px 12px rgba(255, 255, 255, 0.05);
}

button[type="button"]:hover {
	transform: translateY(-2px);
}

/* ===== RESULTS SECTION ===== */
.results {
	background: #e0e5ec;
	padding: 32px;
	border-radius: 40px;
	box-shadow:
		10px 10px 20px rgba(184, 197, 214, 0.8),
		-10px -10px 20px rgba(255, 255, 255, 0.9);
}

.dark-mode .results {
	background: #2c3e50;
	box-shadow:
		10px 10px 20px rgba(0, 0, 0, 0.3),
		-10px -10px 20px rgba(255, 255, 255, 0.05);
}

.results h2 {
	color: #5a6f88;
	font-size: 28px;
	margin-bottom: 8px;
}

.dark-mode .results h2 {
	color: #ecf0f1;
}

.results > p {
	color: #64748b;
	font-size: 16px;
	margin-bottom: 32px;
}

/* ===== EMPTY STATE ===== */
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
	color: #5a6f88;
	font-size: 24px;
	margin-bottom: 12px;
}

.dark-mode .empty-state h3 {
	color: #ecf0f1;
}

.empty-state p {
	color: #64748b;
	font-size: 16px;
	max-width: 500px;
	margin: 0 auto;
}

/* ===== RESULTS LAYOUT ===== */
.results-layout {
	display: grid;
	grid-template-columns: 1fr 1fr;
	gap: 24px;
	margin-bottom: 32px;
}

.negative-factors,
.positive-factors {
	padding: 24px;
	border-radius: 25px;
	box-shadow:
		inset 5px 5px 10px rgba(184, 197, 214, 0.5),
		inset -5px -5px 10px rgba(255, 255, 255, 0.3);
}

.negative-factors {
	background: #e0e5ec;
}

.dark-mode .negative-factors {
	background: #2c3e50;
	box-shadow:
		inset 5px 5px 10px rgba(0, 0, 0, 0.3),
		inset -5px -5px 10px rgba(255, 255, 255, 0.05);
}

.negative-factors h3 {
	color: #ef4444;
	display: flex;
	align-items: center;
	gap: 8px;
	font-size: 18px;
	margin-bottom: 20px;
}

.positive-factors {
	background: #e0e5ec;
}

.dark-mode .positive-factors {
	background: #2c3e50;
	box-shadow:
		inset 5px 5px 10px rgba(0, 0, 0, 0.3),
		inset -5px -5px 10px rgba(255, 255, 255, 0.05);
}

.positive-factors h3 {
	color: #10b981;
	display: flex;
	align-items: center;
	gap: 8px;
	font-size: 18px;
	margin-bottom: 20px;
}

/* ===== RESULT CARDS ===== */
.result-card {
	display: grid;
	grid-template-columns: 40px 1fr 40px;
	align-items: center;
	gap: 16px;
	padding: 16px 20px;
	border-radius: 20px;
	background: #e0e5ec;
	box-shadow:
		5px 5px 10px rgba(184, 197, 214, 0.8),
		-5px -5px 10px rgba(255, 255, 255, 0.9);
	margin-bottom: 12px;
	transition: all 0.2s ease;
	opacity: 0;
	transform: translateX(-30px);
	animation: slideInLeft 0.5s ease forwards;
}

.card-positive {
	transform: translateX(30px);
	animation: slideInRight 0.5s ease forwards;
}

@keyframes slideInLeft {
	from {
		opacity: 0;
		transform: translateX(-30px);
	}
	to {
		opacity: 1;
		transform: translateX(0);
	}
}

@keyframes slideInRight {
	from {
		opacity: 0;
		transform: translateX(30px);
	}
	to {
		opacity: 1;
		transform: translateX(0);
	}
}

.dark-mode .result-card {
	background: #2c3e50;
	box-shadow:
		5px 5px 10px rgba(0, 0, 0, 0.3),
		-5px -5px 10px rgba(255, 255, 255, 0.05);
}

.result-card:hover {
	transform: translateY(-2px);
}

.positive-icon,
.negative-icon {
	font-size: 28px;
	animation: iconPop 0.6s ease forwards;
}

@keyframes iconPop {
	0% {
		transform: scale(0);
		opacity: 0;
	}
	50% {
		transform: scale(1.2);
	}
	100% {
		transform: scale(1);
		opacity: 1;
	}
}

.positive-icon {
	color: #10b981;
}
.negative-icon {
	color: #ef4444;
}

.result-content strong {
	display: block;
	font-size: 15px;
	font-weight: 700;
	margin-bottom: 4px;
	color: #5a6f88;
	text-align: center;
}

.dark-mode .result-content strong {
	color: #ecf0f1;
}

.result-content .positive,
.result-content .negative {
	font-size: 18px;
	font-weight: 800;
	margin-top: 8px;
	animation: numberCount 0.8s ease forwards;
}

@keyframes numberCount {
	from {
		opacity: 0;
		transform: scale(0.5);
	}
	to {
		opacity: 1;
		transform: scale(1);
	}
}

/* ===== RISK SCORE SECTION ===== */
.risk-score-section {
	margin: 32px 0 24px 0;
	display: flex;
	justify-content: center;
}

.risk-level-badge {
	padding: 32px 48px;
	border-radius: 30px;
	text-align: center;
	width: 100%;
	background: #e0e5ec;
	box-shadow:
		10px 10px 20px rgba(184, 197, 214, 0.8),
		-10px -10px 20px rgba(255, 255, 255, 0.9);
}

.dark-mode .risk-level-badge {
	background: #2c3e50;
	box-shadow:
		10px 10px 20px rgba(0, 0, 0, 0.3),
		-10px -10px 20px rgba(255, 255, 255, 0.05);
}

.risk-badge-icon {
	font-size: 64px;
	margin-bottom: 16px;
	animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
	0%,
	100% {
		transform: scale(1);
	}
	50% {
		transform: scale(1.1);
	}
}

.risk-level-badge.low {
	border-left: 6px solid #10b981;
}
.risk-level-badge.mid {
	border-left: 6px solid #f59e0b;
}
.risk-level-badge.high {
	border-left: 6px solid #ef4444;
}

.risk-level-badge h3 {
	font-size: 24px;
	font-weight: 800;
	text-transform: uppercase;
	margin-bottom: 16px;
}

.risk-level-badge.low h3 {
	color: #10b981;
}
.risk-level-badge.mid h3 {
	color: #f59e0b;
}
.risk-level-badge.high h3 {
	color: #ef4444;
}

.risk-score-value {
	font-size: 48px;
	font-weight: 900;
	margin: 20px 0;
	color: #5a6f88;
}

.dark-mode .risk-score-value {
	color: #ecf0f1;
}

/* ===== TAB NAVIGATION ===== */
.tab-navigation {
	display: flex;
	gap: 12px;
	margin: 32px 0 0 0;
}

.tab-navigation button {
	background: #e0e5ec;
	color: #5a6f88;
	border: none;
	padding: 16px 32px;
	cursor: pointer;
	font-size: 16px;
	font-weight: 600;
	border-radius: 20px;
	box-shadow:
		5px 5px 10px rgba(184, 197, 214, 0.8),
		-5px -5px 10px rgba(255, 255, 255, 0.9);
	transition: all 0.3s ease;
}

.dark-mode .tab-navigation button {
	background: #2c3e50;
	color: #cbd5e1;
	box-shadow:
		5px 5px 10px rgba(0, 0, 0, 0.3),
		-5px -5px 10px rgba(255, 255, 255, 0.05);
}

.tab-navigation button:hover {
	transform: translateY(-2px);
}

.tab-navigation button.active {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: white;
	box-shadow:
		inset 3px 3px 6px rgba(0, 0, 0, 0.2),
		inset -3px -3px 6px rgba(255, 255, 255, 0.1);
}

/* ===== RESULTS CONTAINER ===== */
.results-container {
	margin-top: 32px;
}

.results-container h3 {
	font-size: 22px;
	color: #5a6f88;
	margin-bottom: 24px;
	padding-bottom: 12px;
	border-bottom: 2px solid #667eea;
}

.dark-mode .results-container h3 {
	color: #ecf0f1;
}

/* ===== IMPACT TABLE ===== */
.impact-table {
	width: 100%;
	border-collapse: separate;
	border-spacing: 0;
	margin-top: 20px;
	background: #e0e5ec;
	border-radius: 25px;
	overflow: hidden;
	box-shadow:
		8px 8px 16px rgba(184, 197, 214, 0.8),
		-8px -8px 16px rgba(255, 255, 255, 0.9);
}

.dark-mode .impact-table {
	background: #2c3e50;
	box-shadow:
		8px 8px 16px rgba(0, 0, 0, 0.3),
		-8px -8px 16px rgba(255, 255, 255, 0.05);
}

.impact-table thead {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: white;
}

.impact-table th {
	padding: 18px 20px;
	text-align: left;
	font-weight: 700;
	text-transform: uppercase;
	font-size: 13px;
	letter-spacing: 0.1em;
}

.impact-table td {
	padding: 18px 20px;
	font-size: 15px;
	color: #5a6f88;
}

.dark-mode .impact-table td {
	color: #ecf0f1;
}

.impact-table tbody tr {
	transition: all 0.2s ease;
}

.impact-table tbody tr:hover {
	background: rgba(102, 126, 234, 0.1);
	transform: scale(1.01);
}

.rank-cell {
	font-weight: 800;
	font-size: 18px;
	color: #667eea;
	text-align: center;
	width: 60px;
}

.guideline-text {
	color: #64748b;
	font-size: 13px;
	font-style: italic;
}

.impact-percentage {
	display: inline-block;
	margin-left: 8px;
	font-size: 12px;
	font-weight: 700;
	opacity: 0.8;
}

/* ===== RISK LEVELS ===== */
.risk-level-high {
	background: linear-gradient(135deg, #fca5a5 0%, #ef4444 100%);
	color: #991b1b;
	padding: 8px 16px;
	border-radius: 15px;
	font-weight: 700;
	display: inline-flex;
	align-items: center;
	gap: 6px;
	box-shadow:
		3px 3px 6px rgba(184, 197, 214, 0.5),
		-3px -3px 6px rgba(255, 255, 255, 0.5);
}

.risk-level-high::before {
	content: "⚠️";
}

.risk-level-medium {
	background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
	color: #92400e;
	padding: 8px 16px;
	border-radius: 15px;
	font-weight: 700;
	display: inline-flex;
	align-items: center;
	gap: 6px;
	box-shadow:
		3px 3px 6px rgba(184, 197, 214, 0.5),
		-3px -3px 6px rgba(255, 255, 255, 0.5);
}

.risk-level-medium::before {
	content: "⚡";
}

.risk-level-low {
	background: linear-gradient(135deg, #86efac 0%, #10b981 100%);
	color: #065f46;
	padding: 8px 16px;
	border-radius: 15px;
	font-weight: 700;
	display: inline-flex;
	align-items: center;
	gap: 6px;
	box-shadow:
		3px 3px 6px rgba(184, 197, 214, 0.5),
		-3px -3px 6px rgba(255, 255, 255, 0.5);
}

.risk-level-low::before {
	content: "✓";
}

/* ===== SHAP SECTION ===== */
.shap-section {
	background: #e0e5ec;
	border-radius: 25px;
	padding: 32px;
	margin-top: 24px;
	box-shadow:
		inset 5px 5px 10px rgba(184, 197, 214, 0.5),
		inset -5px -5px 10px rgba(255, 255, 255, 0.3);
}

.dark-mode .shap-section {
	background: #2c3e50;
	box-shadow:
		inset 5px 5px 10px rgba(0, 0, 0, 0.3),
		inset -5px -5px 10px rgba(255, 255, 255, 0.05);
}

.shap-section h3 {
	color: #667eea;
	font-size: 24px;
	margin-bottom: 24px;
	display: flex;
	align-items: center;
	gap: 12px;
}

.shap-section h3::before {
	font-size: 28px;
}

.shap-section h4 {
	color: #5a6f88;
	font-size: 18px;
	margin: 24px 0 12px 0;
	font-weight: 700;
}

.dark-mode .shap-section h4 {
	color: #ecf0f1;
}

.shap-section p {
	color: #5a6f88;
	font-size: 16px;
	line-height: 1.7;
}

.dark-mode .shap-section p {
	color: #cbd5e1;
}

.shap-section img {
	max-width: 100%;
	border-radius: 20px;
	box-shadow:
		8px 8px 16px rgba(184, 197, 214, 0.8),
		-8px -8px 16px rgba(255, 255, 255, 0.9);
	margin: 20px 0;
}

.dark-mode .shap-section img {
	box-shadow:
		8px 8px 16px rgba(0, 0, 0, 0.3),
		-8px -8px 16px rgba(255, 255, 255, 0.05);
}

/* ===== INTERACTIVE CHART ===== */
.interactive-chart-container {
	background: #e0e5ec;
	padding: 24px;
	border-radius: 20px;
	box-shadow:
		inset 5px 5px 10px rgba(184, 197, 214, 0.5),
		inset -5px -5px 10px rgba(255, 255, 255, 0.3);
	margin: 24px 0;
	min-height: 400px;
}

.dark-mode .interactive-chart-container {
	background: #2c3e50;
	box-shadow:
		inset 5px 5px 10px rgba(0, 0, 0, 0.3),
		inset -5px -5px 10px rgba(255, 255, 255, 0.05);
}

.interactive-chart-container canvas {
	max-height: 500px;
}

/* ===== INFO BOX ===== */
.info-box {
	background: #e0e5ec;
	border-radius: 20px;
	padding: 24px 28px;
	margin: 24px 0;
	box-shadow:
		6px 6px 12px rgba(184, 197, 214, 0.8),
		-6px -6px 12px rgba(255, 255, 255, 0.9);
}

.dark-mode .info-box {
	background: #2c3e50;
	box-shadow:
		6px 6px 12px rgba(0, 0, 0, 0.3),
		-6px -6px 12px rgba(255, 255, 255, 0.05);
}

.info-box h5 {
	color: #667eea;
	font-weight: 700;
	font-size: 18px;
	margin-bottom: 16px;
	display: flex;
	align-items: center;
	gap: 8px;
}

.info-box p {
	font-size: 15px;
	line-height: 1.6;
	color: #5a6f88;
	margin-bottom: 12px;
}

.dark-mode .info-box p {
	color: #cbd5e1;
}

.info-box ul {
	padding-left: 24px;
	margin: 16px 0;
}

.info-box li {
	font-size: 15px;
	line-height: 1.8;
	color: #5a6f88;
	margin-bottom: 8px;
}

.dark-mode .info-box li {
	color: #cbd5e1;
}

/* ===== RESPONSIVE ===== */
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

@media (max-width: 480px) {
	.container {
		padding: 0 12px;
	}

	.sidebar,
	.results {
		padding: 20px;
	}
}
</style>
