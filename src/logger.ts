import express from "express";
import geoip from "geoip-lite";
import bodyParser from "body-parser";
import fs from "fs";

type Log = {
  ip: `${number}.${number}.${number}.${number}`;
  port: number;
  lat: number;
  long: number;
  userAgent: string;
  createTime: string;
  headers: string; // JSON.stringify(req.headers)
};

const app = express();
const port = 3000;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.post("/", async (req, res) => {
  const ip = req.body.ip;
  const port = req.socket.remotePort ?? 0;
  const headers = req.headers;

  try {
    const geoResponse = geoip.lookup(ip);
    if (geoResponse) {
      const logData: Log = {
        ip,
        port,
        lat: geoResponse.ll[0],
        long: geoResponse.ll[1],
        userAgent: headers["user-agent"] ?? "",
        createTime: new Date().toISOString(),
        headers: JSON.stringify(headers),
      };
      console.log(logData);

      fs.appendFileSync("logs.txt", JSON.stringify(logData) + "\n");
    }
  } catch (error) {
    console.error("Error fetching geolocation:", error);
    res.status(500).send("Error fetching geolocation");
  }

  res.status(200).send("success");
});

app.listen(port, "0.0.0.0", () => {
  console.log(`Server running at http://localhost:${port}/`);
});
