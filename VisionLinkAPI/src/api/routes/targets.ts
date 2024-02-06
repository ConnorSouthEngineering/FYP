const express = require('express');
const router = express.Router();

router.get('/',(req,res,next)=>{
    res.status(200).json({  
        message: "Handling requests for /target"
    });
})

router.get('/:targetID',(req,res,next)=>{
    const id = req.params.targetID;
    const message = "Handling requests for target "+id+" number"
    res.status(200).json({  
        message:  message
    });
})

module.exports = router;