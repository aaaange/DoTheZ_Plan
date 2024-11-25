<template>
  <div class="parent-container" style="padding: 80px 0 0 0; text-align: center;">
    <h2 style="color: #585547; font-size: 50px; font-family: 'IBM Plex Sans KR', sans-serif;">전체 상품 목록</h2>

    <!-- 검색 창 -->
    <div style="margin-top: 20px; display: flex; justify-content: center; gap: 20px;">
      <!-- 은행명 검색 -->
      <input type="text" v-model="searchQuery.bank" placeholder="은행명 검색" 
        style="padding: 12px; width: 300px; border-radius: 8px; border: 1px solid #D9D9D9; font-size: 16px; outline: none;">
      <!-- 금융상품명 검색 -->
      <input type="text" v-model="searchQuery.product" placeholder="금융상품명 검색" 
        style="padding: 12px; width: 300px; border-radius: 8px; border: 1px solid #D9D9D9; font-size: 16px; outline: none;">
      <!-- 예금/적금 선택 -->
      <select v-model="searchQuery.type" 
        style="padding: 12px; width: 300px; border-radius: 8px; border: 1px solid #D9D9D9; font-size: 16px; outline: none;">
        <option value="예금 / 적금" disabled>예금 / 적금</option>
        <option value="예금">예금</option>
        <option value="적금">적금</option>
      </select>
      <!-- 검색 버튼 -->
      <button class="search-button" @click="applyFilter">
        검색
      </button>
    </div>

    <!-- 상품 리스트 -->
    <div class="product-list-container" style="margin-top: 40px;" v-if="!isLoading">
      <div v-if="filteredProducts.length === 0">
        <p>조건에 맞는 상품이 없습니다.</p>
      </div>
      <div class="product-card" v-for="(option, index) in filteredProducts" :key="index">
        <router-link :to="{ name: 'productdetail', params: { productId: option.fin_prdt_cd } }" 
          style="display: flex; text-decoration: none; width: 100%; align-items: center;">
          <!-- 은행 로고 이미지 -->
          <img class="product-image" 
            :src="getBankImage(option.product.kor_co_nm)" 
            :alt="option.product.kor_co_nm" 
            style="width: 64px; height: 64px; margin-right: 16px; margin-left: 16px; border-radius: 8px; object-fit: cover;"/>
          
          <div class="product-details">
            <p class="product-name" style="font-size: 18px; font-weight: 500; text-align: left;">
              <span class="product-box" style="display: inline-block; margin-top: 10px; margin-left: 10px;">금융상품명</span> {{ option.product.fin_prdt_nm }}<br>
              <span class="product-box" style="display: inline-block; margin-top: 10px; margin-left: 10px;">상품유형  </span> {{ option.product.is_saving ? '적금' : '예금' }}<br>
              <span class="product-box" style="display: inline-block; margin-top: 10px; margin-left: 10px;">금리      </span> {{ option.intr_rate }}%
            </p>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      allProducts: [],          // 전체 제품 리스트
      filteredProducts: [],     // 필터링된 제품 리스트
      searchQuery: {
        bank: '',               // 은행명 검색
        product: '',            // 금융상품명 검색
        type: "예금 / 적금",     // 상품유형 검색
      },
      isLoading: true,          // 데이터 로딩 상태
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
        '흥국저축은행': '흥국저축은행.jpg'}
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
        // 서버에서 데이터 요청
        const response = await axios.get('http://127.0.0.1:8000/product/options/');
        const data = response.data;
        this.allProducts = data;         // 전체 상품 리스트 저장
        this.filteredProducts = data;    // 초기에는 모든 상품 표시
      } catch (error) {
        console.error("Error fetching product data:", error);
      } finally {
        this.isLoading = false;  // 로딩이 끝났음을 표시
      }
    },
    applyFilter() {
      // 검색 조건에 맞는 상품 필터링
      this.filteredProducts = this.allProducts.filter(option => {
        // 은행명 필터링
        const matchesBank = this.searchQuery.bank 
          ? option.product.kor_co_nm && option.product.kor_co_nm.includes(this.searchQuery.bank) 
          : true;
        
        // 금융상품명 필터링
        const matchesProduct = this.searchQuery.product 
          ? option.product.fin_prdt_nm && option.product.fin_prdt_nm.includes(this.searchQuery.option) 
          : true;

        // 상품유형 필터링
        const matchesType = this.searchQuery.type && this.searchQuery.type !== "예금 / 적금"
          ? option.is_saving ? this.searchQuery.type === '적금' : this.searchQuery.type === '예금'
          : true;

        return matchesBank && matchesProduct && matchesType;
      });
    }
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

.product-box {
  display: inline-block;
  padding: 4px 8px;
  margin-right: 8px;
  background-color: #f4f4f4; /* 박스 배경색 */
  border-radius: 6px;       /* 둥근 모서리 */
  font-weight: bold;        /* 텍스트 굵게 */
  font-size: 14px;          /* 텍스트 크기 */
  color: #585547;           /* 텍스트 색상 */
  border: 1px solid #d9d9d9; /* 테두리 */
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

/* 버튼 */
.search-button {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  background-color: #E6AF69;
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* 기본 그림자 효과 */
}

.search-button:hover {
  background-color: #E6AF69; /* 예: hover시 버튼 색상 변경 */
  transform: scale(1.05); /* hover시 버튼 크기 커지기 */
}
</style>
