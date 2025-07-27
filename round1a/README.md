
# 📄 Adobe India Hackathon 2025 - Round 1A Submission

## 🚀 Challenge

Extract the **document title** and structured **semantic heading outline (H1, H2, H3)** from PDF files using text properties like font size and boldness.

---

## 🧠 Approach

- Used **PyMuPDF (fitz)** to parse PDF documents
- Extracted all text spans with font size, font name, boldness, and page info
- Classified headings based on **relative font size ranking**:
  - Largest → `title`
  - Next sizes → `H1`, `H2`, `H3`
- Skipped long paragraph-style spans (more than 6 words) to avoid false positives
- Generated structured JSON with heading levels and page numbers

---

## 📂 Folder Structure

adobe-hackathon/

├── main.py           # Python script for heading extraction

├── Dockerfile        # Docker build file

├── README.md         # This documentation

├── input/            # Folder for input PDF files

│   └── sample.pdf

├── output/           # Folder for output JSON files

│   └── sample.json

---

## ⚙️ How to Run the Project

### 🛠 1. Build Docker Image

```bash
docker build --platform linux/amd64 -t pdf-outliner:latest .
```
🚀 2. Run Docker Container
```bash
docker run --rm \
  -v "$(pwd)/input":/app/input \
  -v "$(pwd)/output":/app/output \
  pdf-outliner:latest
```
✅ Output will be printed in the terminal and saved to `/app/output/` inside the container.

---

## 📥 Input Format

Place one or more `.pdf` files in the `input/` folder:

```
input/
└── sample.pdf
```

---

## 📤 Output Format

For each `.pdf`, a `.json` file is generated:

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "1. Introduction", "page": 1 },
    { "level": "H2", "text": "1.1 What is AI?", "page": 1 },
    { "level": "H3", "text": "1.1.1 History of AI", "page": 1 }
  ]
}
```

---

## 📊 Sample Output Preview

Here’s an example of actual output:

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "1. Introduction", "page": 1 },
    { "level": "H3", "text": "This section introduces the basics of Artificial Intelligence...", "page": 1 },
    { "level": "H2", "text": "1.1 What is AI?", "page": 1 },
    { "level": "H3", "text": "1.1.1 History of AI", "page": 1 },
    { "level": "H3", "text": "AI has a rich history from symbolic reasoning to deep learning...", "page": 1 }
  ]
}
```
---

## ✅ Constraints Met

⏱ Executes within 10 seconds

📦 Docker image under 200MB

❌ No internet required during runtime

🐳 Fully compatible with --platform=linux/amd64

🧠 Skips paragraphs and detects true headings only

🧼 Handles multiple pages and inconsistent font styles
 
---
## 🛡️ Error Handling & Edge Cases

- Skips blank or non-text PDF pages

- Ignores overly long text spans (likely paragraphs)

- Gracefully handles PDFs with unexpected or inconsistent font usage


---
## 🧪 Tested With

✔️ Python 3.10

✔️ Docker 24+

✔️ GitHub Codespaces (Ubuntu Linux)

---

## ⏭️ Future Work (Round 1B Goals)

- Connect similar sections across multiple documents

- Build a cross-document semantic map

- Enable visual navigation of outlines and content flow

---

## 👥 Team Members

👤 Gurrala Sindhuja (Team Lead)

👤 Valapala Indhuja

---

## ✅ Status
🎉 Fully implemented and tested using Docker.
This solution meets all Round 1A constraints and is ready for submission to Adobe India Hackathon 2025.
