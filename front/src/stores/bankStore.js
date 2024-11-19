import { defineStore } from 'pinia';
import axios from 'axios';

export const useBankStore = defineStore('bankStore', {

  state: () => ({
    banks: [],
  }),
  actions: {
    async fetchBanks(lat, lng) {
      const url = `https://dapi.kakao.com/v2/local/search/keyword.json?query=은행&x=${lng}&y=${lat}&radius=2000`;
      
      try {
        const response = await axios.get(url, {
          headers: {
            appkey: import.meta.env.VITE_YOUTUBE_API_KEY,
          },
        });
        this.banks = response.data.documents;
      } catch (error) {
        console.error("근처 은행 검색 중 오류 발생:", error);
      }
    },
  },
});
