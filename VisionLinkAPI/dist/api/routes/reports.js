"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express = require('express');
const router = express.Router();
router.get('/', (req, res, next) => {
    res.status(200).json({
        message: "Handling requests for /reports"
    });
});
router.get('/:reportID', (req, res, next) => {
    const id = req.params.reportID;
    const message = "Handling requests for report " + id;
    res.status(200).json({
        message: message
    });
});
module.exports = router;
//# sourceMappingURL=reports.js.map