const express = require('express');
const router = express.Router();
const executeSP = require('../execute_SP.js');
const executeF= require('../execute_F.js');

router.post('/create',(req,res,next)=>{
    const _task_id = req.body.task_id;
    const _location_name = req.body.location_name;
    const params = [_task_id,_location_name];
    executeF("vision_data", "insert_models", params)
    .then(result => {
        res.status(200).json(result);
    })
    .catch(err => {
        res.status(500).json({error: err});
    });
})

module.exports = router;