class Schedule {
  constructor() {
    this.appointments = [];
  }

  addAppointment(appointment) {
    this.appointments.push(appointment);
  }

  getAllAppointments() {
    return this.appointments;
  }
}

module.exports = Schedule;
