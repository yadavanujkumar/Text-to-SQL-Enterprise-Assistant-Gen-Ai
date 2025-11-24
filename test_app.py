#!/usr/bin/env python3
"""
Test script for validating the Text-to-SQL functionality
This script tests the core functionality without needing to run the full Streamlit app
"""

import os
import sys
from langchain_community.utilities import SQLDatabase

def test_database():
    """Test database connection and basic queries"""
    print("=" * 60)
    print("Testing Database Connection")
    print("=" * 60)
    
    try:
        db = SQLDatabase.from_uri("sqlite:///sales.db")
        print("✓ Database connection successful")
        
        # Test getting schema
        schema = db.get_table_info()
        print(f"✓ Schema retrieved ({len(schema)} characters)")
        print("\nDatabase Schema:")
        print(schema)
        
        # Test running queries
        print("\n" + "=" * 60)
        print("Testing SQL Queries")
        print("=" * 60)
        
        queries = [
            ("Count products", "SELECT COUNT(*) FROM products"),
            ("Count transactions", "SELECT COUNT(*) FROM transactions"),
            ("List categories", "SELECT DISTINCT category FROM products"),
            ("Total sales", "SELECT SUM(total_amount) FROM transactions"),
        ]
        
        for name, query in queries:
            try:
                result = db.run(query)
                print(f"\n✓ {name}")
                print(f"  SQL: {query}")
                print(f"  Result: {result}")
            except Exception as e:
                print(f"\n✗ {name} failed: {e}")
        
        return True
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_imports():
    """Test that all required imports work"""
    print("\n" + "=" * 60)
    print("Testing Imports")
    print("=" * 60)
    
    try:
        from langchain_community.utilities import SQLDatabase
        print("✓ SQLDatabase import successful")
        
        from langchain_openai import ChatOpenAI
        print("✓ ChatOpenAI import successful")
        
        from langchain_core.prompts import PromptTemplate
        print("✓ PromptTemplate import successful")
        
        import streamlit
        print("✓ Streamlit import successful")
        
        from dotenv import load_dotenv
        print("✓ python-dotenv import successful")
        
        return True
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False

def test_sql_generation():
    """Test SQL generation logic (without calling OpenAI API)"""
    print("\n" + "=" * 60)
    print("Testing SQL Generation Logic")
    print("=" * 60)
    
    try:
        db = SQLDatabase.from_uri("sqlite:///sales.db")
        schema = db.get_table_info()
        
        # Test the prompt template
        from langchain_core.prompts import PromptTemplate
        
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
        
        test_question = "What are all products in Electronics category?"
        formatted_prompt = sql_prompt.format(schema=schema, question=test_question)
        
        print("✓ Prompt template created successfully")
        print(f"✓ Formatted prompt length: {len(formatted_prompt)} characters")
        print("\nSample prompt (first 300 chars):")
        print(formatted_prompt[:300] + "...")
        
        return True
    except Exception as e:
        print(f"✗ SQL generation logic test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Text-to-SQL Assistant - Component Tests")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Database", test_database()))
    results.append(("SQL Generation", test_sql_generation()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n✓ All tests passed! The application is ready to use.")
        print("\nNext steps:")
        print("1. Set your OPENAI_API_KEY in a .env file")
        print("2. Run: streamlit run app.py")
        return 0
    else:
        print("\n✗ Some tests failed. Please fix the issues before running the application.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
