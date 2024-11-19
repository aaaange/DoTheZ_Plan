<script setup>
import SearchInput from '@/components/SearchInput.vue';
import BankMap from '@/components/BankMap.vue';
import BankList from '@/components/BankList.vue';
import { ref } from 'vue';

const places = ref([]);
const mapInstance = ref(null);

const initMap = (map) => {
  mapInstance.value = map;
};

const handleSearch = (searchText) => {
  const geocoder = new kakao.maps.services.Geocoder();
  
  // 주소 검색
  geocoder.addressSearch(searchText, (result, status) => {
    if (status === kakao.maps.services.Status.OK && result.length > 0) {
      const coords = new kakao.maps.LatLng(result[0].y, result[0].x);
      if (mapInstance.value) {
        mapInstance.value.setCenter(coords);
      }
      searchNearbyBanks(coords);
    } else {
      // 주소 검색 실패 시 Places API로 키워드 검색
      searchWithPlacesAPI(searchText);
    }
  });
};

// Places API 키워드 검색
const searchWithPlacesAPI = (keyword) => {
  const ps = new kakao.maps.services.Places();
  ps.keywordSearch(keyword, (data, status) => {
    if (status === kakao.maps.services.Status.OK && data.length > 0) {
      const coords = new kakao.maps.LatLng(data[0].y, data[0].x);
      if (mapInstance.value) {
        mapInstance.value.setCenter(coords);
      }
      searchNearbyBanks(coords);
    } else {
      alert("입력한 주소를 찾을 수 없습니다.");
    }
  });
};

// 주변 은행 검색
const searchNearbyBanks = (coords) => {
  const ps = new kakao.maps.services.Places();
  ps.keywordSearch("은행", (data, status) => {
    if (status === kakao.maps.services.Status.OK) {
      places.value = data.slice(0, 5);
    } else {
      alert("근처 은행을 찾을 수 없습니다.");
    }
  }, {
    location: coords,
  });
};
</script>

<template>
  <div class="map-view-container">
    <!-- 검색 입력 컴포넌트 -->
    <div class="search-container">
      <SearchInput @search="handleSearch" />
    </div>
    
    <!-- 지도 및 은행 목록 -->
    <div class="map-and-list-container">
      <!-- 지도 영역 -->
      <div class="map-container">
        <BankMap :onInitMap="initMap" :places="places" />
      </div>
      
      <!-- 은행 목록 영역 -->
      <div class="bank-list-container">
        <BankList :places="places" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.map-view-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f8f9fa;
}

.search-container {
  width: 100%;
  max-width: 600px;
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}

.map-and-list-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
  max-width: 1200px;
}

.map-container {
  flex: 0 0 60%;
  height: 500px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.bank-list-container {
  flex: 0 0 35%;
  height: 500px;
  overflow-y: auto;
  background-color: white;
  border-radius: 10px;
  margin-left: 20px;
  padding: 15px;
}

.bank-list-container h2 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
}

.bank-list-container ul {
  list-style: none;
  padding: 0;
}

.bank-list-container li {
  font-size: 16px;
  margin-bottom: 10px;
  color: #555;
  line-height: 1.5;
}

.search-container input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.search-container button {
  padding: 10px 15px;
  margin-left: 10px;
  background-color: #E6AF69;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.search-container button:hover {
  background-color: #E6AF69;
}
</style>
