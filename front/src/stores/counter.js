import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useRouter } from 'vue-router';

export const useCounterStore = defineStore('counter', () => {
  const API_URL = 'http://127.0.0.1:8000';  // API URL
  const token = ref(null);  // 로그인 상태를 나타내는 token 변수
  const router = useRouter();  // Vue Router 인스턴스

  // 사용자 정보 상태
  const userProfile = ref(null);

  // 로그인 여부를 computed로 처리
  const isLogin = computed(() => token.value !== null);


  // 회원가입 요청
  const signUp = function (payload) {
    const { username, password1, password2, email, phone, birth } = payload;

    axios.post(`${API_URL}/accounts/api/v1/signup/`, {
      username,
      password: password1,
      password2,
      email,
      phone,
      birth,
    })
    .then((res) => {
      console.log('회원가입 성공:', res.data);
      logIn({ username, password: password1 });  // 회원가입 후 바로 로그인
      router.push({ name: 'mainpage' });  // 회원가입 후 메인 페이지로 이동
    })
    .catch((err) => {
      console.error('회원가입 실패:', err.response?.data || err.message);
      if (err.response?.data?.error) {
        const errorMessages = Object.entries(err.response.data.error)
          .map(([field, messages]) => `${field}: ${messages.join(', ')}`)
          .join('\n');
        alert(`회원가입에 실패했습니다.\n${errorMessages}`);
      } else {
        alert('회원가입에 실패했습니다. 입력 정보를 확인해주세요.');
      }
    });
  };

  // 로그인 요청
  const logIn = function (payload) {
    const { username, password } = payload;

    axios.post(`${API_URL}/accounts/api/v1/login/`, { username, password })
    .then((res) => {
      token.value = res.data.key;  // 로그인 성공 시 받은 토큰 저장
      localStorage.setItem('token', res.data.key);  // 토큰을 로컬 스토리지에 저장
      fetchUserProfile();  // 로그인 후 프로필 정보 가져오기
      console.log('로그인 성공');  // 로그인 성공 메시지 콘솔에 출력
      router.push({ name: 'mainpage' });  // 로그인 후 메인 페이지로 이동
    })
    .catch((err) => {
      console.log('로그인 실패:', err.response || err.message);  // 로그인 실패 시 콘솔에 오류 메시지 출력
      alert('로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.');
    });
  };


  // 사용자 프로필 정보 가져오기 함수
  const fetchUserProfile = async () => {
    if (!token.value) return null;

    try {
      const response = await axios.get(`${API_URL}/accounts/api/v1/profile/`, {
        headers: { Authorization: `Token ${token.value}` }
      });
      userProfile.value = response.data;
      return userProfile.value;
    } catch (error) {
      console.error('사용자 프로필 정보를 가져오는 데 실패했습니다:', error);
      return null;
    }
  };


  return { signUp, token, isLogin, logIn, API_URL, userProfile, fetchUserProfile };
});
