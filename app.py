"""
Text-to-SQL Assistant
A Streamlit application that converts natural language questions to SQL queries
and executes them against a SQLite database.
"""

import os
import re
import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
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

# SQL Query Generation Prompt
sql_prompt_template = """You are a SQL expert. Given an input question, create a syntactically correct SQLite query to run.

Use the following database schema:

{schema}

Question: {question}

Instructions:
- Only use tables and columns that exist in the schema
- Use SQLite syntax
- Return ONLY the SQL query, without any explanation or markdown formatting
- Do not include ```sql or ``` markers
- The query should be ready to execute

SQL Query:"""

sql_prompt = PromptTemplate(
    input_variables=["schema", "question"],
    template=sql_prompt_template
)

def extract_sql_query(text):
    """Extract SQL query from LLM response"""
    # Remove markdown code blocks
    text = re.sub(r'```sql\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    # Remove extra whitespace
    text = text.strip()
    return text

def generate_and_execute_query(question):
    """Generate SQL query and execute it"""
    try:
        # Get database schema
        schema = db.get_table_info()
        
        # Generate SQL query
        formatted_prompt = sql_prompt.format(schema=schema, question=question)
        response = llm.invoke(formatted_prompt)
        
        # Extract SQL query from response
        sql_query = extract_sql_query(response.content)
        
        # Execute query
        result = db.run(sql_query)
        
        return sql_query, result, None
    except Exception as e:
        return None, None, str(e)

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
    - What is the most expensive product?
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
        if "sql" in message and message["sql"]:
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
        with st.spinner("Generating and executing SQL query..."):
            sql_query, result, error = generate_and_execute_query(prompt)
            
            if error:
                st.error(f"Error: {error}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Error: {error}"
                })
            else:
                # Display the generated SQL
                st.markdown("**Generated SQL Query:**")
                st.code(sql_query, language="sql")
                
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

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <small>Text-to-SQL Assistant | Built with Streamlit, LangChain, and OpenAI</small>
</div>
""", unsafe_allow_html=True)
