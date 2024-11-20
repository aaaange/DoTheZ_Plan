import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useCounterStore = defineStore('counter', () => {
    // const articles = ref([])
    const API_URL = 'http://127.0.0.1:8000'
    const token = ref(null)
    const isLogin = computed(() => {
        if (token.value === null) {
        return false
        } else {
        return true
        }
    })

    // 회원가입 요청 액션
    const signUp = function (payload) {
        // const username = payload.username
        // const password1 = payload.password1
        // const password2 = payload.password2
        const { username, password1, password2, email, phone, birth } = payload

        axios({
        method: 'post',
        url: `${API_URL}/accounts/api/v1/signup/`,
        data: {
            username, password1, password2,
        }
        })
        .then((res) => {
            // console.log(res)
            // console.log('회원가입 성공')
            const password = password1
            logIn({ username, password, email, phone, birth })
        })
        .catch((err) => {
            console.log(err)
        })
    }
    return { signUp, token, isLogin }
})
