from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UserSurvey
from .serializers import UserSurveySerializer
from django.shortcuts import render
from django.http import JsonResponse
from product.models import Product, ProductOption


@api_view(['GET', 'POST'])
def user_survey_view(request, user):
    # GET 요청: 저장된 모든 UserSurvey 데이터 조회
    if request.method == 'GET':
        surveys = UserSurvey.objects.all()  # 모든 설문 데이터 가져오기
        serializer = UserSurveySerializer(surveys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST 요청: 새로운 UserSurvey 데이터 생성
    elif request.method == 'POST':
        serializer = UserSurveySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # 데이터 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def calculate_expected_return(deposit_or_saving, minimum_deposit, investment_period, interest_rate, interest_rate_type):
    # 단리 또는 복리 계산
    if interest_rate_type == "단리":
        return minimum_deposit * interest_rate * (investment_period / 12)
    elif interest_rate_type == "복리":
        return minimum_deposit * ((1 + interest_rate / 100) ** (investment_period / 12)) - minimum_deposit
    else:
        return 0

@api_view(['GET'])
def recommend_product(request, user_survey_id):
    # 사용자 설문조사 정보 가져오기
    user_survey = UserSurvey.objects.get(id=user_survey_id)

    # 사용자가 선택한 항목들
    deposit_or_saving = user_survey.deposit_or_saving
    minimum_deposit = user_survey.minimum_deposit
    investment_period = user_survey.investment_period
    expected_return = user_survey.expected_return
    interest_rate_type = user_survey.interest_rate_type
    investment_goal = user_survey.investment_goal

    # 예금/적금에 맞는 금융상품 필터링
    products = Product.objects.filter(is_saving=deposit_or_saving)
    for product in products:
        product['save_trm'] = ProductOption.objects.get(fin_prdt_cd=product.fin_prdt_cd).save_trm

    # 최소 예치금 기준 필터링
    if minimum_deposit:
        products = products.filter(max_limit__gte=minimum_deposit)

    # 투자 기간 기준 필터링 (예: 1년 이상, 3년 이하)
    if investment_period:
        products = products.filter(productoption__save_trm__gte=investment_period)

    # 금리 유형 (단리/복리)에 맞는 상품 필터링
    if interest_rate_type:
        products = products.filter(intr_rate_type_nm=interest_rate_type)

    # 필터링된 상품 목록을 금융회사 이름(kor_co_nm)과 상품 옵션과 함께 제공
    product_data = []
    for product in products:
        product_options = ProductOption.objects.filter(product=product)
        for option in product_options:
            expected_profit = calculate_expected_return(
                deposit_or_saving, 
                minimum_deposit, 
                investment_period, 
                option.intr_rate, 
                option.intr_rate_type_nm
            )
            product_data.append({
                '상품 이름': product.fin_prdt_nm,
                '금융 회사': product.kor_co_nm,
                '저축 금리 유형': option.intr_rate_type_nm,
                '저축 금리': option.intr_rate,
                '저축 기간': option.save_trm,
                '최고 우대 금리': option.intr_rate2,
                '예상 수익': expected_profit  # 예상 수익 추가
            })

    sorted_product_data = sorted(product_data, key=lambda x: x['expected_profit'], reverse=True)

    return JsonResponse({'recommended_products': sorted_product_data})


# 군집화 알고리즘

# # 필요한 라이브러리 임포트
# from faker import Faker
# import random
# import numpy as np
# from sklearn.preprocessing import StandardScaler
# from sklearn.cluster import KMeans, DBSCAN
# from sklearn.metrics import silhouette_score
# from collections import Counter
# from sklearn.datasets import make_blobs

# # 1단계: 데이터 생성
# def generate_survey_data(num_samples=5000):
#     fake = Faker()
#     user_survey_data = []
    
#     for _ in range(num_samples):
#         user_survey_data.append({
#             'deposit_or_saving': fake.boolean(),
#             'minimum_deposit': fake.random_int(min=500000, max=50000000),  # 최소 예금액 범위를 확장
#             'investment_period': fake.random_int(min=1, max=20),  # 투자 기간을 넓혀서 다양화
#             'expected_return': fake.random_int(min=1, max=20),  # 예상 수익률 범위 확장
#             'interest_rate_type': fake.random_element(elements=("단리", "복리")),
#             'investment_goal': fake.random_element(elements=("결혼자금", "주택마련", "노후준비")),
#             'spending_habit_1': fake.random_element(elements=("쇼핑", "여가", "식비", "교통", "주거", "저축", "기타")),
#             'spending_habit_2': fake.random_element(elements=("쇼핑", "여가", "식비", "교통", "주거", "저축", "기타")),
#             'spending_habit_3': fake.random_element(elements=("쇼핑", "여가", "식비", "교통", "주거", "저축", "기타")),
#             'fixed_income': fake.random_int(min=100000, max=20000000),  # 고정 수입 범위 확장
#             'main_bank': fake.company(),
#             'household_type': fake.random_element(elements=("1인가구", "2인가구", "4인 이상")),
#             'age': fake.random_int(min=18, max=90),  # 나이 범위 확장
#             'risk_tolerance': fake.random_element(elements=("낮음", "보통", "높음")),
#         })
    
#     return user_survey_data


# # 2단계: 유효성 검사
# def validate_survey_data(survey):
#     required_fields = [
#         'deposit_or_saving', 'minimum_deposit', 'investment_period',
#         'expected_return', 'interest_rate_type', 'investment_goal',
#         'spending_habit_1', 'spending_habit_2', 'spending_habit_3',
#         'fixed_income', 'main_bank', 'household_type', 'age', 'risk_tolerance'
#     ]
#     for field in required_fields:
#         if field not in survey or survey[field] is None:
#             raise ValueError(f"필드 {field}가 누락되었습니다.")

# # 3단계: 데이터 전처리
# CATEGORICAL_MAPPINGS = {
#     "interest_rate_type": {"단리": 0, "복리": 1},
#     "investment_goal": {"결혼자금": 0, "주택마련": 1, "노후준비": 2},
#     "spending_habit": {"쇼핑": 0, "여가": 1, "식비": 2, "교통": 3, "주거": 4, "저축": 5, "기타": 6},
#     "household_type": {"1인가구": 0, "2인가구": 1, "4인 이상": 2},
#     "risk_tolerance": {"낮음": 0, "보통": 1, "높음": 2},
# }

# def preprocess_survey_data(user_surveys):
#     survey_data = []
#     for survey in user_surveys:
#         validate_survey_data(survey)
#         survey_data.append([
#             survey['deposit_or_saving'],
#             survey['minimum_deposit'],
#             survey['investment_period'],
#             survey['expected_return'],
#             CATEGORICAL_MAPPINGS["interest_rate_type"][survey['interest_rate_type']],
#             CATEGORICAL_MAPPINGS["investment_goal"][survey['investment_goal']],
#             CATEGORICAL_MAPPINGS["spending_habit"][survey['spending_habit_1']],
#             CATEGORICAL_MAPPINGS["spending_habit"][survey['spending_habit_2']],
#             CATEGORICAL_MAPPINGS["spending_habit"][survey['spending_habit_3']],
#             survey['fixed_income'],
#             hash(survey['main_bank']) % 10,
#             CATEGORICAL_MAPPINGS["household_type"][survey['household_type']],
#             survey['age'],
#             CATEGORICAL_MAPPINGS["risk_tolerance"][survey['risk_tolerance']],
#         ])
#     return survey_data

# # 3.5단계 필터링으로 상품 추천 후 실제 선택한 상품 저장
# def recommend_top_3_products(user_survey):
#     # 1. 설문조사 정보에 맞는 상품 필터링
#     products = Product.objects.all()
#     for product in products:
#         product_option = ProductOption.objects.get(fin_prdt_cd=product.fin_prdt_cd)
#         product['save_trm'] = product_option['save_trm']
#     # 최소 예치금 기준 필터링
#     if user_survey['minimum_deposit']:
#         products = products.filter(max_limit__gte=user_survey['minimum_deposit'])
#     # 투자 기간 기준 필터링 (예: 1년 이상, 3년 이하)
#     if user_survey['investment_period']:
#         products = products.filter(save_trm__gte=user_survey['investment_period'])
#     # 금리 유형 (단리/복리)에 맞는 상품 필터링
#     if user_survey['interest_rate_type']:
#         products = products.filter(intr_rate_type_nm=user_survey['interest_rate_type'])
#     # 2. 각 상품에 대해 예상 수익 계산 후, 상위 3개 추천
#     recommended_products = []

#     for product in products:
#         # 예상 수익 계산
#         expected_return = calculate_expected_return(
#             product.deposit_or_saving,  # 예금 또는 적금
#             user_survey.minimum_deposit,  # 최소 예치금 (월 최소 투자 금액)
#             user_survey.investment_period,  # 투자 기간
#             product.intr_rate_type_nm,  # 금리 (단리/복리)
#             product.interest_rate  # 이자율
#         )
#         recommended_products.append({
#             'product': product,
#             'expected_return': expected_return
#         })

#     # 예상 수익을 기준으로 상위 3개 상품 추천
#     recommended_products = sorted(recommended_products, key=lambda x: x['expected_return'], reverse=True)[:3]

#     # 3. 랜덤으로 하나의 상품을 선택하여 'selected_product'에 저장
#     selected_product = random.choice(recommended_products)

#     # 4. 선택된 상품을 'selected_product'에 저장 (user_survey의 필드로 저장)
#     user_survey.selected_product = selected_product['product']  # 또는 필요한 필드를 저장

#     # 5. 추천된 상품 리스트 반환
#     result = []
#     for recommended_product in recommended_products:
#         result.append({
#             'product_name': recommended_product['product'].name,
#             'expected_return': recommended_product['expected_return']
#         })
    
#     return result

# # 4단계: 군집화
# def cluster_users(preprocessed_data):
#     scaler = StandardScaler()
#     scaled_data = scaler.fit_transform(preprocessed_data)

#     kmeans = KMeans(n_clusters=3, random_state=42)
#     kmeans_labels = kmeans.fit_predict(scaled_data)

#     dbscan = DBSCAN(eps=0.5, min_samples=5)
#     dbscan_labels = dbscan.fit_predict(scaled_data)

#     return kmeans, scaler, kmeans_labels, dbscan_labels

# # 5단계: 군집별 대표 상품 설정
# def set_cluster_representative_product(cluster_labels, user_surveys):
#     cluster_representatives = {}
#     for cluster_id in set(cluster_labels):
#         cluster_users = [user for user, label in zip(user_surveys, cluster_labels) if label == cluster_id]
#         product_choices = [user['selected_product'] for user in cluster_users if 'selected_product' in user]
#         most_common_product = Counter(product_choices).most_common(1)
#         cluster_representatives[cluster_id] = most_common_product[0][0] if most_common_product else "추천할 상품 없음"
#     return cluster_representatives

# # 6단계: 군집화 알고리즘 비교
# # def compare_clustering_algorithms(preprocessed_data, kmeans_labels, dbscan_labels):
# #     kmeans_score = silhouette_score(preprocessed_data, kmeans_labels)
# #     dbscan_score = silhouette_score(preprocessed_data, dbscan_labels)
# #     return {"KMeans": kmeans_score, "DBSCAN": dbscan_score}

# # 7단계: 새로운 사용자 추천
# def recommend_for_new_user(new_user_survey, scaler, kmeans_model, cluster_representatives):
#     new_user_data = preprocess_survey_data([new_user_survey])[0]
#     scaled_user_data = scaler.transform([new_user_data])

#     cluster_label = kmeans_model.predict(scaled_user_data)[0]
#     return cluster_representatives.get(cluster_label, "추천할 상품 없음")

# # 전체 실행 흐름 수정
# def run_full_process(num_samples=5000, new_user_survey=None):
#     # 1단계: 설문 데이터 생성
#     user_surveys = generate_survey_data(num_samples)

#     # 2단계: 데이터 전처리
#     preprocessed_data = preprocess_survey_data(user_surveys)

#     # 3단계: 군집화 모델 훈련 (KMeans와 DBSCAN)
#     kmeans, scaler, kmeans_labels, dbscan_labels = cluster_users(preprocessed_data)

#     # 3.5단계: 필터링으로 상품 추천 후 실제 선택한 상품 저장
#     for user_survey in user_surveys:
#         recommend_top_3_products(user_survey)  # 각 사용자에 대해 상품 추천 및 저장

#     # 4단계: 군집별 대표 상품 설정
#     cluster_representatives = set_cluster_representative_product(kmeans_labels, user_surveys)

#     # 5단계: 새로운 사용자 추천 (사용자가 있다면)
#     if new_user_survey:
#         recommended_product = recommend_for_new_user(new_user_survey, scaler, kmeans, cluster_representatives)
#         print(f"새로운 사용자에게 추천할 상품: {recommended_product}")

#     return cluster_representatives

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

# # 결과 출력
# print(f"군집별 대표 상품: {cluster_representatives}")
