const assert = require('assert');
const fs = require('fs');
const path = require('path');
const PosterService = require('../src/services/posterService');
const posterData = require('./input.json');

// 测试函数
async function runTests() {
  console.log('开始测试海报服务...\n');
  let passed = 0;
  const totalTests = 1;


  // 测试2: 生成水晶海报
  try {
    console.log('\n测试2: 生成水晶海报');
    
    // console.log(posterData, 'posterData')

    let posterBuffer = await PosterService.createCrystalPoster({ posterData });

    console.log('海报Buffer类型:', posterBuffer instanceof Buffer);
    console.log('海报Buffer长度:', posterBuffer.length);
    if (!(posterBuffer instanceof Buffer)) {
      // 当不为buffer时，将base64转换为buffer
      posterBuffer = Buffer.from(posterBuffer, 'base64');
    }
    if (posterBuffer.length <= 0) {
      throw new Error('水晶海报Buffer不应该为空');
    }

    const outputPath = path.join(__dirname, '../assets', `result.webp`);
    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    fs.writeFileSync(outputPath, posterBuffer);
    console.log(`✓ 测试通过: 水晶海报已保存到 ${outputPath}`);
    passed++;
  } catch (error) {
    console.log('✗ 测试失败: 生成水晶海报');
    console.error(error);
  }

  console.log(`\n测试结果: ${passed}/${totalTests} 通过`);

  // 关闭浏览器集群
  await PosterService.closeCluster();
}

// 运行测试
runTests();