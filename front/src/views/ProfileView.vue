<template>
  <div
    style="width: 100%; height: 100vh; padding-top: 119px; background: #F9EB87; justify-content: center; align-items: center; display: inline-flex"
  >
    <div class="Group6" style="width: 863px; height: 800px; position: relative">
      <div
        class="Rectangle1"
        style="width: 863px; height: 790px; top: 0px; position: absolute; background: #FBF9F4; box-shadow: 6px 9px 4px rgba(0, 0, 0, 0.20); border-radius: 30px"
      >
        <!-- 상단 영역 -->
        <div
          class="Group5"
          style="width: 642px; height: 114px; left: 110px; top: 38px; position: absolute"
        >
          <div
            style="width: 278px; height: 65px; top: 0px; position: absolute; color: #585547; font-size: 50px; font-family: IBM Plex Sans KR; font-weight: 700;"
          >
            내 프로필
          </div>
          <div
            style="width: 385px; left: 5px; top: 75px; position: absolute; color: #585547; font-size: 16px; font-family: IBM Plex Sans KR; font-weight: 300;"
          >
            회원 프로필 페이지
          </div>
          <div
            class="Line1"
            style="width: 642px; height: 0px; left: 0px; top: 114px; position: absolute; border-top: 1px solid #CDC7C0;"
          ></div>
        </div>

        <!-- 탈퇴하기 버튼 -->
        <button
          class="delete-button"
          style="position: absolute; top: 40px; right: 40px; background: #E6AF69; color: white; border: none; border-radius: 5px; padding: 10px 15px; cursor: pointer; font-size: 16px;"
          @click="deleteAccount"
        >
          탈퇴하기
        </button>

        <!-- 사용자 정보 -->
        <div
          class="user-info"
          style="position: absolute; top: 180px; left: 110px; right: 110px; display: flex; align-items: center; background-color: #EDEDED; padding: 20px; border-radius: 10px;"
        >
          <img
            src="/src/image/dothez.jpg"
            alt="프로필 사진"
            class="user-avatar"
            style="width: 120px; height: 120px; border-radius: 50%; margin-right: 20px; margin-left: 15px;"
            />
          <div class="user-details">
            <h2
              style="font-size: 30px; color: #585547; margin-top: 0px; margin-bottom: 50px; margin-left:20px"
            >
              {{ username ? username : "로그인을 해주세요" }}
            </h2>
            <p style="font-size: 18px; color: #585547;">
              <!-- 작성한 리뷰 {{ userProfile ? userProfile.reviewsCount : "2" }}개 -->
            </p>
          </div>
        </div>
        <!-- 가입한 상품 목록 -->
        <div
          class="product-section"
          style="position: absolute; top: 350px; left: 110px; right: 110px;"
        >
          <h3 style="font-size: 24px; color: #585547; margin-bottom: 20px;">
            가입한 상품
          </h3>
          <div class="product-list" style="max-height: 350px; overflow-y: auto;">
            <div v-if="my_products.length > 0">
              <div v-for="(product, index) in my_products" :key="index" class="product-item" style="background-color: #F7F4EA; border-radius: 10px; border: 1px solid #585547; padding: 15px; margin-bottom: 10px;">
                <p style="font-size: 18px; color: #585547; font-weight: 500;">{{ product.fin_prdt_nm }}</p>
              </div>
            </div>
            <div v-else class="no-products" style="display: flex; justify-content: center; align-items: center; height: 100px; font-size: 18px; color: #585547;">
              가입한 상품이 없습니다.
            </div>
          </div>
          <!-- 그래프 표시 영역 추가 -->
          <div class="graph-section" style="position: absolute; top: 720px; left: 110px; right: 110px;">
            <h3 style="font-size: 24px; color: #585547; margin-bottom: 20px;">가입 상품 금리 비교</h3>
            <div v-if="graph" class="graph-container">
              <img :src="'data:image/png;base64,' + graph" alt="Interest Rate Graph" style="width: 100%; max-width: 600px;">
            </div>
            <div v-else class="no-graph" style="display: flex; justify-content: center; align-items: center; height: 100px; font-size: 18px; color: #585547;">
              그래프를 불러오는 중입니다...
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { useCounterStore } from "@/stores/counter";
import axios from "axios";

export default {
  setup() {
    const store = useCounterStore();  // useCounterStore 호출
    const token = store.token;  // store에서 token 가져오기

    return {
      token,  // 반환하여 컴포넌트에서 사용
    };
  },
  data() {
    return {
      username: '', // 제품 상세 정보
      user_id: '',
      my_products: [ ],
      graph: null,
    };
  },

  mounted() {
    // 서버에서 데이터를 가져오는 메소드 호출
    this.fetchProfiles()
    this.fetchProducts()
    this.fetchGraphs()
  },

  methods: {
    async fetchProfiles() {
      try {
        const response = await axios.get(
          'http://127.0.0.1:8000/accounts/api/v1/user_info/',
        {
          headers: { Authorization: `Token ${this.token}` }  // this.token 사용
        })
        this.username = response.data.username; // 상품 상세 정보 저장
        this.user_id = response.data.pk
      } catch (error) {
        console.error("Error fetching product data:", error);
      }
    },
    async fetchProducts() {
      try {
        const response = await axios.get(
          'http://127.0.0.1:8000/accounts/api/v1/my/',
        {
          headers: { Authorization: `Token ${this.token}` }  // this.token 사용
        })
        console.log(response.data)
        this.my_products = response.data
      } catch (error) {
        console.error("Error fetching product data:", error);
      }
    },
    async fetchGraphs() {
      try {
        const response = await axios.get(
          'http://127.0.0.1:8000/accounts/api/v1/product_graph/',
        {
          headers: { Authorization: `Token ${this.token}` }  // this.token 사용
        })
        console.log(response.data)
        this.graph = response.data.graph
      } catch (error) {
        console.error("Error fetching graph data:", error);
      }
    },
    // 탈퇴하기 기능
    async deleteAccount() {
      if (!this.token) {
        alert("로그인 후 탈퇴할 수 있습니다.");
        return;
      }

      if (confirm("정말 탈퇴하시겠습니까?")) {
        try {
          // 탈퇴 API 호출
          const response = await axios.delete("http://127.0.0.1:8000/accounts/api/v1/delete/", {
            headers: {
              Authorization: `Token ${this.token}`,  // 토큰을 헤더에 포함
            },
          });

          if (response.status === 204) {
            alert("탈퇴가 완료되었습니다.");
            
            // 토큰 삭제
            this.token = null; 
            localStorage.removeItem("token");

            // 메인 페이지로 이동 후 새로고침
            this.$router.push({ name: "mainpage" }).then(() => {
              window.location.reload(); // 새로고침
            });
          }
        }  catch (error) {
          alert("탈퇴 처리에 실패했습니다. 다시 시도해주세요.");
          console.error(error);
        }
      }
    },
  },
};
</script>

<style scoped>
.product-list::-webkit-scrollbar {
  width: 5px;
}
.product-list::-webkit-scrollbar-thumb {
  background-color: #888;
  border-radius: 10px;
}
.product-list::-webkit-scrollbar-track {
  background-color: #f1f1f1;
  border-radius: 10px;
}
</style>
