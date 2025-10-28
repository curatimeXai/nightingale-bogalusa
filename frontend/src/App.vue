<template>
  <div id="app" :class="{ 'dark-mode': darkMode }">
    <DisclaimerPopup v-if="showDisclaimer" @accepted="handleAccepted" />

    <div v-else>
      <nav class="navbar">
        <div class="navbar-left">
          <router-link to="/">
            <img :src="logoJGU" alt="Logo" class="logo" />
          </router-link>
          <a href="https://nightingaleheart.com/demos/healthlife" style="text-decoration:none">
            <v-btn class="button">Return to Healthlife</v-btn>
          </a>
        </div>
        <div class="navbar-center">
          <router-link to="/" class="nav-link">Heart Disease Prediction App</router-link>
          
          <!-- Dark Mode Toggle - Centered -->
          <button class="dark-mode-toggle" @click="darkMode = !darkMode">
            <span v-if="darkMode">☀️</span>
            <span v-else>🌙</span>
          </button>
        </div>
        <div class="navbar-right">
          <router-link to="/info" class="nav-link">About Service</router-link>
        </div>
      </nav>
      
      <router-view :dark-mode="darkMode" />
    </div>
  </div>
</template>

<script>
import DisclaimerPopup from './components/DisclaimerPopup.vue'
import logoJGU from '@/assets/logoJGU.svg'

export default {
  name: 'App',
  components: {
    DisclaimerPopup
  },
  data() {
    return {
      showDisclaimer: true,
      darkMode: true,
      logoJGU
    }
  },
  created() {
    const accepted = localStorage.getItem('disclaimerAccepted')
    if (accepted === 'true') {
      this.showDisclaimer = false
    }
    
    // Load dark mode preference
    const darkModePreference = localStorage.getItem('darkMode')
    if (darkModePreference !== null) {
      this.darkMode = darkModePreference === 'true'
    }
  },
  watch: {
    darkMode(newVal) {
      localStorage.setItem('darkMode', newVal.toString())
    }
  },
  methods: {
    handleAccepted(persistChoice) {
      if (persistChoice) {
        localStorage.setItem('disclaimerAccepted', 'true')
      }
      this.showDisclaimer = false
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  transition: background-color 0.3s ease, color 0.3s ease;
  min-height: 100vh;
}

#app.dark-mode {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  color: #f1f5f9;
}

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 90px;
  background-color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 1.5rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  border-bottom: 4px solid red;
  z-index: 1000;
  transition: background-color 0.3s ease;
}

.dark-mode .navbar {
  background-color: #1e293b;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
}

.navbar-left, .navbar-center, .navbar-right {
  flex: 1;
  display: flex;
  align-items: center;
}

.navbar-center {
  justify-content: center;
  position: relative;
}

.navbar-right {
  justify-content: flex-end;
  margin-right: 3%;
}

.logo {
  height: 70px;
}

.button {
  margin-left: 10px;
  margin-right: 10px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: #c1002a;
  color: white;
  border: none;
  border-radius: 5px;
  position: relative;
  z-index: 100;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.button:hover {
  background-color: #a11b1b;
}

.nav-link {
  text-decoration: none;
  color: #333;
  font-weight: bold;
  font-size: 26px;
  padding: 0 10px;
  transition: color 0.3s ease;
}

.dark-mode .nav-link {
  color: #f1f5f9;
}

.nav-link:hover {
  text-decoration: underline;
}

/* Dark Mode Toggle Button - Centered in navbar-center */
.dark-mode-toggle {
  position: absolute;
  right: -80px;
  background: #14b8a6;
  border: none;
  border-radius: 50%;
  width: 45px;
  height: 45px;
  font-size: 22px;
  cursor: pointer;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1001;
}

.dark-mode-toggle:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 12px -2px rgba(0, 0, 0, 0.4);
  background: #0f766e;
}

/* Responsive adjustments */
@media (max-width: 1024px) {
  .navbar-center {
    flex-direction: column;
    gap: 10px;
  }
  
  .dark-mode-toggle {
    position: static;
    margin-top: 5px;
  }
  
  .nav-link {
    font-size: 20px;
  }
}

@media (max-width: 768px) {
  .navbar {
    height: auto;
    flex-direction: column;
    padding: 1rem;
  }
  
  .navbar-left, .navbar-center, .navbar-right {
    justify-content: center;
    margin: 0.5rem 0;
  }
  
  .navbar-center {
    order: 1;
  }
  
  .navbar-left {
    order: 2;
  }
  
  .navbar-right {
    order: 3;
    margin-right: 0;
  }
  
  .dark-mode-toggle {
    position: static;
    margin-top: 10px;
  }
}
</style>