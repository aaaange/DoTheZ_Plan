<template>
  <div style="width: 1280px; height: 832px; position: relative; background: #F9EB87">
    <div style="width: 1280px; height: 32px; padding: 32px; left: 0px; top: 0px; position: absolute; background: white; border-bottom: 1px #D9D9D9 solid; justify-content: flex-start; align-items: center; gap: 24px; display: inline-flex">
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
          <div v-if="is_authenticated"><RouterLink :to="{ name: 'logout'}"><div style="color: #1E1E1E; font-size: 16px; font-family: Inter; font-weight: 400; line-height: 16px; word-wrap: break-word">로그아웃</div></RouterLink></div>
          <div v-else><RouterLink :to="{ name: 'login' }"><div style="color: #1E1E1E; font-size: 16px; font-family: Inter; font-weight: 400; line-height: 16px; word-wrap: break-word">로그인</div></RouterLink></div>
        </div>
        <div style="flex: 1 1 0; height: 32px; padding: 8px; background: #2C2C2C; border-radius: 8px; overflow: hidden; border: 1px #2C2C2C solid; justify-content: center; align-items: center; gap: 8px; display: flex">
          <div v-if="is_authenticated"><RouterLink :to="{ name: 'profile' }"><div style="color: #F5F5F5; font-size: 16px; font-family: Inter; font-weight: 400; line-height: 16px; word-wrap: break-word">프로필</div></RouterLink></div>
          <div v-else><RouterLink :to="{ name: 'signup' }"><div style="color: #F5F5F5; font-size: 16px; font-family: Inter; font-weight: 400; line-height: 16px; word-wrap: break-word">회원가입</div></RouterLink></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { RouterLink } from 'vue-router';
import axios from 'axios';

export default {
  data() {
    return {
      isAuthenticated: false,
      username: ''
    };
  },
  methods: {
    async fetchAuthStatus() {
      try {
        const response = await axios.get('/api/check-auth/');
        this.isAuthenticated = response.data.is_authenticated;
        this.username = response.data.username;
      } catch (error) {
        console.error('Failed to fetch authentication status:', error);
      }
    }
  },
  created() {
    this.fetchAuthStatus();
  }
};
</script>

<style scoped>

</style>