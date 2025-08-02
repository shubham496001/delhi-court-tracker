const mongoose = require('mongoose');

const CaseSchema = new mongoose.Schema({
  caseNumber: { type: String, required: true },
  caseType: { type: String, default: 'CRL' },
  year: { type: Number, required: true },
  petitioner: { type: String, required: true },
  respondent: { type: String, default: 'Unknown' },
  status: { type: String, default: 'Pending' },
  nextHearing: { type: Date },
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Case', CaseSchema);