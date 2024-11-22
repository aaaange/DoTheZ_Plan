<template>
  <div
    style="width: 100%; height: 100vh; padding-top: 119px; background: #F9EB87; justify-content: center; align-items: center; display: inline-flex"
  >
    <div class="Group6" style="width: 863px; height: 800px; position: relative">
      <div
        class="Rectangle1"
        style="width: 863px; height: 790px; top: 0px; position: absolute; background: #FBF9F4; box-shadow: 6px 9px 4px rgba(0, 0, 0, 0.20); border-radius: 30px"
      >
        <!-- 상단 영역 -->
        <div
          class="Group5"
          style="width: 642px; height: 114px; left: 110px; top: 38px; position: absolute"
        >
          <div
            style="width: 278px; height: 65px; top: 0px; position: absolute; color: #585547; font-size: 50px; font-family: IBM Plex Sans KR; font-weight: 700;"
          >
            내 프로필
          </div>
          <div
            style="width: 385px; left: 5px; top: 75px; position: absolute; color: #585547; font-size: 16px; font-family: IBM Plex Sans KR; font-weight: 300;"
          >
            회원 프로필 페이지
          </div>
          <div
            class="Line1"
            style="width: 642px; height: 0px; left: 0px; top: 114px; position: absolute; border-top: 1px solid #CDC7C0;"
          ></div>
        </div>

        <!-- 탈퇴하기 버튼 -->
        <button
          class="delete-button"
          style="position: absolute; top: 40px; right: 40px; background: #E6AF69; color: white; border: none; border-radius: 5px; padding: 10px 15px; cursor: pointer; font-size: 16px;"
          @click="deleteAccount"
        >
          탈퇴하기
        </button>

        <!-- 사용자 정보 -->
        <div
          class="user-info"
          style="position: absolute; top: 180px; left: 110px; right: 110px; display: flex; align-items: center; background-color: #EDEDED; padding: 20px; border-radius: 10px;"
        >
          <img
            :src="userImage"
            alt="프로필 사진"
            class="user-avatar"
            style="width: 120px; height: 120px; border-radius: 50%; margin-right: 20px;"
          />
          <div class="user-details">
            <h2
              style="font-size: 28px; color: #585547; margin-bottom: 5px;"
            >
              {{ username ? username : "로그인을 해주세요" }}
            </h2>
            <p style="font-size: 18px; color: #585547;">
              작성한 리뷰 {{ userProfile ? userProfile.reviewsCount : "2" }}개
            </p>
          </div>
        </div>

        <!-- 가입한 상품 목록 -->
        <div
          class="product-section"
          style="position: absolute; top: 350px; left: 110px; right: 110px;"
        >
          <h3 style="font-size: 24px; color: #585547; margin-bottom: 20px;">
            가입한 상품
          </h3>
          <!-- <div v-if="userProfile" class="product-list" style="max-height: 350px; overflow-y: auto;">
            <div v-for="(product, index) in userProfile.products" :key="index" class="product-item" style="background-color: #F7F4EA; border-radius: 10px; border: 1px solid #585547; padding: 15px; margin-bottom: 10px;">
              <p style="font-size: 18px; color: #585547; font-weight: 500;">{{ product.name }}</p>
              <p style="font-size: 14px; color: #585547;">이자율 {{ product.rate }}</p>
            </div>
          </div>
          <div v-else class="login-message" style="display: flex; justify-content: center; align-items: center; height: 200px; font-size: 24px; color: #585547;">
            로그인 해주세요
          </div> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import img from "@/image/dothez.jpg";

const store = useCounterStore();
const username = ref("");
const userImage = ref(img);

if (store.userProfile) {
  username.value = store.userProfile.username;
}

const deleteAccount = () => {
  if (confirm("정말 탈퇴하시겠습니까?")) {
    // 여기에 탈퇴 로직 추가
    console.log("탈퇴 처리 로직 실행");
  }
};
</script>

<style scoped>
.product-list::-webkit-scrollbar {
  width: 5px;
}
.product-list::-webkit-scrollbar-thumb {
  background-color: #888;
  border-radius: 10px;
}
.product-list::-webkit-scrollbar-track {
  background-color: #f1f1f1;
  border-radius: 10px;
}
</style>
