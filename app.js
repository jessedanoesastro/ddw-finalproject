const express = require("express");
const app = express();
const apiRoutes = require("./api/apiRoutes");

app.use(express.json());
app.use("/api", apiRoutes);

app.listen(3000, () => {
  console.log("Server running on port 3000");
});

const fs = require("fs");
const path = require("path");
const db = require("./config/database");

const initSQL = fs.readFileSync(
  path.join(__dirname, "database/init.sql"),
  "utf8"
);

db.exec(initSQL);

