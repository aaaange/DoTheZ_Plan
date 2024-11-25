<template>
  <div class="calculator-container">
    <div class="calculator">
      <h1 class="title">환율 계산기</h1>
      <p class="subtitle">간편하게 환율 정보를 알아볼 수 있어요!</p>
      <div class="exchange-info">
        <p>1 {{ selectedFromCurrencyName }} =</p> 
        <p class="exchange-rate">{{ exchangeRate }} {{ selectedToCurrencyName }}</p>
      </div>
      <div class="input-group">
        <div class="input-box">
          <input
            type="number"
            v-model="amount"
            placeholder="0"
            class="input"
            @input="convertCurrency"
          />
          <!-- 출발 통화 드롭박스 클릭 시 표시 -->
          <div class="currency" @click="toggleFromDropdown">
            {{ selectedFromCurrency }}
          </div>
          <!-- 드롭박스 표시/숨기기 -->
          <div v-if="isFromDropdownVisible">
            <select
              v-model="selectedFromCurrency"
              @change="updateSelectedFromCurrencyName(); fetchExchangeRate(); toggleFromDropdown()"
              class="currency-dropdown"
            >
              <option v-for="currency in currencies" :key="currency.code" :value="currency.code">
                {{ currency.name }} ({{ currency.code }})
              </option>
            </select>
          </div>
        </div>
        <p> > </p>
        <div class="input-box">
          <input
            type="text"
            :value="convertedAmount"
            readonly
            class="input"
          />
          <!-- 도착 통화 드롭박스 클릭 시 표시 -->
          <div class="currency" @click="toggleToDropdown">
            {{ selectedToCurrency }}
          </div>
          <!-- 드롭박스 표시/숨기기 -->
          <div v-if="isToDropdownVisible">
            <select
              v-model="selectedToCurrency"
              @change="updateSelectedToCurrencyName(); fetchExchangeRate(); toggleToDropdown()"
              class="currency-dropdown"
            >
              <option v-for="currency in currencies" :key="currency.code" :value="currency.code">
                {{ currency.name }} ({{ currency.code }})
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- 환율 변동 그래프 표시 -->
      <div class="chart-container">
        <canvas id="exchangeRateChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";
import axios from 'axios'


export default {
  data() {
    return {
      amount: 1,
      exchangeRate: 0.0,
      historicalRates: [], // 환율 그래프 데이터
      labels: [], // 환율 그래프 날짜

      // 드롭다운 상태 및 선택된 통화
      isFromDropdownVisible: false,
      isToDropdownVisible: false,
      selectedFromCurrency: "KRW", // 기본값 (출발 통화)
      selectedToCurrency: "USD", // 기본값 (목적 통화)

      // 선택된 통화 이름
      selectedFromCurrencyName: "대한민국 원",
      selectedToCurrencyName: "미국 달러",

      // 사용 가능한 통화 목록
      currencies: [
        { code: "AED", name: "아랍에미리트 디르함" },
        { code: "AUD", name: "호주 달러" },
        { code: "BHD", name: "바레인 디나르" },
        { code: "BND", name: "브루나이 달러" },
        { code: "CAD", name: "캐나다 달러" },
        { code: "CHF", name: "스위스 프랑" },
        { code: "CNH", name: "중국 위안" },
        { code: "DKK", name: "덴마크 크로네" },
        { code: "EUR", name: "유럽연합 유로" },
        { code: "GBP", name: "영국 파운드" },
        { code: "HKD", name: "홍콩 달러" },
        { code: "IDR(100)", name: "인도네시아 루피아" },
        { code: "JPY(100)", name: "일본 엔" },
        { code: "KRW", name: "한국 원" },
        { code: "KWD", name: "쿠웨이트 디나르" },
        { code: "MYR", name: "말레이시아 링깃" },
        { code: "NOK", name: "노르웨이 크로네" },
        { code: "NZD", name: "뉴질랜드 달러" },
        { code: "SAR", name: "사우디 리얄" },
        { code: "SEK", name: "스웨덴 크로나" },
        { code: "SGD", name: "싱가포르 달러" },
        { code: "THB", name: "태국 달러" },
        { code: "USD", name: "미국 달러" },
      ],
      // 차트 인스턴스를 저장할 변수
      chartInstance: null,
    };
  },
  computed: {
    convertedAmount() {
      
      return (this.amount * this.exchangeRate).toFixed(5); // 환율 변환 후 소수점 5자리로 표시
    },
  },
  created() {
    this.fetchExchangeRate(); // 초기 환율 데이터 가져오기
    Chart.register(...registerables);
  },
  methods: {
    // 환율 데이터 API 호출
    async fetchExchangeRate() {
      try {
        
        const response = await axios.get("http://127.0.0.1:8000/exchange/api/v1/exchange/", {
          params: {
            searchDate: new Date().toISOString().split("T")[0], // 오늘 날짜
            from: this.selectedFromCurrency,
            to: this.selectedToCurrency,
          },
        });
        // 응답 데이터 로그 추가
        console.log("API 응답 데이터:", response.data); // 로그로 확인

        const data = response.data;

         // 선택된 통화 로그 추가
        console.log("선택된 출발 통화:", this.selectedFromCurrency);
        console.log("선택된 도착 통화:", this.selectedToCurrency);

        // 수정: selectedFromCurrency와 selectedToCurrency에 해당하는 데이터를 찾아 deal_bas_r 값을 설정
        const fromCurrency = data.find(item => item.cur_unit === this.selectedFromCurrency);
        const toCurrency = data.find(item => item.cur_unit === this.selectedToCurrency);

        // fromCurrency와 toCurrency가 존재하는지 확인
        if (fromCurrency && toCurrency) {
          // deal_bas_r 값을 가져와 숫자로 변환 (공백 제거)
          const fromRate = parseFloat(fromCurrency.deal_bas_r.replace(",", "").trim());
          const toRate = parseFloat(toCurrency.deal_bas_r.replace(",", "").trim());

          // NaN인 경우 기본값 설정
          if (isNaN(fromRate) || isNaN(toRate)) {
            console.error("유효하지 않은 환율 값:", fromCurrency.deal_bas_r, toCurrency.deal_bas_r);
            this.exchangeRate = 0; // 기본값으로 0 설정
          } else {
            // 환율 계산: (fromRate / toRate)으로 계산
            // this.exchangeRate = toRate/ fromRate;

            // 교차 환율 계산 (KRW -> selectedFromCurrency -> selectedToCurrency)
            this.exchangeRate = (fromRate/1) * toRate;
          }
        } else {
          console.error("선택한 통화 정보가 없습니다.");
          this.exchangeRate = 0; // 선택한 통화가 없으면 기본값 0 설정
        }
        this.historicalRates = data.map(item => item.deal_bas_r); // 과거 환율 데이터
        this.labels = data.map(item => item.search_date); // 그래프에 사용할 날짜 데이터
        this.updateChart(); // 환율 차트 업데이트
      } catch (error) {
        console.error("환율 데이터를 가져오는 중 오류 발생:", error);
      }
    },
    // 환율 변동 그래프 업데이트
    updateChart() {
      const ctx = document.getElementById("exchangeRateChart").getContext("2d");
      // 기존 차트가 있으면 삭제
      if (this.chartInstance) {
        this.chartInstance.destroy(); // 수정된 부분: 기존 차트 삭제
      }

      // 새로운 차트 생성
      this.chartInstance = new Chart(ctx, {
        type: "line",
        data: {
          labels: this.labels,
          datasets: [
            {
              label: "환율 변동",
              data: this.historicalRates,
              borderColor: "rgba(75, 192, 192, 1)",
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: false,
            },
          },
        },
      });
    },
    // 출발 통화와 도착 통화 변경 시 환율 가져오기
    async updateExchangeRate() {
      await this.fetchExchangeRate();
    },
    // 출발 통화 드롭다운 열기/닫기
    toggleFromDropdown() {
      this.isFromDropdownVisible = !this.isFromDropdownVisible;
      this.isToDropdownVisible = false; // 다른 드롭다운은 닫기
    },
    // 도착 통화 드롭다운 열기/닫기
    toggleToDropdown() {
      this.isToDropdownVisible = !this.isToDropdownVisible;
      this.isFromDropdownVisible = false; // 다른 드롭다운은 닫기
    },
    // 출발 통화 이름 업데이트
    updateSelectedFromCurrencyName() {
      const selected = this.currencies.find(
        (currency) => currency.code === this.selectedFromCurrency
      );
      this.selectedFromCurrencyName = selected ? selected.name : "대한민국 원";
    },
    // 도착 통화 이름 업데이트
    updateSelectedToCurrencyName() {
      const selected = this.currencies.find(
        (currency) => currency.code === this.selectedToCurrency
      );
      this.selectedToCurrencyName = selected ? selected.name : "미국 달러";
    },
    // 환율 변환 처리
    convertCurrency() {
      // 변환된 금액 계산
      console.log(
        `Converting ${this.selectedFromCurrency} to ${this.selectedToCurrency}`
      );
    },
  },
};
</script>

<style scoped>
.calculator-container {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f9eb87;
  padding-top: 50px; /* 상단 여백 추가 */
}
.calculator {
  width: 660px;
  padding: 20px;
  background: #fbf9f4;
  box-shadow: 6px 9px 4px rgba(0, 0, 0, 0.2);
  border-radius: 20px;
  text-align: center;
}
.title {
  font-size: 40px;
  font-weight: 700;
  margin-bottom: 10px;
  color: #585547;
}
.subtitle {
  font-size: 16px;
  font-weight: 300;
  color: #585547;
  margin-bottom: 30px;
}
.exchange-info {
  margin: 20px 0;
  font-size: 16px;
  color: #585547;
}
.exchange-rate {
  font-size: 32px;
  font-weight: 600;
}
.input-group {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
}
.input-box {
  display: flex;
  align-items: center;
  background: #fbf9f4;
  border: 1px solid #d9d9d9;
  border-radius: 15px;
  padding: 10px 15px;
  width: 250px;
}
.input {
  font-size: 16px;
  padding: 10px;
  width: 150px;
  border: none;
  background: transparent;
  color: #585547;
}
.currency {
  font-size: 16px;
  color: #e6af69;
  cursor: pointer;
  margin-left: 10px;
}
.currency-dropdown {
  width: 100%;
  padding: 5px;
  background: white;
  border-radius: 5px;
}
.chart-container {
  margin-top: 30px;
  height: 300px;
  width: 100%;
}
</style>
