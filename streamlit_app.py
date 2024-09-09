import thirdai
import streamlit as st
import nltk
import os
import time
from thirdai import licensing, neural_db as ndb
from dotenv import load_dotenv
import os
#nltk.download("punkt")
load_dotenv()
#if os.environ.get('third_ai') :
#    licensing.activate('third_ai')
if "THIRD_KEY" not in os.environ:
    licensing.activate(os.getenv('THIRD_AI_KEY'))
insertable_docs = [
]
db=ndb.NeuralDB()

pdf_folder_path = 'E:\\D drive\\Desktop\\sandhuruteam\\chatbot\\data' 
doc_files = [os.path.join(pdf_folder_path, file) for file in os.listdir(pdf_folder_path) if file.endswith('.pdf')]

# Process each file and insert it into the database
insertable_docs = []
for file in doc_files:
    doc = ndb.PDF(file)
    insertable_docs.append(doc)

# Insert documents into NeuralDB
db.insert(insertable_docs, train=False)


if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] =os.getenv('OPEN_AI_KEY')
    
import openai

# Make sure to set the API key correctly
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = os.getenv('OPEN_AI_KEY')

openai.api_key = os.getenv('OPENAI_API_KEY')  # Set API key for OpenAI

def generate_answers(query, references):
    context = "\n\n".join(references[:3])

    prompt = f"""
As an insurance expert of IndiaFirst Life Company, your task is to provide a direct and concise answer to the following question using the information from the referenced documents. Prioritize any numerical or quantitative data, and only explain key terms if they are essential to understanding the answer.

**Question:** {query}

**Context:** Review the content from the documents listed below:
{", ".join([f'Document {i+1}' for i in range(len(doc_files))])}

**Instructions:**
- greet the user only once and answer with little respect.
- Focus on delivering a clear, factual answer using the data from the {doc_files}.
- Carefully check if the {query} is about the age of entry or age of maturity and give answers accordingly.
- Provide the most accurate answer possible given the context.
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    return response.choices[0].message['content']

def generate_queries_chatgpt(original_query):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates multiple search queries based on a single input query."},
            {"role": "user", "content": f"Generate multiple search queries related to: {original_query}"},
            {"role": "user", "content": "OUTPUT (5 queries):"}
        ]
    )

    generated_queries = response.choices[0].message['content'].strip().split("\n")
    return generated_queries

def get_references(query):
    search_results = db.search(query, top_k=100)
    references = []
    for result in search_results:
        references.append(result.text)
    return references

def reciprocal_rank_fusion(reference_list, k=60):
    fused_scores = {}
        
    for i in reference_list:
        for rank, j in enumerate(i):
            if j not in fused_scores:
                fused_scores[j] = 0
            fused_scores[j] += 1 / ((rank+1) + k)
    
    reranked_results = {}
    sorted_fused_scores = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    for j, score in sorted_fused_scores:
        reranked_results[j] = score
    return reranked_results

def get_answer(query, r):
    return generate_answers(
        query=query,
        references=r
    )

st.set_page_config(page_title="Insurance Bot", page_icon=":robot_face:", layout="centered")

def main():
    st.title("Insurance Bot 🤖")
    st.write("Who summon me here!")
    st.write("Is it You, What you want to know?🧙‍♀️ ")

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    chat_placeholder = st.empty()

    display_chat_history(chat_placeholder)

    query = st.chat_input("Enter your question...", key="unique_query_input")

    if query:
        st.session_state["chat_history"].append({"user": query, "bot": "..."})

        display_chat_history(chat_placeholder)

        #with st.spinner("Bot is typing..."):
        query_list = generate_queries_chatgpt(query)
        reference_list = [get_references(q) for q in query_list]
        r = reciprocal_rank_fusion(reference_list)
        ranked_reference_list = list(r.keys())
        ans = get_answer(query, ranked_reference_list)

        st.session_state["chat_history"][-1]["bot"] = ans

        display_chat_history(chat_placeholder)

def display_chat_history(placeholder):
    with placeholder.container():
        for chat in st.session_state["chat_history"]:
            st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                    <div style="background-color: #e8f5e9; padding: 10px; border-radius: 5px; max-width: 60%;">
                        <strong>You:</strong> {chat['user']} <span style="font-size: 20px;">👤</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            if chat['bot']:
                st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                        <div style="background-color: #e0f7fa; padding: 10px; border-radius: 5px; max-width: 60%;">
                            <span style="font-size: 20px;">🤖</span> <strong>Bot:</strong> {chat['bot']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()




