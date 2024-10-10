# src/prompt.py

prompt_template = """
Think as you're medical assistant. Use the following pieces of information to answer the user's question. Only add new information as needed to provide a complete and coherent response. 
If you do not know the answer, kindly let the user know.

Current context: {current_context}
Question: {question}

Ensure your response is helpful.
"""
