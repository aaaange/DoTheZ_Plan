<template>
  <div class="navbar">
    <div class="navbar-left">
      <RouterLink :to="{ name: 'mainpage' }">
        <img src="../../image/logo.png" alt="logo" class="logo" />
      </RouterLink>
    </div>
    <div class="navbar-center">
      <RouterLink :to="{ name: 'productlist' }" class="nav-link">상품 조회</RouterLink>
      <RouterLink :to="{ name: 'exchangerate' }" class="nav-link">환율 조회</RouterLink>
      <RouterLink :to="{ name: 'map' }" class="nav-link">가까운 은행 찾기</RouterLink>
      <RouterLink :to="{ name: 'survey' }" class="nav-link">금융 상품 추천</RouterLink>
    </div>
    <div class="navbar-right">
      <div class="auth-button">
        <template v-if="isAuthenticated">
          <a href="#" @click.prevent="logOut" class="btn">로그아웃</a>
        </template>
        <template v-else>
          <RouterLink :to="{ name: 'login' }" class="btn">로그인</RouterLink>
        </template>
      </div>
      <div class="profile-button">
        <template v-if="isAuthenticated">
          <RouterLink :to="{ name: 'profile', params: { userId: user_id } }" class="btn_a profile-btn">프로필</RouterLink>
        </template>
        <template v-else>
          <RouterLink :to="{ name: 'signup' }" class="btn_a profile-btn">회원가입</RouterLink>
        </template>
      </div>
    </div>
    <!-- Chatbot 컴포넌트를 우측 하단에 추가 -->
    <Chatbot class="chatbot-container" />
  </div>
</template>


<script>
import { ref, onMounted, watch } from 'vue';
import { useCounterStore } from "@/stores/counter";
import axios from 'axios';
import Chatbot from '../ChatBot.vue';

export default {
  components: {
    Chatbot, // 컴포넌트 등록
  },
  setup() {
    const store = useCounterStore();
    const isAuthenticated = ref(store.isLogin);
    const isLoading = ref(true);
    const user_id = ref(0);

    const checkLoginStatus = async () => {
      isLoading.value = true;
      try {
        // 토큰이 있는지 확인
        const token = store.token;
        if (token) {
          // 토큰 유효성 검사 (선택적)
          const response = await axios.get(`${store.API_URL}/accounts/api/v1/user_info/`, {
            headers: { Authorization: `Token ${token}` }
          })
          isAuthenticated.value = true;
          user_id.value = response.data.pk;
        } else {
          isAuthenticated.value = false;
        }
      } catch (error) {
        console.error('인증 상태 확인 중 오류 발생:', error);
        isAuthenticated.value = false;
      } finally {
        isLoading.value = false;
      }
    };

    onMounted(() => {
      checkLoginStatus();
    });

    // store의 isLogin 상태 변화 감지
    watch(() => store.isLogin, (newValue) => {
      isAuthenticated.value = newValue;
    });

    const logOut = () => {
      store.logOut(); // store에서 logOut 호출
    };

    return {
      isAuthenticated,
      isLoading,
      checkLoginStatus,
      user_id,
      logOut,
    };
  },
}; 
</script>

<style scoped>
.navbar {
  width: 100%;
  height: 80px;
  background: #FBF9F4;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  position: fixed;
  top: 0;
  z-index: 10;
  font-family: 'Roboto', sans-serif;
  left: 0px;
}

.logo {
  width: 70px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  margin-left: 50px;
  border-radius: 50%;
}

.navbar-center {
  display: flex;
  gap: 24px;
}

.nav-link {
  font-size: 22px;
  color: #585547;
  font-weight: bold;
  text-decoration: none;
  padding: 10px 20px;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

.navbar-right {
  display: flex;
  gap: 16px;
  align-items: center;
  margin-right: 40px;
}

.btn {
  font-size: 18px;
  color: #585547;
  padding: 10px 20px;
  border: none;
  border-radius: 20px;
  background: #E3E3E3;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.btn:hover {
  background: #f1f1f1;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.btn_a {
  font-size: 18px;
  color: #E3E3E3;
  padding: 10px 20px;
  border: none;
  border-radius: 20px;
  background: #E3E3E3;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.profile-btn {
  background: #585547;
}

.profile-btn:hover {
  background: rgb(70, 67, 56);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.chatbot-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}


@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    height: auto;
    padding: 16px;
  }

  .navbar-center {
    flex-wrap: wrap;
    justify-content: center;
    gap: 12px;
  }

  .navbar-right {
    flex-wrap: wrap;
    justify-content: center;
    gap: 12px;
  }
}
</style>
