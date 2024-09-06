import thirdai
import streamlit as st
import nltk
import os
import time
from thirdai import licensing, neural_db as ndb
from dotenv import load_dotenv
#nltk.download("punkt")
load_dotenv()
#if os.environ.get('third_ai') :
#    licensing.activate('third_ai')
if "THIRD_KEY" not in os.environ:
    licensing.activate(os.getenv('THIRD_AI_KEY'))
insertable_docs = [
]
db=ndb.NeuralDB()
#streamlit run D.py
#doc_files = [r"D:\coding\Python\Policy\accidental-death-benefit-rider-brochure.pdf", r"D:\coding\Python\Policy\cash-back-plan-brochuree.pdf", r"D:\coding\Python\Policy\gold-brochure.pdf", r"D:\coding\Python\Policy\guaranteed-protection-plus-plan-brochure.pdf", r"D:\coding\Python\Policy\indiafirst-csc-shubhlabh-plan-brochure.pdf", r"D:\coding\Python\Policy\indiafirst-life-elite-term-plan-brochure.pdf", r"D:\coding\Python\Policy\indiafirst-life-guaranteed-benefit-plan-brochure1.pdf", r"D:\coding\Python\Policy\indiafirst-life-insurance-khata-plan-brochure.pdf", r"D:\coding\Python\Policy\indiafirst-life-little-champ-plan-brochure.pdf", r"D:\coding\Python\Policy\indiafirst-life-long-guaranteed-income-plan-brochure.pdf",r"D:\coding\Python\Policy\indiafirst-life-micro-bachat-plan-brochure.pdf", r"D:\coding\Python\Policy\indiafirst-life-plan-brochure.pdf", r"D:\coding\Python\Policy\indiafirst-life-radiance-smart-investment-plan-brochure.pdf", r"D:\coding\Python\Policy\indiafirst-life-saral-bachat-bima-A-brochure.pdf", r"D:\coding\Python\Policy\indiafirst-life-saral-jeevan-bima-brochure.pdf", r"D:\coding\Python\Policy\indiafirst-life-smart-pay-plan-brochure.pdf", r"D:\coding\Python\Policy\indiafirst-maha-jeevan-plan-brochure.pdf", r"D:\coding\Python\Policy\indiafirst-money-balance-plan-brochure.pdf", r"D:\coding\Python\Policy\indiafirst-pos-cash-back-plan-brochure.pdf", r"D:\coding\Python\Policy\indiafirst-simple-benefit-plan-brochure.pdf", r"D:\coding\Python\Policy\single-premium-brochure.pdf", r"D:\coding\Python\Policy\smart-save-plan-brochure.pdf", r"D:\coding\Python\Policy\tulip-brochure.pdf", r"D:\coding\Python\Policy\wealth-maximizer-brochure.pdf"] 
doc_files = [r"D:\rag\policies\Policies.pdf",r"D:\rag\policies\accidental-death-benefit-rider-brochure.pdf",r"D:\rag\policies\cash-back-plan-brochuree.pdf",r"D:\rag\policies\gold-brochure (1).pdf",r"D:\rag\policies\gold-brochure.pdf",r"D:\rag\policies\guaranteed-protection-plus-plan-brochure.pdf",r"D:\rag\policies\indiafirst-csc-shubhlabh-plan-brochure.pdf",r"D:\rag\policies\indiafirst-life-elite-term-plan-brochure.pdf",r"D:\rag\policies\indiafirst-life-guaranteed-benefit-plan-brochure1 (1).pdf",r"D:\rag\policies\indiafirst-life-guaranteed-benefit-plan-brochure1.pdf",r"D:\rag\policies\indiafirst-life-long-guaranteed-income-plan-brochure (1).pdf",r"D:\rag\policies\indiafirst-life-little-champ-plan-brochure.pdf",r"D:\rag\policies\indiafirst-life-insurance-khata-plan-brochure.pdf",r"D:\rag\policies\indiafirst-life-micro-bachat-plan-brochure.pdf",r"D:\rag\policies\indiafirst-life-micro-bachat-plan-brochure (1).pdf",r"D:\rag\policies\indiafirst-life-long-guaranteed-income-plan-brochure.pdf",r"D:\rag\policies\indiafirst-life-saral-bachat-bima-plan-brochure.pdf",r"D:\rag\policies\indiafirst-life-radiance-smart-investment-plan-brochure.pdf",r"D:\rag\policies\indiafirst-life-plan-brochure.pdf",r"D:\rag\policies\indiafirst-maha-jeevan-plan-brochure.pdf",r"D:\rag\policies\indiafirst-life-smart-pay-plan-brochure.pdf",r"D:\rag\policies\indiafirst-life-saral-jeevan-bima-brochure.pdf",r"D:\rag\policies\indiafirst-pos-cash-back-plan-brochure.pdf",r"D:\rag\policies\indiafirst-money-balance-plan-brochure.pdf",r"D:\rag\policies\indiafirst-maha-jeevan-plan-brochure.pdf",r"D:\rag\policies\single-premium-brochure.pdf",r"D:\rag\policies\single-premium-brochure (1).pdf",r"D:\rag\policies\indiafirst-simple-benefit-plan-brochure.pdf",r"D:\rag\policies\wealth-maximizer-brochure.pdf",r"D:\rag\policies\tulip-brochure.pdf",r"D:\rag\policies\smart-save-plan-brochure.pdf"] 

#doc_files = ["C:\\Users\\kamal\\OneDrive\\Desktop\\InsuranceBot\\Policies -  1.CSC Shubhlabh Plan.csv"]
for file in doc_files:
    doc = ndb.PDF(file)
    insertable_docs.append(doc)
db.insert(insertable_docs, train=False)

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] =os.getenv('OPEN_AI_KEY')

from openai import OpenAI
def generate_answers(query, references):
    openai_client = OpenAI()
    context = "\n\n".join(references[:3])

    #prompt = f"As an insurance expert, provide a direct and concise answer to the following question, focusing on any numerical or quantitative aspects first. Use the provided context and explain only the most relevant terms if necessary:\n\nQuestion: {query}\n\nContext: {context}\n\nPlease avoid asking for additional information unless absolutely necessary, and give a clear answer based on the available context."
    prompt = f"""
As an insurance expert of IndiaFirst Life Company , your task is to provide a direct and concise answer to the following question using the information from the referenced documents. Prioritize any numerical or quantitative data, and only explain key terms if they are essential to understanding the answer.

**Question:** {query}

**Context:** Review the content from the documents listed below:
{", ".join([f'Document {i+1}' for i in range(len(doc_files))])}

**Instructions:**
-greet the user only once and answer with little respect.
-You strictly don't have to greet the user every single time.
- Focus on delivering a clear, factual answer using the data from the {doc_files}.
-first read the {doc_files} completely and answer by analysing the questions carefully. 
- Highlight numerical values, percentages, or any other quantitative information first.
- Pay close attention to data presented in tabular columns within the {doc_files}. Extract and reference this tabular data accurately, as it often contains key details such as coverage amounts, premium rates, benefits, and terms. Use this structured information to support your answer, ensuring that any figures or statistics you mention are drawn directly from these tables.
- Try to provie the answers with similar words from the {doc_files}.
- Ensure that all money-related values are provided in Indian Rupees (INR).
- Only explain relevant terms if they are crucial for understanding the response.
- Avoid asking for additional information unless absolutely necessary.
- Respond based solely on the content of the provided {doc_files}.
-Do not answer 18 years for all the {query} asking about age .
- carefully check if the {query} is about age og entry or age og maturity and give anwsers accordingly.
- carefully check if the {query} is about Whole of Life Income Option   or Definite Income Option  and give anwsers accordingly.
Provide the most accurate answer possible given the context.
The example of how you should answer is given below :
question: What is the minimum age at entry for Definite Income Option in Long Guaranteed Income Plan  ?
answer :8 years  is the minimum age at entry for Definite Income Option 
question: What is the maximum age at entry for the Definite Income Option under this policy in Long Guaranteed Income Plan?
answer:  50 years is the maximum age at entry for the Definite Income Option under this policy"""

    messages = [{"role": "user", "content": prompt}]

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages, temperature=0
    )
    return response.choices[0].message.content

def generate_queries_chatgpt(original_query):
    openai_client = OpenAI()
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates multiple search queries based on a single input query."},
            {"role": "user", "content": f"Generate multiple search queries related to: {original_query}"},
            {"role": "user", "content": "OUTPUT (5 queries):"}
        ]
    )

    generated_queries = response.choices[0].message.content.strip().split("\n")
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




