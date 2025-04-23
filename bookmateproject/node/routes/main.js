const express = require("express");
const bodyParser = require("body-parser");
const XMLHttpRequest = require("xhr2");
const axios = require('axios');
const app = express();

 
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// GET /genre-change: 클라이언트에서 받은 세대 정보로 FastAPI에 요청 후 결과 반환
app.get('/genre-change', async (req, res) => {
    const { ageGroup, startDt, endDt } = req.query;
    console.log(ageGroup, startDt, endDt)
    try {
        const FASTAPI_URL = process.env.FASTAPI_URL || 'http://localhost:3000/genre-change/';
        const response = await axios.get(FASTAPI_URL, {
            params: { ageGroup, startDt, endDt }
        });
        res.json(response.data);
    } catch (err) {
        console.error('FastAPI 연동 오류:', err.message);
        res.status(500).json({ error: 'FastAPI 연동 실패', detail: err.message });
    }
});

module.exports = app;