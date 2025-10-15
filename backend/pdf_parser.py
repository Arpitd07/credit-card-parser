# pdf_parser.py
import sys, json, re, pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import io

pdf_path = sys.argv[1]

BANK_PATTERNS = {
    "HDFC Bank": {
        "Last_4_digits": r"(?:XXXX|\*{4}|XXXX-)\s*(\d{4})",
        "Billing_cycle": r"Statement\s*Period\s*(?:[:\-]?\s*)?(\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4})\s*[-to–—]+\s*(\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4})",
        "Payment_due_date": r"Payment\s*Due\s*Date\s*(?:[:\-]?\s*)?(\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4})",
        "Total_outstanding_balance": r"Total\s*(?:Due|Dues|Amount\s*Due)\s*(?:[:\-]?\s*)?(?:INR|Rs\.|₹)?\s*([\d,]+\.\d{2})"
    },
    "ICICI Bank": {
        "Last_4_digits": r"(?:XXXX|\*{4}|XXXX-)\s*(\d{4})",
        "Billing_cycle": r"Statement\s*Period\s*[:\-]?\s*(\d{1,2}(?:/|-|\s)(?:\d{1,2}|\w{3})\s?\d{4})\s*[-to–—]+\s*(\d{1,2}(?:/|-|\s)(?:\d{1,2}|\w{3})\s?\d{4})",
        "Payment_due_date": r"Payment\s*Due\s*Date\s*[:\-]?\s*(\d{1,2}(?:/|-|\s)(?:\d{1,2}|\w{3})\s?\d{4})",
        "Total_outstanding_balance": r"Amount\s*Due\s*[:\-]?\s*(?:INR|₹)?\s*([\d,]+\.\d{2})"
    },
    "SBI Card": {
        "Last_4_digits": r"(?:XXXX|\*{4}|XXXX-)\s*(\d{4})",
        "Billing_cycle": r"Statement\s*Period\s*[:\-]?\s*(\d{1,2}(?:/|-|\s)(?:\d{1,2}|\w{3})\s?\d{4})\s*[-to–—]+\s*(\d{1,2}(?:/|-|\s)(?:\d{1,2}|\w{3})\s?\d{4})",
        "Payment_due_date": r"Due\s*Date\s*[:\-]?\s*(\d{1,2}(?:/|-|\s)(?:\d{1,2}|\w{3})\s?\d{4})",
        "Total_outstanding_balance": r"Total\s*Amount\s*Due\s*[:\-]?\s*(?:INR|₹)?\s*([\d,]+\.\d{2})"
    },
    "Axis Bank": {
        "Last_4_digits": r"(?:XXXX|\*{4}|XXXX-)\s*(\d{4})",
        "Billing_cycle": r"Statement\s*Period\s*[:\-]?\s*(\d{1,2}(?:/|-|\s)(?:\d{1,2}|\w{3})\s?\d{4})\s*[-to–—]+\s*(\d{1,2}(?:/|-|\s)(?:\d{1,2}|\w{3})\s?\d{4})",
        "Payment_due_date": r"Payment\s*Due\s*Date\s*[:\-]?\s*(\d{1,2}(?:/|-|\s)(?:\d{1,2}|\w{3})\s?\d{4})",
        "Total_outstanding_balance": r"Amount\s*Due\s*[:\-]?\s*(?:INR|₹)?\s*([\d,]+\.\d{2})"
    },
    "Kotak Mahindra Bank": {
        "Last_4_digits": r"(?:XXXX|\*{4}|XXXX-)\s*(\d{4})\s*",
        "Billing_cycle": r"Statement\s*Period\s*(?:[:\-]?\s*)?(\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4})\s*[-to–—]+\s*(\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4})",
        "Payment_due_date": r"Payment\s*Due\s*Date\s*[:\-]?\s*(\d{1,2}(?:/|-|\s)(?:\d{1,2}|\w{3})\s?\d{4})",
        "Total_outstanding_balance": r"Statement\s*Balance\s*[:\-]?\s*(?:INR|₹)?\s*([\d,]+\.\d{2})"
    }
}


def extract_text(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
    except Exception as e:
        print("pdfplumber failed:", e)

    if not text.strip():
        print("WARNING: No text found - using OCR...")
        try:
            pages = convert_from_path(pdf_path)
            for page in pages:
                image_bytes = io.BytesIO()
                page.save(image_bytes, format='JPEG')
                img = Image.open(image_bytes)
                text += pytesseract.image_to_string(img)
        except Exception as e:
            print("Error OCR failed:", e)

    return text

def detect_bank(text):
    """Detects bank by looking for unique keywords in text."""
    for bank in BANK_PATTERNS:
        if bank.lower() in text.lower():
            return bank
    return None

def extract_fields(text, bank):
    """Extracts required fields using regex patterns for the bank."""
    patterns = BANK_PATTERNS.get(bank, {})
    result = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result[field] = next((g for g in match.groups() if g), "")
        else:
            result[field] = ""
    return result

if __name__ == "__main__":
    text = extract_text(pdf_path)
    bank = detect_bank(text)

    if not bank:
        print(json.dumps({"error": "Bank not detected"}))
        sys.exit(1)

    fields = extract_fields(text, bank)
    output = {"Bank": bank, **fields}
    print(json.dumps(output, indent=4))
