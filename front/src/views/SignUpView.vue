<template>
  <div class="signup-page" style="width: 100%; height: 100vh; background: #F9EB87; display: flex; justify-content: center; align-items: center;">
    <div class="signup-container" style="width: 800px; background: #FBF9F4; padding: 40px; border-radius: 20px; box-shadow: 6px 9px 4px rgba(0, 0, 0, 0.2);">
      <h1 style="color: #585547; font-size: 32px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 700; margin-bottom: 10px;">회원가입</h1>
      <p style="color: #585547; font-size: 16px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 300; margin-bottom: 30px;">어서오세요! 두더Z와 깊이 있는 금융 생활 해요 :)</p>

      <h2 style="color: #585547; font-size: 18px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 600; margin-bottom: 15px;">기본 정보 입력</h2>

      <!-- 아이디 입력 -->
      <div style="margin-bottom: 20px;">
        <label for="username" style="display: block; color: #585547; font-size: 16px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 400; margin-bottom: 8px;">아이디</label>
        <div style="display: flex; gap: 10px;">
          <input
            id="username"
            type="text"
            v-model="username"
            placeholder="아이디를 입력해주세요."
            style="flex-grow: 1; padding: 10px; border: 1px solid #CDC7C0; border-radius: 10px; font-size: 16px; color: #585547; background: #FBF9F4;"
          />
          <!-- <button
            @click="checkUsername"
            style="padding: 10px 20px; background: #F8C471; border: none; border-radius: 10px; font-size: 16px; color: white; cursor: pointer;"
          >
            중복 확인
          </button>
          <span v-if="usernameCheck === 'success'" style="color: green; font-size: 18px;">✔</span>
          <span v-else-if="usernameCheck === 'failure'" style="color: red; font-size: 18px;">✖</span> -->
        </div>
      </div>

      <!-- 비밀번호 입력 -->
      <div style="margin-bottom: 20px;">
        <label for="password" style="display: block; color: #585547; font-size: 16px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 400; margin-bottom: 8px;">비밀번호</label>
        <input
          id="password"
          type="password"
          v-model="password"
          placeholder="비밀번호는 문자, 숫자, 특수문자를 조합해 10~20자로 입력해주세요."
          style="width: 100%; padding: 10px; border: 1px solid #CDC7C0; border-radius: 10px; font-size: 16px; color: #585547; background: #FBF9F4;"
          @input="checkPasswordMatch"
        />
      </div>

      <!-- 비밀번호 확인 -->
      <div style="margin-bottom: 20px;">
        <label for="password-confirm" style="display: block; color: #585547; font-size: 16px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 400; margin-bottom: 8px;">비밀번호 확인</label>
        <input
          id="password-confirm"
          type="password"
          v-model="passwordConfirm"
          placeholder="비밀번호를 다시 입력해주세요."
          style="width: 100%; padding: 10px; border: 1px solid #CDC7C0; border-radius: 10px; font-size: 16px; color: #585547; background: #FBF9F4;"
          @input="checkPasswordMatch"
        />
        <p v-if="!isPasswordMatch" style="color: red; font-size: 14px; margin-top: 5px;">* 비밀번호가 일치하지 않습니다.</p>
      </div>

      <!-- 이메일 입력 -->
      <div style="margin-bottom: 20px;">
        <label for="email" style="display: block; color: #585547; font-size: 16px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 400; margin-bottom: 8px;">E-Mail</label>
        <div style="display: flex; gap: 10px;">
          <!-- 이메일 아이디 입력 -->
          <input
            id="email"
            type="text"
            v-model="emailId"
            placeholder="아이디"
            style="flex-grow: 1; padding: 10px; border: 1px solid #CDC7C0; border-radius: 10px; font-size: 16px; color: #585547; background: #FBF9F4;"
          />
          <span style="padding: 10px 0; color: #585547; font-size: 16px;">@</span>
          <!-- 드롭다운 또는 입력 필드 -->
          <div style="flex-grow: 1;">
            <template v-if="isCustomDomain">
              <input
                type="text"
                placeholder="직접 입력"
                v-model="customDomain"
                @blur="toggleCustomDomain(false)"
                style="width: 100%; padding: 10px; border: 1px solid #CDC7C0; border-radius: 10px; font-size: 16px; color: #585547; background: #FBF9F4;"
              />
            </template>
            <template v-else>
              <select
                id="email-domain-select"
                v-model="emailDomain"
                @change="checkCustomDomain"
                style="width: 100%; padding: 10px; border: 1px solid #CDC7C0; border-radius: 10px; font-size: 16px; color: #585547; background: #FBF9F4;"
              >
                <option value="" disabled selected>도메인 선택</option>
                <option value="naver.com">naver.com</option>
                <option value="hanmail.net">hanmail.net</option>
                <option value="gmail.com">gmail.com</option>
                <option value="nate.com">nate.com</option>
                <option value="hotmail.com">hotmail.com</option>
                <option value="custom">직접 입력</option>
              </select>
            </template>
          </div>
        </div>
      </div>


      <!-- 휴대폰 번호 입력 -->
      <div style="margin-bottom: 20px;">
        <label for="phone" style="display: block; color: #585547; font-size: 16px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 400; margin-bottom: 8px;">휴대폰 번호</label>
        <input
          id="phone"
          type="text"
          v-model="phone"
          placeholder="휴대폰 번호를 입력해주세요. 예: 010-1234-5678"
          style="width: 100%; padding: 10px; border: 1px solid #CDC7C0; border-radius: 10px; font-size: 16px; color: #585547; background: #FBF9F4;"
        />
      </div>

      <!-- 생년월일 입력 -->
      <div style="margin-bottom: 20px;">
        <label for="birth" style="display: block; color: #585547; font-size: 16px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 400; margin-bottom: 8px;">생년월일</label>
        <input
          id="birth"
          type="date"
          v-model="birth"
          style="width: 100%; padding: 10px; border: 1px solid #CDC7C0; border-radius: 10px; font-size: 16px; color: #585547; background: #FBF9F4;"
        />
      </div>

      <!-- 제출 버튼 -->
      <div style="text-align: center; margin-top: 30px;">
        <button @click="handleSubmit" style="padding: 15px 30px; background: #E6AF69; color: #FBF9F4; border: none; border-radius: 15px; font-size: 18px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 700; cursor: pointer;">
          회원가입 하기
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'

const store = useCounterStore()

// 상태 관리
const username = ref('')
const usernameCheck = ref('')
const password = ref('')
const passwordConfirm = ref('')
const emailId = ref('')
const phone = ref('')
const birth = ref('')
const emailDomain = ref('')
const customDomain = ref('')
const isCustomDomain = ref(false)

const isPasswordMatch = computed(() => password.value === passwordConfirm.value)

// // 아이디 중복 확인
// // 아이디 중복 확인
// async function checkUsername() {
//   // 중복 확인 요청
//   if (username.value === '') {
//     alert('아이디를 입력해주세요.')
//     return
//   }

//   try {
//     // 실제 백엔드 URL로 수정 필요
//     const response = await axios.post('http://127.0.0.1:8000/accounts/api/v1/check_username/', { username: username.value })
    
//     // 서버 응답 처리
//     if (response.data.isAvailable) {
//       usernameCheck.value = 'success' // 중복이 없는 경우
//     } else {
//       usernameCheck.value = 'failure' // 중복이 있는 경우
//     }
//   } catch (error) {
//     console.error('아이디 중복 확인 중 오류 발생:', error)
//     alert('서버 오류가 발생했습니다. 다시 시도해주세요.')
//   }
// }


// 비밀번호 확인
function checkPasswordMatch() {
  // 비밀번호 일치 여부 체크
}

// 이메일 도메인 선택
// "직접 입력" 선택 시 처리
function checkCustomDomain() {
  if (emailDomain.value === 'custom') {
    isCustomDomain.value = true;
    customDomain.value = ''; // 직접 입력 초기화
  }
}

// 입력 필드에서 벗어날 때 드롭다운 복구
function toggleCustomDomain(isCustom) {
  if (!customDomain.value) {
    isCustomDomain.value = isCustom;
  }
}

// 회원가입 제출
function handleSubmit() {
  // 필수 입력 값 검사
  if (!username.value || !password.value || !emailId.value || !phone.value || !birth.value || !emailDomain.value) {
    alert('모든 필드를 입력해주세요.')
    return
  }

  if (password.value !== passwordConfirm.value) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }

  // 백엔드 요청
  const formData = {
    username: username.value,
    password1: password.value,
    password2: passwordConfirm.value,
    email: `${emailId.value}@${emailDomain.value === 'custom' ? customDomain.value : emailDomain.value}`,
    phone: phone.value,
    birth: birth.value,
  }

  store.signUp(formData)
}
</script>

<style scoped>
/* 추가적인 스타일을 여기에 넣을 수 있습니다. */
</style>
