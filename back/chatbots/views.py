import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import logging

# 로그 설정 (로깅 레벨 설정)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")
        logger.debug(f"User message: {user_message}")  # 입력 받은 메시지 출력

        try:
            openai.api_key = settings.CHATGPT_API_KEY
            logger.debug(f"Using API key: {openai.api_key}")  # API 키 출력

            # OpenAI API 호출
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "이제부터 모든 응답은 한국어로 해주세요."},
                          {"role": "user", "content": user_message}]
            )
            logger.debug(f"Response: {response}")  # API 응답 출력

            bot_reply = response["choices"][0]["message"]["content"]
            return JsonResponse({"reply": bot_reply})

        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")  # 오류 메시지 로깅
            return JsonResponse({"error": str(e)}, status=500)
