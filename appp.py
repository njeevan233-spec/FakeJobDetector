
from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import fitz
import pytesseract
from PIL import Image
import io
import os

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB

# Tesseract OCR path for Windows
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Demo training dataset
training_texts = [
    "Pay registration fee to get guaranteed job immediately",
    "No interview required pay processing charges",
    "Work from home earn huge money pay security deposit",
    "Send bank account details and OTP for job verification",
    "Urgent hiring pay training fee before joining",
    "Guaranteed placement pay application fee",
    "You must purchase our course to get employment",
    "Earn 50000 per day without experience pay joining fee",

    "Software developer job with Python and Java experience",
    "Company hiring software engineer through official interview",
    "Full time data analyst role with SQL and Excel skills",
    "Submit resume through official company careers portal",
    "Experienced marketing manager required for office role",
    "Engineering internship with technical interview process",
    "Job vacancy with salary based on qualifications",
    "Recruitment through company website and HR interview"
]

training_labels = [
    1, 1, 1, 1, 1, 1, 1, 1,
    0, 0, 0, 0, 0, 0, 0, 0
]

model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2)
    )),
    ("classifier", LogisticRegression())
])

model.fit(training_texts, training_labels)

suspicious_phrases = [
    "registration fee",
    "processing fee",
    "security deposit",
    "pay to apply",
    "guaranteed job",
    "no interview",
    "earn money instantly",
    "pay training fee",
    "bank account details",
    "send otp",
    "whatsapp only",
    "buy our course",
    "urgent hiring",
    "limited seats",
    "payment required"
]


@app.route("/")
def home():
    return render_template("index.html")


# Upload and extract text from PDF or photo
@app.route("/extract", methods=["POST"])
def extract_text():
    if "file" not in request.files:
        return jsonify({"error": "No file selected"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Please select a file"}), 400

    filename = file.filename.lower()
    file_bytes = file.read()

    try:
        extracted_text = ""

        # PDF extraction
        if filename.endswith(".pdf"):
            pdf = fitz.open(stream=file_bytes, filetype="pdf")

            for page in pdf:
                text = page.get_text()
                extracted_text += text + "\n"

                # OCR for scanned PDF pages
                if not text.strip():
                    pix = page.get_pixmap(dpi=200)
                    image = Image.open(
                        io.BytesIO(pix.tobytes("png"))
                    )
                    extracted_text += (
                        pytesseract.image_to_string(image) + "\n"
                    )

            pdf.close()

        # Photo/image extraction
        elif filename.endswith((".png", ".jpg", ".jpeg")):
            image = Image.open(io.BytesIO(file_bytes))
            extracted_text = pytesseract.image_to_string(image)

        else:
            return jsonify({
                "error": "Upload only PDF, JPG, JPEG or PNG files."
            }), 400

        if not extracted_text.strip():
            return jsonify({
                "error": "No readable text found. Try a clearer image."
            }), 400

        return jsonify({
            "text": extracted_text.strip(),
            "filename": file.filename
        })

    except Exception as e:
        return jsonify({
            "error": "Could not read the file: " + str(e)
        }), 500


# Analyze the job posting
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    job_text = data.get("job_text", "").strip()

    if len(job_text) < 30:
        return jsonify({
            "error": "Please enter at least 30 characters."
        }), 400

    probabilities = model.predict_proba([job_text])[0]
    ml_fake_probability = probabilities[1] * 100

    text_lower = job_text.lower()

    found_phrases = [
        phrase for phrase in suspicious_phrases
        if phrase in text_lower
    ]

    rule_score = min(len(found_phrases) * 12, 60)

    final_score = min(
        (ml_fake_probability * 0.6) + (rule_score * 0.4),
        100
    )

    if final_score >= 65:
        status = "Likely Suspicious"
        color = "red"
    elif final_score >= 35:
        status = "Needs Verification"
        color = "orange"
    else:
        status = "Likely Legitimate"
        color = "green"

    suggestions = []

    if found_phrases:
        suggestions.append(
            "Suspicious phrases were detected in this job posting."
        )

    if "fee" in text_lower or "payment" in text_lower:
        suggestions.append(
            "Never pay money to secure a job or interview."
        )

    if "whatsapp" in text_lower:
        suggestions.append(
            "Verify the recruiter through the official company website."
        )

    if not suggestions:
        suggestions.append(
            "No major suspicious keywords detected. "
            "Verify the company independently."
        )

    return jsonify({
        "score": round(final_score, 2),
        "status": status,
        "color": color,
        "detected_phrases": found_phrases,
        "suggestions": suggestions,
        "word_count": len(job_text.split())
    })


if __name__ == "__main__":
    app.run(debug=True)
#python appp.py