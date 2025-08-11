<template>
<!-- <Home msg="Welcome to Your Vue.js App" /> -->
    <div id="app">
    <router-view />
    <DisclaimerPopup v-if="showDisclaimer" @accepted="handleAccepted" />

    <div v-else>
      <nav class="navbar">
        <div class="navbar-left">
        <router-link to="/">
          <img :src="logoJGU" alt="Logo" class="logo" />
        </router-link>
        <a href="https://nightingaleheart.com/demos/healthlife" style="text-decoration:none"><v-btn class="button">Return to Healthlife</v-btn></a>
        </div>
        <div class="navbar-center">
          <router-link to="/" class="nav-link">Heart Disease Prediction App</router-link>
        </div>
        <div class="navbar-right">
          <router-link to="/info" class="nav-link">About Service</router-link>
        </div>
      </nav>
    </div>
  </div>
</template>

<script>
import DisclaimerPopup from './components/DisclaimerPopup.vue'
import logoJGU  from '@/assets/logoJGU.svg'

export default {
  name: 'App',
  components: {
    DisclaimerPopup
  },
  data() {
    return {
      showDisclaimer: true,
      logoJGU
    }
  },
  created() {
    const accepted = localStorage.getItem('disclaimerAccepted')
    if (accepted === 'true') {
      this.showDisclaimer = false
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
}

.navbar-left, .navbar-center, .navbar-right {
  flex: 1;
  display: flex;
  align-items: center;
}

.navbar-center {
  justify-content: center;
}

.navbar-right {
  justify-content: flex-end;
  margin-right: 3%;
}

.logo {
  height: 70px;
}
.button{
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
}

.nav-link:hover {
  text-decoration: underline;
}

</style>