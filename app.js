const express = require("express");
const app = express();
const apiRoutes = require("./api/apiRoutes");

app.use(express.json());
app.use("/api", apiRoutes);

app.listen(3000, () => {
  console.log("Server running on port 3000");
});
