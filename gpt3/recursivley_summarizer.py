import openai
import os
from time import time,sleep
import textwrap
import re
from PyPDF2 import PdfReader
import docx

openai.api_key = "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"

def readdoc(file_url):
    doc = docx.Document('gpt3/'+file_url)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def readpdf(file_url):
    reader = PdfReader('gpt3/'+file_url)
    print(len(reader.pages))
    summarizeText = ''
    i = 0
    while i < len(reader.pages):
        page = reader.pages[i]
        text = page.extract_text()
        summarizeText += text
        i += 1
    return summarizeText

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def gpt3_completion(prompt, engine='text-babbage-001', temp=0.6, top_p=1.0, tokens=1000, freq_pen=0.25, pres_pen=0.0, stop=['<<END>>']):
    max_retry = 5
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            text = re.sub('\s+', ' ', text)
            filename = '%s_gpt3.txt' % time()
            with open('gpt3/gpt3_logs/%s' % filename, 'w') as outfile:
                outfile.write('PROMPT:\n\n' + prompt + '\n\n==========\n\nRESPONSE:\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)


def summarizer(file_url):
    print(file_url)
    ext = file_url[file_url.find(".")+1:]
    if ext == 'pdf':
        temp = readpdf(file_url)
    elif ext == 'doc' or ext == 'docx':
        temp = readdoc(file_url)
    else:
        return 'Whooop. This file type is not supported.'

    print('====temp',temp)
    # alltext = open_file('gpt3/'+file_url)
    # print(alltext)
    # temp = alltext
    
    while True:
        chunks = textwrap.wrap(temp, 2000)
        result = list()
        count = 0
        for chunk in chunks:
            count = count + 1
            prompt = open_file('gpt3/prompt.txt').replace('<<SUMMARY>>', chunk)
            prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
            summary = gpt3_completion(prompt)
            result.append(summary)
        temp = ''.join(result);
        if len(temp)<2000:
            break
    save_file(temp, 'gpt3/output_result_%s.txt' % time())  
    return temp