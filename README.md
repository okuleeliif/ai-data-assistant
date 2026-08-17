# 🪩 AI Data Assistant

Upload your Excel or CSV file and talk to your data in natural language: filter tables, get summaries, or generate charts. Under the hood, Google Gemini turns your request into pandas code and runs it for you.

## Features

- 📁 **CSV / Excel upload** — supports `.csv` and `.xlsx` files
- 👾 **Instant preview** — shows the first 5 rows of the uploaded data
- 🧸 **Natural language queries** — understands requests like "Get records where city is Istanbul" or "Plot a bar chart of sales by category"
- 📊 **Automatic chart / table / summary generation** — returns a matplotlib chart, a filtered DataFrame, or a text summary depending on the request
- 🔁 **Self-correction** — if the generated code throws an error, the error is fed back to the model and the code is regenerated, up to 3 attempts

## How It Works

1. The uploaded file is loaded into a `pandas.DataFrame` (`df`) inside Streamlit.
2. The user's natural language request, along with the column names, is wrapped into a prompt and sent to Gemini (`gemini-3.5-flash-lite`).
3. The model generates only executable Python code (for a chart: `result = fig`; for a table: `result` is a DataFrame; for a summary: `result` is text/number).
4. The generated code runs in a controlled `exec` environment; if it errors out, the error message is sent back to the model and new code is generated (up to 3 attempts).
5. The result is displayed in the UI according to its type (DataFrame / chart / text).

## Setup

```bash
git clone https://github.com/okuleeliif/ai-data-assistant.git
cd ai-data-assistant
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### API Key

Create a `.env` file in the project root and add your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

> You can get an API key from [Google AI Studio](https://aistudio.google.com/).

## Usage

```bash
streamlit run main.py
```

Once the app opens in your browser:

1. Upload a CSV or Excel file
2. Check the data preview
3. Type your question or request, for example:
   - `Plot a bar chart of sales by category`
   - `Get records where city is Istanbul`
   - `Calculate the average salary`

## Tech Stack

- [Streamlit](https://streamlit.io/) — UI
- [pandas](https://pandas.pydata.org/) — data processing
- [Google Gemini API](https://ai.google.dev/) (`google-generativeai`) — natural language to code
- [matplotlib](https://matplotlib.org/) — chart generation
- [python-dotenv](https://pypi.org/project/python-dotenv/) — environment variable management
- [openpyxl](https://openpyxl.readthedocs.io/) — Excel file support

## Notes / Known Limitations

- Since generated code is run via `exec`, this is best suited for trusted/personal use; review code-execution safety before deploying it as a public-facing service.
- If the model misinterprets a request, or the code still fails after 3 attempts, an error message is shown instead.
- Each user currently needs their own Gemini API key (set via `.env`) to run the app.

## Roadmap

- [ ] Save query history
- [ ] Support multiple/merged data files
- [ ] Download results as CSV/Excel/PNG
