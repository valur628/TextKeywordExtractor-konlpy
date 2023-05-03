#Text Keyword Extractor
#텍스트 키워드 추출기

import json
import configparser
import random
import time
import datetime
from konlpy.tag import Okt
from collections import Counter

#측정용 시작 시간
timeStart = time.time()

#실시간으로 흐른 시간을 알려주는 타이머. true=긴 타이머, false=짧은 타이머
def timer_get(length):
    timer_second = time.time()-timeStart
    timer_long = str(datetime.timedelta(seconds=timer_second))
    if length:
        return timer_long
    else:
        timer_short = timer_long.split(".")[0]
        return timer_short

# 설정 파일을 읽어오는 함수
def read_config():
    print("\n sys: 소요 시간(" + timer_get(True) + ")")
    print("\n sys: 설정 파일 읽기\n")
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    return config['settings']

# 텍스트 파일을 읽어오는 함수
def read_txt_file(file_path):
    print("\n sys: 소요 시간(" + timer_get(True) + ")")
    print("\n sys: 텍스트 파일 읽기 시작")
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    print("\n sys: 텍스트 파일 읽기 완료\n")
    return text

# 텍스트를 문장 단위로 나누는 함수
def split_into_sentences(text):
    print("\n sys: 소요 시간(" + timer_get(True) + ")")
    print("\n sys: 텍스트 문장 단위로 나누기 시작")
    sentences = text.split('\n')
    print("\n sys: 텍스트 문장 단위로 나누기 완료\n")
    return sentences

# 문장들을 묶어 문단으로 만드는 함수
def group_sentences_into_paragraphs(sentences, min_sentences, max_sentences):
    print("\n sys: 소요 시간(" + timer_get(True) + ")")
    print("\n sys: 문단 만들기 시작")
    paragraphs = []
    i = 0
    while i < len(sentences):
        num_sentences = random.randint(min_sentences, max_sentences)
        paragraph = ' '.join(sentences[i:i+num_sentences]).strip()
        paragraphs.append(paragraph)
        i += num_sentences
    print("\n sys: 문단 만들기 종료\n")
    return paragraphs

# 텍스트에서 키워드를 추출하는 함수
def extract_keywords(text, num_keywords):
    print("\n sys: 키워드 추출 시작")
    okt = Okt()
    nouns = okt.nouns(text)
    count = Counter(nouns)
    keywords = count.most_common(num_keywords)
    keywords_str = ", ".join([str(keyword) for keyword in keywords])
    print("\n keywords: <[ " + keywords_str + " ]>")
    print("\n sys: 키워드 추출 종료\n")
    return [keyword[0] for keyword in keywords]


# 문단들을 JSONL 형식으로 변환하고 저장하는 함수
def convert_to_jsonl(paragraphs, num_keywords, output_path):
    print("\n sys: 소요 시간(" + timer_get(True) + ")")
    print("\n sys: JSONL 변환 및 저장 시작")
    with open(output_path, 'w', encoding='utf-8') as f:
        for paragraph in paragraphs:
            # 문단에서 키워드를 추출합니다.
            keywords = extract_keywords(paragraph, num_keywords)
            # 추출한 키워드를 공백으로 구분하여 연결합니다.
            prompt = ' '.join(keywords)
            # 문단의 앞뒤 공백을 제거합니다.
            completion = paragraph.strip()
            # JSONL 형식의 데이터를 만듭니다.
            data = {"prompt": prompt, "completion": completion}
            # JSONL 형식의 데이터를 파일에 저장합니다.
            f.write(json.dumps(data, ensure_ascii=False) + '\n')
    print("\n sys: JSONL 변환 및 저장 종료\n")

if __name__ == "__main__":
    print("\n sys: 프로그램 시작")
    settings = read_config()
    input_file_path = settings.get('input_file_path')
    output_file_path = settings.get('output_file_path')
    min_sentences = settings.getint('min_sentences')
    max_sentences = settings.getint('max_sentences')
    num_keywords = settings.getint('num_keywords')

    # 텍스트 파일을 읽어옵니다.
    text = read_txt_file(input_file_path)
    # 텍스트를 문장 단위로 나눕니다.
    sentences = split_into_sentences(text)
    # 문장들을 묶어 문단으로 만듭니다.
    paragraphs = group_sentences_into_paragraphs(sentences, min_sentences, max_sentences)
    # 문단들을 JSONL 형식으로 변환하고 저장합니다.
    convert_to_jsonl(paragraphs, num_keywords, output_file_path)
    
    print("\n\n sys: 종료 시간(" + timer_get(True) + ")")
    print("\n sys: 프로그램 종료")

