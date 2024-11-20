<template>
  <div>
    <div v-if="userData">
      <h2>User Profile</h2>
      <p>User ID: {{ userData.user_id }}</p>
      <p>Username: {{ userData.username }}</p>
      <p>Email: {{ userData.email }}</p>
      <p>Phone: {{ userData.phone }}</p>
      <p>Birth: {{ userData.birth }}</p>
    </div>
    <p v-else>Loading profile information...</p>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router'; // Vue Router에서 useRoute 훅을 가져옵니다.

export default {
  setup() {
    const userData = ref(null);
    const route = useRoute(); // 현재 라우트 정보를 가져옵니다.
    const userId = route.params.userId; // URL에서 userId를 가져옵니다.

    const getProfile = async () => {
      try {
        // URL에서 가져온 userId를 사용하여 프로필 정보를 요청합니다.
        const response = await axios.get(`http://127.0.0.1:8000/accounts/api/v1/profile/${userId}/`, { withCredentials: true });
        userData.value = response.data; // 사용자 데이터 저장
      } catch (error) {
        console.error('Error fetching profile:', error);
        userData.value = null; // 에러 발생 시 null로 설정
      }
    };

    onMounted(() => {
      getProfile(); // 컴포넌트가 마운트될 때 프로필 정보 요청
    });

    return { userData };
  },
};
</script>

<style scoped>
/* 스타일을 여기에 추가할 수 있습니다 */
</style>