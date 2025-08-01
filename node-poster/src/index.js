const express = require('express');
const path = require('path');
const posterRoutes = require('./api/poster');

// 创建应用
const app = express();
const port = process.env.PORT || 8000;

// 中间件
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));
app.use('/assets', express.static(path.join(__dirname, '../assets')));

// 注册路由
app.use('/api', posterRoutes);

// 启动服务器
app.listen(port, '0.0.0.0', () => {
  console.log(`Poster generator server running at http://localhost:${port}`);
  console.log(`Server accessible on local network at http://${require('os').networkInterfaces()['en0']?.find(addr => addr.family === 'IPv4')?.address}:${port}`);
});

module.exports = app;