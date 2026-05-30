# Medical LLM Newcomer Challenge

This repository contains the submission materials for the **Medical LLM Research Group Newcomer Challenge**. The project includes three tasks covering large language model API calling, Chinese medical case entity extraction, heart failure mortality prediction, LaTeX academic writing, AI-assisted figure generation, Markdown documentation, and GitHub-based project organization.

The project was completed with AI-assisted workflows using ChatGPT as a research copilot for code generation, debugging, paper revision, figure prompt design, and documentation writing. All AI-assisted conversations are recorded in [`AI_Chat_Records.md`](AI_Chat_Records.md).

---

## Repository Structure

```text
medical-llm-newcomer-challenge/
├── README.md
├── requirements.txt
├── AI_Chat_Records.md
├── .gitignore
│
├── TASK1/
│   ├── data/
│   │   └── case_report.pdf
│   ├── results/
│   │   ├── case_entities.json
│   │   └── case_report_text.txt
│   ├── .env.example
│   ├── requirements.txt
│   ├── extract_case_entities.py
│   ├── extract_pdf_text.py
│   ├── README.md
│   └── test_qwen_api.py
│
├── TASK2/
│   ├── analysis2.ipynb
│   ├── run_analysis.py
│   ├── feature_importance.png
│   ├── heart_failure_clinical_records_dataset.csv
│   ├── heart_failure_paper.pdf
│   ├── heart_failure_paper.tex
│   ├── heatmap.png
│   ├── model_performance.csv
│   ├── outlier_summary.csv
│   ├── roc_curve.png
│   └── workflow.png
│
└── TASK3/
    ├── Medical_AI_Beginner_Guide.md
    └── Medical_AI_Beginner_Guide.pdf
```

---

## Project Requirements Covered

This project addresses the required toolchain and research skills:

- Python programming
- LLM API calling
- Medical text information extraction
- JSON result generation
- Data preprocessing and exploratory data analysis
- Machine learning and deep learning model comparison
- Risk factor detection
- ROC-AUC based model evaluation
- LaTeX academic paper writing
- AI-assisted scientific figure generation
- Markdown guide writing
- GitHub project organization
- AI-assisted workflow documentation

---

# Task 1: Chinese Medical Case Entity Extraction with Qwen-Plus API

## Objective

Task 1 aimed to extract structured medical entities from a Chinese case report using a large language model API. The case report was provided as a PDF file.

The extraction focused on key medical entities, including:

- Patient basic information
- Chief complaint
- Main symptoms
- Past medical history
- Diagnoses
- Treatment plan
- Examination findings
- Clinical outcome
- Uncertain or missing information

---

## API Model

The selected API model was:

```text
Alibaba Cloud Model Studio Qwen-Plus
```

The model was called through Python using an OpenAI-compatible API client.

The API key was stored locally in a `.env` file using the environment variable:

```text
DASHSCOPE_API_KEY
```

The real `.env` file is excluded from GitHub by `.gitignore`. A template file `.env.example` is provided.

---

## Workflow

The Task 1 workflow was divided into three parts:

1. **API connectivity test**
   - Script: `test_qwen_api.py`
   - Purpose: verify that Python can successfully call Qwen-Plus API.

2. **PDF text extraction**
   - Script: `extract_pdf_text.py`
   - Input: `data/case_report.pdf`
   - Output: `results/case_report_text.txt`

3. **Medical entity extraction**
   - Script: `extract_case_entities.py`
   - Input: extracted case report text
   - Output: `results/case_entities.json`

---

## Main Outputs

| File | Description |
|---|---|
| `TASK1/test_qwen_api.py` | Minimal script for Qwen-Plus API connectivity testing |
| `TASK1/extract_pdf_text.py` | Python script for extracting text from the case report PDF |
| `TASK1/extract_case_entities.py` | Python script for LLM-based medical entity extraction |
| `TASK1/results/case_report_text.txt` | Extracted raw text from the case report |
| `TASK1/results/case_entities.json` | Standardized JSON output of extracted medical entities |

---

## Reproduction

Create a local `.env` file based on `.env.example`:

```env
DASHSCOPE_API_KEY=your_api_key_here
```

Then run:

```bash
cd TASK1
python test_qwen_api.py
python extract_pdf_text.py
python extract_case_entities.py
```

---

## Notes

The real API key is not included in this repository.

The extracted JSON result was manually checked against the original case report text to reduce hallucination and avoid unsupported medical information.

---

# Task 2: Heart Failure Mortality Prediction and LaTeX Paper

## Objective

Task 2 aimed to build and evaluate machine learning models for predicting mortality risk in patients with heart failure. The task also required writing a short English academic paper using LaTeX.

---

## Dataset

The dataset used was:

```text
heart_failure_clinical_records_dataset.csv
```

The dataset contains:

```text
299 patients
13 clinical variables
```

The target variable was:

```text
DEATH_EVENT
```

Clinical variables included age, anaemia, creatinine phosphokinase, diabetes, ejection fraction, high blood pressure, platelets, serum creatinine, serum sodium, sex, smoking, follow-up time, and death event.

---

## Data Analysis Workflow

The analysis workflow included:

1. Loading the clinical dataset
2. Descriptive statistical analysis
3. Missing value checking
4. Duplicate record checking
5. Outlier detection using the IQR method
6. Standardization for scale-sensitive models
7. Correlation heatmap analysis
8. Welch's t-test for risk factor screening
9. Random Forest feature importance analysis
10. Train-test split with stratification
11. Model training and comparison
12. Probability prediction for mortality risk
13. Model evaluation using multiple metrics
14. ROC curve and AUC comparison

---

## Models Compared

Four models were trained and evaluated:

| Model | Description |
|---|---|
| Logistic Regression | Traditional linear classifier with regularization |
| Random Forest | Tree-based ensemble model |
| XGBoost | Gradient boosting tree model |
| MLP | Simple multilayer perceptron neural network |

---

## Evaluation Metrics

The models were evaluated using:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

---

## Main Results

The model performance on the internal test set was:

| Model | Accuracy | Precision | Recall | F1 Score | AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.800 | 0.733 | 0.579 | 0.647 | 0.855 |
| Random Forest | 0.850 | 0.857 | 0.632 | 0.727 | 0.897 |
| XGBoost | 0.850 | 0.857 | 0.632 | 0.727 | 0.849 |
| MLP | 0.750 | 0.667 | 0.421 | 0.516 | 0.745 |

Random Forest achieved the best overall performance in the internal test set, with:

```text
Accuracy = 0.850
Precision = 0.857
Recall = 0.632
F1 Score = 0.727
AUC = 0.897
```

---

## Risk Factor Detection

The top three predictors identified by Random Forest feature importance were:

```text
follow-up time
serum creatinine
ejection fraction
```

Clinical interpretation:

- **Follow-up time** showed strong predictive value but should be interpreted cautiously because it may introduce information leakage in baseline-only prediction tasks.
- **Serum creatinine** reflects renal function and is clinically associated with prognosis in heart failure.
- **Ejection fraction** reflects cardiac systolic function and is a clinically meaningful indicator in heart failure patients.

---

## Figures Generated

The following figures were generated and used in the LaTeX paper:

| File | Description |
|---|---|
| `heatmap.png` | Correlation heatmap |
| `feature_importance.png` | Random Forest feature importance plot |
| `roc_curve.png` | ROC curves of evaluated models |
| `workflow.png` | AI-generated heart failure mortality prediction workflow figure |

---

## LaTeX Paper

The LaTeX paper includes:

- Title
- Abstract
- Introduction
- Methods
- Results
- Discussion
- Conclusion
- References
- Mathematical formula
- Model performance table
- ROC curve
- Feature importance figure
- AI workflow figure

Main paper files:

| File | Description |
|---|---|
| `heart_failure_paper.tex` | LaTeX source file |
| `heart_failure_paper.pdf` | Compiled PDF paper |

---

## Reproduction

**Option A — One-click reproduction (recommended):**

```bash
cd TASK2
pip install -r requirements.txt
python run_analysis.py
```

This single command regenerates all output files from the raw CSV.

**Option B — Step-by-step notebook:**

Open `TASK2/analysis2.ipynb` and run cells sequentially.

## Output File Mapping

Each output file is generated by a specific step in the analysis pipeline:

| Output File | Generated By | Step |
|---|---|---|
| `outlier_summary.csv` | `run_analysis.py` / Notebook cell 5 | Outlier detection (IQR) |
| `heatmap.png` | `run_analysis.py` / Notebook cell 17 | Correlation heatmap |
| `feature_importance.png` | `run_analysis.py` / Notebook cell 26 | Random Forest importance |
| `model_performance.csv` | `run_analysis.py` / Notebook cell 40 | Model evaluation |
| `roc_curve.png` | `run_analysis.py` / Notebook cell 42 | ROC curve plotting |

All model metrics in `model_performance.csv` match the values reported in `heart_failure_paper.tex`.
- risk factor analysis
- model training
- model evaluation
- generated figures
- result tables

---

## Notes

The analysis is exploratory and based on a relatively small public dataset. The results are not intended for direct clinical decision-making. Follow-up time was treated cautiously due to possible information leakage in baseline prediction settings.

---

# Task 3: Medical AI Beginner Guide

## Objective

Task 3 aimed to summarize the experience from Task 1 and Task 2 and write a beginner-friendly Markdown guide for future medical AI newcomers.

The target readers are medical students or junior researchers who have limited programming experience and are new to medical AI research.

---

## Guide Content

The guide covers three main parts:

### 1. Tool Section

Topics include:

- Python environment setup
- VS Code usage
- Terminal basics
- Python package installation
- Jupyter Notebook setup
- Domestic LLM API selection
- Qwen-Plus API usage
- API key management
- Efficient use of ChatGPT, Claude, and Gemini for programming

### 2. Practical Debugging Section

Topics include:

- How to write effective Debug prompts
- Why full error messages are important
- How to provide directory paths and commands to AI
- Real debugging cases from this project

Included real cases:

- `cd TASK1` path error
- `git add .gitignore` pathspec error

### 3. Advanced AI Figure Section

Topics include:

- How to use AI tools for scientific figure generation
- How to design a workflow figure prompt
- How to reduce AI-generated figure hallucinations
- Common hallucination types in AI-generated figures
- Which figures should be generated by Python and which can be assisted by AI

---

## Main Outputs

| File | Description |
|---|---|
| `TASK3/Medical_AI_Beginner_Guide.md` | Markdown source guide |
| `TASK3/Medical_AI_Beginner_Guide.pdf` | Exported PDF version of the guide |

---

# AI-Assisted Workflow

AI tools were used as research copilots throughout the project.

AI assistance was used for:

- API model selection
- Python code generation
- Code debugging
- Prompt optimization
- JSON structure checking
- Machine learning workflow design
- LaTeX paper drafting and revision
- AI figure prompt design
- Markdown guide writing
- Final project review

The project followed this principle:

> AI drafts, humans verify.

All important results, including JSON content, model metrics, figures, and paper statements, were manually checked before submission.

---

# AI Chat Records

The project required recording the complete AI-assisted conversation links.

All AI conversation records are organized in:

```text
AI_Chat_Records.md
```

This file includes categorized conversation links and short descriptions for:

- Task 1 API calling and medical entity extraction
- Task 2 data analysis, machine learning, LaTeX paper writing, and AI figure generation
- Task 3 Markdown beginner guide writing and project review

---

# Security and Privacy

This repository does not include real API keys or private credentials.

The following files are excluded by `.gitignore`:

```text
.env
.venv/
__pycache__/
.ipynb_checkpoints/
*.log
.DS_Store
```

For Task 1, users should create a local `.env` file:

```env
DASHSCOPE_API_KEY=your_api_key_here
```

Medical privacy considerations:

- No real private patient identifiers should be uploaded.
- API inputs should avoid identifiable personal health information.
- Public case reports and public datasets should be used only for research training and educational purposes.

---

# Final Submission Checklist

Before submission, the repository should contain:

```text
[ ] README.md in the repository root
[ ] AI_Chat_Records.md in the repository root
[ ] TASK1/ with Python source files and JSON output
[ ] TASK2/ with notebook, LaTeX source, figures, result files, and PDF paper
[ ] TASK3/ with Markdown guide and exported PDF
[ ] .gitignore excluding .env and temporary files
[ ] No real API key uploaded
[ ] AI conversation links added to AI_Chat_Records.md
[ ] GitHub repository set to public
```

---

# Disclaimer

This repository is for educational and research training purposes only.

The extracted medical entities, machine learning predictions, and generated figures are not intended for direct clinical decision-making.

All model outputs and AI-generated materials should be manually reviewed before use in academic or clinical contexts.