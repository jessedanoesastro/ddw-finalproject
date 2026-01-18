class User {
  constructor(id, name, email, role = "user") {
    this.id = id;
    this.name = name;
    this.email = email;
    this.role = role;
    this.preferences = [];
    this.isBanned = false;
  }

  updatePreferences(preferences) {
    this.preferences = preferences;
  }

  ban() {
    this.isBanned = true;
  }
}

module.exports = User;
