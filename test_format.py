#!/usr/bin/env python3
import re

def clean_content_option1(title, body):
    """옵션 1: 운세지수 앞에만 띄움"""
    cut_markers = ["저작권자 ©", "키워드", "#오늘의운세"]
    for marker in cut_markers:
        if marker in body:
            body = body.split(marker)[0]

    body = body.replace("*해당 내용의 저작권은 지윤철학원에 있습니다", "")
    body = re.sub(r'(〈.+?띠〉)', r'\n\1', body)
    body = re.sub(r'(운세지수 .+?\n)', r'\n\1', body)  # 앞만 띄움
    body = re.sub(r'\n{3,}', '\n\n', body).strip()
    message = f"📢 {title}\n\n{body}"
    return message

def clean_content_option2(title, body):
    """옵션 2: 운세지수 앞뒤 모두 띄움"""
    cut_markers = ["저작권자 ©", "키워드", "#오늘의운세"]
    for marker in cut_markers:
        if marker in body:
            body = body.split(marker)[0]

    body = body.replace("*해당 내용의 저작권은 지윤철학원에 있습니다", "")
    body = re.sub(r'(〈.+?띠〉)', r'\n\1', body)
    body = re.sub(r'(운세지수 .+?\n)', r'\n\1\n', body)  # 앞뒤 띄움
    body = re.sub(r'\n{3,}', '\n\n', body).strip()
    message = f"📢 {title}\n\n{body}"
    return message

# 샘플 데이터
title = "2026년 4월 13일 운세"
body = """〈쥐띠〉
운세지수 72
재정운이 상승하는 날입니다. 새로운 기회가 찾아올 수 있으니 주의깊게 살펴보세요.
금전 거래는 신중하게 진행하세요.

〈소띠〉
운세지수 68
오늘은 대인관계가 중요한 날입니다. 주변 사람들과의 소통을 소중히 여기세요.
건강 관리도 필요합니다."""

print("\n" + "="*60)
print("【 옵션 1: 운세지수 앞에만 띄움 】")
print("="*60)
print(clean_content_option1(title, body))

print("\n\n" + "="*60)
print("【 옵션 2: 운세지수 앞뒤 모두 띄움 】")
print("="*60)
print(clean_content_option2(title, body))
