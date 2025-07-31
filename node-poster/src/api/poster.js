const express = require('express');
const PosterService = require('../services/posterService');
const router = express.Router();

// 生成水晶手串海报
router.post('/generate-crystal-poster', async (req, res) => {
  try {
    // 添加更多调试信息
    // console.log('Request headers:', req.headers);
    // console.log('Request body:', req.body);
    // console.log('Is Content-Type application/json?', req.headers['content-type'] === 'application/json');
    
    const { crystal_data } = req.body || {};
    if (!crystal_data) {
      console.error('crystal_data is missing in request body');
      return res.status(400).send('crystal_data is required');
    }
    
    const image = await PosterService.createCrystalPoster({
      posterData: crystal_data
    });
    // console.log('生成成功', image);
    res.send({
      code: 0,
      msg: '生成成功',
      data: image
    });
  } catch (error) {
    console.error('Error generating crystal poster:', error);
    res.status(500).send('Error generating crystal poster: ' + error.message);
  }
});

module.exports = router;