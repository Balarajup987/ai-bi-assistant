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