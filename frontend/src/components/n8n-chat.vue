<template>
  <div id="n8n-chat"></div>
</template>

<script setup>
import { onMounted } from 'vue';
import '@n8n/chat/style.css';
import { createChat } from '@n8n/chat';

onMounted(() => {
  // Construye la URL completa del webhook
  const webhookUrl = `http://localhost:5678/webhook/53c136fe-3e77-4709-a143-fe82746dd8b6/chat`;

  createChat({
	webhookUrl: webhookUrl,
	webhookConfig: {
		method: 'POST',
		headers: {}
	},
	target: '#n8n-chat',
	mode: 'window',
	chatInputKey: 'chatInput',
	chatSessionKey: 'sessionId',
	metadata: {},
	showWelcomeScreen: false,
	defaultLanguage: 'en',
	initialMessages: [
		'Hi there PrintAI 👋',
		'How can I assist you today?'
	],
	i18n: {
		en: {
			title: 'Hi there 👋',
			subtitle: "Your Assistant for PrintAI",
			getStarted: 'New Conversation',
			inputPlaceholder: 'Type your question..',
		},
	},
});
});
</script>

<style scoped>
html, body, #n8n-chat {
  width: 100%;
  height: 100%;
  margin: 0;
}
</style>
