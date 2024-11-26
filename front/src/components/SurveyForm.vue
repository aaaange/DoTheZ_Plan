<template>
  <div class="background">
    <div class="container">
      <h1>나와 꼭 맞는 상품을 알아봐요🔍</h1>
      <form @submit.prevent="submitForm" class="survey-form">

        <!-- 기타 설문 항목 -->
        <div v-for="(question, index) in otherQuestions" :key="index" class="question-group">
          <label :for="question.field" class="question-label">{{ question.label }}</label>
          <!-- ENUM 타입 -->
          <div v-if="question.type === 'enum'" class="options-group">
            <div v-for="(option, idx) in question.options" :key="idx">
              <input
                type="radio"
                :id="`${question.field}-${idx}`"
                :value="option"
                v-model="formData[question.field]"
              />
              <label :for="`${question.field}-${idx}`">{{ option }}</label>
            </div>
          </div>
          <!-- BOOLEAN 타입 -->
          <div v-else-if="question.type === 'boolean'" class="input-group">
            <select v-model="formData[question.field]">
              <option :value="true">예금</option>
              <option :value="false">적금</option>
            </select>
          </div>
          <!-- FLOAT 및 INT 타입 -->
          <div v-else-if="question.type === 'float' || question.type === 'int'" class="input-group">
            <input
              type="number"
              :id="question.field"
              v-model.number="formData[question.field]"
              :placeholder="question.label"
            />
            <span v-if="question.field === 'minimum_deposit' || question.field === 'fixed_income' || question.field === 'current_assets'">만 원</span>
            <span v-else-if="question.field === 'investment_period'">개월</span>
            <span v-else-if="question.field === 'expected_return'">%</span>
            <span v-else-if="question.field === 'age'">세</span>
          </div>
          <!-- TEXT 입력 -->
          <div v-else-if="question.type === 'text'" class="input-group">
            <input
              type="text"
              :id="question.field"
              v-model="formData[question.field]"
              :placeholder="question.label"
            />
          </div>
        </div>
        <!-- 소비 습관 항목: 가로 정렬 -->
        <div class="question-group">
          <div class="spending-habits-container">
            <div
              v-for="(question, index) in spendingHabitQuestions"
              :key="index"
              class="spending-habit-column"
            >
              <label :for="question.field" class="question-label">{{ question.label }}</label>
              <div class="vertical-options">
                <div v-for="(option, idx) in question.options" :key="idx">
                  <input
                    type="radio"
                    :id="`${question.field}-${idx}`"
                    :value="option"
                    v-model="formData[question.field]"
                  />
                  <label :for="`${question.field}-${idx}`">{{ option }}</label>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 제출 버튼 -->
        <button type="submit" class="submit-button action-button">제출하기</button>
      </form>

      <!-- 경고 메시지 -->
      <div v-if="errorMessage" class="error-message">
        <p>{{ errorMessage }}</p>
      </div>

      <!-- 제출된 데이터 -->
      <div v-if="submitted" class="result-section">
        <h2>제출된 데이터:</h2>
        <pre>{{ formData }}</pre>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useCounterStore } from '@/stores/counter';

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
      user_id: '',
      surveyQuestions: [
        { field: "deposit_or_saving", label: "예금/적금", type: "boolean" },
        { field: "age", label: "만 나이", type: "int" },
        { field: "minimum_deposit", label: "최소 예치금", type: "float" },
        { field: "investment_period", label: "투자 기간", type: "float" },
        { field: "expected_return", label: "요구 수익률", type: "float" },
        { field: "fixed_income", label: "고정 수입", type: "float" },
        { field: "main_bank", label: "주 거래 은행", type: "text" },
        { field: "current_assets", label: "현재 자산", type: "float" },
        {
          field: "interest_rate_type",
          label: "저축 금리 유형",
          type: "enum",
          options: ["단리", "복리"],
        },
        {
          field: "investment_goal",
          label: "투자 목적",
          type: "enum",
          options: ["결혼자금", "주택마련", "노후준비"],
        },
        {
          field: "spending_habit_1",
          label: "소비 습관 1",
          type: "enum",
          options: ["쇼핑", "여가", "식비", "교통", "주거", "저축", "기타"],
        },
        {
          field: "spending_habit_2",
          label: "소비 습관 2",
          type: "enum",
          options: ["쇼핑", "여가", "식비", "교통", "주거", "저축", "기타"],
        },
        {
          field: "spending_habit_3",
          label: "소비 습관 3",
          type: "enum",
          options: ["쇼핑", "여가", "식비", "교통", "주거", "저축", "기타"],
        },
        {
          field: "household_type",
          label: "가구 유형",
          type: "enum",
          options: ["1인가구", "2인가구", "4인 이상"],
        },
        {
          field: "risk_tolerance",
          label: "위험 성향",
          type: "enum",
          options: ["낮음", "보통", "높음"],
        },
      ],
      formData: { },
      submitted: false,
      errorMessage: "",
      user_survey_id: '',
    };
  },
  computed: {
    spendingHabitQuestions() {
      return this.surveyQuestions.filter((q) =>
        ["spending_habit_1", "spending_habit_2", "spending_habit_3"].includes(q.field)
      );
    },
    otherQuestions() {
      return this.surveyQuestions.filter(
        (q) =>
          !["spending_habit_1", "spending_habit_2", "spending_habit_3"].includes(q.field)
      );
    },
  },
  mounted() {
    this.surveyQuestions.forEach((question) => {
      this.formData[question.field] = null;
    });
    this.formData.user = null;
    this.fetchProfiles()
  },
  methods: {
    async fetchProfiles() {
      try {
        const response = await axios.get(
          'http://127.0.0.1:8000/accounts/api/v1/user_info/',
        {
          headers: { Authorization: `Token ${this.token}` }  // this.token 사용
        })
        this.user_id = response.data.pk
      } catch (error) {
        console.error("Error fetching product data:", error);
      }
    },
    async submitForm() {
      const incompleteField = this.surveyQuestions.find(
        (question) =>
          this.formData[question.field] === null || this.formData[question.field] === ""
      );

      if (incompleteField) {
        this.errorMessage = `${incompleteField.label} 항목을 입력해 주세요.`;
        this.submitted = false;
        return;
      }

      if (!this.user_id) {
        this.errorMessage = "사용자 정보를 불러오는 데 실패했습니다.";
        return;
      }

      this.errorMessage = "";
      this.formData.user = this.user_id;

      try {
        const response = await axios.post(`http://127.0.0.1:8000/surveys/api/v1/user-survey/`, this.formData);
        console.log('서버 응답:', response.data);
        this.submitted = true;
        this.user_survey_id = response.data.id
        console.log(this.user_survey_id)

        // 추천 결과로 이동 (현재 페이지에서 Recommend가 표시됨)
        this.$router.push({ name: 'recommend', params: { userSurveyId: this.user_survey_id } }); // 필요하면 router 처리
        
      } catch (error) {
        if (error.response) {
          this.errorMessage = `서버 오류: ${error.response.data.message || '알 수 없는 오류'}`;
        } else {
          this.errorMessage = '서버에 오류가 발생했습니다. 다시 시도해주세요.';
        }
        console.error('서버 요청 오류:', error);
      }
    }
  },
};
</script>

<style>
.background {
  width: 100%;
  height: 100%;
  background-color: #F9EB87;
  justify-content: center;
  align-items: center; 
  display: inline-flex;
}

.container {
  width: 1000px;
  margin: 0 auto; /* auto로 중앙 정렬 */
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

h1 {
  color: #585547;
  text-align: center;
  margin-bottom: 70px;
  font-size: 50px;
  justify-content: left;
  margin-top: 20px;
}

.survey-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
  overflow-y: auto;
  flex: 1;
  padding-right: 10px;
}

.question-group {
  padding: 15px;
  padding-left: 22px;
  background: #ffffff;
  border: 1px solid #dcdcdc;
  border-radius: 10px;
}

.question-label {
  display: block; 
  font-weight: bold;
  margin-bottom: 8px;
}

.input-group {
  display: flex;
  align-items: center;
}

.input-group input,
.input-group select {
  flex: 1;
  padding: 10px;
  border: 1px solid #dcdcdc;
  border-radius: 4px;
  width: 50%;
  max-width: 100px;
}

.input-group textarea {
  flex: 1;
  padding: 10px;
  border: 1px solid #dcdcdc;
  border-radius: 4px;

}

.input-group span {
  margin-left: 10px;
  font-weight: bold;
}

.options-group label {
  margin-left: 8px;
}

.spending-habits-container {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  flex-direction: row;
}

.spending-habit-column {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.vertical-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.submit-button {
  background-color: #E6AF69;
  color: white;
  border: none;
  padding: 12px 20px;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #E6AF69;
}

.error-message {
  color: #e74c3c;
  font-weight: bold;
  text-align: center;
  margin-top: 10px;
}

.result-section {
  margin-top: 20px;
  background: #ecf0f1;
  padding: 15px;
  border-radius: 8px;
}

.action-button:hover {
  background: #E6AF69;
  transform: scale(1.05);
}
</style>