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

      <!-- 리뷰 섹션 -->
      <div class="review-page">
        <div class="review-container" >
          <h1 style="color: #585547; font-size: 32px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 700; margin-bottom: 10px; margin-top: 100px;">이 상품에 대한 나의 생각은?</h1>
          <!-- 리뷰 입력 및 버튼 -->
          <hr class="title-divider" />
          <div style="display: flex; align-items: center; margin-bottom: 20px; margin-top: 50px;">
            <input 
              id="review-content" 
              type="text" 
              v-model="newReviewContent" 
              placeholder="리뷰를 입력해주세요." 
              @keydown.enter="submitReview" 
              style="flex-grow: 1; padding: 10px; border: 1px solid #CDC7C0; border-radius: 10px; font-size: 16px; color: #585547; background: #FBF9F4;" 
              />
            <button @click="submitReview" style="padding: 10px 20px; background: #E6AF69; color: #FBF9F4; border: none; border-radius: 15px; font-size: 18px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 700; cursor: pointer; margin-left: 10px;" class="action-button">리뷰 작성하기</button>
          </div>

          <!-- 작성된 리뷰 목록 -->
          <div v-for="(review, index) in reviews" :key="index" style="margin-top: 30px; padding: 30px; border: 1px solid #E6AF69; border-radius: 10px; margin-bottom: 10px; background: #FBF9F4;">
            <div style="font-size: 14px; color: #585547; " >{{ review.user.username }} | {{ review.created_at }}</div>
            <div style="font-size: 20px; color: #585547; margin-top: 10px;">{{ review.content }}</div>
            <div v-if="review.user.id === user_id"style="margin-top: 20px;">
              <button @click="editReview(review)"  style="padding: 3px 10px; background: #E6AF69; color: #FBF9F4; border: none; border-radius: 15px; font-size: 16px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 700; cursor: pointer; " class="edit-action-button">수정</button>
              <button @click="deleteReview(review)"  style="padding: 3px 10px; background: #E6AF69; color: #FBF9F4; border: none; border-radius: 15px; font-size: 16px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 700; cursor: pointer; margin-left: 10px;" class="edit-action-button">삭제</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useCounterStore } from "@/stores/counter";
import axios from "axios";
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from "vue-router";
import { format } from 'date-fns';

export default {
  setup() {
    const store = useCounterStore();  // useCounterStore 호출
    const token = store.token;  // store에서 token 가져오기
    const route = useRoute();
    const router = useRouter();
    const isSubscribed = ref(null)
    const productId = route.params.productId;
    // const productCode = 'productInfo.fin_prdt_cd';
    const user_id = ref()

    const reviews = ref([]); // 리뷰 데이터 배열
    const newReviewContent = ref(""); // 새로운 리뷰 내용

    // **유저 ID를 가져오는 함수 추가**
    const fetchUserId = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/accounts/api/v1/user_info/",
          {
            headers: { Authorization: `Token ${token}` },
          }
        );
        user_id.value = response.data.pk; // 서버로부터 받은 유저 ID 저장
        console.log("User ID fetched successfully:", user_id.value);
      } catch (error) {
        console.error("Error fetching user ID:", error);
      }
    };

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

      } catch (error) {
        console.error('구독 상태를 가져오는 중 오류 발생:', error);
      }
    };

    const fetchReviews = async () => {
      const productId = route.params.productId;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/product/product_detail/${productId}/reviews/`); // 리뷰 조회
        reviews.value = response.data.map(review => ({
      ...review,
      created_at: format(new Date(review.created_at), 'yyyy-MM-dd HH:mm:ss'), // 날짜 포맷 변경
    }));
      } catch (error) {
        if (error.response) {
          // console.error("리뷰 조회 중 서버 에러:", error.response.data);
          console.error("리뷰 조회 중 서버 에러:");
        } else {
          console.error("리뷰 조회 중 기타 오류:", error.message);
        }
      }
    };

    const submitReview = async () => {
      const productId = route.params.productId;
      if (!newReviewContent.value.trim()) return; // 리뷰 내용이 비어 있을 경우 중단
      if (!token) {
        console.error("사용자 인증이 필요합니다."); // 토큰이 없을 경우 에러
        alert('로그인 후 이용해주세요');
        return;
      }

      try {
        // console.log("토큰 값:", token);  // 토큰 값 확인
        
        // 서버에 새로운 리뷰를 POST 요청
        const response = await axios.post(
          `http://127.0.0.1:8000/product/product_detail/${productId}/reviews/create/`,
          {
            content: newReviewContent.value,
          },
          {
            headers: { Authorization: `Token ${token}` }, // 인증 헤더 추가
          }
        );
        const newReview = response.data;
        newReview.created_at = format(new Date(newReview.created_at), 'yyyy-MM-dd HH:mm:ss');
        // 서버에서 응답받은 리뷰 데이터를 로컬 배열에 추가
        reviews.value.push(response.data); 
        // 리뷰 내용 입력 필드 초기화
        newReviewContent.value = "";
        
      } catch (error) {
        if (error.response) {
          console.error("리뷰 작성 중 서버 에러:", error.response.data);
        } else {
          console.error("리뷰 작성 중 기타 오류:", error.message);
        }
      }
    };


    const editReview = async (review) => {
      // 수정할 내용 입력 받기
      const updatedContent = prompt("수정할 내용을 입력하세요:", review.content);

      // 입력 내용이 없으면 종료
      if (updatedContent === null || updatedContent.trim() === "") return;

      try {
        // 서버에 PUT 요청을 보내서 리뷰 수정
        const response = await axios.put(
          `http://127.0.0.1:8000/product/product_detail/${productId}/reviews/${review.id}/`,
          { content: updatedContent },
          { headers: { Authorization: `Token ${token}` } }
        );

        // 서버 응답에서 수정된 내용으로 로컬 데이터 업데이트
        // 실제 서버에서 가져온 수정된 내용으로 업데이트하여 동기화
        const updatedReview = response.data;

        // 'created_at'과 'updated_at' 날짜 포맷 변경
        updatedReview.created_at = format(new Date(updatedReview.created_at), 'yyyy-MM-dd HH:mm:ss');
        updatedReview.updated_at = format(new Date(updatedReview.updated_at), 'yyyy-MM-dd HH:mm:ss');

        // 리뷰 목록에서 수정된 리뷰 찾아서 업데이트
        const index = reviews.value.findIndex((r) => r.id === review.id);
        if (index !== -1) {
          reviews.value[index] = updatedReview;
        }
      } catch (error) {
        console.error("리뷰 수정 중 오류 발생:", error);
      }
    };


    const deleteReview = async (review) => {
      if (!confirm("정말 삭제하시겠습니까?")) return;
      try {
        await axios.delete(`http://127.0.0.1:8000/product/product_detail/${productId}/reviews/${review.id}/`, {
          headers: { Authorization: `Token ${token}` },
        });
        reviews.value = reviews.value.filter((r) => r.id !== review.id); // 삭제된 리뷰 제거
        console.log("리뷰 삭제 완료!")
      } catch (error) {
        console.error("리뷰 삭제 중 오류 발생:", error);
      }
    };

    // 3. 컴포넌트가 로드될 때 초기값 로드
    onMounted(() => {
      fetchUserId();
      fetchSubscriptionStatus();
      fetchReviews();
    });

    return {
      token,  // 반환하여 컴포넌트에서 사용
      isSubscribed,
      reviews,
      newReviewContent,
      fetchReviews,
      submitReview,
      editReview,
      deleteReview,
      user_id,
    };
  },
  data() {
    return {
      productInfo: {}, // 제품 상세 정보
      bank_dict: {
        'HB저축은행': 'HB저축은행.png',
        '경남은행': '경남은행.png', 
        '고려저축은행': '고려저축은행.png', 
        '광주은행': '광주은행.jpg', 
        '국민은행': '국민은행.jpg', 
        '국제저축은행': '국제저축은행.png', 
        '금화저축은행': '금화저축은행.jfif', 
        '남양저축은행': '남양저축은행.png', 
        '농협은행주식회사': '농협은행주식회사.jfif', 
        '다올저축은행': '다올저축은행.png', 
        '더케이저축은행': '더케이저축은행.jpeg', 
        '디비저축은행': '디비저축은행.jpg', 
        '디에이치저축은행': '디에이치저축은행.jpg', 
        '모아저축은행': '모아저축은행.jpg', 
        '민국저축은행': '민국저축은행.jpg', 
        '바로저축은행': '바로저축은행.jpg', 
        '부산은행': '부산은행.jpg', 
        '수협은행': '수협은행.jpg', 
        '스카이저축은행': '스카이저축은행.png', 
        '신한은행': '신한은행.jpg', 
        '아이엠뱅크': '아이엠뱅크.png', 
        '안국저축은행': '안국저축은행.jpg', 
        '애큐온저축은행': '애큐온저축은행.png', 
        '에스비아이저축은행': '에스비아이저축은행.png', 
        '오에스비저축은행': '오에스비저축은행.jpg', 
        '우리은행': '우리은행.jpg', 
        '우리저축은행': '우리저축은행.png', 
        '유안타저축은행': '유안타저축은행.png', 
        '인성저축은행': '인성저축은행.jpg', 
        '전북은행': '전북은행.jfif', 
        '제주은행': '제주은행.png', 
        '조은저축은행': '조은저축은행.png', 
        '주식회사 카카오뱅크': '주식회사_카카오뱅크.jpg', 
        '주식회사 케이뱅크': '케이뱅크.png', 
        '중소기업은행': '중소기업은행.jpg', 
        '키움예스저축은행': '키움예스저축은행.webp', 
        '토스뱅크 주식회사': '주식회사_토스뱅크.jpg', 
        '평택저축은행': '평택저축은행.png', 
        '푸른상호저축은행': '푸른상호저축은행.jpg', 
        '하나은행': '하나은행.jpg', 
        '한국산업은행': '한국산업은행.jpg', 
        '한국스탠다드차타드은행': '한국스탠다드차타드은행.jpg', 
        '흥국저축은행': '흥국저축은행.jpg'},
      fieldMappings: {
        is_saving: "예금 / 적금",
        kor_co_nm: "금융회사 이름",
        fin_prdt_nm: "금융상품명",
        join_way: "가입방법",
        mtrt_int: "만기 후 이자율",
        spcl_cnd: "우대조건",
        join_deny: "가입제한",
        join_member: "가입대상",
        etc_note: "기타유의사항",
        max_limit: "최고한도",
      },
    };
  },

  mounted() {
    // 서버에서 데이터를 가져오는 메소드 호출
    this.fetchProducts();
  },

  methods: {
    getBankImage(bankName) {
      const imageName = this.bank_dict[bankName];
      return imageName ? `/assets/banks/${imageName}` : '/assets/banks/placeholder.png'; // public 디렉토리 기준
    },
    async fetchProducts() {
      try {
        const productCode = this.$route.params.productId;
        const response = await axios.get(
          `http://127.0.0.1:8000/product/product_detail/${productCode}`
        );
        this.productInfo = response.data; // 상품 상세 정보 저장
        delete this.productInfo.fin_prdt_cd;
        delete this.productInfo.fin_co_no;
        delete this.productInfo.reviews;
        this.productInfo.is_saving = this.productInfo.is_saving ? "적금" : "예금";
        const joinDenyMapping = {
          1: '제한없음',
          2: '서민전용',
          3: '일부제한'
        };

        // 'join_deny' 필드가 있을 경우 매핑 적용
        if (this.productInfo.join_deny !== undefined) {
          this.productInfo.join_deny = joinDenyMapping[this.productInfo.join_deny] || '기타';
        }
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
  },
};
</script>

<style scoped>
/* 부모 컨테이너 */
.parent-container {
  width: 100%;
  height: 100%;
  margin-top: 40px;
  background: #F9EB87;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 40px;
}

/* 카드 컨테이너 */
.card-container {
  justify-content: center;
  width: 870px;
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
  justify-content: center; /* 가운데 정렬 */
  align-items: center; /* 수직 가운데 정렬 */
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

/* 상품 정보 컨테이너 */
.product-details-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  box-sizing: border-box;
}

/* 상품 정보 박스 */
.product-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  flex-grow: 1; /* 모든 박스가 동일하게 크기를 나누게 함 */
  flex-wrap: nowrap;
}

/* 상품 라벨 박스 */
.product-label-box {
  flex-shrink: 0;
  max-width: 30%;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  border: 1px solid #d9d9d9;
  border-radius: 8px;
  padding: 8px;
  background-color: #E6AF69;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 상품 값 박스 */
.product-value-box {
  padding: 8px 12px;
  border: none;
  border-radius: 8px;
  background-color: transparent;
  color: #585547;
  width: 100%; /* 부모의 크기를 채우게 함 */
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
  font-size: 18px;
  color: #ffffff;
  font-family: "IBM Plex Sans KR", sans-serif;
  font-weight: 00;
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
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3);
}

.action-button:hover {
  background: #E6AF69;
  transform: scale(1.05);
}

.edit-action-button {
  background: #E6AF69;
  color: #FBF9F4;
  font-size: 15px;
  font-family: "IBM Plex Sans KR", sans-serif;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s, transform 0.3s ease;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3);
}

.edit-action-button:hover {
  background: #E6AF69;
  transform: scale(1.05);
}
</style>
