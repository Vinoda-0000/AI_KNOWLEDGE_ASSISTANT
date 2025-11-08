import streamlit as st
from workflow_graph import ingest_data
from db_module import fetch_all_texts, connect_db
from rag_module import load_faiss_index, retrieve
from llm_module import generate_response

st.set_page_config(page_title="AI Knowledge Assistant", layout="wide")
st.title("AI Knowledge Assistant")

# Step 0: Ingest data and prepare FAISS index
with st.spinner("Ingesting data and preparing documents..."):
    ingest_data()
    rows = fetch_all_texts()
    texts = [r[2] for r in rows]  # all document contents
    load_faiss_index(texts)
st.success("Data ready!")

# Step 1: Load FAQ
st.subheader("FAQs")
conn = connect_db()
cur = conn.cursor()
cur.execute("SELECT content FROM documents WHERE title='faq.txt'")
faq_data = cur.fetchone()
conn.close()
faq_text = faq_data[0] if faq_data else ""
st.markdown(faq_text if faq_text else "No FAQ found.")

# Step 2: Ask AI a question
query = st.text_input("Ask a question to the AI:")

if query:
    # Simple keyword-based handling for "manager list"
    if "manager" in query.lower() and ("list" in query.lower() or "names" in query.lower()):
        # Filter rows containing "Manager" in text
        manager_rows = [r[2] for r in rows if "manager" in r[2].lower()]
        if manager_rows:
            st.markdown("**Manager List:**")
            for i, m in enumerate(manager_rows, 1):
                st.markdown(f"{i}. {m}")
        else:
            st.warning("No managers found in the documents.")
    else:
        # Use RAG + AI for other queries
        with st.spinner("Searching for relevant documents..."):
            context_docs = retrieve(query, k=5)
            if not context_docs:
                st.warning("No relevant documents found. Generating AI answer without context...")
                answer = generate_response("", query)
            else:
                # Remove duplicates and trim
                unique_docs = list(dict.fromkeys(context_docs))
                trimmed_docs = [doc[:500] for doc in unique_docs]
                context = "\n".join(trimmed_docs)
                with st.spinner("Generating AI response..."):
                    answer = generate_response(context, query)
        st.markdown("**Bot:** " + answer)
