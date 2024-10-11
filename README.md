# Med Chat Bot

The **Med Chat Bot** is designed to provide accurate and helpful responses to medical inquiries using advanced AI models and document retrieval systems. It leverages cutting-edge AI technologies to search through indexed medical documents and generate detailed answers based on the user's queries.

## Features
- **Medical Inquiry Support**: Ask questions about medical conditions, treatments, symptoms, or medications, and get relevant, data-driven responses based on stored documents.
- **AI-Powered Responses**: The chatbot is powered by Google Generative AI (**Gemini**) and can optionally use **LLaMA2** for generating responses. These advanced AI models ensure high-quality and accurate answers.
- **Document Retrieval**: Uses **Pinecone vector store** for fast and efficient search across indexed medical PDFs, ensuring that the most relevant information is retrieved.
- **Natural Language Processing**: Employs **LangChain** and **Hugging Face Sentence Transformers** for processing, understanding, and embedding medical texts to enhance the precision of document searches and queries.

## Setup Instructions

1. **API Keys**:
   Add your **Pinecone** and **Google Generative AI (Gemini)** API keys in the `.env` file before running the application.

2. **Document Data**:
   Download medical PDFs, such as [this one](https://staibabussalamsula.ac.id/wp-content/uploads/2024/06/The-Gale-Encyclopedia-of-Medicine-3rd-Edition-staibabussalamsula.ac_.id_.pdf), and place them in the `data/` folder. The system indexes the documents for future queries.

3. **Install Dependencies**:
   Install all required Python packages by running the following command:
   - `pip install -r requirements.txt`

4. **Index the Documents**:
   After adding the PDFs, index the documents using the `store_index.py` script to add them to the **Pinecone vector store**.

5. **Running the Application**:
   Start the chatbot by executing the `app.py` script. The application runs locally, and you can access it via your browser for interaction.

## Optional: LLaMA2 Model
The chatbot uses **Google’s Gemini** by default. To switch to **LLaMA2**, download the model and place it in the `model/` folder, then uncomment the relevant parts of the `app.py` code to enable LLaMA2 as the response generator.

## Example Image
Here's a preview of how the chatbot works:

![Example Image](https://github.com/user-attachments/assets/385c5627-390a-43c9-ae14-578fbf27cabe)

## How It Works
The chatbot processes user queries by:
1. Retrieving relevant content from indexed medical PDFs.
2. Using **Pinecone** to efficiently search for the most relevant documents.
3. Generating contextually accurate responses using either **Gemini** or **LLaMA2** models.

The document processing and search system is powered by **LangChain** and **Hugging Face Sentence Transformers**, ensuring high precision and relevance in its answers.

## Technologies Used
- **LangChain**: Helps build a robust and modular framework for document retrieval and query handling.
- **Hugging Face Sentence Transformers**: Used for text embedding to improve the accuracy of document searches and response generation.
- **Pinecone**: A vector database that allows for fast and scalable document retrieval.
- **Google Generative AI (Gemini)**: Provides powerful AI-driven responses to user queries.
- **LLaMA2 (Optional)**: An alternative AI model that can be used for generating responses.

## License
This project is licensed under the MIT License.
