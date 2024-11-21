import requests
from django.http import JsonResponse
from .models import Product, ProductOption
from django.conf import settings  # settings에서 API_KEY 가져오기

# API 키 및 URL 설정
API_KEY = settings.PRODUCT_API_KEY
SAVING_API_URL = "http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"
DEPOSIT_API_URL = "http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"

def fetch_saving_products(request):
    """
    적금 상품 데이터를 외부 API에서 가져와 저장하는 함수
    """
    params = {
        "auth": API_KEY,
        "topFinGrpNo": "020000",
        "pageNo": 1,
        "format": "json",  # JSON 응답 요청
    }
    headers = {
        "Accept": "application/json",  # 응답 형식 강제 설정
    }
    response = requests.get(SAVING_API_URL, params=params, headers=headers)

    # 상태 코드와 응답 본문 출력 (디버깅용)
    print("Saving API 상태 코드:", response.status_code)
    print("Saving API 응답 본문:", response.text)

    # JSON 파싱 시도
    try:
        data = response.json()
    except ValueError:
        return JsonResponse({
            "error": "잘못된 JSON 응답",
            "message": f"응답 본문: {response.text}",
        }, status=500)

    # 상태 코드가 200이 아닌 경우 처리
    if response.status_code != 200:
        return JsonResponse({
            "error": "API 요청 실패",
            "message": f"상태 코드: {response.status_code}, 응답: {response.text}",
        }, status=500)

    # API 응답 처리
    if data.get("result") == "success":
        base_list = data.get("baseList", [])
        option_list = data.get("optionList", [])

        # Product 저장
        for item in base_list:
            product, created = Product.objects.update_or_create(
                product_id=item["fin_prdt_cd"],
                defaults={
                    "is_saving": True,
                    "fin_co_no": item["fin_co_no"],
                    "fin_prdt_nm": item["fin_prdt_nm"],
                    "join_way": item["join_way"],
                    "mtrt_int": item.get("mtrt_int", ""),
                    "spcl_cnd": item.get("spcl_cnd", ""),
                    "join_deny": item["join_deny"],
                    "etc_note": item.get("etc_note", ""),
                    "max_limit": item.get("max_limit", 0.0),
                }
            )

        # ProductOption 저장
        for option in option_list:
            product = Product.objects.get(product_id=option["fin_prdt_cd"])
            ProductOption.objects.update_or_create(
                product_id=product,
                save_trm=option["save_trm"],
                defaults={
                    "is_saving": True,
                    "intr_rate_type_nm": option["intr_rate_type_nm"],
                    "rsrv_type_nm": option.get("rsrv_type_nm", ""),
                    "intr_rate": option["intr_rate"],
                    "intr_rate2": option.get("intr_rate2", 0.0),
                }
            )

        return JsonResponse({"message": "Saving products saved successfully."})
    else:
        return JsonResponse({"error": "Saving products fetch failed.", "details": data}, status=500)

# 예금 데이터 가져오기
def fetch_deposit_products(request):
    """
    예금 상품 데이터를 외부 API에서 가져와 저장하는 함수
    """
    params = {
        "auth": API_KEY,
        "topFinGrpNo": "020000",  # 올바르게 수정
        "pageNo": 1,
        "format": "json",  # JSON 응답 요청
    }
    
    # API 요청
    response = requests.get(DEPOSIT_API_URL, params=params)

    # 상태 코드와 응답 본문 출력 (디버깅용)
    print("Deposit API 상태 코드:", response.status_code)
    print("Deposit API 응답 URL:", response.url)
    print("Deposit API 응답 본문:", response.text)

    # JSON 파싱 시도
    try:
        data = response.json()
    except ValueError:
        return JsonResponse(
            {"error": "잘못된 JSON 응답", "message": f"응답 본문: {response.text}"},
            status=500,
        )

    # 상태 코드가 200이 아닌 경우 처리
    if response.status_code != 200:
        return JsonResponse(
            {"error": "Deposit API 요청 실패", "message": f"상태 코드: {response.status_code}, 응답: {response.text}"},
            status=500,
        )

    # API 응답 처리
    if data.get("result") == "success":
        base_list = data.get("baseList", [])
        option_list = data.get("optionList", [])

        # Product 저장
        for item in base_list:
            product, created = Product.objects.update_or_create(
                product_id=item["fin_prdt_cd"],
                defaults={
                    "is_saving": False,
                    "fin_co_no": item["fin_co_no"],
                    "fin_prdt_nm": item["fin_prdt_nm"],
                    "join_way": item["join_way"],
                    "mtrt_int": item.get("mtrt_int", ""),
                    "spcl_cnd": item.get("spcl_cnd", ""),
                    "join_deny": item["join_deny"],
                    "etc_note": item.get("etc_note", ""),
                    "max_limit": item.get("max_limit", 0.0),
                }
            )
            if created:
                print(f"새로운 상품 생성: {product.product_id}")
            else:
                print(f"기존 상품 업데이트: {product.product_id}")

        # ProductOption 저장
        for option in option_list:
            try:
                product = Product.objects.get(product_id=option["fin_prdt_cd"])
                product_option, created = ProductOption.objects.update_or_create(
                    product_id=product,
                    save_trm=option["save_trm"],
                    defaults={
                        "is_saving": False,
                        "intr_rate_type_nm": option["intr_rate_type_nm"],
                        "rsrv_type_nm": option.get("rsrv_type_nm", ""),
                        "intr_rate": option["intr_rate"],
                        "intr_rate2": option.get("intr_rate2", 0.0),
                    }
                )
                if created:
                    print(f"새로운 상품 옵션 생성: {product_option.save_trm}")
                else:
                    print(f"기존 상품 옵션 업데이트: {product_option.save_trm}")
            except Product.DoesNotExist:
                print(f"상품 ID {option['fin_prdt_cd']}에 해당하는 Product가 없음")

        return JsonResponse({"message": "Deposit products saved successfully."})
    else:
        return JsonResponse({"error": "Deposit products fetch failed.", "details": data}, status=500)
