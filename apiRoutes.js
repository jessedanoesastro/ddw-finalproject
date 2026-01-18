const express = require("express");
const router = express.Router();
const { users, schedules } = require("../models/dataStore");

router.get("/users", (req, res) => {
  res.json(users);
});

router.get("/appointments", (req, res) => {
  if (schedules.length === 0) {
    return res.json([]);
  }
  res.json(schedules[0].getAllAppointments());
});

module.exports = router;
