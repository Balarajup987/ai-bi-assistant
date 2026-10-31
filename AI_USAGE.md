# AI Usage Documentation

## 1. AI Tools Used

- **ChatGPT:** Used for understanding project requirements, planning the architecture, debugging errors, and improving code.
- **Groq API (GPT-OSS-120B):** Integrated into the application to interpret natural-language business questions and generate business-friendly explanations.

## 2. How AI Is Used in the Application

The application uses an LLM to understand questions such as:

- Which region generated the highest revenue?
- Which product has the highest sales?
- Show monthly revenue.

The LLM selects the appropriate analytics function and provides its arguments.

Python validates the requested function and arguments. The application then executes predefined SQL queries against the SQLite database.

The actual database results are sent back to the LLM to generate a natural-language explanation.

## 3. AI Safety and Validation

- The LLM cannot execute arbitrary SQL queries.
- Only predefined analytics functions are available.
- Allowed metrics, dimensions, filters, and sorting options are validated.
- SQL values are passed using parameterized queries.
- The application does not allow the LLM to modify or delete database records.
- Business explanations must be based on retrieved database results.

## 4. Limitations

- The application depends on the Groq API and an internet connection.
- Unsupported business questions may not be answered correctly.
- The LLM may misunderstand ambiguous questions.
- The current analytics functions support only the available dataset and predefined dimensions.
- AI-generated explanations should be checked against the returned figures.

## 5. Human Verification

The analytics calculations are performed using Python and SQLite rather than relying on the LLM to calculate business figures.

The results were verified using direct database queries and automated tests.

## 6. Problems Encountered and Debugging

### Problem 1: Data quality issues

The CSV contained missing unit prices and invalid quantity values.

**How I debugged it:**
- Used Pandas to inspect and identify invalid records.
- Converted numeric columns and dates into appropriate data types.
- Stored data-quality issues and excluded invalid transactions from analytics.

### Problem 2: LLM-generated business analysis

The LLM could misunderstand questions or potentially produce incorrect business figures.

**How I debugged it:**
- Implemented function/tool calling.
- Restricted the LLM to predefined analytics functions.
- Validated function arguments before execution.
- Used SQLite to calculate actual business figures instead of trusting the LLM to calculate them.

### Problem 3: Frontend response formatting

The frontend initially needed to display formatted AI-generated answers and charts.

**How I debugged it:**
- Used Marked.js to render Markdown.
- Used DOMPurify to sanitize generated HTML.
- Used Chart.js to visualize structured analytics results.

## 7. Improvements With Another Day of Work

If I had another day, I would:

1. Support more complex business questions, including month-to-month comparisons and revenue growth.
2. Improve LLM question interpretation and handling of ambiguous questions.
3. Add more automated tests, including API integration and error-handling tests.
4. Improve the frontend with filters, better visualizations, and downloadable reports.
5. Add more detailed data-quality reports and logging.