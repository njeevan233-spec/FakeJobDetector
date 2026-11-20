# 🛡️ Fake Job Detector AI

An AI-powered web application that analyzes job postings to identify potential fake jobs, recruitment scams, and suspicious hiring practices. Users can paste job descriptions or upload PDF/image job advertisements for analysis.

## 🚀 Features

- **AI-Based Detection:** Uses Machine Learning to classify suspicious job postings.
- **PDF Upload:** Extracts text from PDF job advertisements.
- **Image Upload:** Reads job advertisements from JPG, JPEG, and PNG images using OCR.
- **Risk Score:** Provides a suspiciousness score for analyzed job descriptions.
- **Suspicious Phrase Detection:** Identifies red flags such as registration fees, security deposits, guaranteed jobs, and suspicious payment requests.
- **Recommendations:** Provides safety suggestions based on detected warning signs.
- **Interactive Web Interface:** Simple and responsive interface built using HTML, CSS, and JavaScript.

## 🛠️ Technologies Used

- Python
- Flask
- Scikit-learn
- TF-IDF
- Logistic Regression
- PyMuPDF
- Pytesseract OCR
- Pillow
- HTML
- CSS
- JavaScript

## 📂 Project Structure

```text
FakeJobDetector/
│
├── appp.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/FakeJobDetector.git
```

### 2. Navigate to the project directory

```bash
cd FakeJobDetector
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the application

```bash
python appp.py
```

### 6. Open in your browser

```text
http://127.0.0.1:5000
```

## 🔍 How It Works

1. The user pastes a job description or uploads a PDF/image.
2. Text is extracted from the uploaded document using PDF extraction or OCR.
3. TF-IDF converts the text into numerical features.
4. A Logistic Regression model predicts suspicious job content.
5. Rule-based detection identifies suspicious keywords and phrases.
6. The system generates a risk score and recommendations.

## 🚩 Examples of Suspicious Indicators

- Registration or processing fees
- Security deposits
- Guaranteed employment
- No interview required
- Unrealistic salary promises
- Requests for bank details or OTPs
- Suspicious WhatsApp-only recruitment

## ⚠️ Disclaimer

This project is an educational prototype. Its predictions are not guaranteed to be accurate and should not be considered proof that a job is fraudulent or legitimate.

Always independently verify recruiters, company websites, contact details, and job offers before sharing personal information or making payments.

## 👨‍💻 Author

Developed as a Python, Machine Learning, and Web Development project.

---

⭐ If you find this project interesting, consider giving it a star on GitHub!
