import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


def load_case_text(text_path: Path) -> str:
    if not text_path.exists():
        raise FileNotFoundError(f"Text file not found: {text_path}")

    text = text_path.read_text(encoding="utf-8").strip()

    if not text:
        raise ValueError("The case report text file is empty.")

    return text


def build_prompt(case_text: str) -> str:
    return f"""
You are a medical information extraction assistant.

Your task is to extract structured medical entities from the following Chinese case report.

Important rules:
1. Return ONLY valid JSON.
2. Do not use Markdown code blocks.
3. Do not add explanations outside JSON.
4. Do not infer or fabricate information that is not explicitly stated in the case report.
5. If information is missing, use null or an empty list [].
6. Keep the extracted content in Chinese.
7. For key medical entities, preserve the original clinical wording as much as possible.

Please extract the following fields:

{{
  "patient_basic_info": {{
    "age": null,
    "sex": null,
    "admission_reason": null
  }},
  "chief_complaint": [],
  "main_symptoms": [],
  "past_medical_history": [],
  "diagnoses": [],
  "treatment_plan": [],
  "examination_findings": {{
    "physical_examination": [],
    "laboratory_tests": [],
    "imaging_examinations": []
  }},
  "clinical_outcome": null,
  "uncertain_or_missing_information": []
}}

Chinese case report text:
{case_text}
"""


def extract_entities_with_qwen(case_text: str) -> dict:
    load_dotenv()

    api_key = os.getenv("DASHSCOPE_API_KEY")

    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY is not set. Please check your .env file.")

    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    prompt = build_prompt(case_text)

    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {
                "role": "system",
                "content": "You are a careful medical information extraction assistant. You must output valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content

    try:
        result = json.loads(content)
    except json.JSONDecodeError as e:
        print("Raw model output:")
        print(content)
        raise ValueError("Failed to parse model output as JSON.") from e

    return result


def save_json(data: dict, output_path: Path) -> None:
    output_path.parent.mkdir(exist_ok=True)

    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def main():
    base_dir = Path(__file__).resolve().parent

    text_path = base_dir / "results" / "case_report_text.txt"
    output_path = base_dir / "results" / "case_entities.json"

    case_text = load_case_text(text_path)
    entities = extract_entities_with_qwen(case_text)
    save_json(entities, output_path)

    print("Medical entities extracted successfully.")
    print(f"Output file: {output_path}")


if __name__ == "__main__":
    main()