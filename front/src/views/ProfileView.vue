<template>
  <div
    style="width: 100%; height: 100%; padding-top: 119px; background: #F9EB87; justify-content: center; align-items: center; display: inline-flex"
  >
    <div class="Group6" style="width: 863px; height: 800px; position: relative">
      <div
        class="Rectangle1"
        style="width: 1000px; height: 800px; top: 0px; position: absolute; justify-content: center; background: #FBF9F4; box-shadow: 6px 9px 4px rgba(0, 0, 0, 0.20); border-radius: 30px"
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
          class="delete-button product-item"
          style="position: absolute; top: 40px; right: 40px; background: #E6AF69; color: white; border: none; border-radius: 5px; padding: 10px 15px; cursor: pointer; font-size: 16px;"
          @click="deleteAccount"
        >
          탈퇴하기
        </button>

        <!-- 사용자 정보 -->
        <div
          class="user-info"
          style="position: absolute; top: 190px; left: 110px; right: 110px; display: flex; align-items: center; background-color: #EDEDED; padding: 20px; border-radius: 10px;"
        >
          <img
            src="@/image/dothez.jpg"
            alt="프로필 사진"
            class="user-avatar"
            style="width: 120px; height: 120px; border-radius: 50%; margin-right: 20px; margin-left: 15px;"
            />
          <div class="user-details">
            <h2
              style="font-size: 30px; color: #585547; margin-top: 0px; margin-bottom: 10px; margin-left:20px"
            >
              {{ username ? username : "로그인을 해주세요" }}
            </h2>
            <p style="font-size: 18px; color: #585547; margin-left:20px">
              작성한 리뷰 {{ reviewCount ? reviewCount : "0" }}개
            </p>
          </div>
        </div>
        <div style="margin-top: 370px; width: 90%;">
          <div style="max-height: 400px; overflow-y: auto; position: relative; margin-left: 100px;">
            <!-- 가입한 상품 목록 -->
            <div class="product-section" style="margin-bottom: 30px;">
              <h3 style="font-size: 24px; color: #585547; margin-bottom: 20px;">
                가입한 상품
              </h3>
              <div class="product-list" style="max-height: 350px;">
                <div v-if="my_products.length > 0">
                  <div v-for="(product, index) in my_products" :key="index" class="product-item" 
                      style="background-color: #F7F4EA; border-radius: 10px; border: 1px solid #585547; padding: 15px; margin-bottom: 10px;">
                    <router-link :to="{ name: 'productdetail', params: { productId: product.fin_prdt_cd } }" 
                      style="display: block; text-decoration: none;">
                      <p style="font-size: 18px; color: #585547; font-weight: 500;">{{ product.fin_prdt_nm }}</p>
                    </router-link>
                  </div>
                </div>
                <div v-else class="no-products" style="display: flex; justify-content: center; align-items: center; height: 100px; font-size: 18px; color: #585547;">
                  가입한 상품이 없습니다.
                </div>
              </div>
            </div>
            <!-- 그래프 표시 영역 추가 -->
            <div class="graph-section" style="margin-top: 100px;">
              <h3 style="font-size: 24px; color: #585547; margin-bottom: 20px;">가입 상품 금리 비교</h3>
              <div v-if="chartData" class="graph-container">
                <!-- 차트 영역 -->
                <canvas id="interestRateChart"></canvas>
              </div>
              <div v-else class="no-graph" style="display: flex; justify-content: center; align-items: center; height: 100px; font-size: 18px; color: #585547;">
                그래프를 불러오는 중입니다...
              </div>
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
// import { Line } from 'chart.js';
import { Chart } from 'chart.js/auto';

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
      chartData: null,  // 차트 데이터를 저장할 변수
      chartInstance: null,  // 차트 인스턴스를 저장할 변수
      reviewCount: 0,
    };
  },
  props: {
    userId: {
      type: Number,
      required: true,
    },
  },
  mounted() {
    // 서버에서 데이터를 가져오는 메소드 호출
    this.fetchProfiles().then(() => {
      this.fetchUserReviewCount();
    })
    this.fetchProducts().then(() => {
      this.renderChart();
    })
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
            headers: { Authorization: `Token ${this.token}` }, // this.token 사용
          }
        );
        this.my_products = response.data; // 상품 목록
        const res = await axios.get(
          'http://127.0.0.1:8000/product/options/',
          {
            headers: { Authorization: `Token ${this.token}` }, // this.token 사용
          }
        );
        
        const labels = [];  // 상품 이름을 저장할 배열

        const interestRates = [];  // 기본 금리를 저장할 배열
        const bestRates = [];  // 최고 우대 금리를 저장할 배열

        // 상품 목록에서 금리 정보를 추출하여 배열에 저장
        this.my_products.forEach(product => {
          if (product) {
            labels.push(product.fin_prdt_nm);  // 상품 이름
          }
          const matchingProduct = res.data.find(option => option.fin_prdt_cd === product.fin_prdt_cd);
          if (matchingProduct) {
            interestRates.push(matchingProduct.intr_rate);
            bestRates.push(matchingProduct.intr_rate2);
          }
        });
        // 차트 데이터 설정
        this.chartData = {
          labels: labels,  // 상품 이름을 X축에 표시
          datasets: [
            {
              label: '기본 금리',  // 기본 금리 데이터
              data: interestRates,
              backgroundColor: 'rgba(75, 192, 192, 0.5)',  // 기본 금리 색상 (반투명한 막대 색)
              borderColor: 'rgba(75, 192, 192, 1)',  // 기본 금리 테두리 색상
              borderWidth: 1,  // 테두리 두께
              fill: true,  // 막대 내부 채우기
            },
            {
              label: '최고 우대 금리',  // 최고 우대 금리 데이터
              data: bestRates,
              backgroundColor: 'rgba(153, 102, 255, 0.5)',  // 우대 금리 색상 (반투명한 막대 색)
              borderColor: 'rgba(153, 102, 255, 1)',  // 우대 금리 테두리 색상
              borderWidth: 1,  // 테두리 두께
              fill: true,  // 막대 내부 채우기
            }
          ]
        };
      } catch (error) {
        console.error('Error fetching product data:', error);
      }
    },
    renderChart() {
      // 차트가 이미 있으면 삭제하고 새로 렌더링
      if (this.chartInstance) {
        this.chartInstance.destroy();
      }

      // 차트 인스턴스 생성
      const ctx = document.getElementById('interestRateChart').getContext('2d');
      const interestRateChart = new Chart(ctx, {
        type: 'bar',  // 차트 유형을 막대 그래프('bar')로 설정
        data: this.chartData,
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,  // y축이 0부터 시작하도록 설정
              ticks: {
                callback: function(value) {
                  return value + '%';  // y축 값 뒤에 '%' 추가
                }
              }
            }
          },
          plugins: {
            legend: {
              position: 'top',  // 범례 위치
            },
          },
        },
      });
    },
    async fetchUserReviewCount() {
      try {
        if (!this.user_id) {
          console.log("사용자 ID를 가져오지 못했습니다.");
          return;
        }
        const response = await axios.get(
          `http://127.0.0.1:8000/accounts/api/v1/profile/${this.user_id}/reviews/count/`, 
          {
            headers: {
              Authorization: `Token ${this.token}`
            }
          })
          this.reviewCount = response.data.review_count
      } catch (error) {
        console.log("댓글 수를 불러오는 중 오류 발생: ", error)
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
}

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
.product-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}
</style>
