<template>
  <div
    style="width: 100%; height: 100vh; padding-top: 119px; background: #F9EB87; justify-content: center; align-items: center;"
  >
    <div class="recommend-container">
      <h1>나에게 가장 어울리는 상품은?</h1>
      <ul class="product-list">
        <li v-for="(product, index) in recommendedProducts" :key="index" class="product-card">
          <div class="product-info">
            <div class="product-rank">{{ index + 1 }}</div>
            <div class="product-details">
              <p class="product-name">상품 이름 : {{ product['상품 이름'] }}</p>
              <p class="product-name">은행 이름 : {{ product['금융 회사'] }}</p>
              <p class="product-name">예상 수익 : {{ product['예상 수익'] }}만 원</p>
            </div>
          </div>
          <router-link :to="'/productdetail/' + String(product['상품 코드'])">
            <button class="join-button">가입하기</button>
          </router-link>
        </li>
      </ul>

      <!-- 로딩 상태 표시 -->
      <div v-if="isLoading" class="loading-message">
        모델 생성 중입니다... 잠시만 기다려 주세요.
      </div>

      <!-- 추가 추천 버튼 -->
      <button v-else @click="initializeAndFetchRecommendations" class="additional-recommendation-button">
        추가 추천 받기
      </button>

      <!-- 추가 추천 리스트 -->
      <div v-if="additionalRecommendations" class="additional-product-list">
        <p class="product-name">상품 이름 : {{ additionalRecommendations.recommended_product }}</p>
        <p class="product-name">은행 이름 : {{ additionalRecommendations.kor_co_nm }}</p>
        <router-link :to="'/productdetail/' + String(additionalRecommendations.product_code)">
          <button class="join-button">가입하기</button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRoute } from 'vue-router';

  // 기존 추천 리스트
  const recommendedProducts = ref([]);

  // 추가 추천 리스트
  const additionalRecommendations = ref([]);

  // 로딩 상태 관리
  const isLoading = ref(false);

  // 라우트에서 userSurveyId 추출
  const route = useRoute();
  const userSurveyId = route.params.userSurveyId;
  const user_survey_id = parseInt(userSurveyId, 10);

  // 초기 추천 상품 요청
  onMounted(async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/surveys/api/v1/product-filtering/${user_survey_id}/`);
      recommendedProducts.value = response.data.recommended_products;
    } catch (error) {
      console.error("상품 추천 정보를 가져오는 데 실패했습니다:", error);
    }
  });

  const fetchProductDetails = async (productName) => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/surveys/api/v1/get_product_by_name/", {
        product_name: productName
      });

      if (response.data.kor_co_nm) {
        console.log("상품의 기업 이름:", response.data.kor_co_nm);
        // 추가 처리: UI에 표시하거나 상태 업데이트
        additionalRecommendations.value = response.data
      } else {
        console.error("상품을 찾을 수 없습니다.");
      }
    } catch (error) {
      console.error("상품 조회 실패:", error);
    }
  };

  // 추가 추천 요청
  const initializeAndFetchRecommendations = async () => {
    isLoading.value = true; // 로딩 상태 활성화
    try {
      // 모델 초기화 요청
      const initResponse = await axios.post("http://127.0.0.1:8000/surveys/api/v1/initialize_model/");
      if (initResponse.data.message) {
        console.log("모델 초기화 성공:", initResponse.data.message);

        // user_survey_id 기반으로 추천 요청
        const recommendResponse = await axios.post(`http://127.0.0.1:8000/surveys/api/v1/recommend_product_for_user/`, {
          user_survey_id: user_survey_id,
        });
        if (recommendResponse.data.recommended_product) {
          fetchProductDetails(recommendResponse.data.recommended_product);
        }
        else {
          console.warn("추천 상품이 없습니다.");
        }
      }
    } catch (error) {
      console.error("추가 추천 요청 실패:", error.response?.data || error.message);
    } finally {
      isLoading.value = false; // 로딩 상태 비활성화
    }
  };

  // 상품 이름을 이용해서 추가 추천 상품의 세부 정보를 가져옵니다
  
</script>


<style scoped>

/* 전체 컨테이너 스타일 */
.recommend-container {
  max-width: 650px;
  margin: 0 auto;
  padding: 40px;
  background-color: #FBF9F4; /* 연한 베이지 배경 */
  border-radius: 30px;
  box-shadow: 6px 9px 4px rgba(0, 0, 0, 0.2);
  text-align: center;
}

/* 제목 스타일 */
h1 {
  font-size: 30px;
  font-family: "IBM Plex Sans KR", sans-serif;
  font-weight: 700;
  color: #585547;
  margin-bottom: 30px;
}

/* 상품 리스트 스타일 */
.product-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

/* 개별 상품 카드 스타일 */
.product-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #F7F4EA; /* 밝은 베이지 */
  border-radius: 15px;
  border: 1px solid #585547; /* 테두리 */
  padding: 20px;
  margin-bottom: 15px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.product-details {
  text-align: left;
}

/* 상품 순위 스타일 */
.product-rank {
  font-size: 24px;
  font-weight: 700;
  color: #4A4A4A;
  margin-right: 20px;
}

/* 상품 정보 영역 */
.product-info {
  display: flex;
  align-items: center;
}

/* 상품 이름 스타일 */
.product-name {
  font-size: 20px;
  font-family: "IBM Plex Sans KR", sans-serif;
  font-weight: 500;
  color: #585547;
}

/* 가입하기 버튼 스타일 */
.join-button {
  font-size: 16px;
  font-family: "IBM Plex Sans KR", sans-serif;
  color: #FFFFFF;
  background-color: #E6AF69; /* 메인 버튼 색상 */
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.join-button:hover {
  background-color: #D69558; /* hover 색상 */
  transform: scale(1.05); /* hover 시 살짝 확대 */
}


</style>
