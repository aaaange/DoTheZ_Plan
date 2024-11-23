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
        <img class="product-image" src="" alt="상품 이미지" />
        <span class="product-name">{{ productInfo.fin_prdt_cd }}</span>
        <!-- 상품 가입 페이지로 이동 버튼을 상품 이름 옆에 배치 -->
        <button class="action-button">상품 가입 페이지로 이동</button>
      </div>

      <!-- 상품 상세 정보 -->
      <div class="product-details-container">
        <div v-for="(info, index) in productInfo" :key="index" class="product-info">
          <span class="product-label">{{ info }}</span>
        </div>
      </div>

      <!-- 버튼 섹션 -->
      <div class="button-container">
        <button class="action-button" @click="toggleSubscription">
          {{ isSubscribed ? '내 상품에 삭제' : '내 상품에 등록' }}
        </button>
      </div>
    </div>
  </div>
  <!-- 리뷰 섹션 -->
  <div class="review-page" style="width: 100%; min-height: 100vh; background: #F9EB87; display: flex; justify-content: center; align-items: center; padding: 20px;">
    <div class="review-container" style="width: 800px; background: #FBF9F4; padding: 40px; border-radius: 20px; box-shadow: 6px 9px 4px rgba(0, 0, 0, 0.2);">
      <!-- <h1 style="color: #585547; font-size: 32px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 700; margin-bottom: 10px;">상품 상세 페이지</h1> -->

      <!-- 리뷰 내용 입력 및 버튼 배치 -->
      <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <input
          id="review-content"
          type="text"
          v-model="newReviewContent"
          placeholder="리뷰를 입력해주세요."
          style="flex-grow: 1; padding: 10px; border: 1px solid #CDC7C0; border-radius: 10px; font-size: 16px; color: #585547; background: #FBF9F4;"
        />
        <button @click="submitReview" style="padding: 10px 20px; background: #E6AF69; color: #FBF9F4; border: none; border-radius: 15px; font-size: 18px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 700; cursor: pointer; margin-left: 10px;">
          리뷰 작성하기
        </button>
      </div>

      <!-- 작성된 리뷰 목록 -->
      <div v-for="(review, index) in reviews" :key="index" style="margin-top: 30px; padding: 15px; border: 1px solid #E6AF69; border-radius: 10px; margin-bottom: 10px; background: #FBF9F4;">
        <div style="font-size: 14px; color: #585547;">{{ review.username }} | {{ review.date }}</div>
        <div style="font-size: 16px; color: #585547; margin-top: 10px;">{{ review.content }}</div>
        <div style="margin-top: 10px;">
          <button @click="editReview(index)" style="padding: 5px 10px; background: #E6AF69; color: #FBF9F4; border: none; border-radius: 10px; font-size: 14px; cursor: pointer;">수정</button>
          <button @click="deleteReview(index)" style="padding: 5px 10px; background: #E6AF69; color: #FBF9F4; border: none; border-radius: 10px; font-size: 14px; cursor: pointer; margin-left: 10px;">삭제</button>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import { useCounterStore } from "@/stores/counter";
import axios from "axios";
import { onMounted, ref } from 'vue';
import { useRoute } from "vue-router";

export default {
  setup() {
    const store = useCounterStore();  // useCounterStore 호출
    const token = store.token;  // store에서 token 가져오기
    const route = useRoute();
    const isSubscribed = ref(null)
    const productId = route.params.productId;

    const fetchSubscriptionStatus = async () => {
      try {
        // Authorization 헤더에 token을 포함시켜 요청
        const response = await axios.get(
          `http://127.0.0.1:8000/accounts/api/v1/check_state/${productId}/`,
          {
            headers: { Authorization: `Token ${token}` }  // this.token 사용
          }
        );
        isSubscribed.value = response.data.state;
        console.log(isSubscribed.value)

      } catch (error) {
        console.error('구독 상태를 가져오는 중 오류 발생:', error);
      }
    };

    // 3. 컴포넌트가 로드될 때 초기값 로드
    onMounted(() => {
      fetchSubscriptionStatus();
    });

    return {
      token,  // 반환하여 컴포넌트에서 사용
      isSubscribed,
    };
  },
  data() {
    return {
      newReviewContent: '', // 리뷰 내용
      reviews: [
        {
          username: '닉네임12345',
          date: '2024-11-22 15:30',
          content: '해당 메세지는 댓글 내용입니다.'
        },
        {
          username: '닉네임67890',
          date: '2024-11-21 10:20',
          content: '해당 메세지는 다른 댓글 내용입니다.'
        }
      ], // 리뷰 목록
      productInfo: {}, // 제품 상세 정보
    };
  },

  mounted() {
    // 서버에서 데이터를 가져오는 메소드 호출
    this.fetchProducts();
  },

  methods: {
    async fetchProducts() {
      try {
        const productCode = this.$route.params.productId;
        const response = await axios.get(
          `http://127.0.0.1:8000/product/product_detail/${productCode}`
        );
        this.productInfo = response.data; // 상품 상세 정보 저장
      } catch (error) {
        console.error("Error fetching product data:", error);
      }
    },

    // 상품 등록 토글
    async toggleSubscription() {
      try {
        const productId = this.$route.params.productId; // 현재 상품 ID

        // Authorization 헤더에 token을 포함시켜 요청
        const response = await axios.post(
          `http://127.0.0.1:8000/accounts/api/v1/subscribe/${productId}/`,
          {},
          {
            headers: { Authorization: `Token ${this.token}` }  // this.token 사용
          }
        );

        // 서버 응답 메시지 출력
        alert(response.data.message);

        // 응답 데이터에서 사용자 가입 상품 목록을 업데이트하거나 처리
        console.log("Subscribed products:", response.data.user_products);

        this.isSubscribed = !this.isSubscribed

      } catch (error) {
        console.error("Error toggling subscription:", error);
        alert("상품 등록에 실패했습니다. 다시 시도해주세요.");
      }
    },

    submitReview() {
      if (!this.newReviewContent) return;
      this.reviews.push({
        username: '새로운 사용자',
        date: new Date().toLocaleString(),
        content: this.newReviewContent
      });
      this.newReviewContent = '';
    },

    editReview(index) {
    const updatedContent = prompt('수정할 내용을 입력하세요:', this.reviews[index].content);
    if (updatedContent !== null && updatedContent.trim() !== '') {
      this.reviews[index].content = updatedContent;
      this.reviews[index].date = new Date().toLocaleString();
    }
  },



    deleteReview(index) {
      if (confirm('정말 삭제하시겠습니까?')) {
        this.reviews.splice(index, 1);
      }
    }
  },
};
</script>

<style scoped>
/* 부모 컨테이너 */
.parent-container {
  width: 100%;
  height: 100vh;
  margin-top: 40px;
  background: #F9EB87;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 40px;
  overflow-y: auto; /* 스크롤이 가능하도록 */
}

/* 카드 컨테이너 */
.card-container {
  width: 863px;
  background: #FBF9F4;
  border-radius: 30px;
  box-shadow: 6px 9px 4px rgba(0, 0, 0, 0.20);
  padding: 40px;
  box-sizing: border-box;
  margin-top: 40px; /* 타이틀이 카드 안에 있도록 여백 설정 */
}

/* 타이틀 섹션 */
.title-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px; /* 타이틀과 콘텐츠 간 간격 조정 */
}

.page-title {
  font-size: 50px;
  font-family: "IBM Plex Sans KR", sans-serif;
  font-weight: 700;
  color: #585547;
  margin: 0;
}

.title-divider {
  width: 100%;
  border: 1px solid #CDC7C0;
  margin-top: 10px;
}

/* 상품 이름 박스 */
.product-name-box {
  background-color: #F1E8D2;
  padding: 20px;
  margin-bottom: 30px;
  border-radius: 8px;
  display: flex;
  justify-content: space-between; /* 버튼과 상품 이름을 양쪽으로 배치 */
  align-items: center;
}

.product-name {
  font-size: 24px;
  font-family: "IBM Plex Sans KR", sans-serif;
  font-weight: 600;
  color: #585547;
}

/* 상품 이미지 왼쪽 배치 */
.product-image {
  width: 40px; /* 적절한 크기로 설정 */
  height: 40px;
  margin-right: 15px; /* 이미지와 상품 이름 사이의 간격 */
}

/* 상품 상세 정보 */
.product-details-container {
  margin-top: 20px;
}

.product-info {
  display: flex;
  justify-content: space-between;
  padding: 15px 0;
  border-bottom: 1px solid #D9D9D9;
}

.product-label {
  font-size: 20px;
  color: #585547;
  font-family: "IBM Plex Sans KR", sans-serif;
  font-weight: 400;
}

.product-info-text {
  font-size: 18px;
  color: #585547;
  font-family: "IBM Plex Sans KR", sans-serif;
  font-weight: 400;
}

/* 버튼 섹션 */
.button-container {
  margin-top: 40px;
  display: flex;
  justify-content: flex-end; /* 오른쪽 정렬 */
}

.action-button {
  padding: 15px 30px;
  background: #E6AF69;
  color: #FBF9F4;
  font-size: 15px;
  font-family: "IBM Plex Sans KR", sans-serif;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s, transform 0.3s ease;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.action-button:hover {
  background: #707070;
  transform: scale(1.05);
}
</style>
