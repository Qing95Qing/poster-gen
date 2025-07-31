const express = require('express');
const PosterService = require('../services/posterService');
const router = express.Router();

// 生成海报API
router.post('/generate-poster', async (req, res) => {
  try {
    const { html, width, height, format, quality, isLongImage, generateMethod } = req.body;

    // 如果提供了html，则使用它；否则使用默认模板
    let posterHtml = html;
    if (!posterHtml) {
      const { text, imageUrl, backgroundColor } = req.body;
      posterHtml = PosterService.createDefaultHtmlTemplate({
        text, imageUrl, backgroundColor
      });
    }

    // 生成海报
    let result;
    if (generateMethod === 'dom-to-image') {
      // 注意：dom-to-image只能在浏览器环境运行
      // 这里我们只是演示如何集成，实际项目中需要在前端实现
      throw new Error('dom-to-image method can only run in browser environment');
    } else {
      // 使用puppeteer生成海报
      result = await PosterService.generatePoster({
        html: posterHtml,
        width: width || 800,
        height: height || 1000,
        format: format || 'jpeg',
        quality: quality || 90,
        isLongImage: isLongImage || false
      });
    }

    res.setHeader('Content-Type', `image/${format || 'jpeg'}`);
    res.send(screenshot);
  } catch (error) {
    console.error('Error generating poster:', error);
    res.status(500).send('Error generating poster: ' + error.message);
  }
});

router.post('/generate-crystal-poster', async (req, res) => {
  try {
    // 添加更多调试信息
    // console.log('Request headers:', req.headers);
    // console.log('Request body:', req.body);
    // console.log('Is Content-Type application/json?', req.headers['content-type'] === 'application/json');
    
    const { crystalData } = req.body || {};
    if (!crystalData) {
      console.error('crystalData is missing in request body');
      return res.status(400).send('crystalData is required');
    }
    
    const image = await PosterService.createCrystalPoster({
      crystalData
    });
    // console.log('生成成功', image);
    res.send(image);
  } catch (error) {
    console.error('Error generating crystal poster:', error);
    res.status(500).send('Error generating crystal poster: ' + error.message);
  }
});

// 获取默认HTML模板
router.get('/default-template', (req, res) => {
  try {
    const { text, imageUrl, backgroundColor } = req.query;
    const html = PosterService.createDefaultHtmlTemplate({
      text, imageUrl, backgroundColor
    });
    res.send(html);
  } catch (error) {
    res.status(500).send('Error generating template: ' + error.message);
  }
});

module.exports = router;