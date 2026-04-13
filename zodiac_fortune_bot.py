import os
import asyncio
import re
import json
import requests
from datetime import datetime
from playwright.async_api import async_playwright

# === GitHub Secrets 환경 변수 ===
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ADMIN_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

class ZodiacFortuneBot:
    def __init__(self):
        self.base_url = "https://www.joongboo.com"
        self.section_url = f"{self.base_url}/news/articleList.html?sc_serial_code=SRN361&view_type=sm"

    def clean_content(self, title, body):
        """가독성 개선 및 불필요 요소 제거 (컨펌된 양식)"""
        # 1. 특정 키워드 기준 하단 내용 절삭
        cut_markers = ["저작권자 ©", "키워드", "#오늘의운세"]
        for marker in cut_markers:
            if marker in body:
                body = body.split(marker)[0]

        # 2. 저작권 문구 삭제 및 공백 정리
        body = body.replace("*해당 내용의 저작권은 지윤철학원에 있습니다", "")
        
        # 3. 가독성 개선 (띠별 줄바꿈 추가)
        body = re.sub(r'(〈.+?띠〉)', r'\n\1', body)
        body = re.sub(r'\n(운세지수 .+?\n)', r'\n\1\n', body)
        body = re.sub(r'\n{3,}', '\n\n', body).strip()
        
        # 4. 최종 메시지 구성
        message = f"📢 {title}\n\n{body}"
        return message

    def get_subscriber_list(self):
        """구독자 목록 가져오기"""
        subs = []
        if os.path.exists("subscribers.json"):
            try:
                with open("subscribers.json", "r", encoding="utf-8") as f:
                    subs = json.load(f)
            except:
                subs = []
        
        # 관리자 ID 추가 (정수형 변환 및 중복 제거)
        if ADMIN_CHAT_ID:
            try:
                subs.append(int(ADMIN_CHAT_ID))
            except:
                pass
        return list(set(subs))

    def send_telegram(self, message, chat_ids):
        """구독자 전원에게 텔레그램 발송"""
        success_count = 0
        for chat_id in chat_ids:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            payload = {"chat_id": chat_id, "text": message}
            try:
                res = requests.post(url, data=payload, timeout=10)
                if res.status_code == 200:
                    success_count += 1
            except Exception as e:
                print(f"[!] 발송 실패 (ID: {chat_id}): {e}")
        
        print(f"[+] 총 {success_count}명에게 발송 완료!")

    async def run(self):
        async with async_playwright() as p:
            # 브라우저 실행
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            try:
                print(f"[*] {datetime.now().strftime('%Y-%m-%d')} 운세 수집 시작...")
                await page.goto(self.section_url, wait_until="domcontentloaded")
                
                items = await page.query_selector_all(".list-block, .type2, .list-item")
                if not items:
                    print("[!] 기사 목록을 찾을 수 없습니다.")
                    return

                # 최상단 기사 선택
                item = items[0]
                link_el = await item.query_selector(".list-titles a, .titles a")
                if link_el:
                    href = await link_el.get_attribute("href")
                    target_url = self.base_url + href if href.startswith("/") else href
                    target_title = (await link_el.inner_text()).strip()
                    
                    # 상세 페이지 접속 및 추출
                    print(f"[*] 기사 접속: {target_url}")
                    await page.goto(target_url, wait_until="domcontentloaded")
                    body_el = await page.query_selector("#article-view-content-div, .article-body")
                    
                    if body_el:
                        body_raw = await body_el.inner_text()
                        final_msg = self.clean_content(target_title, body_raw)
                        
                        # 구독자 목록 확보 및 발송
                        subscribers = self.get_subscriber_list()
                        self.send_telegram(final_msg, subscribers)
                    else:
                        print("[!] 본문 영역을 찾을 수 없습니다.")
            except Exception as e:
                print(f"[X] 실행 에러: {e}")
            finally:
                await browser.close()

if __name__ == "__main__":
    if not TELEGRAM_TOKEN or not ADMIN_CHAT_ID:
        print("[!] 텔레그램 토큰 또는 채팅 ID가 설정되지 않았습니다. (Secrets 확인)")
    else:
        asyncio.run(ZodiacFortuneBot().run())
