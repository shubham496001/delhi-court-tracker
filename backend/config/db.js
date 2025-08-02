const mongoose = require('mongoose');

const connectDB = async () => {
  try {
    await mongoose.connect(
      'mongodb+srv://shubhamnamdeojso4157:your_password_here@delhi-court-cluster.bmd4llt.mongodb.net/courtCases?retryWrites=true&w=majority',
      {
        useNewUrlParser: true,
        useUnifiedTopology: true,
        // Recommended additional options:
        serverSelectionTimeoutMS: 5000, // Timeout after 5s instead of 30s
        maxPoolSize: 10, // Maximum number of socket connections
      }
    );
    console.log('MongoDB Connected');
  } catch (err) {
    console.error('MongoDB Connection Error:', err);
    process.exit(1); // Exit process with failure
  }
};

module.exports = connectDB;