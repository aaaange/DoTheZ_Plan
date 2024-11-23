<template>
  <div
    class="main-page"
    style="
      width: 100%;
      height: 100vh;
      background: #F9EB87;
      display: flex;
      justify-content: center;
      align-items: center;
      padding-top: 50px;
    "
  >
    <div
      class="content-container"
      style="
        width: 800px; /* Adjusted width to match sign-up form */
        background: #FBF9F4;
        box-shadow: 6px 9px 4px rgba(0, 0, 0, 0.2);
        border-radius: 20px; /* Adjusted border-radius to match sign-up form */
        padding: 40px;
      "
    >
      <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #585547; font-size: 48px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 700;">
          두더Z
        </h1>
        <p style="color: #585547; font-size: 16px; font-family: 'IBM Plex Sans KR', sans-serif; font-weight: 300;">
          어서오세요! 두더Z와 깊이 있는 금융 생활 해요 :)
        </p>
      </div>

      <div
        class="card-grid"
        style="
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
          gap: 20px;
        "
      >
        <!-- 예적금 상품 조회 카드 -->
        <div
          style="
            background: #ffffff;
            border: 1px solid #e6af69;
            box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
          "
        >
          <img src="../image/free-icon-deposit-2132991.png" alt="Deposit" style="width: 80px; height: 80px;" />
          <h2 style="color: #585547; font-size: 16px; font-weight: 500; margin-top: 10px;">예적금 상품 조회</h2>
          <p style="color: #585547; font-size: 14px; font-weight: 400;">
            현재 판매 중인 예금, 적금 상품을 한눈에 확인할 수 있습니다.
          </p>
          <RouterLink :to="{ name: 'productlist' }">
            <button style="margin-top: 10px; padding: 10px 20px; background: #e6af69; color: white; border: none; border-radius: 8px; cursor: pointer;">
              바로가기
            </button>
          </RouterLink>
        </div>

        <!-- 환율 계산기 카드 -->
        <div
          style="
            background: #ffffff;
            border: 1px solid #e6af69;
            box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
          "
        >
          <img src="../image/free-icon-exchange-rate-3309969.png" alt="Exchange Rate" style="width: 80px; height: 80px;" />
          <h2 style="color: #585547; font-size: 16px; font-weight: 500; margin-top: 10px;">환율 계산기</h2>
          <p style="color: #585547; font-size: 14px; font-weight: 400;">
            선택하신 국가와 원화와의 환율을 계산할 수 있습니다.
          </p>
          <RouterLink :to="{ name: 'exchangerate' }">
            <button style="margin-top: 10px; padding: 10px 20px; background: #e6af69; color: white; border: none; border-radius: 8px; cursor: pointer;">
              바로가기
            </button>
          </RouterLink>
        </div>

        <!-- 가까운 은행 찾기 카드 -->
        <div
          style="
            background: #ffffff;
            border: 1px solid #e6af69;
            box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
          "
        >
          <img src="../image/free-icon-map-2086172.png" alt="Map" style="width: 80px; height: 80px;" />
          <h2 style="color: #585547; font-size: 16px; font-weight: 500; margin-top: 10px;">가까운 은행 찾기</h2>
          <p style="color: #585547; font-size: 14px; font-weight: 400;">
            지도 위에서 가까운 은행을 찾아 정보를 확인할 수 있습니다.
          </p>
          <RouterLink :to="{ name: 'map' }">
            <button style="margin-top: 10px; padding: 10px 20px; background: #e6af69; color: white; border: none; border-radius: 8px; cursor: pointer;">
              바로가기
            </button>
          </RouterLink>
        </div>

        <!-- 금융 상품 추천 카드 -->
        <div
          style="
            background: #ffffff;
            border: 1px solid #e6af69;
            box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
          "
        >
          <img src="../image/free-icon-rating-6962022.png" alt="Recommendation" style="width: 80px; height: 80px;" />
          <h2 style="color: #585547; font-size: 16px; font-weight: 500; margin-top: 10px;">금융 상품 추천</h2>
          <p style="color: #585547; font-size: 14px; font-weight: 400;">
            몇 가지 질문을 통해 고객님께 알맞은 금융 상품을 추천해드립니다.
          </p>
          <RouterLink :to="{ name: 'recommend' }">
            <button style="margin-top: 10px; padding: 10px 20px; background: #e6af69; color: white; border: none; border-radius: 8px; cursor: pointer;">
              바로가기
            </button>
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>
