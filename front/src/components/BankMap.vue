<script setup>
import { onMounted, ref, watch } from 'vue';

const props = defineProps({
  onInitMap: Function, // 지도 객체 초기화 핸들러
  places: Array, // 검색 결과
});

let map;
let markers = []; // 지도에 표시된 마커 리스트

const initMap = () => {
  const mapKey = import.meta.env.VITE_KAKAO_MAP_KEY;

  const script = document.createElement('script');
  script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${mapKey}&libraries=services&autoload=false`;
  script.onload = () => {
    kakao.maps.load(() => {
      const container = document.getElementById('map');
      const options = {
        center: new kakao.maps.LatLng(37.5012746, 127.0395857), // 초기 지도 중심 (서울 시청)
        level: 3,
      };
      map = new kakao.maps.Map(container, options);

      // 부모 컴포넌트에 지도 객체 전달
      if (props.onInitMap) {
        props.onInitMap(map);
      }
    });
  };
  document.head.appendChild(script);
};

// 마커 표시
const displayMarkers = () => {
  // 기존 마커 삭제
  markers.forEach(marker => marker.setMap(null));
  markers = [];

  props.places.forEach(place => {
    const marker = new kakao.maps.Marker({
      map,
      position: new kakao.maps.LatLng(place.y, place.x),
      title: place.place_name,
      image: new kakao.maps.MarkerImage(
        "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png", // 마커 이미지
        new kakao.maps.Size(24, 35)
      ),
    });
    markers.push(marker);
  });
};

watch(props.places, displayMarkers); // 검색 결과 변경 시 마커 업데이트

onMounted(initMap);
</script>

<template>
  <div id="map"></div>
</template>

<style scoped>
#map {
  width: 100%;
  height: 100%;
  border-radius: 10px;
}
</style>
