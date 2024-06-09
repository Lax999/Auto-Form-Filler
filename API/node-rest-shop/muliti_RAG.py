from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate

import streamlit as st
import os
from dotenv import load_dotenv
from operator import itemgetter
from pathlib import Path
import pandas as pd
import numpy as np
from docx import Document

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

doc_path = Path('./docs')

# Cache the function to load and process PDF documents
# @st.cache(allow_output_mutation=True)
def load_and_process_pdfs(pdf_folder_path):
    documents = []
    for file in os.listdir(pdf_folder_path):
        if file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder_path, file)
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)
    return splits

# Cache the function to initialize the vector store with documents
# @st.cache(allow_output_mutation=True)
def initialize_vectorstore(splits):
    return FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings(api_key=OPENAI_API_KEY))


RAG_folder_path = "./RAG_database"
splits = load_and_process_pdfs(RAG_folder_path)
vectorstore = initialize_vectorstore(splits)

prompt_template = """You are an expert in carbon credit standards. You need to explain why/why not the project satisfy the criteria
given in the questions.  Given below is the context and question. Don't answer question outside the context provided. 
If one or more part of the question cannot be answered because of missing information, after answering the parts can be answered, 
list all the missing information, starting with "MISSING INFORMATION:". For the question/parts of the question that can be answered,
do not answer in bullet points, and include all relevant information that supports the answer. 
context = {context}
question = {question}
"""

prompt = ChatPromptTemplate.from_template(prompt_template)

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, api_key=OPENAI_API_KEY)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": vectorstore.as_retriever() | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

from VCS_form_questions import vcs_questions_list

data_path = Path('./datas')
df = pd.read_csv(data_path / 'VCS_project_data.csv',index_col='info')

missing_info = []

def get_missing_info(input_string):
    index = input_string.find('MISSING INFORMATION:')
    # check if info is missing
    if index != -1:
        return input_string[index + len('MISSING INFORMATION:'):]
    
for i in range(len(vcs_questions_list)):
    question = vcs_questions_list[i]
    # print(f"Question: {question}")
    ans = rag_chain.invoke(question)
    # print(f"Answer: {ans}")
    df.loc[i, 'answer'] = ans
    
    missing_info.append(get_missing_info(ans))

for i in missing_info:
    print(i)


def fill_form(template_path,output_path,data,project):
    doc = Document(template_path)
    for paragraph in doc.paragraphs:
        for i in range(len(vcs_questions_list)):
            if data.index[i] in paragraph.text:
                paragraph.text = paragraph.text.replace(data.index[i],data[project][i])
    doc.save(output_path)

template_path =  'auto-form-filling/VCS-template-empty.docx'
output_path = 'auto-form-filling/filled.docx'
data = df
answer = 'answer'


fill_form(template_path,output_path,data,answer)