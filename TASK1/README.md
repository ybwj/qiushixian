# Task 1: Chinese Case Entity Extraction with Qwen-Plus API

## Objective

This task uses Python to call the Qwen-Plus API via Alibaba Cloud Model Studio and extracts structured medical entities from a Chinese case report.

## Workflow

1. Test Qwen-Plus API connectivity.
2. Extract raw text from the PDF case report.
3. Send the extracted case text to Qwen-Plus.
4. Extract key medical entities.
5. Save the result as a standardized JSON file.

## Files

- `test_qwen_api.py`: tests whether the Qwen-Plus API can be called successfully.
- `extract_pdf_text.py`: extracts raw text from the PDF file.
- `extract_case_entities.py`: calls Qwen-Plus API and extracts medical entities.
- `results/case_entities.json`: final structured extraction result.

## Extracted Entities

The JSON output includes:

- patient basic information
- chief complaint
- main symptoms
- past medical history
- diagnoses
- treatment plan
- examination findings
- clinical outcome
- uncertain or missing information

## Security Note

The API key is loaded from the local `.env` file using the environment variable `DASHSCOPE_API_KEY`. The `.env` file is excluded from GitHub.