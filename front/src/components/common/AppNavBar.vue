<template>
  <div style="width: 100vw; height: 96px; padding: 0; margin: 0; position: fixed; top: 0; left: 0; right: 0; background: white; border-bottom: 1px solid #D9D9D9; justify-content: space-between; align-items: center; gap: 12px; display: flex; box-sizing: border-box;">
    <div style="justify-content: flex-start; align-items: center; gap: 12px; display: flex;">
      <div style="height: 60px; justify-content: center; align-items: center; display: flex;">
        <RouterLink :to="{ name: 'mainpage' }">
          <img src="../../image/logo.png" alt="logo" style="width: 120px; height: 60px; border: 3.50px;">
        </RouterLink>
      </div>
    </div>
    <div style="flex: 1; height: 32px; justify-content: flex-end; align-items: flex-start; gap: 4px; display: flex; flex-wrap: nowrap;">
      <div style="padding: 8px; border-radius: 8px; justify-content: center; align-items: center; gap: 8px; display: flex;">
        <RouterLink :to="{ name: 'productlist' }">
          <div style="color: #1E1E1E; font-size: 14px; font-family: Inter; font-weight: 400; line-height: 16px; word-wrap: break-word;">
            상품 조회
          </div>
        </RouterLink>
      </div>
      <div style="padding: 8px; border-radius: 8px; justify-content: center; align-items: center; gap: 8px; display: flex;">
        <RouterLink :to="{ name: 'exchangerate' }">
          <div style="color: #1E1E1E; font-size: 14px; font-family: Inter; font-weight: 400; line-height: 16px; word-wrap: break-word;">
            환율 조회
          </div>
        </RouterLink>
      </div>
      <div style="padding: 8px; border-radius: 8px; justify-content: center; align-items: center; gap: 8px; display: flex;">
        <RouterLink :to="{ name: 'map' }">
          <div style="color: #1E1E1E; font-size: 14px; font-family: Inter; font-weight: 400; line-height: 16px; word-wrap: break-word;">
            가까운 은행 찾기
          </div>
        </RouterLink>
      </div>
      <div style="padding: 8px; border-radius: 8px; justify-content: center; align-items: center; gap: 8px; display: flex;">
        <RouterLink :to="{ name: 'survey' }">
          <div style="color: #1E1E1E; font-size: 14px; font-family: Inter; font-weight: 400; line-height: 16px; word-wrap: break-word;">
            금융 상품 추천
          </div>
        </RouterLink>
      </div>
    </div>
    <div style="height: 32px; justify-content: flex-end; align-items: center; gap: 8px; display: flex;">
  <div style="flex-shrink: 0; height: 32px; padding: 8px; background: #E3E3E3; border-radius: 8px; overflow: hidden; border: 1px #767676 solid; justify-content: center; align-items: center; gap: 8px; display: flex;">
    <template v-if="isAuthenticated">
      <a href="#" @click.prevent="logOut" style="color: #1E1E1E; font-size: 14px; font-family: Inter; font-weight: 400; line-height: 16px; word-wrap: break-word;">
        로그아웃
      </a>
    </template>
    <template v-else>
      <RouterLink :to="{ name: 'login' }">
        <div style="color: #1E1E1E; font-size: 14px; font-family: Inter; font-weight: 400; line-height: 16px; word-wrap: break-word;">
          로그인
        </div>
      </RouterLink>
    </template>
  </div>
  
  <!-- 프로필 버튼 -->
  <div style="flex-shrink: 0; height: 32px; padding: 8px; background: #2C2C2C; border-radius: 8px; overflow: hidden; border: 1px #2C2C2C solid; justify-content: center; align-items: center; gap: 8px; display: flex; margin-right: 12px;">
    <template v-if="isAuthenticated">
      <RouterLink :to="{ name: 'profile', params: { userId: user_id } }">
        <div style="color: #F5F5F5; font-size: 14px; font-family: Inter; font-weight: 400; line-height: 16px; word-wrap: break-word;">
          프로필
        </div>
      </RouterLink>
    </template>
    <template v-else>
      <RouterLink :to="{ name: 'signup' }">
        <div style="color: #F5F5F5; font-size: 14px; font-family: Inter; font-weight: 400; line-height: 16px; word-wrap: break-word;">
          회원가입
        </div>
      </RouterLink>
    </template>
  </div>
</div>

  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { useCounterStore } from "@/stores/counter";
import axios from 'axios';

export default {
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
/* 필요한 스타일 추가 */
</style>
