# Credit Card Statement Parser

A **Python + React** application that extracts key details from credit card statements (PDFs), supporting multiple banks and formats. The parser handles both **text-based PDFs** and **image PDFs** (via OCR) and is capable of recognizing **different date formats** and **card number styles**.

---

## Features

- Supports multiple banks:
  - HDFC Bank
  - ICICI Bank
  - SBI Card
  - Axis Bank
  - Kotak Mahindra Bank
- Extracts the following details:
  - Last 4 digits of the card
  - Billing cycle (start and end date)
  - Payment due date
  - Total outstanding balance
- Handles different **date formats**:
  - Numeric dates (`01/09/2025` or `01-09-2025`)
  - Short-month format (`01 Sep 2025`)
- Works with both **text PDFs** and **scanned/image PDFs** using OCR
- Flexible regex patterns that handle:
  - Optional colons or dashes after labels
  - Multiple card number formats (`XXXX-XXXX-XXXX-1234`, `**** 1234`, etc.)

---

## Tech Stack

- **Backend:** Python, pdfplumber, pdf2image, pytesseract, PIL
- **Frontend:** React.js
- **Libraries/Tools:**  
  - `pdfplumber` – extract text from text-based PDFs  
  - `pdf2image` + `pytesseract` – extract text from scanned/image PDFs  
  - `FormData` and Fetch API – handle file uploads in React  

---

## Installation

### Backend

1. Clone the repository:

```bash
git clone <your-repo-url>
cd credit-card-parser
````

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Install **Poppler** (required by pdf2image for OCR):

* Windows: [Download Poppler](http://blog.alivate.com.au/poppler-windows/) → add `bin` folder to PATH

4. Install **Tesseract OCR**:

* Windows: [Download Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) → add installation folder to PATH
* Verify installation:

```bash
tesseract -v
```

5. Run the backend:

```bash
python backend/pdf_parser.py <path-to-pdf>
```

---

### Frontend

1. Navigate to the frontend folder:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the React app:

```bash
npm start
```

4. Open in browser: [http://localhost:3000](http://localhost:3000)

---

## Usage

1. Open the frontend in your browser.
2. Select a credit card PDF file using the **file input**.
3. Click **Upload**.
4. The extracted details will be displayed below the form:

```
- Bank: HDFC Bank
- Last 4 digits: 1234
- Billing cycle: 01 Sep 2025 - 30 Sep 2025
- Payment due date: 15 Oct 2025
- Total outstanding balance: 5,250.00
```

---

## Example PDFs Supported

* Text PDFs (downloaded statements)
* Image PDFs (scanned statements)
* Various formats of card numbers and dates

---

## How It Works

1. **Text extraction** using `pdfplumber`.
2. If no text is found, **OCR** is applied using `pdf2image` + `pytesseract`.
3. The text is matched against **bank-specific regex patterns**.
4. Extracted fields are returned in **JSON format** for easy consumption by the frontend.
5. React frontend displays the details in a **clean, readable UI**.

---

## Regex Flexibility

* **Card numbers:** Supports `XXXX-XXXX-XXXX-1234`, `**** 1234`, `XXXX 1234`, etc.
* **Dates:** Supports numeric and short-month formats: `01/09/2025` or `01 Sep 2025`.
* **Labels:** Regex allows missing colons or dashes after labels (`Statement Period 01 Sep 2025` works).

---

## Folder Structure

```
credit-card-parser/
│
├── backend/
│   ├── pdf_parser.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   └── App.jsx
│   └── package.json
│
└── uploads/ (optional folder for storing uploaded PDFs)
```

---

## Future Improvements

* Add **more banks** and custom regex patterns.
* Automatically detect **currency format**.
* Export extracted data as **CSV or Excel**.
* Enhance OCR accuracy for **low-quality scans**.
* Add **authentication** for secure PDF uploads.

---

## License

This project is open-source and free to use.

