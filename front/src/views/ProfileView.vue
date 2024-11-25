<template>
  <div class="parent-container">
    <div class="card-container">
      <!-- 타이틀 섹션 -->
      <div class="title-section">
        <h2 class="page-title">상품 상세 정보</h2>
        <hr class="title-divider" />
      </div>
      <!-- 상품 이름 박스 -->
      <div class="product-name-box">
        <!-- 상품 이름 왼쪽에 이미지 추가 -->
        <img class="product-image" :src="getBankImage(productInfo.kor_co_nm)" :alt="productInfo.kor_co_nm" />
        <span class="product-name">{{ productInfo.fin_prdt_nm }}</span>
      </div>
      <!-- 상품 상세 정보 -->
      <div class="product-details-container">
        <div v-for="(value, key) in productInfo" :key="key" class="product-info">
          <div class="product-label-box">
            <span class="product-label">{{ fieldMappings[key] || key }}</span>
          </div>
          <div class="product-value-box">
            <span class="product-value">{{ value }}</span>
          </div>
        </div>
      </div>
      <!-- 버튼 섹션 -->
      <div class="button-container">
        <button class="action-button" @click="toggleSubscription" :style="{ backgroundColor: isSubscribed ? '#585547' : '#E6AF69', color: '#FBF9F4' }">
          {{ isSubscribed ? '내 상품에 삭제' : '내 상품에 등록' }}
        </button>
      </div>
    </div>

    <!-- 리뷰 섹션 -->
    <div class="review-page" style="width: 870px; background: #F9EB87; justify-content: center;">
      <div class="review-container" style="width: 800px; background: #FBF9F4; padding: 40px; border-radius: 20px; box-shadow: 6px 9px 4px rgba(0, 0, 0, 0.2);">
        <!-- 리뷰 내용 입력 및 버튼 배치 -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
          <input id="review-content" type="text" v-model="newReviewContent" placeholder="리뷰를 입력해주세요." @keydown.enter="submitReview"
                 style="flex-grow: 1; padding: 10px; border: 1px solid #CDC7C0; border-radius: 10px; font-size: 16px; color: #585547; background: #FBF9F4;" />
          <button @click="submitReview" class="action-button"
                  style="padding: 10px 20px; background: #E6AF69; color: #FBF9F4; border: none; border-radius: 15px; font-size: 18px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 700; cursor: pointer; margin-left: 10px;">
            리뷰 작성하기
          </button>
        </div>

        <!-- 작성된 리뷰 목록 -->
        <div v-for="(review, index) in reviews" :key="index"
             style="margin-top: 30px; padding: 15px; border: 1px solid #E6AF69; border-radius: 10px; margin-bottom: 10px; background: #FBF9F4;">
          <div style="font-size: 14px; color: #585547;">{{ review.user.username }} | {{ review.created_at }}</div>
          <div style="font-size: 16px; color: #585547; margin-top: 10px;">{{ review.content }}</div>
          <div style="margin-top: 10px;">
            <button @click="editReview(review)" class="action-button"
                    style="padding: 5px 10px; background: #E6AF69; color: #FBF9F4; border: none; border-radius: 10px; font-size: 14px; cursor: pointer;">수정</button>
            <button @click="deleteReview(review)" class="action-button"
                    style="padding: 5px 10px; background: #E6AF69; color: #FBF9F4; border: none; border-radius: 10px; font-size: 14px; cursor: pointer; margin-left:
                    10px;">삭제</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { useCounterStore } from "@/stores/counter";
import axios from "axios";

export default {
  setup() {
    const store = useCounterStore();  // useCounterStore 호출
    const token = store.token;  // store에서 token 가져오기

    return {
      token,  // 반환하여 컴포넌트에서 사용
    };
  },
  data() {
    return {
      username: '', // 제품 상세 정보
      user_id: '',
      my_products: [ ],
      graph: null,
      reviewCount: 0,
    };
  },
  props: {
    userId: {
      type: Number,
      required: true,
    },
  },
  mounted() {
    // 서버에서 데이터를 가져오는 메소드 호출
    this.fetchProfiles().then(() => {
      this.fetchUserReviewCount()
    })
    this.fetchProducts()
    this.fetchGraphs() 
  },
  methods: {
    async fetchProfiles() {
      try {
        const response = await axios.get(
          'http://127.0.0.1:8000/accounts/api/v1/user_info/',
        {
          headers: { Authorization: `Token ${this.token}` }  // this.token 사용
        })
        this.username = response.data.username; // 상품 상세 정보 저장
        this.user_id = response.data.pk
      } catch (error) {
        console.error("Error fetching product data:", error);
      }
    },
    async fetchProducts() {
      try {
        const response = await axios.get(
          'http://127.0.0.1:8000/accounts/api/v1/my/',
        {
          headers: { Authorization: `Token ${this.token}` }  // this.token 사용
        })

        this.my_products = response.data
      } catch (error) {
        console.error("Error fetching product data:", error);
      }
    },
    async fetchGraphs() {
      try {
        const response = await axios.get(
          'http://127.0.0.1:8000/accounts/api/v1/product_graph/',
        {
          headers: { Authorization: `Token ${this.token}` }  // this.token 사용
        })

        this.graph = response.data.graph
      } catch (error) {
        console.error("Error fetching graph data:", error);
      }
    },
    async fetchUserReviewCount() {
      try {
        if (!this.user_id) {
          console.log("사용자 ID를 가져오지 못했습니다.");
          return;
        }
        const response = await axios.get(
          `http://127.0.0.1:8000/accounts/api/v1/profile/${this.user_id}/reviews/count/`, 
          {
            headers: {
              Authorization: `Token ${this.token}`
            }
          })
          this.reviewCount = response.data.review_count
      } catch (error) {
        console.log("댓글 수를 불러오는 중 오류 발생: ", error)
      }
    },
    // 탈퇴하기 기능
    async deleteAccount() {
      if (!this.token) {
        alert("로그인 후 탈퇴할 수 있습니다.");
        return;
      }

      if (confirm("정말 탈퇴하시겠습니까?")) {
        try {
          // 탈퇴 API 호출
          const response = await axios.delete("http://127.0.0.1:8000/accounts/api/v1/delete/", {
            headers: {
              Authorization: `Token ${this.token}`,  // 토큰을 헤더에 포함
            },
          });

          if (response.status === 204) {
            alert("탈퇴가 완료되었습니다.");
            
            // 토큰 삭제
            this.token = null; 
            localStorage.removeItem("token");

            // 메인 페이지로 이동 후 새로고침
            this.$router.push({ name: "mainpage" }).then(() => {
              window.location.reload(); // 새로고침
            });
          }
        }  catch (error) {
          alert("탈퇴 처리에 실패했습니다. 다시 시도해주세요.");
          console.error(error);
        }
      }
    },
  },
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
.product-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}
</style>
