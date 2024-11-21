from django.db import models


class Product(models.Model):
    fin_prdt_cd = models.CharField(max_length=100, unique=True, primary_key=True)  # 금융상품 코드(PK)
    is_saving = models.BooleanField()  
    fin_co_no = models.CharField(max_length=255)
    fin_prdt_nm = models.CharField(max_length=255, default="Unknown")
    join_way = models.CharField(max_length=255)
    mtrt_int = models.TextField()
    spcl_cnd = models.TextField()
    join_deny = models.CharField(max_length=255, null=True)
    etc_note = models.TextField(default="")
    max_limit = models.FloatField(null=True)


class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    fin_prdt_cd = models.TextField()
    is_saving = models.BooleanField()
    intr_rate_type_nm = models.CharField(max_length=255)
    rsrv_type_nm = models.CharField(max_length=255, null=True)
    save_trm = models.IntegerField()
    intr_rate = models.FloatField()
    intr_rate2 = models.FloatField()



# class UserProduct(models.Model):
#     user_id = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='products')

#     product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.user_id} - {self.product_id}"
