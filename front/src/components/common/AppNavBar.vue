<template>
  <div style="justify-content: flex-start; align-items: center; gap: 24px; display: flex">
      <div style="height: 35px; justify-content: center; align-items: center; display: flex">
        <RouterLink :to="{ name: 'mainpage' }"><img src="../../image/logo.png" alt="logo" style="width: 120px; height: 60px; border: 3.50px"></img></RouterLink>
      </div>
    </div>
    <div style="flex: 1 1 0; height: 32px; justify-content: flex-end; align-items: flex-start; gap: 8px; display: flex">
      <div style="padding: 8px; border-radius: 8px; justify-content: center; align-items: center; gap: 8px; display: flex">
        <RouterLink :to="{ name: 'productlist' }"><div style="color: #1E1E1E; font-size: 16px; font-family: Inter; font-weight: 400; line-height: 16px; word-wrap: break-word">상품 조회</div></RouterLink>
      </div>
      <div style="padding: 8px; border-radius: 8px; justify-content: center; align-items: center; gap: 8px; display: flex">
        <RouterLink :to="{ name: 'exchangerate' }"><div style="color: #1E1E1E; font-size: 16px; font-family: Inter; font-weight: 400; line-height: 16px; word-wrap: break-word">환율 조회</div></RouterLink>
      </div>
      <div style="padding: 8px; border-radius: 8px; justify-content: center; align-items: center; gap: 8px; display: flex">
        <RouterLink :to="{ name: 'map' }"><div style="color: #1E1E1E; font-size: 16px; font-family: Inter; font-weight: 400; line-height: 16px; word-wrap: break-word">가까운 은행 찾기</div></RouterLink>
      </div>
      <div style="padding: 8px; border-radius: 8px; justify-content: center; align-items: center; gap: 8px; display: flex">
        <RouterLink :to="{ name: 'recommend' }"><div style="color: #1E1E1E; font-size: 16px; font-family: Inter; font-weight: 400; line-height: 16px; word-wrap: break-word">금융 상품 추천</div></RouterLink>
      </div>
    </div>
    <div style="height: 32px; justify-content: flex-start; align-items: center; gap: 12px; display: flex">
      <div style="flex: 1 1 0; height: 32px; padding: 8px; background: #E3E3E3; border-radius: 8px; overflow: hidden; border: 1px #767676 solid; justify-content: center; align-items: center; gap: 8px; display: flex">
        <template v-if="isAuthenticated">
          <RouterLink :to="{ name: 'logout'}">
            <div style="color: #1E1E1E; font-size: 16px; font-family: Inter; font-weight: 400; line-height: 16px; word-wrap: break-word">
              로그아웃
            </div>
          </RouterLink>
        </template>
        <template v-else>
          <RouterLink :to="{ name: 'login' }">
            <div style="color: #1E1E1E; font-size: 16px; font-family: Inter; font-weight: 400; line-height: 16px; word-wrap: break-word">
              로그인
            </div>
          </RouterLink>
        </template>
      </div>
      <div style="flex: 1 1 0; height: 32px; padding: 8px; background: #2C2C2C; border-radius: 8px; overflow: hidden; border: 1px #2C2C2C solid; justify-content: center; align-items: center; gap: 8px; display: flex">
        <template v-if="isAuthenticated">
          <RouterLink :to="{ name: 'profile', params: { userId: user_id } }">
            <div style="color: #F5F5F5; font-size: 16px; font-family: Inter; font-weight: 400; line-height: 16px; word-wrap: break-word">
              프로필
            </div>
          </RouterLink>
        </template>
        <template v-else>
          <RouterLink :to="{ name: 'signup' }">
            <div style="color: #F5F5F5; font-size: 16px; font-family: Inter; font-weight: 400; line-height: 16px; word-wrap: break-word">
              회원가입
            </div>
          </RouterLink>
        </template>
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

    return {
      isAuthenticated,
      isLoading,
      checkLoginStatus,
      user_id
    };
  },
};

</script>

<style scoped>

</style>