import express from "express";
import cors from "cors";
import multer from "multer";
import fs from "fs";
import path from "path";
import { spawn } from "child_process";
import { fileURLToPath } from "url";

const app = express();
app.use(cors());

// Get correct absolute paths (fix for pdfs folder issue)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const uploadDir = path.resolve(__dirname, "../pdfs");

// Create pdfs folder in main directory if it doesn’t exist
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true });
}

// Configure Multer storage
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, uploadDir);
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname);
  },
});

const upload = multer({ storage });

// === API ROUTES ===

// Health check route
app.get("/", (req, res) => {
  res.send("✅ Backend is running...");
});

// Upload route
app.post("/upload", upload.single("file"), (req, res) => {
  try {
    const filePath = path.join(uploadDir, req.file.filename);

    // Spawn the Python parser
    const pythonProcess = spawn("python", ["pdf_parser.py", filePath]);

    let output = "";
    let errorOutput = "";

    pythonProcess.stdout.on("data", (data) => {
      output += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
      errorOutput += data.toString();
      console.error("Python Error:", data.toString());
    });

    pythonProcess.on("close", (code) => {
      // Delete uploaded file after parsing
      try {
        fs.unlinkSync(filePath);
      } catch (err) {
        console.error("Error deleting file:", err);
      }

      if (code !== 0) {
        return res.status(500).json({ error: "Python script failed", details: errorOutput });
      }

      try {
        const result = JSON.parse(output);
        res.json(result);
      } catch (err) {
        console.error("JSON Parse Error:", err);
        res.status(500).json({ error: "Invalid JSON output from Python" });
      }
    });
  } catch (err) {
    console.error("Upload error:", err);
    res.status(500).json({ error: "Server error during upload" });
  }
});

// Start server
const PORT = 5000;
app.listen(PORT, () => console.log(`🚀 Server running at http://localhost:${PORT}`));
