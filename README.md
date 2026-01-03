# 🛡️ AI 기반 자산 EoS 및 취약점 자동 모니터링 시스템
> **Project: Smart AI Security Monitor**

자산(서버, SW, DB)의 **기술지원 종료(EoS)** 현황을 자동 관리하고, 매일 쏟아지는 보안 뉴스 중 **내 자산에 치명적인 위협**만을 선별하여 알려주는 지능형 보안 비서 프로젝트입니다.

---

## 🎯 프로젝트 목적
- **자동화에 의한 효율성 증가:** 수동으로 관리되던 EoS 날짜 및 취약점 매칭의 자동화
- **Alert Fatigue 감소:** 단순 키워드 매칭이 아닌, **LLM(Gemini)의 문맥 분석**을 통해 실제 위험한 버전인지 판단 후 알림
- **하이브리드 엔진:** 정확성이 필요한 EoS는 **Rule-base(API)** 로, 문맥 판단이 필요한 취약점 분석은 **AI(LangChain)** 로 이원화

## 🛠️ 기술 스택 (Tech Stack)
- **Language:** Python 3.13
- **LLM Engine:** Google Gemini
- **Framework:** LangChain
- **Data Source:**
  - EoS Info: `endoflife.date` API
  - Threat Intel: KISA 보안공지 RSS (`feedparser`)
- **Data Processing:** Pandas, Regular Expressions

---

## 🚀 AI Engineering & Troubleshooting

프로젝트 개발 중 LLM(Gemini)을 연동하며 발생한 주요 이슈와 해결 과정을 정리

### 1. API Rate Limit 해결을 위한 배치 처리 (Batch Processing) 전환
- **문제 상황 (Problem):**
  - 초기에는 수집된 뉴스 10건을 `for` 반복문으로 하나씩 AI에게 보내서 분석함.
  - 이 방식은 뉴스 개수만큼 API를 호출하게 되어, `429 RESOURCE_EXHAUSTED` (Quota Exceeded) 에러가 빈번하게 발생하고 분석 속도가 느림.

  - **해결책 (Solution):**
  - 개별 호출 대신, 수집된 모든 뉴스를 하나의 거대한 텍스트 블록(Context)으로 합침.
  - 모든 뉴스를 분석하도록 구조를 변경하여 API 호출 횟수를 **N회 → 1회**로 줄임.
  - 정확도는 떨어질수 있으나, 하루 제한때문에 임시적으로..

### 2. RAG 품질 향상을 위한 데이터 전처리 (Data Preprocessing)
- **문제 상황 (Problem):**
  - RSS에서 가져온 데이터(`description`)에 HTML 태그(<`br`>, <`table`>, `&nbsp;`)와 불필요한 공백이 다수 포함됨.
  - 이는 LLM의 토큰(Token)을 낭비할 뿐만 아니라, AI가 텍스트의 맥락을 이해하는 데 방해가 됨

  - **해결책 (Solution):**
  - **정규표현식(Regex) 적용**: re 모듈을 사용하여 HTML 태그를 제거하고 순수 텍스트(Plain Text)만 추출하는 전처리 파이프라인 구축.
  - **데이터 소스 최적화**: 단순 공지사항 URL 대신, 상세 취약점 정보(CVE, 영향 버전 등)가 포함된 '보안 권고문' URL로 변경하여 AI 판단 정확도 향상.
