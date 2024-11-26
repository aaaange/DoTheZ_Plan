from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UserSurvey
from .serializers import UserSurveySerializer
from django.shortcuts import render
from django.http import JsonResponse
from product.models import Product, ProductOption


@api_view(['GET', 'POST'])
def user_survey_view(request):
    # GET 요청: 저장된 모든 UserSurvey 데이터 조회
    if request.method == 'GET':
        surveys = UserSurvey.objects.all()  # 모든 설문 데이터 가져오기
        serializer = UserSurveySerializer(surveys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST 요청: 새로운 UserSurvey 데이터 생성
    elif request.method == 'POST':
        serializer = UserSurveySerializer(data=request.data)
        if serializer.is_valid():
            user_survey_instance  = serializer.save()  # 데이터 저장
            return Response(UserSurveySerializer(user_survey_instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def calculate_expected_return(deposit_or_saving, minimum_deposit, investment_period, interest_rate, interest_rate_type):
    # 단리 또는 복리 계산
    if interest_rate_type == "단리":
        return minimum_deposit * (1 + interest_rate / 100) * (investment_period) - (minimum_deposit * investment_period)
    elif interest_rate_type == "복리":
        return minimum_deposit * ((1 + interest_rate / 100) ** (investment_period)) - (minimum_deposit)
    else:
        return minimum_deposit

@api_view(['GET'])
def recommend_product(request, user_survey_id):
    # 사용자 설문조사 정보 가져오기
    user_survey = UserSurvey.objects.get(id=user_survey_id)

    # 사용자가 선택한 항목들
    deposit_or_saving = user_survey.deposit_or_saving
    minimum_deposit = user_survey.minimum_deposit
    investment_period = user_survey.investment_period
    interest_rate_type = user_survey.interest_rate_type

    # 예금/적금에 맞는 금융상품 필터링
    products = Product.objects.filter(is_saving=deposit_or_saving)

    # 최소 예치금 기준 필터링
    if minimum_deposit:
        products = products.filter(max_limit__gte=minimum_deposit)

    # 필터링된 상품 목록
    product_data = []

    for product in products:
        # Product와 연결된 ProductOption 가져오기
        product_options = ProductOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)

        for option in product_options:
            # 금리 유형 기준 필터링
            if interest_rate_type and option.intr_rate_type_nm != interest_rate_type:
                continue  # 조건에 맞지 않는 옵션은 건너뛰기

            # 예상 수익 계산 (매개변수 순서를 수정)
            expected_profit = calculate_expected_return(
                deposit_or_saving,          # 예금 또는 적금 여부
                minimum_deposit,            # 최소 예치금
                investment_period,          # 투자 기간
                option.intr_rate,           # 금리
                option.intr_rate_type_nm    # 금리 유형
            )
            # 결과 데이터 추가
            product_data.append({
                '상품 코드': str(product.fin_prdt_cd),
                '상품 이름': product.fin_prdt_nm,
                '금융 회사': product.kor_co_nm,
                '저축 금리 유형': option.intr_rate_type_nm,
                '저축 금리': option.intr_rate,
                '저축 기간': option.save_trm,
                '최고 우대 금리': option.intr_rate2,
                '예상 수익': expected_profit  # 예상 수익 추가
            })

    # 예상 수익을 기준으로 정렬 (내림차순)
    sorted_product_data = sorted(product_data, key=lambda x: x['예상 수익'], reverse=True)[:3]
    for i in range(len(sorted_product_data)):
        sorted_product_data[i]['예상 수익'] = int(sorted_product_data[i]['예상 수익'])

    return JsonResponse({'recommended_products': sorted_product_data})


# 군집화 알고리즘

# 필요한 라이브러리 임포트
from faker import Faker
import random
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from collections import Counter


# 1단계: 데이터 생성
def generate_survey_data(num_samples):
    fake = Faker()
    user_survey_data = []
    
    for _ in range(num_samples):
        user_survey_data.append({
            'deposit_or_saving': fake.boolean(),
            'minimum_deposit': fake.random_int(min=500000, max=50000000),  # 최소 예금액 범위를 확장
            'investment_period': fake.random_int(min=1, max=20),  # 투자 기간을 넓혀서 다양화
            'expected_return': fake.random_int(min=1, max=20),  # 예상 수익률 범위 확장
            'interest_rate_type': fake.random_element(elements=("단리", "복리")),
            'investment_goal': fake.random_element(elements=("결혼자금", "주택마련", "노후준비")),
            'spending_habit_1': fake.random_element(elements=("쇼핑", "여가", "식비", "교통", "주거", "저축", "기타")),
            'spending_habit_2': fake.random_element(elements=("쇼핑", "여가", "식비", "교통", "주거", "저축", "기타")),
            'spending_habit_3': fake.random_element(elements=("쇼핑", "여가", "식비", "교통", "주거", "저축", "기타")),
            'fixed_income': fake.random_int(min=100000, max=20000000),  # 고정 수입 범위 확장
            'main_bank': fake.company(),
            'household_type': fake.random_element(elements=("1인가구", "2인가구", "4인 이상")),
            'age': fake.random_int(min=18, max=90),  # 나이 범위 확장
            'risk_tolerance': fake.random_element(elements=("낮음", "보통", "높음")),
        })
    
    return user_survey_data

# 2단계 필터링으로 상품 추천 후 실제 선택한 상품 저장
def recommend_top_3_products(user_survey):
    # 1. 설문조사 정보에 맞는 상품 필터링
    products = Product.objects.all()

    # 최소 예치금 기준 필터링
    if user_survey['minimum_deposit']:
        products = products.filter(max_limit__gte=user_survey['minimum_deposit'])

    # 추천 상품 리스트
    recommended_products = []

    for product in products:
        # Product와 연결된 ProductOption 가져오기
        product_options = ProductOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)

        for option in product_options:
            # 투자 기간 기준 필터링
            # if user_survey['investment_period'] and option.save_trm < user_survey['investment_period']:
            #     continue  # 조건에 맞지 않으면 건너뛰기

            # 금리 유형 기준 필터링
            if user_survey['interest_rate_type'] and option.intr_rate_type_nm != user_survey['interest_rate_type']:
                continue  # 조건에 맞지 않으면 건너뛰기

        # 예상 수익 계산
        expected_return = calculate_expected_return(
            product.is_saving,  # 예금 또는 적금 여부
            user_survey['minimum_deposit'],  # 최소 예치금
            user_survey['investment_period'],  # 투자 기간
            option.intr_rate,  # 이자율
            option.intr_rate_type_nm,  # 금리 유형
        )

        # 추천 상품에 필요한 데이터만 추가
        recommended_products.append({
            'product_name': product.fin_prdt_nm,  # 상품명
            'company_name': product.kor_co_nm,   # 금융 회사 이름
            'interest_rate': option.intr_rate,   # 금리
            'interest_rate_type': option.intr_rate_type_nm,  # 금리 유형
            'investment_period': option.save_trm,  # 투자 기간
            'expected_return': expected_return    # 예상 수익
        })

        # user_survey에 예상 수익 추가
        user_survey['expected_return'] = expected_return

    # 예상 수익 기준 상위 3개 상품 선택
    recommended_products = sorted(recommended_products, key=lambda x: x['expected_return'], reverse=True)[:3]

    # 3. 랜덤으로 하나의 상품 선택
    selected_product = random.choice(recommended_products)

    # 4. 선택된 상품을 'selected_product'에 저장
    # (user_survey 객체에 저장)
    user_survey['selected_product'] = selected_product['product_name']  # 상품명 저장

    # 5. 추천된 상품 리스트 반환
    return user_survey

# 3단계: 유효성 검사
def validate_survey_data(survey):
    required_fields = [
        'deposit_or_saving', 'minimum_deposit', 'investment_period',
        'expected_return', 'interest_rate_type', 'investment_goal',
        'spending_habit_1', 'spending_habit_2', 'spending_habit_3',
        'fixed_income', 'main_bank', 'household_type', 'age', 'risk_tolerance'
    ]
    for field in required_fields:
        if field not in survey or survey[field] is None:
            raise ValueError(f"필드 {field}가 누락되었습니다.")

# 4단계: 데이터 전처리
CATEGORICAL_MAPPINGS = {
    "interest_rate_type": {"단리": 0, "복리": 1},
    "investment_goal": {"결혼자금": 0, "주택마련": 1, "노후준비": 2},
    "spending_habit": {"쇼핑": 0, "여가": 1, "식비": 2, "교통": 3, "주거": 4, "저축": 5, "기타": 6},
    "household_type": {"1인가구": 0, "2인가구": 1, "4인 이상": 2},
    "risk_tolerance": {"낮음": 0, "보통": 1, "높음": 2},
}

def preprocess_survey_data(user_surveys):
    survey_data = []
    for survey in user_surveys:
        validate_survey_data(survey)
        survey_data.append([
            survey['deposit_or_saving'],
            survey['minimum_deposit'],
            survey['investment_period'],
            survey['expected_return'],
            CATEGORICAL_MAPPINGS["interest_rate_type"][survey['interest_rate_type']],
            CATEGORICAL_MAPPINGS["investment_goal"][survey['investment_goal']],
            CATEGORICAL_MAPPINGS["spending_habit"][survey['spending_habit_1']],
            CATEGORICAL_MAPPINGS["spending_habit"][survey['spending_habit_2']],
            CATEGORICAL_MAPPINGS["spending_habit"][survey['spending_habit_3']],
            survey['fixed_income'],
            hash(survey['main_bank']) % 10,
            CATEGORICAL_MAPPINGS["household_type"][survey['household_type']],
            survey['age'],
            CATEGORICAL_MAPPINGS["risk_tolerance"][survey['risk_tolerance']],
        ])
    return survey_data


# 5단계: 군집화
def cluster_users(preprocessed_data):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(preprocessed_data)

    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans_labels = kmeans.fit_predict(scaled_data)

    return kmeans, scaler, kmeans_labels

# 6단계: 군집별 대표 상품 설정
def set_cluster_representative_product(cluster_labels, user_surveys):
    cluster_representatives = {}
    for cluster_id in set(cluster_labels):
        cluster_users = [user for user, label in zip(user_surveys, cluster_labels) if label == cluster_id]
        product_choices = [
            {
                "product_name": user.get('selected_product'),
                "expected_return": user.get('expected_return'),
            }
            for user in cluster_users
            if 'selected_product' in user
        ]

        # 가장 많이 선택된 상품과 해당 상품의 예상 수익 찾기
        most_common_product = Counter([choice["product_name"] for choice in product_choices]).most_common(1)

        if most_common_product:
            most_common_product_name = most_common_product[0][0]
            # 예상 수익률 가져오기
            expected_return = next(
                (choice["expected_return"] for choice in product_choices if choice["product_name"] == most_common_product_name),
                0
            )
            cluster_representatives[cluster_id] = {
                "product_name": most_common_product_name,
                "expected_return": expected_return,
            }
        else:
            cluster_representatives[cluster_id] = {
                "product_name": "추천할 상품 없음",
                "expected_return": 0,
            }

    return cluster_representatives

# 7단계: 새로운 사용자 추천
def recommend_for_new_user(new_user_survey, scaler, kmeans_model, cluster_representatives):
    new_user_data = preprocess_survey_data([new_user_survey])[0]
    scaled_user_data = scaler.transform([new_user_data])

    cluster_label = kmeans_model.predict(scaled_user_data)[0]
    representative = cluster_representatives.get(cluster_label, {"product_name": "추천할 상품 없음", "expected_return": 0})

    # 추천 상품과 예상 수익 반환
    return {
        "recommended_product": representative["product_name"],
        "expected_return": f'{int(representative["expected_return"])}원',
    }

import os
import joblib

def save_model(kmeans, scaler, cluster_representatives, save_dir="model_files"):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    # 모델과 스케일러 저장
    joblib.dump(kmeans, os.path.join(save_dir, "kmeans_model.pkl"))
    joblib.dump(scaler, os.path.join(save_dir, "scaler.pkl"))
    # 군집별 대표 상품 저장
    joblib.dump(cluster_representatives, os.path.join(save_dir, "cluster_representatives.pkl"))
    print("모델 저장 완료!")

def load_model(save_dir="model_files"):
    try:
        kmeans = joblib.load(os.path.join(save_dir, "kmeans_model.pkl"))
        scaler = joblib.load(os.path.join(save_dir, "scaler.pkl"))
        cluster_representatives = joblib.load(os.path.join(save_dir, "cluster_representatives.pkl"))
        print("모델 로드 완료!")
        return kmeans, scaler, cluster_representatives
    except FileNotFoundError:
        raise ValueError("모델 파일이 없습니다. 먼저 모델을 저장하세요.")
    

@api_view(['POST'])
def initialize_model(request):
    try:
        # 1단계: 설문 데이터 생성
        user_surveys = generate_survey_data(num_samples=500)

        # 1.5단계: 각 사용자에 대해 상품 추천
        for user_survey in user_surveys:
            recommend_top_3_products(user_survey)

        # 2단계: 데이터 전처리
        preprocessed_data = preprocess_survey_data(user_surveys)

        # 3단계: 군집화 모델 훈련
        kmeans, scaler, kmeans_labels = cluster_users(preprocessed_data)

        # 4단계: 군집별 대표 상품 설정
        cluster_representatives = set_cluster_representative_product(kmeans_labels, user_surveys)

        # 5단계: 모델 저장
        save_model(kmeans, scaler, cluster_representatives)

        return JsonResponse({"message": "모델 초기화 및 저장 완료!"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@api_view(['POST'])
def recommend_product_for_user(request):
    try:
        # 요청 데이터에서 user_survey_id 추출
        user_survey_id = request.data.get("user_survey_id")
        if not user_survey_id:
            return JsonResponse({"error": "user_survey_id is required"}, status=400)

        # UserSurvey 모델 데이터 가져오기
        user_survey = UserSurvey.objects.filter(pk=user_survey_id).first()
        if not user_survey:
            return JsonResponse({"error": "UserSurvey not found"}, status=404)

        # 저장된 모델과 데이터를 로드
        kmeans, scaler, cluster_representatives = load_model()

        # 사용자 데이터를 변환하고 추천 수행
        user_data = transform_user_survey(user_survey)
        recommended_product = recommend_for_new_user(user_data, scaler, kmeans, cluster_representatives)

        return JsonResponse({"recommended_product": recommended_product})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def transform_user_survey(user_survey):
    return {
        "age": int(user_survey.age),
        "risk_tolerance": user_survey.risk_tolerance,
        "fixed_income": float(user_survey.fixed_income),
        "current_assets": float(user_survey.current_assets),
        "deposit_or_saving": user_survey.deposit_or_saving,
        "minimum_deposit": float(user_survey.minimum_deposit),
        "investment_period": float(user_survey.investment_period),
        "expected_return": float(user_survey.expected_return),
        "interest_rate_type": user_survey.interest_rate_type,
        "investment_goal": user_survey.investment_goal,
        "spending_habit_1": user_survey.spending_habit_1,
        "spending_habit_2": user_survey.spending_habit_2,
        "spending_habit_3": user_survey.spending_habit_3,
        "main_bank": user_survey.main_bank,
        "household_type": user_survey.household_type,
    }

@api_view(['POST'])
def get_product_by_name(request):
    product_name = request.data.get('product_name')

    if not product_name:
        return Response({"error": "상품 이름이 필요합니다."}, status=400)

    try:
        # 상품명으로 Product 모델에서 상품 찾기
        product = Product.objects.get(fin_prdt_nm=product_name['recommended_product'])
        return Response({
            "kor_co_nm": product.kor_co_nm,
            "product_code": product.fin_prdt_cd,
            "recommended_product": product.fin_prdt_nm
        })
    except Product.DoesNotExist:
        return Response({"error": "해당 상품을 찾을 수 없습니다."}, status=404)
    
# # 실행 예시:
# new_user_survey = {
#     'deposit_or_saving': True,
#     'minimum_deposit': 1000000,
#     'investment_period': 5,
#     'expected_return': 5,
#     'interest_rate_type': '복리',
#     'investment_goal': '주택마련',
#     'spending_habit_1': '식비',
#     'spending_habit_2': '저축',
#     'spending_habit_3': '여가',
#     'fixed_income': 2000000,
#     'main_bank': '새로운 은행',
#     'household_type': '2인가구',
#     'age': 30,
#     'risk_tolerance': '보통'
# }

# cluster_representatives = run_full_process(num_samples=5000, new_user_survey=new_user_survey)
