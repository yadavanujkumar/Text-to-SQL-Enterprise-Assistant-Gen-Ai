# 🤖 Text-to-SQL Enterprise Assistant

A powerful AI-driven assistant that converts natural language questions into SQL queries and executes them against your database. Built with Streamlit, LangChain, and OpenAI's GPT-3.5-turbo.

## ✨ Features

- 💬 **Natural Language Interface**: Ask questions in plain English
- 🔍 **SQL Generation**: Automatically generates optimized SQL queries
- 📊 **Instant Results**: Executes queries and displays results in real-time
- 🎯 **Schema-Aware**: Understands your database structure automatically
- 🖥️ **User-Friendly UI**: Clean, intuitive Streamlit interface with chat-style interactions
- 🔒 **Transparent**: Shows both the generated SQL query and results for debugging

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yadavanujkumar/Text-to-SQL-Enterprise-Assistant-Gen-Ai.git
   cd Text-to-SQL-Enterprise-Assistant-Gen-Ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**
   
   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-actual-api-key-here
   ```

4. **Create the sample database**
   ```bash
   python setup_db.py
   ```
   
   This creates a `sales.db` SQLite database with sample data:
   - **products** table: 10 products with id, name, category, and price
   - **transactions** table: 20 sample transactions with product_id, date, quantity, and total_amount

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   
   The app will automatically open at `http://localhost:8501`

## 💡 Example Questions

Try asking questions like:

- "What are all the products in the Electronics category?"
- "Show me the total sales amount by category"
- "Which product generated the most revenue?"
- "How many transactions were made in the last 30 days?"
- "What is the average transaction amount?"
- "List the top 5 products by quantity sold"
- "What is the most expensive product?"
- "Show me all transactions for Laptops"

## 📁 Project Structure

```
.
├── app.py              # Main Streamlit application
├── setup_db.py         # Database setup script
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore         # Git ignore rules
├── README.md          # This file
└── sales.db           # SQLite database (generated)
```

## 🛠️ Technical Stack

- **UI Framework**: Streamlit
- **LLM Integration**: LangChain with OpenAI GPT-3.5-turbo
- **Database**: SQLite with SQLAlchemy
- **Key Libraries**:
  - `streamlit` - Web UI framework
  - `langchain` - LLM orchestration
  - `langchain-community` - Community integrations
  - `langchain-openai` - OpenAI integration
  - `sqlalchemy` - Database toolkit
  - `python-dotenv` - Environment variable management

## 🔧 Configuration

### Database

The default configuration uses SQLite with the `sales.db` file. To use a different database:

1. Modify the connection string in `app.py`:
   ```python
   db = SQLDatabase.from_uri("your-database-uri")
   ```

2. Supported databases: PostgreSQL, MySQL, SQLite, and more via SQLAlchemy

### LLM Model

To use a different OpenAI model, edit `app.py`:
```python
llm = ChatOpenAI(model="gpt-4", temperature=0)  # or gpt-4-turbo, etc.
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Powered by [OpenAI](https://openai.com/)
- UI with [Streamlit](https://streamlit.io/)

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Note**: This is a demonstration project with sample data. For production use, implement proper security measures, authentication, and database access controls.