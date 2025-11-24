"""
Text-to-SQL Assistant
A Streamlit application that converts natural language questions to SQL queries
and executes them against a SQLite database.
"""

import os
import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Text-to-SQL Assistant",
    page_icon="🤖",
    layout="wide"
)

# Title and description
st.title("🤖 Text-to-SQL Enterprise Assistant")
st.markdown("""
Ask questions about your sales data in plain English, and I'll generate and execute the SQL for you!
""")

# Check for OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ OPENAI_API_KEY not found! Please set it in your .env file or environment variables.")
    st.info("""
    **How to set up:**
    1. Create a `.env` file in the project directory
    2. Add your OpenAI API key: `OPENAI_API_KEY=your-api-key-here`
    3. Restart the application
    """)
    st.stop()

# Initialize database connection
@st.cache_resource
def init_database():
    """Initialize database connection"""
    try:
        db = SQLDatabase.from_uri("sqlite:///sales.db")
        return db
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        st.info("Make sure to run `python setup_db.py` first to create the database!")
        return None

db = init_database()

if db is None:
    st.stop()

# Initialize LLM
@st.cache_resource
def init_llm():
    """Initialize the language model"""
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

llm = init_llm()

# Create SQL query chain
@st.cache_resource
def init_chains(_db, _llm):
    """Initialize LangChain components"""
    # Chain to generate SQL query
    query_chain = create_sql_query_chain(_llm, _db)
    # Tool to execute SQL query
    execute_query = QuerySQLDataBaseTool(db=_db)
    return query_chain, execute_query

query_chain, execute_query = init_chains(db, llm)

# Sidebar with database info
with st.sidebar:
    st.header("📊 Database Schema")
    st.markdown("**Tables:**")
    st.markdown("- `products` (id, name, category, price)")
    st.markdown("- `transactions` (id, product_id, date, quantity, total_amount)")
    
    st.markdown("---")
    st.subheader("💡 Example Questions")
    st.markdown("""
    - What are all the products in the Electronics category?
    - Show me the total sales amount by category
    - Which product generated the most revenue?
    - How many transactions were made in the last 30 days?
    - What is the average transaction amount?
    - List the top 5 products by quantity sold
    """)
    
    st.markdown("---")
    st.caption("Powered by LangChain & OpenAI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sql" in message:
            st.code(message["sql"], language="sql")
        if "result" in message:
            st.success("**Result:**")
            st.write(message["result"])

# Chat input
if prompt := st.chat_input("Ask a question about your sales data..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Generating SQL query..."):
            try:
                # Generate SQL query
                sql_query = query_chain.invoke({"question": prompt})
                
                # Clean up the SQL query (remove markdown formatting if present)
                if sql_query.startswith("```sql"):
                    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
                elif sql_query.startswith("```"):
                    sql_query = sql_query.replace("```", "").strip()
                
                # Display the generated SQL
                st.markdown("**Generated SQL Query:**")
                st.code(sql_query, language="sql")
                
                # Execute the query
                with st.spinner("Executing query..."):
                    result = execute_query.invoke(sql_query)
                
                # Display the result
                st.success("**Result:**")
                st.write(result)
                
                # Save to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "I've generated and executed the SQL query for you:",
                    "sql": sql_query,
                    "result": result
                })
                
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <small>Text-to-SQL Assistant | Built with Streamlit, LangChain, and OpenAI</small>
</div>
""", unsafe_allow_html=True)
