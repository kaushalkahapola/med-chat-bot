prompt_template="""
Use the following pieces of information to answer the user's question. Continue from where the previous context ends (if there is any) and give me the new answer also with the previous context, like a complete answer. Only add new information as needed to provide a complete and coherent response. 
If you do not know the answer, just say that you do not know. Do not make up the answer.

Previous context: {previous_context}
Current context: {current_context}
Question: {question}

Only return the helpful answer below and nothing else.

"""