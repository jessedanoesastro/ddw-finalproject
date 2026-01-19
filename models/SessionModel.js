const db = require("../config/database");

const SessionModel = {
  create(session, callback) {
    const sql = `
      INSERT INTO sessions
      (subject, description, date, time, location, created_by)
      VALUES (?, ?, ?, ?, ?, ?)
    `;
    db.run(sql, [
      session.subject,
      session.description,
      session.date,
      session.time,
      session.location,
      session.created_by
    ], callback);
  },

  getAll(callback) {
    db.all("SELECT * FROM sessions", callback);
  },

  join(sessionId, userId, callback) {
    db.run(
      "INSERT INTO session_participants (session_id, user_id) VALUES (?, ?)",
      [sessionId, userId],
      callback
    );
  },

  leave(sessionId, userId, callback) {
    db.run(
      "DELETE FROM session_participants WHERE session_id = ? AND user_id = ?",
      [sessionId, userId],
      callback
    );
  }
};

module.exports = SessionModel;
