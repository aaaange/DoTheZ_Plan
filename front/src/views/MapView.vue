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
    <div class="box">
      <div class="header">
        주변 은행 찾기
      </div>
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
  </div>
</template>

<style scoped>
.map-view-container {
  width: 100%;
  height: 100%;
  background: #F9EB87;
  justify-content: center;
  align-items: center;
  display: inline-flex;
}

.box {
  width: 1000px; /* 너비 설정 */
  margin: 0 auto;
  padding: 50px;
  background: #FBF9F4;
  border-radius: 30px;
  box-shadow: 6px 9px 4px rgba(0, 0, 0, 0.20);
  font-family: "Roboto", sans-serif;
  height: 70%; 
  display: flex;
  flex-direction: column;
  position: absolute; /* 이 부분을 추가해서 박스만 위치 조정 */
  top: 140px; /* 박스를 아래로 내리기 위한 값 */
}

.header {
  width: 100%;
  height: 65px;
  color: #585547;
  font-size: 50px;
  font-family: 'IBM Plex Sans KR', sans-serif; /* 폰트 패밀리 추가 */
  font-weight: 800;
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}

.search-container {
  display: flex;
  width: 100%;
  margin-bottom: 30px;
  justify-content: center;
}

.map-and-list-container {
  display: flex;
  justify-content: center;
  margin-top: 70px;
}

.map-container {
  flex: 0 0 50%;
  border-radius: 10px;
  height: 500px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.bank-list-container {
  flex: 0 0 35%;
  height: 700px;
  border-radius: 10px;
  margin-left: 30px;
  padding: 20px;
}

.bank-list-container h2 {
  font-size: 30px;
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
