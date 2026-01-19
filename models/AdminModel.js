const db = require("../config/database");

const AdminModel = {
  create(admin, callback) {
    db.run(
      "INSERT INTO admins (email, password) VALUES (?, ?)",
      [admin.email, admin.password],
      callback
    );
  },

  getByEmail(email, callback) {
    db.get(
      "SELECT * FROM admins WHERE email = ?",
      [email],
      callback
    );
  }
};

module.exports = AdminModel;
