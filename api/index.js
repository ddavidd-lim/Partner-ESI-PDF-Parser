const express = require('express');
const multer = require('multer');
const { exec } = require('child_process');
const app = express();
const port = 3000;

// Configure multer for file storage
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/')
  },
  filename: function (req, file, cb) {
    cb(null, file.fieldname + '-' + Date.now() + file.originalname.slice(-4))
  }
});

const upload = multer({ storage: storage });

// POST endpoint to receive the file and run the Python script
app.post('/upload', upload.single('file'), (req, res) => {
  const file = req.file;
  if (!file) {
    return res.status(400).send('No file uploaded.');
  }

  // Execute the Python script using the uploaded file
  exec(`python main.py ${file.path}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`exec error: ${error}`);
      return res.status(500).send(`Execution Error: ${error.message}`);
    }
    if (stderr) {
      console.error(`stderr: ${stderr}`);
      return res.status(500).send(`Script Error: ${stderr}`);
    }
    res.json({file: stdout.trim()});
    // res.send(`File processed successfully:\n${stdout}`);
  });
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
