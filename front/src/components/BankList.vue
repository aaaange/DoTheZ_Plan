<script setup>
const props = defineProps({
  places: Array, // 검색 결과
});
</script>

<template>
  <div>
    <h2 class="results-title">검색 결과</h2>
    <div v-if="places.length > 0" class="bank-list">
      <div v-for="place in places" :key="place.id" class="bank-item">
        <h3 class="bank-name">{{ place.place_name }}</h3>
        <p class="bank-address">{{ place.road_address_name || place.address_name }}</p>
      </div>
    </div>
    <p v-else class="no-results">근처 은행을 찾을 수 없습니다.</p>
  </div>
</template>

<style scoped>
.results-title {
  font-size: 1.5em;
  color: #333;
  margin-bottom: 20px;
}

.bank-list {
  display: flex;
  flex-direction: column;
}

.bank-item {
  background-color: white;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.bank-name {
  font-size: 1.2em;
  font-weight: bold;
  margin-bottom: 5px;
}

.bank-address {
  font-size: 1em;
  color: #555;
}

.no-results {
  color: #ff6666;
  font-size: 1.2em;
  text-align: center;
}
</style>
