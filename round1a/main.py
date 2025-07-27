import fitz  # PyMuPDF
import os
import json

# Set paths depending on environment
if os.path.exists("/app"):
    INPUT_DIR = "/app/input"
    OUTPUT_DIR = "/app/output"
else:
    INPUT_DIR = "input"
    OUTPUT_DIR = "output"

def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    text_blocks = []

    for page_number in range(len(doc)):
        page = doc[page_number]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["text"].strip():
                            text_blocks.append({
                                "text": span["text"].strip(),
                                "size": round(span["size"], 1),
                                "font": span["font"],
                                "bold": "bold" in span["font"].lower(),
                                "page": page_number + 1
                            })

    return classify(text_blocks)

def classify(spans):
    sizes = sorted(set(span["size"] for span in spans), reverse=True)
    if len(sizes) < 4:
        sizes += [0] * (4 - len(sizes))

    size_map = {
        sizes[0]: "title",
        sizes[1]: "H1",
        sizes[2]: "H2",
        sizes[3]: "H3"
    }

    output = {"title": "", "outline": []}
    seen = set()

    for span in spans:
        level = size_map.get(span["size"], None)
        text = span["text"].strip()
        text_lower = text.lower()

        # Title (only one)
        if level == "title" and not output["title"]:
            output["title"] = text
            continue

        # Filters for outline
        if level in ["H1", "H2", "H3"]:
            if not span["bold"]:
                continue
            if len(text.split()) > 6:
                continue
            if not any(c.isalpha() for c in text):
                continue
            if len(text) <= 2 and any(c.isdigit() for c in text):
                continue
            if text_lower in seen:
                continue
            if text_lower in {"overview", "march 2003", "version 1.0"}:
                continue

            output["outline"].append({
                "level": level,
                "text": text,
                "page": span["page"]
            })
            seen.add(text_lower)

    output["outline"].sort(key=lambda x: x["page"])
    return output

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            result = extract_headings(pdf_path)

            json_filename = filename.replace(".pdf", ".json").replace(".PDF", ".json")
            json_path = os.path.join(OUTPUT_DIR, json_filename)

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            print(f"\n✅ Output for {filename}:\n", json.dumps(result, indent=2))

if __name__ == "__main__":
    main()