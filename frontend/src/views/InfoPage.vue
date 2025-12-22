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
        The AI model is trained based on a dataset from the Center of Disease Control Behavioural Risk Factors 
        Surveillance System (CDC BRFSS) called "Indicators of Heart Disease". The risk is calculated by an average of three models: SVM and XGBoost, the percentage for each risk factor came from shapley-scores.
        the participants were all US residents,and uses your personal input only for making predictions — not for training.
        
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
}}
</style>