import requests
from django.http import JsonResponse
from .models import Product, ProductOption
from django.conf import settings  # settings에서 API_KEY 가져오기

API_KEY = settings.PRODUCT_API_KEY

SAVING_API_URL = "https://finlife.fss.or.kr/finlife/api/fdrmDpstApi/list.do"

def fetch_saving_products(request):
    params = {
        "auth": settings.API_KEY,
        "topFinGrpNo": "020000",
        "pageNo": 1,
    }
    response = requests.get(SAVING_API_URL, params=params)
    data = response.json()

    if data.get("result") == "success":
        base_list = data["baseList"]
        option_list = data["optionList"]

        # Product 저장
        for item in base_list:
            product, created = Product.objects.update_or_create(
                product_id=item["fin_prdt_cd"],
                defaults={
                    "is_saving": True,  # 적금
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
                    "is_saving": True,  # 적금
                    "intr_rate_type_nm": option["intr_rate_type_nm"],
                    "rsrv_type_nm": option.get("rsrv_type_nm", ""),
                    "intr_rate": option["intr_rate"],
                    "intr_rate2": option.get("intr_rate2", 0.0),
                }
            )

        return JsonResponse({"message": "Saving products saved successfully."})
    else:
        return JsonResponse({"error": "Failed to fetch saving products."})


DEPOSIT_API_URL = "https://finlife.fss.or.kr/finlife/api/fdrmEntyApi/list.do"

def fetch_deposit_products(request):
    params = {
        "auth": settings.API_KEY,
        "topFinGrpNo": "020000",
        "pageNo": 1,
    }
    response = requests.get(DEPOSIT_API_URL, params=params)
    data = response.json()

    if data.get("result") == "success":
        base_list = data["baseList"]
        option_list = data["optionList"]

        # Product 저장
        for item in base_list:
            product, created = Product.objects.update_or_create(
                product_id=item["fin_prdt_cd"],
                defaults={
                    "is_saving": False,  # 예금
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
                    "is_saving": False,  # 예금
                    "intr_rate_type_nm": option["intr_rate_type_nm"],
                    "rsrv_type_nm": option.get("rsrv_type_nm", ""),
                    "intr_rate": option["intr_rate"],
                    "intr_rate2": option.get("intr_rate2", 0.0),
                }
            )

        return JsonResponse({"message": "Deposit products saved successfully."})
    else:
        return JsonResponse({"error": "Failed to fetch deposit products."})
