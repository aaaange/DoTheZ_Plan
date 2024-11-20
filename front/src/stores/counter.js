import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
    // const articles = ref([])
    const API_URL = 'http://127.0.0.1:8000'
    const token = ref(null)
    const router = useRouter() // useRouter 훅을 사용해 router 객체 가져오기
    const isLogin = computed(() => {
        if (token.value === null) {
        return false
        } else {
        return true
        }
    })

    // 회원가입 요청 액션
    const signUp = function (payload) {
      const { username, password1, password2, email, phone, birth } = payload
    
      axios({
        method: 'post',
        url: `${API_URL}/accounts/api/v1/signup/`,
        data: {
          username,
          password: password1,  // 'password1'을 'password'로 변경
          password2,
          email,
          phone,
          birth
        }
      })
      .then((res) => {
        console.log('회원가입 성공:', res.data)
        const password = password1
        // logIn({ username, password })
        router.push({ name: 'mainpage' }) // 메인 페이지로 이동
      })
      .catch((err) => {
        console.error('회원가입 실패:', err.response?.data || err.message)
        if (err.response?.data?.error) {
          const errorMessages = Object.entries(err.response.data.error)
            .map(([field, messages]) => `${field}: ${messages.join(', ')}`)
            .join('\n')
          alert(`회원가입에 실패했습니다.\n${errorMessages}`)
        } else {
          alert('회원가입에 실패했습니다. 입력 정보를 확인해주세요.')
        }
      })
    }
    return { signUp, token, isLogin }
})
