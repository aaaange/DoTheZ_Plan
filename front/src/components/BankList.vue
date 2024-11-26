<script setup>
const props = defineProps({
  places: Array, // 검색 결과
});
</script>

<template>
  <div class="results-container">
    <h2 class="results-title">검색 결과</h2>
    <div v-if="places.length > 0" class="bank-list">
      <div v-for="place in places" :key="place.id" class="bank-item">
        <h3 class="bank-name">▶ {{ place.place_name }}</h3>
        <p class="bank-address">{{ place.road_address_name || place.address_name }}</p>
        <p class="bank-address">전화번호 : {{ place.phone || place.phone }}</p>
        
      </div>
    </div>
    <p v-else class="no-results">근처 은행을 찾을 수 없습니다.</p>
  </div>
</template>

<style scoped>
/* 전체 컨테이너 */
.results-container {
  max-width: 700px;
  height: 600px;
  position: relative;
  top: -80px;
}

/* 제목 스타일 */
.results-title {
  font-size: 1.8em;
  color: #585547;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: left;
}

/* 리스트 스타일 */
.bank-list {
  max-height: 430px; /* 스크롤 높이 제한 */
  overflow-y: auto;
  list-style: none;
  text-align: left;
}

/* 개별 아이템 스타일 */
.bank-item {
  margin-bottom: 10px;
}

/* 은행 이름 */
.bank-name {
  font-size: 1.2em;
  font-weight: bold;
  color: #585547;
}

/* 은행 주소 */
.bank-address {
  font-size: 1em;
  color: #7f8c8d;
  margin-top: 4px;
}

/* 결과 없음 메시지 */
.no-results {
  color: #e74c3c;
  font-size: 20px;
  font-weight: bold;
  margin-top: 20px;
}
</style>
