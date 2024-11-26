<template>
  <div class="chatbot-container">
      <!-- 챗봇이 열려있는 경우에만 표시 -->
      <div v-if="isChatOpen" class="chatbot">
          <div class="chat-log" ref="chatLog">
              <div v-for="(message, index) in messages" :key="index" :class="['message', message.role]">
                  <p>{{ message.content }}</p>
              </div>
          </div>
          <div class="chat-input-container">
            <textarea
              v-model="userMessage"
              @keyup.enter="sendMessage"
              placeholder="챗봇에게 질문하세요"
              class="chat-input"
            ></textarea>
            <button @click="sendMessage" class="send-button">전송</button>
          </div>
      </div>
      <!-- 챗봇 열기/닫기 버튼 -->
      <button v-if="!isChatOpen" @click="toggleChat" class="chatbot-toggle">
          💬
      </button>
      <!-- 챗봇 닫기 버튼 -->
      <button v-if="isChatOpen" @click="toggleChat" class="chatbot-toggle-close">
          💬
      </button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      userMessage: "",
      messages: [],
      isChatOpen: false, // 챗봇이 열려있는지 여부
    };
  },
  methods: {
    async sendMessage() {
      if (this.userMessage.trim() === "") return;

      // 사용자 메시지를 메시지 배열에 추가
      this.messages.push({ role: "user", content: this.userMessage });

      // 메시지를 전송하기 전에 입력 필드를 비움
      this.userMessage = "";

      try {
        const response = await axios.post("http://127.0.0.1:8000/chatbots/api/v1/chatbot/", {
          message: this.userMessage,
        });
        console.log(response); // 응답 확인
        this.messages.push({ role: "bot", content: response.data.reply });
      } catch (error) {
        this.messages.push({
          role: "bot",
          content: "서버 접속에 오류가 있습니다.",
        });
      }

      // 메시지가 추가된 후, 스크롤을 맨 아래로 이동
      this.scrollToBottom();
    },
    toggleChat() {
      this.isChatOpen = !this.isChatOpen; // 챗봇 열고 닫기
    },
    scrollToBottom() {
      // Vue의 nextTick을 사용하여 DOM 업데이트 후 실행
      this.$nextTick(() => {
        const chatLog = this.$refs.chatLog;
        chatLog.scrollTop = chatLog.scrollHeight; // 스크롤을 맨 아래로
      });
    },
  },
};
</script>

<style scoped>
/* 챗봇 컨테이너 위치 및 스타일 */
.chatbot-container {
  position: fixed;
  bottom: 70px;
  right: 20px;
  z-index: 1000;
}

.chatbot {
  background: #FBF9F4;
  border: 2px solid #E3E3E3;
  border-radius: 15px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  padding: 15px;
  display: flex;
  flex-direction: column;
  width: 350px;
  max-width: 80%;
  transition: all 0.3s ease;
  font-size: 12px;
}

.chat-log {
  flex-grow: 1;
  overflow-y: auto;
  max-height: 300px;
  margin-bottom: 10px;
  padding-right: 5px;
  background-color: #FBF9F4;
  border-radius: 10px;
  padding: 10px;
}

.message {
  margin: 8px 0;
  padding: 10px;
  border-radius: 10px;
}

.message.user {
  background-color: #e5e5e5;
  text-align: right;
}

.message.bot {
  background-color: #f1f1f1;
  text-align: left;
}

.chat-input-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.chat-input {
  flex-grow: 1;
  padding: 10px;
  border-radius: 20px;
  border: 1px solid #ccc;
  font-size: 16px;
  outline: none;
  transition: all 0.3s ease;
  resize: none;  /* 사용자가 textarea 크기를 조정하지 않도록 */
  overflow-y: auto;  /* 텍스트가 길어지면 세로 스크롤 */
  font-size: 12px;
}

.chat-input:focus {
  border-color: #6c6c6c;
}

.send-button {
  padding: 10px 15px;
  background-color: #6c6c6c;
  color: #fff;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 12px;
}

.send-button:hover {
  background-color: #555;
}

.chatbot-toggle, .chatbot-toggle-close {
  background: #6c6c6c;
  color: #fff;
  border: none;
  border-radius: 50%;
  padding: 12px;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  font-size: 24px;
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1001;
  transition: all 0.3s ease;
}

.chatbot-toggle:hover, .chatbot-toggle-close:hover {
  background: #555;
  transform: scale(1.1);
}

@media (max-width: 768px) {
  .chatbot-container {
    bottom: 10px;
  }

  .chatbot {
    width: 90%;
  }
}
</style>
