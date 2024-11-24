<template>
  <div class="login-page">
    <div class="login-container">
      <h1 class="title">로그인</h1>
      <p class="sub-title">오늘도 두더Z와 함께!</p>

      <!-- 아이디 입력 -->
      <div class="input-group-1">
        <label for="username">아이디</label>
        <input
          id="username"
          type="text"
          v-model="username"
          placeholder="아이디를 입력해주세요."
        />
      </div>

      <!-- 비밀번호 입력 -->
      <div class="input-group-1">
        <label for="password">비밀번호</label>
        <input
          id="password"
          type="password"
          v-model="password"
          placeholder="비밀번호를 입력해주세요."
        />
      </div>

      <!-- 오류 메시지 -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <!-- 로그인 버튼 -->
      <div class="login-button">
        <button @click="handleLogin">로그인</button>
      </div>
    </div>
  </div>
</template>

<script>
import { useCounterStore } from "@/stores/counter"; // Pinia store import

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
    };
  },
  methods: {
    async handleLogin() {
      const store = useCounterStore(); // Pinia store 사용
      if (this.username === '' || this.password === '') {
        this.errorMessage = '아이디 혹은 비밀번호를 입력해주세요.';
        return;
      }

      // Pinia store의 logIn 메소드 사용
      try {
        await store.logIn({ username: this.username, password: this.password });
        // 로그인 성공 후 메인 페이지로 이동
        this.$router.push({ name: 'mainpage' });
      } catch (error) {
        // 오류 메시지 처리
        this.errorMessage = error.response ? error.response.data.detail : '로그인에 실패했습니다.';
        console.log('로그인 실패:', error.response || error.message);  // 실패 시 콘솔 로그 출력
      }
    }
  }
};
</script>

<style scoped>
.login-page {
  width: 100%;
  height: 100vh;
  background-color: #F9EB87;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-container {
  width: 100%;
  max-width: 480px;
  background-color: #FBF9F4;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 6px 9px 4px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.title {
  color: #585547;
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 10px;
}

.sub-title {
  color: #585547;
  font-size: 16px;
  font-weight: 300;
  margin-bottom: 30px;
}

.input-group-1 {
  margin-bottom: 20px;
  text-align: left;
}

.input-group-1 label {
  color: #585547;
  font-size: 16px;
  font-weight: 400;
  margin-bottom: 8px;
}

.input-group-1 input {
  width: 100%;
  padding: 10px;
  border: 1px solid #CDC7C0;
  border-radius: 10px;
  font-size: 16px;
  color: #585547;
  background-color: #FBF9F4;
  box-sizing: border-box;
}

.error-message {
  color: #FF4747;
  font-size: 16px;
  font-weight: 200;
  margin-top: 10px;
}

.login-button button {
  width: 100%;
  padding: 15px;
  background-color: #E6AF69;
  color: #FBF9F4;
  border: none;
  border-radius: 15px;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  box-sizing: border-box;
}
</style>
