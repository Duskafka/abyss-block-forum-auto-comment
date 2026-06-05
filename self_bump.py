import os
import requests
import time
import random

# 깃허브 시크릿에서 유저 토큰만 가져옵니다.
USER_TOKEN = os.environ['USER_TOKEN']

# 보낼 메시지 (마침표)
messages = [
    {"content": "."},
]

# 실제 사람이 브라우저로 보내는 것처럼 헤더 설정
headers = {
    "Authorization": USER_TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 1. 외부 posts.txt 파일에서 ID 읽어오기
POST_IDS = []
try:
    with open("posts.txt", "r", encoding="utf-8") as f:
        for line in f:
            clean_line = line.strip()

            # 빈 줄이거나, #으로 시작하는 주석(메모) 줄은 건너뜁니다.
            if not clean_line or clean_line.startswith("#"):
                continue

            # 숫자 뒤에 한 칸 띄고 적은 메모가 있어도 숫자만 쏙 빼냅니다. (예: "12345 # 골드포스트" -> "12345")
            if "#" in clean_line:
                clean_line = clean_line.split("#")[0].strip()

            # 최종적으로 남은 숫자가 있으면 리스트에 추가합니다.
            if clean_line.isdigit():
                POST_IDS.append(int(clean_line))

except FileNotFoundError:
    print("오류: posts.txt 파일을 찾을 수 없습니다. 파일을 먼저 생성해주세요.")
    exit(1)

print(f"총 {len(POST_IDS)}개의 포스트에 끌올을 시작합니다.")

# 2. 읽어온 포스트 ID들을 하나씩 순서대로 돕니다.
for index, post_id in enumerate(POST_IDS, start=1):
    url = f"https://discord.com/api/v9/channels/{post_id}/messages"
    payload = random.choice(messages)

    print(f"[{index}/{len(POST_IDS)}] 포스트 ID: {post_id} 작업 중...")

    # 메시지 전송 (댓글 달기)
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print(f"-> {post_id} 댓글 작성(끌올) 성공!")
    else:
        print(f"-> {post_id} 오류 발생! 에러 코드: {response.status_code}")
        print(response.text)

    # 도배 방지를 위해 마지막 포스트가 아니라면 3~6초간 대기합니다.
    if index < len(POST_IDS):
        sleep_time = random.randint(3, 6)
        print(f"도배 방지를 위해 {sleep_time}초간 대기합니다...")
        time.sleep(sleep_time)

print("모든 포스트의 끌올 작업이 완료되었습니다!")