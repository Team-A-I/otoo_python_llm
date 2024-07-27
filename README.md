### 설치 및 실행
의존성 설치
```
pip install --no-cache-dir -r requirements.txt
```

필요한 파일
```
#.env
OPENAI_API_KEY=
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
```

실행
```
uvicorn main:app --reload --port 8001
```

### 프로젝트 구조
C:.<br/>
├───.github<br/>
│   ├───ISSUE_TEMPLATE<br/>
│   └───workflows<br/>
├───.idea<br/>
├───app<br/>
│   ├───api<br/>
│   │   └───__pycache__<br/>
│   ├───db<br/>
│   │   └───__pycache__<br/>
│   ├───models<br/>
│   │   └───__pycache__<br/>
│   ├───modules<br/>
│   │   └───__pycache__<br/>
│   ├───prompts<br/>
│   │   └───__pycache__<br/>
│   └───__pycache__<br/>
└───__pycache__<br/>


### 주요기능 및 예제

1. **EmotionReportModel**: 다양한 감정 상태를 분석하여 보고서를 생성합니다.
2. **QnaModel**: 사용자 질문에 대한 답변을 제공하고 MongoDB에서 관련 데이터를 검색합니다.
3. **QnAEditorModel**: Q&A 데이터를 수정하고 FAISS 인덱스를 업데이트합니다.
4. **ChatbotModel**: 주어진 대화 모드에 따라 채팅 봇 응답을 생성합니다.
5. **AnalysisModel**: 대화 내용을 분석하여 갈등, 사랑, 우정 등의 상황을 파악합니다.
6. **OcrModel**: 이미지에서 텍스트를 추출하고 분석합니다.
7. **STTModel**: 음성 텍스트 변환(STT) 결과를 분석하여 대화 상황을 평가합니다.
8. **ImageProcessor**: 이미지의 텍스트 영역을 추출하고 OCR을 통해 텍스트를 인식합니다.


#### EmotionReportModel

##### 설명
EmotionReportModel은 사용자의 감정 상태를 분석하여 보고서를 생성합니다.<br/> 이 모델은 OpenAI의 GPT-4 모델을 사용하여 텍스트 데이터를 처리하고 감정 분석 결과를 도출합니다.

##### 예제코드
```
emotion_report_model = EmotionReportModel(api_key=api_key)

messages_request = {
    "messages": [
        {"role": "user", "content": "I am feeling very stressed and anxious."}
    ]
}

response = await emotion_report_model.generate_messages_response(messages_request)
print(response)

```

#### QnaModel

##### 설명
QnaModel은 MongoDB에서 질문과 관련된 데이터를 검색하고, GPT-4 모델을 사용하여 답변을 생성합니다.<br/> 이 모델은 MongoDB와 FAISS 인덱스를 사용하여 효율적인 데이터 검색을 제공합니다.

##### 예제코드
```
qna_model = QnaModel(api_key=api_key)

messages_request = {
    "messages": [
        {"role": "user", "content": "What is the capital of France?"}
    ]
}

response = await qna_model.generate_qna_response(messages_request)
print(response)

```

#### QnAEditorModel

##### 설명
QnAEditorModel은 Q&A 데이터를 수정하고 MongoDB에 저장된 데이터를 업데이트합니다.<br/> 이 모델은 텍스트 데이터를 분할하고 임베딩을 생성하여 FAISS 인덱스를 업데이트합니다.

##### 예제코드
```
qna_editor_model = QnAEditorModel(api_key=api_key)

messages_request = "New Q&A data to be indexed in the database."

response = await qna_editor_model.generate_qna_edit_response(messages_request)
print(response)
```

#### ChatbotModel

##### 설명
ChatbotModel은 사용자가 선택한 대화 모드에 따라 채팅 봇 응답을 생성합니다. <br/> 기본 모드와 모드 2가 있으며, 각 모드는 서로 다른 프롬프트를 사용하여 응답을 생성합니다.
##### 예제코드
```
chatbot_model = ChatbotModel(api_key=api_key)

mode_request = {"mode": "2"}
recent_messages_request = {
    "RecentMessages": [
        "user : Hello, how are you?",
        "assistant : I am fine, thank you! How can I assist you today?"
    ]
}

response = await chatbot_model.generate_chat_response(mode_request, recent_messages_request)
print(response)

```
#### AnalysisModel

##### 설명
AnalysisModel은 대화 내용을 분석하여 갈등, 사랑, 우정 등의 상황을 파악합니다. <br/> 텍스트를 전처리하고 지정된 분석 유형에 따라 분석 결과를 생성합니다.

##### 예제코드
```
analysis_model = AnalysisModel(api_key=api_key)

text = "I feel like there is a lot of tension between us lately."
analysis_type = "conflict"

response = await analysis_model.analyze(text, analysis_type)
print(response)

```

#### OcrModel

##### 설명
OcrModel은 이미지에서 텍스트를 추출하고 분석합니다.  <br/> 이 모델은 OpenAI의 GPT-4 모델과 PaddleOCR을 사용하여 이미지 내 텍스트를 인식하고, <br/>  분석 유형에 따라 결과를 제공합니다.

##### 예제코드

```
ocr_model = OcrModel(api_key=api_key)

files = [open('path/to/image1.png', 'rb'), open('path/to/image2.png', 'rb')]
analysis_type = "love"

response = await ocr_model.process_uploaded_files(files, analysis_type)
print(response)

```

#### STTModel

##### 설명
STTModel은 음성 텍스트 변환(STT) 결과를 분석하여 대화 상황을 평가합니다.<br/>  단일 화자와 다중 화자에 따라 다른 프롬프트를 사용하여 분석합니다.

##### 예제코드
```
stt_model = STTModel(api_key=api_key)

stt_response = STTResponse(
    id="12345",
    status="completed",
    results=STTResults(
        utterances=[
            Utterance(start_at=0, duration=5, spk=0, spk_type="user", msg="Hello, how can I help you?"),
            Utterance(start_at=6, duration=4, spk=1, spk_type="assistant", msg="I need some assistance with my account.")
        ],
        verified=[True, True]
    )
)

response = await stt_model.analyze_stt(stt_response)
print(response)

```

#### ImageProcessor

##### 설명
ImageProcessor는 이미지의 텍스트 영역을 추출하고 OCR을 통해 텍스트를 인식합니다.<br/> 대비를 조정하고 컨투어를 찾아 텍스트 영역을 식별합니다.
##### 예제코드
```
image_processor = ImageProcessor()

image_files = [open('path/to/image1.png', 'rb'), open('path/to/image2.png', 'rb')]

all_left_text, all_right_text = await image_processor.process_images(image_files)
print("Left Text:", all_left_text)
print("Right Text:", all_right_text)

```
