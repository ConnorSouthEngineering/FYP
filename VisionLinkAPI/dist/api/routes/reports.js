"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express = require('express');
const router = express.Router();
const executeSP = require('../execute_SP.js');
const executeF = require('../execute_F.js');
router.get('/', (req, res, next) => {
    const _item_limit = parseInt(req.query.itemLimit, 10) || 10;
    const _current_page = parseInt(req.query.currentPage, 10) || 1;
    const params = [_item_limit, _current_page];
    executeF("vision_data", "get_latest_reports", params)
        .then(result => {
        res.status(200).json(result);
    })
        .catch(err => {
        res.status(500).json({ error: err });
    });
});
router.get('/:_report_id', (req, res, next) => {
    const _report_id = req.params._report_id;
    const params = [_report_id];
    executeF("vision_data", "get_report", params)
        .then(result => {
        res.status(200).json(result);
    })
        .catch(err => {
        res.status(500).json({ error: err });
    });
});
module.exports = router;
//# sourceMappingURL=reports.js.map