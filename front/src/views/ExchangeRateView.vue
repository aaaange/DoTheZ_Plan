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
          />
          <!-- 출발 통화 드롭박스 클릭 시 표시 -->
          <div class="currency" @click="toggleFromDropdown">
            {{ selectedFromCurrency }}
          </div>
          <!-- 드롭박스 표시/숨기기 -->
          <div v-if="isFromDropdownVisible">
            <select
              v-model="selectedFromCurrency"
              @change="updateSelectedFromCurrencyName(); convertCurrency(); toggleFromDropdown()"
              class="currency-dropdown"
            >
              <option value="KRW">대한민국 원 (KRW)</option>
              <option value="USD">미국 달러 (USD)</option>
              <option value="EUR">유로 (EUR)</option>
              <option value="JPY">일본 엔 (JPY)</option>
              <option value="GBP">영국 파운드 (GBP)</option>
              <option value="AUD">호주 달러 (AUD)</option>
              <option value="CAD">캐나다 달러 (CAD)</option>
              <option value="INR">인도 루피 (INR)</option>
              <option value="CNY">중국 위안 (CNY)</option>
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
              @change="updateSelectedToCurrencyName(); convertCurrency(); toggleToDropdown()"
              class="currency-dropdown"
            >
              <option value="KRW">대한민국 원 (KRW)</option>
              <option value="USD">미국 달러 (USD)</option>
              <option value="EUR">유로 (EUR)</option>
              <option value="JPY">일본 엔 (JPY)</option>
              <option value="GBP">영국 파운드 (GBP)</option>
              <option value="AUD">호주 달러 (AUD)</option>
              <option value="CAD">캐나다 달러 (CAD)</option>
              <option value="INR">인도 루피 (INR)</option>
              <option value="CNY">중국 위안 (CNY)</option>
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
import { Chart } from "chart.js";

export default {
  data() {
    return {
      amount: 1,
      exchangeRate: 0.00071, // 기본 환율 값
      historicalRates: [0.00071, 0.00072, 0.00073, 0.00071, 0.00069, 0.00070], // 예시 데이터
      labels: ["11/22", "11/21", "11/20", "11/19", "11/18", "11/17"], // 예시 날짜

      // 드롭다운 상태 및 선택된 통화
      isFromDropdownVisible: false,
      isToDropdownVisible: false,
      selectedFromCurrency: "KRW", // 기본값 (출발 통화)
      selectedToCurrency: "USD", // 기본값 (목적 통화)

      // 선택된 통화 이름
      selectedFromCurrencyName: "대한민국 원",
      selectedToCurrencyName: "미국 달러",
    };
  },
  computed: {
    convertedAmount() {
      return (this.amount * this.exchangeRate).toFixed(5); // 환율 변환 후 소수점 5자리로 표시
    },
  },
  created() {
    this.fetchExchangeRate(); // 초기 환율 데이터 가져오기
  },
  methods: {
    // 환율 데이터 API 호출
    async fetchExchangeRate() {
      try {
        const response = await fetch("http://localhost:8000/api/exchange-rate");
        const data = await response.json();
        this.exchangeRate = data.usdRate; // API에서 환율 값 가져오기
        this.updateChart(); // 환율 차트 업데이트
      } catch (error) {
        console.error("환율 데이터를 가져오는 중 오류 발생:", error);
      }
    },
    // 환율 변동 그래프 업데이트
    updateChart() {
      const ctx = document.getElementById("exchangeRateChart").getContext("2d");
      new Chart(ctx, {
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
      const currencyNames = {
        KRW: "대한민국 원",
        USD: "미국 달러",
        EUR: "유로",
        JPY: "일본 엔",
        GBP: "영국 파운드",
        AUD: "호주 달러",
        CAD: "캐나다 달러",
        INR: "인도 루피",
        CNY: "중국 위안",
      };
      this.selectedFromCurrencyName = currencyNames[this.selectedFromCurrency] || "대한민국 원";
    },
    // 도착 통화 이름 업데이트
    updateSelectedToCurrencyName() {
      const currencyNames = {
        KRW: "대한민국 원",
        USD: "미국 달러",
        EUR: "유로",
        JPY: "일본 엔",
        GBP: "영국 파운드",
        AUD: "호주 달러",
        CAD: "캐나다 달러",
        INR: "인도 루피",
        CNY: "중국 위안",
      };
      this.selectedToCurrencyName = currencyNames[this.selectedToCurrency] || "미국 달러";
    },
    // 환율 변환 처리
    convertCurrency() {
      console.log(`Converting ${this.selectedFromCurrency} to ${this.selectedToCurrency}`);
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
}
.subtitle {
  font-size: 16px;
  font-weight: 300;
  color: #666;
  margin-bottom: 30px;
}
.exchange-info {
  margin: 20px 0;
  font-size: 16px;
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
}
.currency {
  font-size: 16px;
  color: #1f77b4;
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
