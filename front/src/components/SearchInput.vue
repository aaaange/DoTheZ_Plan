<script setup>
import { ref } from 'vue';

const searchText = ref('');
const emit = defineEmits(['search']);

// 검색 버튼 클릭 이벤트
const handleSearch = () => {
  if (searchText.value.trim()) {
    emit('search', searchText.value.trim());
  } else {
    alert("검색어를 입력하세요.");
  }
};
</script>

<template>
  <div class="search-container">
    <input
      type="text"
      v-model="searchText"
      placeholder="지역을 입력하세요"
      @keyup.enter="handleSearch"
      class="search-input"
    />
    <button @click="handleSearch" class="search-button">검색</button>
  </div>
</template>

<style scoped>
.search-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.search-input {
  width: 80%;
  padding: 10px;
  border-radius: 25px;
  border: 1px solid #ccc;
  font-size: 16px;
  outline: none;
  margin-right: 10px;
}

.search-input:focus {
  border-color: #E6AF69;
}

.search-button {
  padding: 10px 20px;
  border-radius: 25px;
  background-color: #E6AF69;
  color: white;
  font-size: 16px;
  border: none;
  cursor: pointer;
}

.search-button:hover {
  background-color: #E6AF69;
}
</style>
