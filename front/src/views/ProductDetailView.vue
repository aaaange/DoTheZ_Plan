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
        <span class="product-name">{{ productName }}</span>
        <!-- 상품 가입 페이지로 이동 버튼을 상품 이름 옆에 배치 -->
        <button class="action-button">상품 가입 페이지로 이동</button>
      </div>

      <!-- 상품 상세 정보 -->
      <div class="product-details-container">
        <div v-for="(info, index) in productInfo" :key="index" class="product-info">
          <span class="product-label">{{ info.label }}</span>
          <span class="product-info-text">{{ info.value }}</span>
        </div>
      </div>

      <!-- 버튼 섹션 -->
      <div class="button-container">
        <button class="action-button">내 상품에 등록</button>
      </div>
    </div>
  </div>
</template>

<script setup>
// 백엔드에서 받아오는 상품 정보 예시
const productName = "상품 이름";
const productInfo = [
  { label: "상품 정보 2", value: "상품 정보 7" },
  { label: "상품 정보 3", value: "상품 정보 3" },
  { label: "상품 정보 4", value: "상품 정보 4" },
  { label: "상품 정보 5", value: "상품 정보 5" },
  { label: "상품 정보 6", value: "상품 정보 6" },
  { label: "상품 정보 7", value: "상품 정보 7" },
];
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
