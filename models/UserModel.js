const db = require("../config/database");

const UserModel = {
  create(user, callback) {
    const sql = `
      INSERT INTO users
      (name, email, password, age, gender, study, faculty, grad_year)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `;
    db.run(sql, [
      user.name,
      user.email,
      user.password,
      user.age,
      user.gender,
      user.study,
      user.faculty,
      user.grad_year
    ], callback);
  },

  getAll(callback) {
    db.all("SELECT * FROM users", callback);
  },

  disable(userId, callback) {
    db.run(
      "UPDATE users SET disabled = 1 WHERE id = ?",
      [userId],
      callback
    );
  }
};

module.exports = UserModel;

