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
              <p class="product-name">{{ product.name }}</p>
            </div>
          </div>
          <button class="join-button">가입하기</button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue';

// 예시 추천 데이터
const recommendedProducts = reactive([
  { name: "튼튼 금융", details: "고수익 예금 상품" },
  { name: "튼튼 금융", details: "장기 적금 상품" },
  { name: "튼튼 금융", details: "저위험 투자 상품" },
]);
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
