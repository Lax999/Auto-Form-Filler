# Carbon Credit Standards Project

## Overview
This project is a tool for automating the evaluation of carbon credit standards using natural language processing and machine learning models. It processes PDF documents, initializes a vector store for efficient retrieval, and uses a language model to answer questions based on the context provided in the documents. The tool can also fill out forms with the evaluated data. Additionally, it includes a server for uploading PDFs and processing them via a Python script.

## Features
- **Load and process PDF documents**: Extract text from PDF documents and split it into manageable chunks.
- **Initialize vector store**: Create a vector store for efficient document retrieval.
- **Question answering**: Use a language model to answer questions based on the provided context.
- **Form filling**: Automatically fill out forms based on the evaluated data.
- **PDF upload and processing**: Upload PDFs to be processed and receive the results.

## Requirements
- Python 3.7 or higher
- Node.js and npm
- Streamlit
- Langchain
- OpenAI
- Pandas
- NumPy
- python-docx
- dotenv
- Express
- Multer
- CORS

## Installation
1. Clone the repository to your local machine:
   ```sh
   git clone https://github.com/yourusername/carbon-credit-standards.git
   ```
2. Navigate to the project directory:
   ```sh
   cd carbon-credit-standards
   ```
3. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```
4. Install the required Node.js packages:
   ```sh
   cd server
   npm install
   ```
5. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

## How to Run
1. Start the Streamlit application:
   ```sh
   streamlit run app.py
   ```
2. Start the server:
   ```sh
   node server.js
   ```

## Code Structure

### main.py
This is the main script that loads and processes PDF documents, initializes the vector store, and sets up the question-answering pipeline.

#### Key Functions:
- **load_and_process_pdfs(pdf_folder_path)**: Loads and processes PDF documents from the specified folder.
- **initialize_vectorstore(splits)**: Initializes a vector store with the processed document splits.
- **format_docs(docs)**: Formats documents for input into the language model.
- **get_missing_info(input_string)**: Extracts missing information from the model's output.
- **fill_form(template_path, output_path, data, project)**: Fills out a form template with the provided data.

### VCS_form_questions.py
This file contains the list of questions related to VCS (Verified Carbon Standard) project data.

### app.py
This is the Streamlit application script to provide a web interface for interacting with the tool.

### server.js
This file contains the server setup using Express.js. It handles PDF file uploads and processes them with a Python script.

#### Key Endpoints:
- **POST /upload**: Endpoint to upload a PDF file and process it using a Python script.

### Environment Variables
- **OPENAI_API_KEY**: Your OpenAI API key for accessing the language model.

## Usage
1. **Load and process PDF documents**: Place your PDF documents in the `./RAG_database` directory. The script will automatically process these documents.
2. **Initialize vector store**: The vector store is initialized with the processed document splits for efficient retrieval.
3. **Ask questions**: Use the provided interface to input questions about the carbon credit standards. The model will retrieve relevant context from the documents and provide answers.
4. **Fill forms**: The script can automatically fill out forms using the evaluated data.
5. **Upload PDFs**: Use the server endpoint to upload PDFs and process them. The processed results will be sent back for download.


Feel free to add the optional sections if you have a license, contact information, or acknowledgments. This will provide more information and completeness to your README file.
