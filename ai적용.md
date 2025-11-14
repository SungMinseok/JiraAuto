현재 프로젝트에 AI 기능을 추가하기 위한 계획과 필요사항을 분석해드리겠습니다. 먼저 코드를 살펴보겠습니다.

[4 tools called]

현재 프로젝트 구조를 파악했습니다. AI 기능 추가를 위한 **계획과 필요사항**을 정리해드리겠습니다.

## 🎯 AI 기능 추가 계획

### 1. **기능 개요**
- **입력**: 이슈 제목 (summary)
- **AI 자동 생성**: 
  - 심각도 (severity)
  - 우선순위 (priority)
  - 재현스텝 (steps)
  - 세부내용 (description)

---

## 📋 필요한 것들

### 1. **AI API 서비스 선택** (필수)

선택 가능한 옵션들:

#### **A. OpenAI API** (가장 추천)
- **장점**: 
  - GPT-4o/GPT-4o-mini 사용 가능
  - 한국어 지원 우수
  - API 사용 간단
  - 문서화 잘 되어있음
- **단점**: 
  - 유료 (토큰당 과금)
  - API 키 필요
- **비용**: 
  - GPT-4o-mini: 매우 저렴 ($0.15/1M 입력 토큰)
  - GPT-4o: 조금 비쌈 ($2.50/1M 입력 토큰)
- **필요**: OpenAI API 키

#### **B. Anthropic Claude API**
- **장점**: 
  - 한국어 지원 우수
  - 긴 컨텍스트 처리 가능
- **단점**: 
  - 유료
  - API 키 필요
- **필요**: Anthropic API 키

#### **C. 로컬 LLM** (무료)
- **장점**: 
  - 무료
  - 데이터 외부 유출 없음
- **단점**: 
  - GPU 메모리 많이 필요 (최소 8GB+)
  - 설정 복잡
  - 응답 품질이 상용 API보다 낮을 수 있음
- **옵션**: Ollama, LM Studio 등

#### **D. Google Gemini API**
- **장점**: 
  - 무료 할당량 제공
  - 한국어 지원
- **단점**: 
  - 무료는 제한적
- **필요**: Google API 키

---

### 2. **설치 필요 패키지**

```python
# OpenAI 사용 시
openai

# 또는 Anthropic 사용 시
anthropic

# 또는 로컬 LLM 사용 시
ollama

# 공통
python-dotenv  # API 키 관리용
```

---

### 3. **구현 위치 및 구조**

#### **새로운 파일 생성**
- `ai_assistant.py`: AI 관련 기능 모듈
  - AI API 호출 클래스
  - 프롬프트 템플릿
  - 응답 파싱 로직

#### **수정이 필요한 파일**
- `main_application.py`: AI 생성 버튼 추가 및 이벤트 연결
- `gui_widgets.py`: AI 생성 버튼 위젯 추가
- `config.py`: AI 관련 설정 추가
- `requirements.txt`: 필요 패키지 추가

---

### 4. **API 키 관리**

#### **방법 1: .env 파일** (추천)
```
OPENAI_API_KEY=sk-...
```

#### **방법 2: 설정 파일**
```json
{
  "ai_api_key": "sk-...",
  "ai_model": "gpt-4o-mini"
}
```

#### **방법 3: GUI에서 입력**
- 설정 다이얼로그에서 API 키 입력/저장

---

### 5. **UI 변경사항**

#### **추가될 버튼/기능**
1. **"AI 자동 생성" 버튼**: Summary 필드 옆에 추가
2. **진행 표시**: AI 응답 대기 중 로딩 표시
3. **설정 메뉴**: AI 모델 선택, API 키 설정 (선택사항)

---

### 6. **프롬프트 설계**

JIRA 버그 리포트 특성에 맞춘 프롬프트 필요:

```
당신은 JIRA 버그 리포트 작성 전문가입니다.
다음 버그 제목을 바탕으로 정보를 생성해주세요:

버그 제목: {summary}

다음 정보를 JSON 형식으로 작성하세요:
1. priority: Blocker/Critical/High/Medium/Low 중 선택
2. severity: 1-Critical/2-Major/3-Minor 중 선택  
3. steps: 재현 단계를 번호로 나열 (한국어)
4. description: 버그 상세 설명 (한국어)
```

---

### 7. **예상 작업 흐름**

```
1. 사용자가 Summary 입력
2. "AI 생성" 버튼 클릭
3. AI API 호출 (로딩 표시)
4. AI 응답 파싱
5. 각 필드에 자동 입력
   - Priority 콤보박스
   - Severity 콤보박스
   - Steps 텍스트 필드
   - Description 텍스트 필드
6. 사용자가 수동으로 수정 가능
```

---

### 8. **예상 비용** (OpenAI 기준)

- GPT-4o-mini 사용 시
- 1회 요청당 약 500~1000 토큰
- **비용**: 요청당 약 $0.0001~0.0003 (약 0.1~0.4원)
- 하루 100회 사용 시: 약 40원

---

### 9. **보안 고려사항**

1. **API 키 관리**
   - `.env` 파일을 `.gitignore`에 추가
   - 하드코딩 금지

2. **데이터 보안**
   - 민감한 정보가 포함된 버그 제목은 주의
   - 회사 정책 확인 필요 (외부 API 사용 가능 여부)

---

## 🎨 추천 구현 방안

### **단계별 추천**

#### **Phase 1: 최소 기능 (MVP)**
1. OpenAI GPT-4o-mini API 사용
2. Summary 옆에 "🤖 AI 생성" 버튼 추가
3. 4개 필드만 자동 생성 (priority, severity, steps, description)
4. .env 파일로 API 키 관리

#### **Phase 2: 개선**
1. AI 모델 선택 기능 (GPT-4o-mini vs GPT-4o)
2. 프롬프트 커스터마이징
3. 과거 생성 히스토리 저장
4. 생성된 내용 재생성 기능

#### **Phase 3: 고급**
1. 프리셋 기반 AI 학습
2. 팀별/라벨별 맞춤 프롬프트
3. Fine-tuning된 모델 사용

---

## 💡 즉시 시작 가능한 방법

가장 빠르게 시작하려면:

1. **OpenAI 계정 생성**: https://platform.openai.com
2. **API 키 발급**: $5 크레딧으로 수천 번 사용 가능
3. **패키지 설치**: `pip install openai python-dotenv`
4. **기본 구현 진행**

---

이 정도 계획이면 충분할까요? 특정 부분에 대해 더 자세한 설명이 필요하거나, 바로 구현을 시작하고 싶으시면 말씀해주세요! 🚀