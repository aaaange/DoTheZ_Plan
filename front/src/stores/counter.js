import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useRouter } from 'vue-router';

export const useCounterStore = defineStore('counter', () => {
  const API_URL = 'http://127.0.0.1:8000';  // API URL
  const token = ref(localStorage.getItem('token') || null);  // 로그인 상태를 나타내는 token 변수
  const router = useRouter();  // Vue Router 인스턴스

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
      if (res.data.key) {
        token.value = res.data.key;  // 로그인 성공 시 받은 토큰 저장
        localStorage.setItem('token', res.data.key);  // 토큰을 로컬 스토리지에 저장

        console.log('로그인 성공');  // 로그인 성공 메시지 콘솔에 출력
        router.push({ name: 'mainpage' });  // 로그인 후 메인 페이지로 이동
      } else {
        console.error('토큰이 없거나 잘못된 응답을 받았습니다.')
      }

    })
    .catch((err) => {
      console.log('로그인 실패:', err.response || err.message);  // 로그인 실패 시 콘솔에 오류 메시지 출력
      alert('로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.');
    });
  };

  // [추가기능] 로그아웃
  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/api/v1/logout/`, // 서버의 로그아웃 API 호출
    })
      .then((res) => {
        console.log(res.data);
        token.value = null; // 인증 토큰 비우기
        localStorage.removeItem('token');  // 로컬 스토리지에서 토큰 삭제
        router.push('/'); // 메인 페이지로 리디렉션
      })
      .catch((err) => {
        console.log(err); // 에러 처리
      });
  };
  
  return { signUp, token, isLogin, logIn, API_URL, logOut };
});
