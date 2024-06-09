const express = require('express');
const multer = require('multer');
const cors = require('cors');
const fs = require('fs'); // File system operations
const path = require('path'); // Path manipulations
const { exec } = require('child_process'); // To execute Python scripts

const app = express();
const port = process.env.PORT || 3000;

// Enable CORS
app.use(cors());

// Configure Multer for file uploads
const upload = multer({
    dest: './uploads/', // Directory to store uploaded files
    limits: { fileSize: 1000000 }, // File size limit (1MB)
    fileFilter: (req, file, cb) => {
        if (!file.mimetype.startsWith('application/pdf')) {
            return cb(new Error('Only PDF files are allowed!'));
        }
        cb(null, true); // Accept PDF files
    },
});

// Define the upload endpoint
app.post('/upload', upload.single('pdfFile'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ message: 'No PDF file uploaded!' });
    }

    const pdfFilePath = req.file.path; // Path to the uploaded file
    const pythonScriptPath = './muliti_RAG.py'; // Path to your Python script

    // Command to execute the Python script with the PDF file as an argument
    const command = `python ${pythonScriptPath} ${pdfFilePath}`; // Execute the script with the uploaded PDF as an argument

    // Execute the Python script
    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error('Error running Python script:', error);
            return res.status(500).json({ message: 'Error processing PDF.' });
        }

        // Assuming stdout contains the path to the processed file or some result
        const processedOutput = stdout.trim(); // Get the output from the Python script

        // Define where to save the processed result (if needed)
        const processedFilePath = path.join('./uploads', 'processed_output.pdf'); // Adjust the name as needed

        // Save the processed result to a file (if the output is file-based)
        fs.writeFileSync(processedFilePath, processedOutput);

        // Send the processed file back to the user for download
        res.download(processedFilePath, 'processed_output.pdf', (err) => {
            if (err) {
                console.error('Error sending processed file:', err);
                return res.status(500).json({ message: 'Error sending processed PDF.' });
            }
        });
    });
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
