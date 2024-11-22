<template>
  <div class="parent-container" style="padding: 80px 0 0 0; text-align: center;">
    <h2 style="color: #585547; font-size: 50px; font-family: 'IBM Plex Sans KR', sans-serif;">전체 상품 목록</h2>

    <!-- 검색 창 -->
    <div style="margin-top: 20px; display: flex; justify-content: center; gap: 20px;">
      <input type="text" v-model="searchQuery.name" placeholder="상품명 검색" style="padding: 12px; width: 300px; border-radius: 8px; border: 1px solid #D9D9D9; font-size: 16px; outline: none;">
      <input type="text" v-model="searchQuery.category" placeholder="카테고리 검색" style="padding: 12px; width: 300px; border-radius: 8px; border: 1px solid #D9D9D9; font-size: 16px; outline: none;">
      <input type="number" v-model="searchQuery.price" placeholder="가격 검색" style="padding: 12px; width: 300px; border-radius: 8px; border: 1px solid #D9D9D9; font-size: 16px; outline: none;">
    </div>

    <!-- 상품 리스트 -->
    <div class="product-list-container" style="margin-top: 40px;">
      <div class="product-card" v-for="(product, index) in filteredProducts" :key="index">
        <router-link
          :to="{ name: 'productdetail' }" 
          style="display: flex; text-decoration: none; width: 100%;" 
        >
          <img class="product-image" src="https://via.placeholder.com/80" alt="상품 이미지" style="width: 64px; height: 64px; margin-right: 16px; border-radius: 8px; object-fit: cover;"/>
          <div class="product-details">
            <p class="product-name" style="font-size: 18px; font-weight: 500;">
              {{ product.name }}
            </p>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProductList", // 컴포넌트 명시적으로 지정
  data() {
    return {
      searchQuery: {
        name: "",
        category: "",
        price: "",
      },
      products: [
        { name: "상품 이름 1", category: "전자", price: 100 },
        { name: "상품 이름 2", category: "의류", price: 50 },
        { name: "상품 이름 3", category: "가전", price: 300 },
        { name: "상품 이름 4", category: "전자", price: 150 },
        { name: "상품 이름 5", category: "의류", price: 70 },
        { name: "상품 이름 6", category: "가전", price: 200 },
        { name: "상품 이름 7", category: "전자", price: 250 },
      ],
    };
  },
  computed: {
    filteredProducts() {
      return this.products.filter(product => {
        return (
          product.name.toLowerCase().includes(this.searchQuery.name.toLowerCase()) &&
          product.category.toLowerCase().includes(this.searchQuery.category.toLowerCase()) &&
          (this.searchQuery.price ? product.price <= this.searchQuery.price : true)
        );
      });
    },
  },
};
</script>

<style scoped>
/* 부모 컨테이너 */
.parent-container {
  width: 100%;
  max-width: 1200px; /* 최대 너비 제한 */
  margin: 0 auto; /* 중앙 정렬 */
  padding: 40px 16px 0 16px; /* 양쪽 패딩 추가 */
  text-align: center;
  box-sizing: border-box; /* 패딩과 경계를 포함한 박스 크기 계산 */
}

/* 상품 리스트 컨테이너 */
.product-list-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* 왼쪽 정렬 유지 */
  gap: 12px;
  width: 100%; /* 부모 너비를 화면 크기에 맞춤 */
  max-width: 1200px; /* 화면 크기에 따라 적절히 제한 */
  margin: 0 auto; /* 가운데 정렬 */
  padding: 16px;
  background: #f9eb87;
  box-sizing: border-box; /* 패딩과 경계를 포함한 박스 크기 계산 */
  overflow-x: hidden; /* 콘텐츠가 부모 너비를 초과할 경우 잘리도록 설정 */
}

/* 상품 카드 */
.product-card {
  display: flex;
  align-items: center;
  width: 100%; /* 부모 너비에 맞게 확장 */
  max-width: 100%; /* 부모 요소 기준 너비 제한 */
  padding: 16px;
  background: #fbf9f4;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  font-family: "IBM Plex Sans KR", sans-serif;
  color: #585547;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
  box-sizing: border-box; /* 패딩 포함 */
}

.router-link {
  display: flex;
  align-items: center;
  width: 100%; /* 부모 너비에 맞게 확장 */
  max-width: 100%; /* 부모 요소 기준 너비 제한 */
  padding: 16px;
  background: #fbf9f4;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  font-family: "IBM Plex Sans KR", sans-serif;
  color: #585547;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
  box-sizing: border-box; /* 패딩 포함 */
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

/* 이미지 */
.product-image {
  width: 64px;
  height: 64px;
  margin-right: 16px;
  border-radius: 8px;
  object-fit: cover;
  background: #e0e0e0;
}

/* 상품 세부정보 */
.product-details {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
}

.product-name {
  font-size: 18px;
  font-weight: 500;
}

input {
  padding: 12px;
  width: 300px;
  border-radius: 8px;
  border: 1px solid #D9D9D9;
  font-size: 16px;
  outline: none;
}
</style>
