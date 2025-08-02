const sqlite3 = require('sqlite3').verbose();
const { MongoClient } = require('mongodb');
const path = require('path');

// Paths
const SQLITE_DB_PATH = path.join(__dirname, 'cases.db');
const MONGODB_URI = 'mongodb://localhost:27017'; // Update if using MongoDB Atlas

// Connect to SQLite
const sqliteDb = new sqlite3.Database(SQLITE_DB_PATH, sqlite3.OPEN_READONLY, (err) => {
  if (err) {
    console.error('SQLite connection error:', err);
    process.exit(1);
  }
  console.log('Connected to SQLite database');
});

// Connect to MongoDB
async function migrateToMongo() {
  const mongoClient = new MongoClient(MONGODB_URI);
  
  try {
    await mongoClient.connect();
    const db = mongoClient.db('courtCases'); // Database name
    const casesCollection = db.collection('cases'); // Collection name

    // Fetch all records from SQLite
    const sqliteData = await new Promise((resolve, reject) => {
      sqliteDb.all('SELECT * FROM cases', [], (err, rows) => {
        if (err) reject(err);
        resolve(rows);
      });
    });

    // Transform SQLite data to MongoDB format
    const mongoData = sqliteData.map(row => ({
      caseNumber: row.case_number,    // Adjust field names as needed
      caseType: row.case_type || 'CRL', // Default to 'CRL' if missing
      year: row.year,
      petitioner: row.petitioner,
      respondent: row.respondent || 'Unknown', // Handle missing fields
      status: row.status || 'Pending',
      nextHearing: row.next_hearing ? new Date(row.next_hearing) : null,
      createdAt: new Date()
    }));

    // Insert into MongoDB
    if (mongoData.length > 0) {
      const result = await casesCollection.insertMany(mongoData);
      console.log(`Inserted ${result.insertedCount} documents into MongoDB`);
    } else {
      console.log('No data found in SQLite to migrate');
    }

  } catch (err) {
    console.error('Migration error:', err);
  } finally {
    await mongoClient.close();
    sqliteDb.close();
  }
}

// Run migration
migrateToMongo();