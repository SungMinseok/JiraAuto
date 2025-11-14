# Jira 티켓 작성 양식 (P2 Project)

## 티켓 기본 정보

### Title (제목)
**형식:** `[카테고리] 한글 설명 / English Description`

**예시:**
- `[ServerConnection] 하이드아웃 서버가 없을 때, 신규 계정은 로딩창에서 무한 로딩에 빠지는 문제 / New accounts get stuck in an infinite loading screen when the hideout server is unavailable`
- `[Hideout Customization][Deco] 일부 패널의 설치 바운더리가 메쉬보다 작아 패널 간 겹칠 수 있는 현상 / Some panels' installation boundary is smaller than meshes, causing panels to overlap each other`

**카테고리 예시:**
- `[ServerConnection]` - 서버 연결 관련
- `[Hideout Customization]` - 하이드아웃 커스터마이징
- `[Deco]` - 데코레이션 관련
- `[UI]` - UI 관련
- `[Icons]` - 아이콘 관련
- `[Server][Crash]` - 서버 크래시 관련

---

## Description (상세 설명)

### 1. Observed (관찰 결과)

**형식:**
```
* 한글로 관찰된 문제 설명
{color:#4c9aff}English description of observed issue{color}
```

**예시:**
```
* 서버가 없을 때, 30초가 아닌 1분 30초 후 로그인 불가 팝업이 출력되는 현상을 확인합니다.
{color:#4c9aff}When there is no server, the "login unavailable" popup appears after 1 min and 30 sec and not 30 sec.{color}
```

---

### 2. Video/Screenshot (영상/스크린샷)

**형식:**
```
*Video(영상):*

* !파일명.mp4|width=2560,height=1440,alt="파일명.mp4"!
```

또는

```
*Screenshot(스크린샷):*

* !image-파일명.png|width=2560,height=1440,alt="image-파일명.png"!
```

**참고:**
- 비디오 또는 스크린샷을 Jira에 직접 첨부하고 위 형식으로 삽입
- width, height는 실제 파일 해상도에 맞게 조정

---

### 3. Expected (기대 결과)

**형식:**
```
* 한글로 기대되는 동작 설명
{color:#4c9aff}English description of expected behavior{color}
```

**예시:**
```
* 서버가 없을 때, 30초 후 로그인 불가 팝업이 출력되어야 합니다.
{color:#4c9aff}When there is no server, the "login unavailable" popup should appear after 30 seconds.{color}
```

---

### 4. Note (참고사항)

**형식:**
```
*Note(참고):*

* 환경 정보 / {color:#4c9aff}Environment{color}
** 빌드/{color:#4c9aff}Build{color}: [빌드명]
** 백엔드/{color:#4c9aff}Backend{color}: [백엔드 버전]
** Chart Version [버전]
** [환경 링크]

* 추가 재현 조건이나 특이사항 설명
{color:#4c9aff}Additional reproduction conditions or special notes{color}
```

**예시:**
```
*Note(참고):*

* 환경 정보 / {color:#4c9aff}Environment{color}
** 빌드/{color:#4c9aff}Build{color}: DailyQLOC_TEST_game_dev_AMS413131_r357221
** 백엔드/{color:#4c9aff}Backend{color}: backend/main/415.zip
** Chart Version 1.32.1
** https://awsdeploy.pbb-qa.pubg.io/environment/sel-game-dev2

* 스팀 연동 후, 신규 계정에서도 발생합니다.
{color:#4c9aff}Also reproduces with new accounts after linking with Steam.{color}
```

---

## 티켓 메타데이터

### Priority (우선순위)
- **Low** - 낮음
- **Medium** - 중간 (기본값)
- **High** - 높음
- **Critical** - 긴급

### Components (컴포넌트)
- `Tech_Outgame` - 아웃게임 기술
- `Design_Contents` - 디자인 컨텐츠
- 기타 프로젝트별 컴포넌트

### Issue Type (이슈 타입)
- **Bug** - 버그
- **Task** - 태스크
- **Story** - 스토리

---

## 작성 체크리스트

- [ ] 제목에 한글/영문 설명 모두 포함
- [ ] 카테고리 태그 정확히 명시
- [ ] Observed 섹션에 문제 명확히 기술
- [ ] 재현 가능한 비디오/스크린샷 첨부
- [ ] Expected 섹션에 기대 동작 명시
- [ ] Note 섹션에 환경 정보 포함 (빌드, 백엔드, 환경 링크)
- [ ] 추가 재현 조건이나 특이사항 기재
- [ ] 우선순위 적절히 설정
- [ ] 컴포넌트 정확히 선택
- [ ] Assignee 지정 (담당자)

---

## 추가 팁

### 링크 삽입
```
[링크 텍스트|실제 URL|smart-link]
```

### 색상 텍스트
```
{color:#4c9aff}파란색 텍스트{color}
{color:#ff0000}빨간색 텍스트{color}
```

### 굵은 글씨
```
*굵은 글씨*
```

### 코드 블록
```
{code}
코드 내용
{code}
```

---

## 완성된 예시

```
Title:
[ServerConnection] 하이드아웃 서버가 없을 때, 신규 계정은 로딩창에서 무한 로딩에 빠지는 문제 / New accounts get stuck in an infinite loading screen when the hideout server is unavailable

Description:
Observed(관찰 결과):

* 하이드아웃 서버가 없을 때, 신규 계정은 로딩창에서 무한 로딩에 빠지는 문제를 확인합니다.
{color:#4c9aff}New accounts get stuck in an infinite loading screen when the hideout server is unavailable.{color}

*Video(영상):*

* !251104_1736.mp4|width=2560,height=1440,alt="251104_1736.mp4"!


*Expected (기대 결과):*

* 하이드아웃 서버가 없을 때, 신규 계정은 로딩창에서 예외 처리
{color:#4c9aff}When the hideout server is unavailable, a new account must be handled with an appropriate exception on the loading screen{color}

*Note(참고):*

* 환경 정보 / {color:#4c9aff}Environment{color}
** 빌드/{color:#4c9aff}Build{color}: DailyQLOC_TEST_game_dev_AMS413131_r357221
** 백엔드/{color:#4c9aff}Backend{color}: backend/main/415.zip
** Chart Version 1.32.1
** https://awsdeploy.pbb-qa.pubg.io/environment/sel-game-dev2
* 스팀 연동 후, 신규 계정에서도 발생합니다.
{color:#4c9aff}Also reproduces with new accounts after linking with Steam.{color}

Priority: Medium
Components: Tech_Outgame
Issue Type: Bug
```
