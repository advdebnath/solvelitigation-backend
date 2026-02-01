const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');
const router = express.Router();

const uploadDirs = {
  supremeCourt: path.join(__dirname, '../uploads/supreme-court'),
  highCourt: path.join(__dirname, '../uploads/high-court'),
  tribunal: path.join(__dirname, '../uploads/tribunal')
};

Object.values(uploadDirs).forEach(dir => {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
});

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const courtType = req.body.courtType || 'high-court';
    let uploadDir = uploadDirs.highCourt;
    if (courtType === 'supremeCourt') uploadDir = uploadDirs.supremeCourt;
    else if (courtType === 'tribunal') uploadDir = uploadDirs.tribunal;
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    cb(null, uuidv4() + '-' + file.originalname);
  }
});

const fileFilter = (req, file, cb) => {
  if (file.mimetype === 'application/pdf') cb(null, true);
  else cb(new Error('Only PDF'), false);
};

const upload = multer({
  storage,
  fileFilter,
  limits: { fileSize: 900 * 1024 * 1024 }
});

const bulkUpload = multer({
  storage,
  fileFilter,
  limits: { fileSize: 900 * 1024 * 1024, files: 2500 }
});

router.post('/upload/supreme-court', upload.single('file'), (req, res) => {
  if (!req.file) return res.status(400).json({ success: false, message: 'No file' });
  res.json({ success: true, message: 'Supreme Court uploaded', data: { fileName: req.file.filename, sizeMB: (req.file.size / (1024 * 1024)).toFixed(2) } });
});

router.post('/upload/high-court', upload.single('file'), (req, res) => {
  if (!req.file) return res.status(400).json({ success: false, message: 'No file' });
  res.json({ success: true, message: 'High Court uploaded', data: { fileName: req.file.filename, sizeMB: (req.file.size / (1024 * 1024)).toFixed(2) } });
});

router.post('/upload/tribunal', upload.single('file'), (req, res) => {
  if (!req.file) return res.status(400).json({ success: false, message: 'No file' });
  res.json({ success: true, message: 'Tribunal uploaded', data: { fileName: req.file.filename, sizeMB: (req.file.size / (1024 * 1024)).toFixed(2) } });
});

router.post('/bulk-upload/supreme-court', bulkUpload.array('files', 2500), (req, res) => {
  if (!req.files?.length) return res.status(400).json({ success: false, message: 'No files' });
  res.json({ success: true, message: req.files.length + ' files uploaded', totalFiles: req.files.length, totalSizeMB: (req.files.reduce((s, f) => s + f.size, 0) / (1024 * 1024)).toFixed(2) });
});

router.post('/bulk-upload/high-court', bulkUpload.array('files', 2500), (req, res) => {
  if (!req.files?.length) return res.status(400).json({ success: false, message: 'No files' });
  res.json({ success: true, message: req.files.length + ' files uploaded', totalFiles: req.files.length, totalSizeMB: (req.files.reduce((s, f) => s + f.size, 0) / (1024 * 1024)).toFixed(2) });
});

router.post('/bulk-upload/tribunal', bulkUpload.array('files', 2500), (req, res) => {
  if (!req.files?.length) return res.status(400).json({ success: false, message: 'No files' });
  res.json({ success: true, message: req.files.length + ' files uploaded', totalFiles: req.files.length, totalSizeMB: (req.files.reduce((s, f) => s + f.size, 0) / (1024 * 1024)).toFixed(2) });
});

router.get('/judgments/:court', (req, res) => {
  try {
    let dir = uploadDirs.highCourt;
    if (req.params.court === 'supreme-court') dir = uploadDirs.supremeCourt;
    else if (req.params.court === 'tribunal') dir = uploadDirs.tribunal;
    const files = fs.readdirSync(dir);
    res.json({ success: true, court: req.params.court, count: files.length, files });
  } catch (e) {
    res.status(500).json({ success: false, message: e.message });
  }
});

router.get('/download/:court/:filename', (req, res) => {
  try {
    const dirs = { 'supreme-court': uploadDirs.supremeCourt, 'high-court': uploadDirs.highCourt, 'tribunal': uploadDirs.tribunal };
    const file = path.join(dirs[req.params.court], req.params.filename);
    if (!fs.existsSync(file)) return res.status(404).json({ success: false });
    res.download(file);
  } catch (e) {
    res.status(500).json({ success: false, message: e.message });
  }
});

router.get('/stats/all', (req, res) => {
  try {
    const stats = {};
    for (const [name, dir] of Object.entries(uploadDirs)) {
      const files = fs.readdirSync(dir);
      const total = files.reduce((s, f) => s + fs.statSync(path.join(dir, f)).size, 0);
      stats[name] = { files: files.length, sizeMB: (total / (1024 * 1024)).toFixed(2) };
    }
    res.json({ success: true, stats });
  } catch (e) {
    res.status(500).json({ success: false, message: e.message });
  }
});

module.exports = router;
