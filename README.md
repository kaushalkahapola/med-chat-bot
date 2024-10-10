# Med Chat Bot

The Med Chat Bot is designed to provide helpful responses to medical questions using advanced AI models. It retrieves relevant medical information from documents and gives detailed answers to user queries.

## Features
- **Medical Inquiry Support**: Ask questions about medical conditions and get relevant answers based on stored data.
- **AI-Powered**: Uses Google Generative AI (Gemini) to generate responses, with the option to switch to LLaMA2 if desired.
- **Document Retrieval**: Relies on a Pinecone vector store to search through indexed documents for the best results.

## Setup Instructions

1. **API Keys**: 
   You’ll need to add your Pinecone and Google Generative AI API keys in the `.env` file before running the app.

2. **Document Data**: 
   Download medical PDFs (such as [this one](https://d1wqtxts1xzle7.cloudfront.net/52909865/Gale_Encyclopedia_of_Medicine_Vol._2_C-F-libre.pdf?1493660297=&response-content-disposition=attachment%3B+filename%3DThe_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf&Expires=1728452013&Signature=ZPfG21wh3c-KbklBOqCoHgucZNBpGgYHT2j1A4Chad89yGxiiTNDbIrVDO2GjaAHKWwHzRoPpBwj-kz6RbbYGdfOyfk3VODdHEydyig7EftDIvTj6qw904AZ4DOCKttmtTCuOTK0y5jVvwFu0hFRW7mwlNmTNd-ll4IzRrDpoWfLGVSYSGRpPJqYNQh2YIrgi6cq99Ly3m2GaoweS-fGKRoKjm5VcEQBU84EEq5M8PQe2jI9n8n2JGwwk79xdvjHotM75iMH3GlRUT7rupuoaVymOVq87U1-hxJx3LEe6GoBydRK-7sfrvjnUF1-4F7RR2r3AV99fYaQ0Eg6J9MXIA__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA)) and place them in the `data/` folder for indexing.

3. **Install Dependencies**: 
   Install the necessary Python libraries by running the following command:
   - `pip install -r requirements.txt`

4. **Index the Documents**:
   Before using the chatbot, you need to add the data to the vector store by running the `store_index.py` script.

5. **Running the Application**:
   Once everything is set up, start the chatbot by running `app.py`. The application will run locally, and you can interact with it through the browser.

## Optional: LLaMA2 Model
By default, the chatbot uses Google’s Gemini model for generating responses. If you prefer to use the LLaMA2 model, download it and place it in the `model/` folder. Uncomment the relevant parts of the code in `app.py` to switch to LLaMA2.

## Example Image
Here is an example of how the chatbot works:

![Example Image](https://github.com/user-attachments/assets/385c5627-390a-43c9-ae14-578fbf27cabe)

## How It Works
The chatbot processes user queries by retrieving relevant content from medical PDFs, using Pinecone for efficient searching, and generating answers with the selected AI model. It provides accurate and contextually relevant responses to medical-related questions.

## License
This project is licensed under the MIT License.
