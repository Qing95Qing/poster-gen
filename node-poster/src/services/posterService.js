const puppeteer = require('puppeteer');
const { default: getCrystalPosterTemplate } = require('../utils/getCrystalPosterTemplate');
const path = require('path');

// 解决Puppeteer新版本中page.waitForTimeout移除的问题
// 这个polyfill会添加到Puppeteer的Page原型上
const addWaitForTimeout = () => {
  const puppeteer = require('puppeteer');
  if (!puppeteer.Page.prototype.waitForTimeout) {
    puppeteer.Page.prototype.waitForTimeout = function (ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    };
  }
};

addWaitForTimeout();


class PosterService {
  /**
   * 生成海报
   * @param {Object} options - 海报选项
   * @param {string} options.html - 海报的HTML内容
   * @param {number} options.width - 海报宽度
   * @param {number} options.height - 海报高度
   * @param {string} options.format - 输出格式 (jpeg, png等)
   * @param {number} options.quality - 图像质量 (0-100)
   * @returns {Buffer} 生成的海报图像buffer
   */
  /**
   * 生成海报（支持长图）
   * @param {Object} options - 海报选项
   * @param {string} options.html - 海报的HTML内容
   * @param {number} options.width - 海报宽度
   * @param {number} options.height - 海报高度（如果设置为0，则自动计算内容高度）
   * @param {string} options.format - 输出格式 (jpeg, png等)
   * @param {number} options.quality - 图像质量 (0-100)
   * @param {boolean} options.isLongImage - 是否为长图
   * @returns {Buffer} 生成的海报图像buffer
   */
  static async generatePoster({ html, posterElementId, width = 600, height = 1000, format = 'jpeg', quality = 90, isLongImage = false }) {
    try {
      // 记录开始时间
      const startTime = Date.now();
      console.log('开始生成海报...');

      // 指向项目根目录
      const projectDir = path.resolve(__dirname, '../..'); 
      console.log(projectDir, 'projectDir')

      // 启动浏览器
      const browser = await puppeteer.launch({ 
        headless: false,
        args: ['--disable-web-security', '--disable-features=IsolateOrigins', '--disable-site-isolation-trials']
      });
      const page = await browser.newPage();
      console.log("浏览器已启动！");

      // 设置视口尺寸
      await page.setViewport({ width, height: isLongImage ? 1000 : height });

      // 设置HTML内容
      await page.setContent(html, {
        waitUntil: ['networkidle2', 'load', 'domcontentloaded'] // 等待多种状态
      });

      // 等待1秒让资源有时间加载
      await page.waitForTimeout(1000);

      // 使用evaluate获取资源加载状态并传递回Node.js环境
      const checkResourceLoadStatus = async () => {
        return await page.evaluate(async () => {
          try {
            // 检查图片加载状态
            const images = document.querySelectorAll('img');
            const loadedImages = Array.from(images).filter(img => img.complete);
            const allImageLoaded = loadedImages.length === images.length;
            console.log(`图片加载状态: ${loadedImages.length}/${images.length} 已加载`);

            // 检查字体加载状态
            const fontsLoaded = document.fonts.status === 'loaded';
            console.log(`字体加载状态: ${fontsLoaded ? '已加载' : '未加载'}`);

            // 检查CSS背景图片加载状态
            const bgImages = [];
            document.querySelectorAll('*').forEach(element => {
              const style = window.getComputedStyle(element);
              const bgImage = style.backgroundImage;
              if (bgImage && bgImage !== 'none') {
                bgImages.push(bgImage);
              }
            });
            console.log(`背景图片数量: ${bgImages.length}`);

            return {
              success: allImageLoaded && fontsLoaded,
              imageCount: images.length,
              loadedImages: loadedImages.length,
              fontStatus: document.fonts.status
            };
          } catch (error) {
            console.error('Error checking resource load status:', error);
            return {
              success: false,
              error: error.message
            };
          }
        });
      };

      // 循环检查资源加载状态，直到加载完成或超时
      let resourceLoadStatus = await checkResourceLoadStatus();
      const maxRetries = 30; // 最多检查30次
      const retryInterval = 1000; // 每1秒检查一次
      let retries = 0;

      while (!resourceLoadStatus.success && retries < maxRetries) {
        console.log(`资源未完全加载，等待${retryInterval}ms后重试...`);
        await page.waitForTimeout(retryInterval);
        resourceLoadStatus = await checkResourceLoadStatus();
        retries++;
      }

      if (!resourceLoadStatus.success) {
        console.warn(`资源加载超时，已尝试${maxRetries}次，仍有${resourceLoadStatus.imageCount - resourceLoadStatus.loadedImages}张图片未加载`);
      } else {
        console.log('所有资源已成功加载');
      }

      // 在Node.js环境中打印最终图片加载状态
      console.log('最终图片加载状态:', resourceLoadStatus);

      let screenshot = null;

      console.log(posterElementId, 'posterElementId')
      // 等待海报元素加载完成
      if (posterElementId) {
        const posterElement = await page.waitForSelector(`#${posterElementId}`);

        // 获取海报元素的实际宽高
        const elementBounds = await posterElement.boundingBox();
        const elementWidth = Math.ceil(elementBounds.width);
        const elementHeight = Math.ceil(elementBounds.height);

        // 设置视口为元素的实际宽高，并应用高清缩放因子
        await page.setViewport({ 
          width: elementWidth, 
          height: elementHeight, 
          deviceScaleFactor: 3 
        });

        screenshot = await posterElement.screenshot({
          type: format,
          // encoding: 'base64',
          path: './poster.png',
          omitBackground: false, // 确保背景不透明
          deviceScaleFactor: 2 // 提高清晰度，2倍像素密度
        });
        // console.log(screenshot, 'screenshot')
      } else {
        // 如果是长图，自动计算内容高度
        if (isLongImage) {
          // 等待页面加载完成
          await new Promise(resolve => setTimeout(resolve, 1000));

          // 获取页面实际高度
          const bodyHeight = await page.evaluate(() => {
            return document.body.scrollHeight;
          });

          // 更新视口高度
          await page.setViewport({ width, height: bodyHeight });
        }

        // 截取屏幕
        screenshot = await page.screenshot({
          type: format,
          quality: format === 'png' ? undefined : quality, // PNG格式不支持quality参数
          fullPage: isLongImage,
          pixelRatio: 3, // 提高清晰度，2倍像素密度
          captureBeyondViewport: true
        });
      }

      // 关闭浏览器
      // await browser.close();

      // 记录结束时间并计算耗时
      const endTime = Date.now();
      const duration = (endTime - startTime) / 1000;
      console.log(`海报生成完成，总耗时: ${duration.toFixed(2)}秒`);
            
      return screenshot;
    } catch (error) {

      console.error('Error generating poster:', error);
      throw new Error('Failed to generate poster');
    }
  }

  static async createCrystalPoster({ crystalData }) {
    const posterHtml = getCrystalPosterTemplate({ crystalData });
    // console.log(posterHtml, 'posterHtml');
    const posterImage = await this.generatePoster({
      html: posterHtml,
      posterElementId: 'poster',
      width: 566,
      height: 800,
      format: 'png',
      quality: 100,
      isLongImage: false
    });
    return posterImage;
  }
}

module.exports = PosterService;