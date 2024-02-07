const express = require('express');
const router = express.Router();
const executeSP = require('../execute_SP.js');
const executeF= require('../execute_F.js');

router.get('/',(req,res,next)=>{
    const _item_limit = parseInt(req.query.itemLimit, 10) || 10; 
    const _current_page = parseInt(req.query.currentPage, 10) || 1;
    const params = [_item_limit,_current_page];
    executeF("vision_data","get_latest_targets", params)
    .then(result => {
        res.status(200).json(result);
    })
    .catch(err => {
        res.status(500).json({error: err});
    });
})

router.get('/:_target_id',(req,res,next)=>{
    const _target_id = req.params._target_id;
    const params = [_target_id];
    executeF("vision_data","get_target", params)
    .then(result => {
        res.status(200).json(result);
    })
    .catch(err => {
        res.status(500).json({error: err});
    });
})

module.exports = router;