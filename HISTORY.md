# 작업 히스토리

## [2026-04-13] GitHub Actions로 매일 6시 자동 운세 발송 봇 완성

### 한 것
1. **Git 리포지토리 초기화**
   - .gitignore, .env.example 파일 생성
   - 초기 커밋 및 GitHub 연결

2. **GitHub Actions 워크플로우 설정**
   - 매일 한국시간 06:00 (UTC 21:00)에 자동 실행
   - Python 3.13 + Playwright 1.48.0 환경 구성

3. **메시지 형식 최적화**
   - 운세지수를 각 띠별 컨텐츠 맨 아래로 이동
   - 운세지수 앞에 한 줄 띄워서 가독성 개선

4. **Telegram 발송 기능**
   - GitHub Secrets (TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)로 안전하게 관리
   - 구독자 전원에게 자동 발송

### 시행착오
- Playwright 1.42.0 → 1.48.0 업그레이드 (greenlet 호환성 문제)
- upload-artifact 버전 업그레이드 (v3 → v4)
- 운세지수 배치 형식 최적화 (정규식 → 직접 string 조작)
- GitHub Secrets 설정 위치 확인 (Repository Secrets 사용)

### 결정 사항과 이유
- **GitHub Actions 선택**: 
  - 이유: 클라우드 기반으로 머신 상태 무관하게 자동 실행 가능
  - 무료 사용량 충분 (공개 리포지토리)

- **한국시간 06:00 설정**:
  - UTC 21:00으로 설정 (한국은 UTC+9)
  - 매일 아침 일정한 시간에 발송 가능

- **메시지 형식 개선**:
  - 운세지수를 맨 아래로: 콘텐츠 읽고 마지막에 지수 확인
  - 한 줄 띄우기: 시각적 구분으로 가독성 향상

### 해결 방법
1. Playwright 버전 호환성: requirements.txt 버그 버전 업그레이드
2. GitHub Actions 오류: 로그 분석으로 greenlet 문제 파악 및 해결
3. 메시지 형식: 정규식 복잡성으로 인해 split/re.search 조합으로 변경

---

## 다음 예정
- Obsidian MCP 연결
- 추가 기능 개발 (필요시)
