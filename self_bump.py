import os
import requests
import time
import random

# 깃허브 시크릿에서 정보 가져오기
USER_TOKEN = os.environ['USER_TOKEN']
FORUM_POST_ID = os.environ['FORUM_POST_ID']

# 디스코드 응답 API 주소
url = f"https://discord.com/api/v9/channels/{FORUM_POST_ID}/messages"

# 실제 사람이 브라우저로 보내는 것처럼 헤더 설정
headers = {
    "Authorization": USER_TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 보낼 메시지 (멘트가 매번 같으면 매크로 탐지에 걸릴 수 있으므로 여러 개 중 랜덤 발송)
messages = [
    {"content": "."},
]

payload = random.choice(messages)

# 메시지 전송 (댓글 달기)
response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    print("댓글 작성(끌올) 성공!")
else:
    print(f"오류 발생! 에러 코드: {response.status_code}")
    print(response.text)