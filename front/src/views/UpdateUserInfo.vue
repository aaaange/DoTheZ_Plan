<template>
  <div
    style="width: 100%; height: 100%; padding-top: 119px; background: #F9EB87; justify-content: center; align-items: center; display: inline-flex"
  >
    <div class="Group6" style="width: 863px; height: 800px; position: relative">
      <div
        class="Rectangle1"
        style="width: 1000px; height: 800px; top: 0px; position: absolute; background: #FBF9F4; box-shadow: 6px 9px 4px rgba(0, 0, 0, 0.20); border-radius: 30px; display: flex; flex-direction: column; align-items: center;"
      >
        <!-- 상단 영역 -->
        <div
          class="Group5"
          style="width: 642px; height: 114px; margin-top: 38px; text-align: center;"
        >
          <h1
            style="color: #585547; font-size: 50px; font-family: IBM Plex Sans KR; font-weight: 700; margin: 0;"
          >
            내 정보 수정하기 📝
          </h1>
          <p
            style="color: #585547; font-size: 16px; font-family: IBM Plex Sans KR; font-weight: 300; margin-top: 15px;"
          >
            회원 정보를 수정할 수 있습니다.
          </p>
          <div
            class="Line1"
            style="width: 100%; height: 1px; margin-top: 20px; background-color: #CDC7C0;"
          ></div>
        </div>

        <!-- 사용자 프로필 수정 폼 -->
        <div
          class="user-info"
          style="width: 70%; margin-top: 50px; background-color: #EDEDED; padding: 20px; border-radius: 10px; display: flex; flex-direction: column; align-items: flex-start;"
        >
          <img
            src="@/image/dothez.jpg"
            alt="프로필 사진"
            class="user-avatar"
            style="width: 120px; height: 120px; border-radius: 50%; margin-bottom: 30px; align-self: center;"
          />
          <!-- 이메일 입력 -->
          <div style="margin-bottom: 20px; width: 85%;">
            <label
              for="email"
              style="display: block; color: #585547; font-size: 16px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 400; margin-bottom: 8px; margin-left: 40px;"
              >E-Mail</label
            >
            <div style="display: flex; gap: 10px;">
              <!-- 이메일 아이디 입력 -->
              <input
                id="emailId"
                type="text"
                v-model="emailId"
                placeholder="이메일"
                style="width: 30%; flex-grow: 1; padding: 10px; border: 1px solid #CDC7C0; border-radius: 10px; font-size: 16px; color: #585547; background: #FBF9F4; margin-left: 70px;"
              />
              <span style="padding: 10px 0; color: #585547; font-size: 16px;">@</span>
              <!-- 도메인 선택 또는 입력 -->
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
          <div style="margin-bottom: 20px; width: 72%;">
            <label for="phone" style="display: block; color: #585547; font-size: 16px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 400; margin-bottom: 8px; margin-left: 40px;">휴대폰 번호</label>
            <input
              id="phone"
              type="text"
              v-model="phone"
              placeholder="예) 010-1234-5678"
              style="width: 100%; padding: 10px; border: 1px solid #CDC7C0; border-radius: 10px; font-size: 16px; color: #585547; background: #FBF9F4; margin-left: 70px;"
            />
          </div>
          <!-- 생년월일 입력 -->
          <div style="margin-bottom: 20px; width: 72%;">
            <label for="birth" style="display: block; color: #585547; font-size: 16px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 400; margin-bottom: 8px; margin-left: 40px;">생년월일</label>
            <input
              id="birth"
              type="date"
              v-model="birth"
              style="width: 100%; padding: 10px; border: 1px solid #CDC7C0; border-radius: 10px; font-size: 16px; color: #585547; background: #FBF9F4; margin-left: 70px;"
            />
          </div>
        </div>

        <!-- 저장 버튼 -->
        <div style="width: 80%; text-align: right; margin-top: 20px;">
          <button
            @click="updateProfile"
            style="background: #E6AF69; color: white; border: none; border-radius: 5px; padding: 10px 20px; cursor: pointer; font-size: 16px;"
            class="button"
          >
            수정완료
          </button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { useCounterStore } from "@/stores/counter";
import axios from "axios";
import { useRouter } from 'vue-router';  // Vue Router import

export default {
  setup() {
    const store = useCounterStore();
    const token = store.token;
    const router = useRouter();  // useRouter hook to navigate to profile page

    return {
      token,
      router,  // router for navigation
    };
  },
  data() {
    return {
      emailId: '',
      emailDomain: '',
      customDomain: '',
      isCustomDomain: false,
      phone: '',
      birth: '',
    };
  },
  methods: {
    async updateProfile() {
      // 템플릿에서 입력받은 데이터를 사용
      const updatedEmail = `${this.emailId}@${this.isCustomDomain ? this.customDomain : this.emailDomain}`;
      const updatedData = {
        email: updatedEmail,
        phone: this.phone,
        birth: this.birth,
      };
      try {
        const response = await axios.put(
          'http://127.0.0.1:8000/accounts/api/v1/update/',  // API URL
          updatedData,
          { headers: { Authorization: `Token ${this.token}` } }
        );
        alert('회원정보가 수정되었습니다.');
        this.$router.push({ name: 'mainpage' });
      } catch (error) {
        console.error("Error updating profile data:", error);
        alert("정보 수정에 실패했습니다. 다시 시도해주세요.");
      }
    },
  },
}
</script>

<style scoped>
/* 입력 폼 스타일 */
input, textarea {
  width: 80%;
  padding: 10px;
  margin-bottom: 20px;
  border-radius: 10px;
  border: 1px solid #585547;
}

/* 저장 버튼 스타일 */
button {
  background: #E6AF69;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 16px;
}
.button:hover {
  background: #D79852;
  scale: calc(1.05)
}
</style>
