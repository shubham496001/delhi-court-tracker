const express = require('express');
const cors = require('cors');
const connectDB = require('./config/db');
const caseRoutes = require('./routes/caseRoutes');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Database
connectDB();

// Routes
app.use('/api/cases', caseRoutes);

// Start server
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));