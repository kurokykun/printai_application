<template>
  <div id="app">
    <header class="app-header">
      <img src="./assets/logo.png" alt="Logo" class="logo" />
      <h1>PrintAI Chat</h1>
    </header>

    <main class="chat-container">
      <div class="chat-card">
        <N8nChat />
      </div>
    </main>

    <footer class="app-footer">
      <p>Powered by n8n & Vue.js</p>
    </footer>
  </div>
</template>

<script>
import N8nChat  from './components/n8n-chat.vue'

export default {
  name: 'App',
  components: {
    N8nChat
  }
}
</script>

<style>
/* Design Variables */
:root {
  --primary-color: #4a90e2;
  --secondary-color: #ffffff;
  --light-gray: #f0f2f5;
  --text-color: #2c3e50;
}

/* Global Styles */
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
  font-family: 'Roboto', sans-serif;
  background: var(--light-gray);
  color: var(--text-color);
}
#app {
  text-align: center;
  margin-top: 60px;
}
.app-header {
  display: flex;
  align-items: center;
  background: var(--primary-color);
  color: var(--secondary-color);
}
.logo {
  width: 40px;
  margin-right: 12px;
  filter: invert(1);
}
.app-header h1 {
  font-size: 1.5rem;
  color: var(--secondary-color);
  margin: 0;
}
.chat-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 112px); /* header + footer height */
}
.chat-card {
  width: 100%;
  max-width: 600px;
  height: 80%;
  background: var(--secondary-color);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  overflow: hidden;
  transition: box-shadow 0.3s ease;
}
.chat-card:hover {
  box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}
.app-footer {
  text-align: center;
  padding: 16px;
  background: #ffffff;
  color: #888;
  font-size: 0.9rem;
}
</style>
