class Appointment {
  constructor(id, time, location, maxParticipants = 5) {
    this.id = id;
    this.time = time;
    this.location = location;
    this.maxParticipants = maxParticipants;
    this.participants = [];
  }

  join(user) {
    if (user.isBanned) {
      throw new Error("User is banned");
    }
    if (this.participants.length >= this.maxParticipants) {
      throw new Error("Appointment is full");
    }
    if (this.participants.includes(user.id)) {
      throw new Error("User already joined");
    }
    this.participants.push(user.id);
  }

  leave(user) {
    this.participants = this.participants.filter(id => id !== user.id);
  }
}

module.exports = Appointment;
