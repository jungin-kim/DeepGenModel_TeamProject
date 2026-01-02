# 🍽️ AI 한양대 점심 메뉴 안내 (DeepGenModel Team Project)

> **2024년 1학기 딥생성모델 과목 팀 프로젝트** > LLM(거대언어모델)을 활용한 한양대학교 오늘 점심 메뉴 안내 서비스

## 📖 프로젝트 개요

이 프로젝트는 학교 홈페이지에 게시된 식단 정보를 실시간으로 파싱하여, 생성형 AI 모델이 이를 기반으로 사용자의 질문("오늘 점심 메뉴가 뭐야?")에 대해 자연스럽게 답변해 주는 프로그램입니다.

단순한 규칙 기반의 답변이 아니라, **EEVE-Korean** LLM 모델을 사용하여 사람과 대화하듯 친절하고 상세하게 메뉴 정보를 안내합니다.

## 👥 팀원 및 역할 (Team Members)

* **김정인**: 기획 및 모델 파이프라인 설계
* **조민호**: 개발 주도

## 🛠️ 기술 스택 (Tech Stack)

* **Language**: Python 3.8+
* **LLM Inference**: [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) (GGUF 포맷 실행)
* **Web Crawling**: BeautifulSoup4, Requests
* **Model**: [heegyu/EEVE-Korean-Instruct-10.8B-v1.0-GGUF](https://huggingface.co/heegyu/EEVE-Korean-Instruct-10.8B-v1.0-GGUF) (Q5_K_M 양자화 버전)

## ⚙️ 작동 원리 (Workflow)

이 프로그램은 **RAG (Retrieval-Augmented Generation)** 의 기초적인 방식을 사용하여 최신 정보를 반영합니다.

1.  **모델 로드 (Model Loading)**
    * Hugging Face Hub에서 `EEVE-Korean-Instruct-10.8B` 모델의 양자화된 버전(`ggml-model-Q5_K_M.gguf`)을 다운로드하고 로드합니다.
    * GPU 가속(`n_gpu_layers=43`)을 사용하여 추론 속도를 높입니다.

2.  **데이터 수집 (Data Crawling)**
    * 한양대학교 생활관 식단 페이지(`https://www.hanyang.ac.kr/web/www/re15`)에 요청을 보냅니다.
    * `BeautifulSoup`을 이용해 HTML을 파싱하고, `h4` 태그의 클래스가 `d-title2`인 요소 중 **"중식"** 키워드가 포함된 메뉴 정보만 추출합니다.

3.  **프롬프트 구성 (Prompt Engineering)**
    * 수집한 메뉴 텍스트를 LLM의 프롬프트(Context)에 주입합니다.
    * `System Prompt` + `Retrieved Context(식단)` + `User Query` 형태로 프롬프트를 구성하여 환각(Hallucination)을 줄이고 사실에 기반한 답변을 유도합니다.

4.  **답변 생성 (Generation)**
    * 완성된 프롬프트를 `llama_cpp` 엔진에 전달하여 최종 답변을 생성합니다.

## 🚀 설치 및 실행 방법

### 환경 설정
1. 필요한 라이브러리를 설치합니다. (GPU 사용을 위해서는 llama-cpp-python의 추가 설정이 필요할 수 있습니다.)
  ```bash
  pip install llama-cpp-python huggingface_hub requests beautifulsoup4
```

2. LLaMA_RAG.py 또는 주피터 노트북 파일을 실행합니다.

  ```bash
  python LLaMA_RAG.py
```

## 📝 코드 분석 (Core Logic)
핵심 로직은 다음과 같이 구성되어 있습니다.
  ```bash
# 1. 웹페이지에서 '중식' 메뉴만 쏙 뽑아내는 크롤링 로직
menu_elements = soup.find_all("h4", class_="d-title2")
menus = []
for menu_element in menu_elements:
    if "중식" in menu_element.text:
        # 제목 태그 바로 다음 형제 요소(실제 메뉴 텍스트)를 가져옴
        menu_text = menu_element.find_next_sibling().text.strip()
        menus.append(menu_text)

# 2. LLM에게 정보를 주는 프롬프트 템플릿
prompt_template = """A chat between a curious user and an artificial intelligence assistant...
Context: {context} 
Human: {prompt}
Assistant:"""
```

## 📄 라이선스
이 프로젝트는 MIT License를 따릅니다.

Copyright (c) 2026 Jungin Kim
