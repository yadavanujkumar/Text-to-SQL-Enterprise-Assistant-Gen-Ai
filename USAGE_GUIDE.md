# Usage Guide - Text-to-SQL Enterprise Assistant

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yadavanujkumar/Text-to-SQL-Enterprise-Assistant-Gen-Ai.git
cd Text-to-SQL-Enterprise-Assistant-Gen-Ai

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup

```bash
# Create the database with sample data
python setup_db.py

# Configure your OpenAI API key
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Run

```bash
# Start the application
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Testing Without OpenAI API Key

You can verify the installation without an API key:

```bash
python test_app.py
```

This will test:
- All Python dependencies are installed correctly
- Database connection and queries work
- Prompt template is configured correctly

## Example Questions

Once you have your OpenAI API key configured, try these questions:

### Basic Queries
- "Show me all products"
- "What are the products in the Electronics category?"
- "List all furniture items"

### Aggregations
- "What is the total sales amount?"
- "Show me the total sales by category"
- "What is the average transaction amount?"

### Complex Queries
- "Which product generated the most revenue?"
- "List the top 5 products by quantity sold"
- "Show me all transactions for products over $100"
- "What is the most expensive product?"

### Time-Based Queries
- "How many transactions were made in the last 30 days?"
- "Show me all sales from November 2025"

## Understanding the Output

For each question, the assistant will show you:

1. **Generated SQL Query** - The exact SQL query that was generated from your natural language question
2. **Result** - The output from executing the query

This transparency helps you:
- Verify the query is correct
- Learn SQL by seeing examples
- Debug if results aren't what you expected

## Database Schema

### Products Table
- `id` (INTEGER) - Primary key
- `name` (TEXT) - Product name
- `category` (TEXT) - Product category
- `price` (REAL) - Product price

### Transactions Table
- `id` (INTEGER) - Primary key
- `product_id` (INTEGER) - Foreign key to products
- `date` (TEXT) - Transaction date (YYYY-MM-DD)
- `quantity` (INTEGER) - Quantity sold
- `total_amount` (REAL) - Total transaction amount

## Customization

### Using Your Own Database

To use your own database instead of the sample one:

1. Edit `app.py` and change the database URI:
   ```python
   db = SQLDatabase.from_uri("your-database-uri")
   ```

2. Supported databases:
   - SQLite: `sqlite:///path/to/db.db`
   - PostgreSQL: `postgresql://user:pass@host:port/dbname`
   - MySQL: `mysql://user:pass@host:port/dbname`

### Changing the LLM Model

To use a different OpenAI model, edit `app.py`:

```python
llm = ChatOpenAI(model="gpt-4", temperature=0)  # or gpt-4-turbo
```

Note: Different models have different costs and capabilities.

## Troubleshooting

### Issue: "OPENAI_API_KEY not found"
**Solution**: Create a `.env` file with your API key:
```
OPENAI_API_KEY=your-actual-api-key-here
```

### Issue: "Error connecting to database"
**Solution**: Run the database setup script:
```bash
python setup_db.py
```

### Issue: Import errors
**Solution**: Reinstall dependencies:
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Query returns unexpected results
**Check**: Look at the generated SQL query to see if it matches your intent. You can rephrase your question to be more specific.

## Tips for Best Results

1. **Be Specific**: More specific questions lead to better SQL queries
   - ❌ "Show me products"
   - ✅ "Show me all products in the Electronics category sorted by price"

2. **Use Table/Column Names**: Mention actual table or column names when relevant
   - ✅ "What's the total_amount of all transactions?"

3. **Ask for Aggregations Clearly**: Be explicit about what you want to calculate
   - ✅ "What is the sum of total_amount grouped by category?"

4. **One Question at a Time**: Break complex questions into simpler parts

## Security Notes

⚠️ **Important for Production Use**:

- Never commit your `.env` file or expose your API key
- Implement proper authentication for multi-user scenarios
- Use read-only database connections when possible
- Sanitize user inputs in production environments
- Set up proper rate limiting for API calls
- Monitor API usage to control costs

## Cost Considerations

- Each query makes an API call to OpenAI
- Costs vary by model (gpt-3.5-turbo is most economical)
- Monitor your OpenAI usage dashboard
- Consider caching frequent queries

## Support

For issues, questions, or contributions:
- GitHub Issues: [Report a bug or request a feature](https://github.com/yadavanujkumar/Text-to-SQL-Enterprise-Assistant-Gen-Ai/issues)

## License

This project is licensed under the MIT License - see LICENSE file for details.
