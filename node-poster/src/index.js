const express = require('express');
const path = require('path');
const posterRoutes = require('./api/poster');

// 创建应用
const app = express();
const port = process.env.PORT || 3000;

// 中间件
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));
app.use('/assets', express.static(path.join(__dirname, '../assets')));

// 注册路由
app.use('/api', posterRoutes);

// 启动服务器
app.listen(port, () => {
  console.log(`Poster generator server running at http://localhost:${port}`);
});

module.exports = app;