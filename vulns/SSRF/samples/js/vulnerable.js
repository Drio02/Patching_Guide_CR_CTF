const express = require('express');
const axios = require('axios');
const router = express.Router();

// Vuln: webhook guardado por el usuario y llamado desde el servidor
router.post('/webhook/test', async (req, res) => {
    const r = await axios.get(req.body.url);       // http://backend:3000/admin/flags
    res.send(r.data);
});

module.exports = router;
