from django.db import models


class Product(models.Model):
    product_id = models.CharField(max_length=255)  # 금융상품 코드(PK)
    is_saving = models.BooleanField()  
    fin_co_no = models.CharField(max_length=255)
    fin_prdt_nm = models.CharField(max_length=255)
    join_way = models.CharField(max_length=255)
    mtrt_int = models.TextField()
    spcl_cnd = models.TextField()
    join_deny = models.CharField(max_length=255)
    etc_note = models.TextField()
    max_limit = models.FloatField()

    def __str__(self):
        return self.fin_prdt_nm


class ProductOption(models.Model):
    is_saving = models.BooleanField()
    intr_rate_type_nm = models.CharField(max_length=255)
    rsrv_type_nm = models.CharField(max_length=255)
    save_trm = models.IntegerField()
    intr_rate = models.FloatField()
    intr_rate2 = models.FloatField()
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Option for {self.product_id}"


class UserProduct(models.Model):
    user_id = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='products')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id} - {self.product_id}"
