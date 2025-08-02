const express = require('express');
const router = express.Router();
const Case = require('../models/Case');

// Get case by number and year
router.get('/search', async (req, res) => {
  try {
    const { caseNumber, year } = req.query;
    const caseData = await Case.findOne({ caseNumber, year });
    if (!caseData) return res.status(404).json({ error: 'Case not found' });
    res.json(caseData);
  } catch (err) {
    res.status(500).json({ error: 'Server error' });
  }
});

module.exports = router;
// Search cases by type (CRL, CIVIL, etc.)
router.get('/search/type', async (req, res) => {
  try {
    const { caseType } = req.query;
    
    // Validate input
    if (!caseType) {
      return res.status(400).json({ error: 'Case type is required' });
    }

    const cases = await Case.find({ 
      caseType: new RegExp(caseType, 'i') // Case-insensitive search
    });

    if (cases.length === 0) {
      return res.status(404).json({ error: 'No cases found for this type' });
    }

    res.json(cases);
  } catch (err) {
    res.status(500).json({ error: 'Server error' });
  }
});