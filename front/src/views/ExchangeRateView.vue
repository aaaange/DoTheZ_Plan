<template>
  <div class="calculator-container">
    <div class="calculator">
      <h1 class="title">환율 계산기</h1>
      <p class="subtitle">간편하게 환율 정보를 알아볼 수 있어요!</p>
      <div class="exchange-info">
        <p>{{amount}} {{ selectedFromCurrencyName }} =</p> 
        <p class="exchange-rate">{{ (amount * exchangeRate).toFixed(5) }} {{ selectedToCurrencyName }}</p>
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
        <p style="font-size: 20px;"> > </p>
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
import axios from "axios";

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
      selectedFromCurrency: "USD", // 기본값 (출발 통화)
      selectedToCurrency: "KRW", // 기본값 (목적 통화)

      // 선택된 통화 이름
      selectedFromCurrencyName: "미국 달러",
      selectedToCurrencyName: "대한민국 원",

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
      const today = new Date();
      const dateArray = [];

      // 오늘을 포함한 100일간의 날짜 계산
      for (let i = 0; i < 100; i++) {
        const date = new Date(today);
        date.setDate(today.getDate() - i); // 오늘부터 5일 전까지
        dateArray.push(date.toISOString().split("T")[0]); // 'yyyy-mm-dd' 형식으로 저장
      }
      try {
      // 각 날짜에 대해 API 요청을 보냄
      const requests = dateArray.map((date) =>
        axios.get("http://127.0.0.1:8000/exchange/api/v1/exchange/", {
          params: {
            searchDate: date,
            from: this.selectedFromCurrency,
            to: this.selectedToCurrency,
          },
        })
      );

        // 여러 요청을 동시에 보냄 (병렬 요청)
        const responses = await Promise.allSettled(requests);

        // 데이터를 처리
        const historicalRates = [];
        const labels = [];

        // responses를 순회하여 환율 데이터 추출
        responses.forEach((response, index) => {
      if (response.status === "fulfilled") {
        const data = response.value.data;
        const fromCurrency = data.find((item) => item.cur_unit === this.selectedFromCurrency);
        const toCurrency = data.find((item) => item.cur_unit === this.selectedToCurrency);

        if (fromCurrency && toCurrency) {
          const fromRate = parseFloat(fromCurrency.deal_bas_r.replace(",", "").trim());
          const toRate = parseFloat(toCurrency.deal_bas_r.replace(",", "").trim());
          
          if (!isNaN(fromRate) && !isNaN(toRate)) {
            historicalRates.push(fromRate / toRate); // 환율 값을 배열에 추가
            labels.push(dateArray[index]); // 날짜 추가
          }
        }
      } else {
        console.warn(`Failed to fetch data for ${dateArray[index]}. Skipping this date.`);
      }
    });

        // 날짜 순서를 반대로 뒤집기
        this.historicalRates = historicalRates.reverse();
        this.labels = labels.reverse();

        // 선택된 통화 이름 갱신
        this.updateSelectedToCurrencyName(); // 이름 갱신

        // exchangeRate 값을 갱신 (환율 계산)
        const fromCurrency = this.historicalRates[this.historicalRates.length - 1]; // 마지막 날짜 기준
        this.exchangeRate = fromCurrency || 0; // 환율 값 설정
        this.updateChart(); // 차트 업데이트

        } catch (error) {
        console.error("환율 데이터를 가져오는 중 오류 발생:", error);
        }
        },
    // 환율 변동 그래프 업데이트
    updateChart() {
      if (!this.historicalRates.length || !this.labels.length) {
        console.warn("차트 데이터를 생성할 수 없습니다: 데이터가 비어있습니다."); 
        return;
      }

      const ctx = document.getElementById("exchangeRateChart").getContext("2d");
      if (this.chartInstance) {
        this.chartInstance.destroy();
      }
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
    toggleFromDropdown() {
      this.isFromDropdownVisible = !this.isFromDropdownVisible;
      this.isToDropdownVisible = false;
    },
    toggleToDropdown() {
      this.isToDropdownVisible = !this.isToDropdownVisible;
      this.isFromDropdownVisible = false;
    },
    updateSelectedFromCurrencyName() {
      const selected = this.currencies.find(
        (currency) => currency.code === this.selectedFromCurrency
      );
      this.selectedFromCurrencyName = selected ? selected.name : "대한민국 원";
    },
    updateSelectedToCurrencyName() {
      const selected = this.currencies.find(
        (currency) => currency.code === this.selectedToCurrency
      );
      this.selectedToCurrencyName = selected ? selected.name : "미국 달러";
    },
    convertCurrency() {
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
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f9eb87;
  padding-top: 50px; /* 상단 여백 추가 */
  position: relative;
}

.calculator {
  width: 1000px; /* 너비 설정 */
  margin: 0 auto;
  padding: 50px;
  background: #FBF9F4;
  border-radius: 30px;
  box-shadow: 6px 9px 4px rgba(0, 0, 0, 0.2);
  text-align: center;  
  position: absolute;
  display: flex;
  flex-direction: column;
  top: 132px;
}

.title {
  font-size: 50px;
  font-weight: 700;
  margin-bottom: -5px;
  color: #585547;
}

.subtitle {
  font-size: 20px;
  font-weight: 400;
  color: #585547;
  margin-bottom: 15px;
}

.exchange-info {
  font-size: 18px;
  color: #585547;
}

.exchange-rate {
  font-size: 32px;
  font-weight: 600;
  margin-top: -5px;
}

.input-group {
  display: flex;
  justify-content: space-around;
  margin-top: 10px;
}

.input-box {
  display: flex;
  align-items: center;
  background: #fbf9f4;
  border: 1px solid #d9d9d9;
  border-radius: 15px;
  padding: 10px 15px;
  width: 270px;
}
.input {
  font-size: 20px;
  padding: 10px;
  width: 180px;
  border: none;
  background: transparent;
  color: #585547;
}
.currency {
  font-size: 20px;
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
  display: flex;
  justify-content: center;
  align-items: center;
  width: 80%;
  height: 80%;
  margin-left: 90px;
}
</style>
