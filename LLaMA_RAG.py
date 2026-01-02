from huggingface_hub import hf_hub_download
from llama_cpp import Llama
import time
from pprint import pprint
import requests
from bs4 import BeautifulSoup

# 모델 다운로드
model_name_or_path = "heegyu/EEVE-Korean-Instruct-10.8B-v1.0-GGUF"
model_basename = "ggml-model-Q5_K_M.gguf"
model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)

# GPU 사용
lcpp_llm = Llama(
    model_path=model_path,
    n_threads=8,  # CPU cores
    n_batch=512,  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
    n_gpu_layers=43,  # Change this value based on your model and your GPU VRAM pool.
    n_ctx=4096,  # Context window
)

# 홈페이지에서 점심 메뉴 HTML 가져오기
url = "https://www.hanyang.ac.kr/web/www/re15"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# 메뉴 정보 추출
menu_elements = soup.find_all("h4", class_="d-title2")
menus = []

for menu_element in menu_elements:
    if "중식" in menu_element.text:
        menu_text = menu_element.find_next_sibling().text.strip()
        menus.append(menu_text)

print(menus)

# 점심 메뉴 문서화
menu_document = "\n".join(menus)

# 프롬프트 준비
prompt_template = "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions based on the provided context.\n\nContext: {context}\n\nHuman: {prompt}\nAssistant:"
prompt = prompt_template.format(context=menu_document, prompt="오늘의 점심 메뉴는 무엇이고 가격은 얼마인가요?")

start = time.time()
response = lcpp_llm(
    prompt=prompt,
    max_tokens=256,
    temperature=0.5,
    top_p=0.95,
    top_k=50,
    stop=['</s>'],  # Dynamic stopping when such token is detected.
    echo=True  # return the prompt
)
pprint(response)
print(time.time() - start)
