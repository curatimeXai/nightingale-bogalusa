<template>
<!-- <Home msg="Welcome to Your Vue.js App" /> -->
    <div id="app">
    <DisclaimerPopup v-if="showDisclaimer" @accepted="handleAccepted" />

    <div v-else>
      <nav class="navbar">
        <div class="navbar-left">
        <img src="https://nightingale.uni-mainz.de/images/logoHigh.svg" alt="Logo" class="logo" />
        </div>
        <div class="navbar-right">
          <router-link to="/" class="nav-link">Home</router-link>
          <router-link to="/info" class="nav-link">About Service</router-link>
        </div>
      </nav>
      <router-view />
    </div>
  </div>
</template>

<script>
import DisclaimerPopup from './components/DisclaimerPopup.vue'

export default {
  name: 'App',
  components: {
    DisclaimerPopup
  },
  data() {
    return {
      showDisclaimer: true
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
  z-index: 1000;
}

.navbar-left {
  display: flex;
  align-items: center;
}

.logo {
  height: 70px;
}

.navbar-right {
  display: flex;
  justify-content: center; /* This will center the nav links horizontally */
  flex: 1; /* This makes the navbar-right container take up the available space */
  gap: 1rem;
}

.nav-link {
  text-decoration: none;
  color: #333;
  font-weight: bold;
}

.nav-link:hover {
  text-decoration: underline;
}

</style>