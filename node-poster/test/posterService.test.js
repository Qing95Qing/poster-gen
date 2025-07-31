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
    
    const crystalData = posterData;

    // console.log(posterData, 'posterData')

    const posterBuffer = await PosterService.createCrystalPoster({ crystalData });

    assert.ok(posterBuffer instanceof Buffer, '水晶海报应该是Buffer类型');
    assert.ok(posterBuffer.length > 0, '水晶海报Buffer不应该为空');

    const outputPath = path.join(__dirname, 'output', 'crystal-poster.png');
    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    fs.writeFileSync(outputPath, posterBuffer);
    console.log(`✓ 测试通过: 水晶海报已保存到 ${outputPath}`);
    passed++;
  } catch (error) {
    console.log('✗ 测试失败: 生成水晶海报');
    console.error(error);
  }

  console.log(`\n测试结果: ${passed}/${totalTests} 通过`);
}

// 运行测试
runTests();