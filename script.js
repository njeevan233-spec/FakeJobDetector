const fileInput = document.getElementById("fileInput");

fileInput.addEventListener("change", async function() {
    const file = fileInput.files[0];

    if (!file) return;

    const status = document.getElementById("uploadStatus");
    const error = document.getElementById("error");

    status.textContent = "Extracting text from file...";
    error.textContent = "";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("/extract", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Upload failed");
        }

        document.getElementById("jobText").value = data.text;

        status.textContent =
            "Successfully extracted text from " + data.filename;

    } catch (err) {
        status.textContent = "";
        error.textContent = err.message;
    }
});


async function analyzeJob() {
    const jobText = document.getElementById("jobText").value.trim();
    const button = document.getElementById("analyzeBtn");
    const loading = document.getElementById("loading");
    const error = document.getElementById("error");
    const result = document.getElementById("result");

    error.textContent = "";
    result.classList.add("hidden");

    if (jobText.length < 30) {
        error.textContent = "Enter at least 30 characters.";
        return;
    }

    button.disabled = true;
    loading.classList.remove("hidden");
    button.textContent = "Analyzing...";

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                job_text: jobText
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Analysis failed");
        }

        document.getElementById("score").textContent =
            data.score + "%";

        document.getElementById("score").className =
            data.color;

        document.getElementById("status").textContent =
            data.status;

        const phrases = document.getElementById("phrases");
        phrases.innerHTML = "";

        if (data.detected_phrases.length === 0) {
            phrases.innerHTML =
                '<p class="safe">No suspicious phrases detected.</p>';
        } else {
            data.detected_phrases.forEach(phrase => {
                const span = document.createElement("span");
                span.className = "phrase";
                span.textContent = phrase;
                phrases.appendChild(span);
            });
        }

        const suggestions =
            document.getElementById("suggestions");

        suggestions.innerHTML = "";

        data.suggestions.forEach(item => {
            const li = document.createElement("li");
            li.textContent = item;
            suggestions.appendChild(li);
        });

        document.getElementById("wordCount").textContent =
            "Words analyzed: " + data.word_count;

        result.classList.remove("hidden");

    } catch (err) {
        error.textContent = err.message;

    } finally {
        button.disabled = false;
        button.textContent = "Analyze Job";
        loading.classList.add("hidden");
    }
}