# AI Business Intelligence Assistant

## 1. Project Overview

AI Business Intelligence Assistant is a web-based application that allows business users to ask questions about sales data using natural language.

The application uses a Large Language Model (LLM) to understand user questions, selects appropriate analytics functions, retrieves actual results from an SQLite database, and generates business-friendly explanations.

## 2. Features

- CSV data ingestion using Pandas.
- SQLite database for storing sales transactions.
- Data validation and handling of missing or invalid records.
- Natural-language question processing using Groq LLM.
- Dynamic sales analytics using predefined Python functions.
- Revenue analysis by product, region, category, sales channel, and month.
- Interactive charts using Chart.js.
- FastAPI backend.
- Automated tests using pytest.
- Markdown-formatted AI responses.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Data Processing | Pandas |
| Database | SQLite |
| Backend | FastAPI |
| AI Integration | Groq API |
| LLM Client | OpenAI Python SDK |
| Frontend | HTML, CSS, JavaScript |
| Charts | Chart.js |
| Testing | Pytest |

## 4. Architecture

1. The CSV file is loaded and validated using Pandas.
2. Valid transaction records are stored in SQLite.
3. The user enters a natural-language question through the web interface.
4. FastAPI receives the question.
5. Groq LLM interprets the question and selects an available analytics tool.
6. Python validates the tool arguments and executes predefined database queries.
7. The database results are returned to the LLM.
8. The LLM generates a natural-language explanation.
9. The frontend displays the answer and relevant charts.

Architecture:

                 User
                   |
                   v
           Frontend (HTML/CSS/JS)
                   |
                   v
            FastAPI Backend
                   |
                   v
              Groq LLM
           (Question Understanding)
                   |
                   v
           Analytics Tool Calling
                   |
                   v
           Python Validation
                   |
                   v
            SQLite Database
                   |
                   v
            Actual Query Results
                   |
                   v
              Groq LLM
           (Generate Explanation)
                   |
                   v
           Frontend (Answer + Chart)

## 5. Project Structure

```text
ai-bi-assistant/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── data_loader.py
│   ├── analytics.py
│   ├── ai_service.py
│
├── data/
│   └── sales1.csv
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── tests/
│   ├── __init__.py
│   └── test_analytics.py
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── AI_USAGE.md
```

## 6. Installation and Setup

### Prerequisites

- Python 3.10 or later
- Groq API key

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

Do not commit your API key to GitHub.

### Load the sales data

```bash
python -m app.data_loader
```

### Start the application

```bash
python -m uvicorn app.main:app --reload
```

Open:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

## 7. Testing

Run automated tests:

```bash
python -m pytest tests/ -v
```

The current test suite covers:

- Total revenue calculation.
- Highest revenue product.
- Region-wise sales.
- Monthly revenue.
- Invalid analytics metric.
- Empty question.
- Missing question.

Current result: 7 tests passed.

## 8. Data Quality

The application uses completed transactions with valid quantities, unit prices, and discount amounts for analytics.

Revenue is calculated as:

**Revenue = Quantity × Unit Price − Discount Amount**

Returned transactions and invalid records are excluded from analytical calculations.

## 9. Limitations

- The application can only answer questions supported by the available sales dataset.
- It cannot provide customer satisfaction, competitor, or marketing campaign insights because those fields are not present.
- AI responses depend on the LLM's interpretation of the user's question.
- Only predefined and validated analytics tools are allowed to access the database.

## 10. Future Improvements

- Add more analytics capabilities.
- Support conversational follow-up questions.
- Add date-range filtering.
- Improve visualization options.
- Add user authentication and role-based access.
- Expand automated API and AI integration testing.