const puppeteer = require('puppeteer');
const { default: getCrystalPosterTemplate } = require('../utils/getCrystalPosterTemplate');

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
  static async generatePoster({ html, posterElementId, width = 800, height = 1000, format = 'jpeg', quality = 90, isLongImage = false }) {
    try {
      // 启动浏览器
      const browser = await puppeteer.launch();
      const page = await browser.newPage();
      console.log("浏览器已启动！");

      // 设置视口尺寸
      await page.setViewport({ width, height: isLongImage ? 1000 : height });

      // 设置HTML内容
      await page.setContent(html);

      let screenshot = null;

      console.log(posterElementId, 'posterElementId')
      // 等待海报元素加载完成
      if (posterElementId) {
        const posterElement = await page.waitForSelector(`#${posterElementId}`);
        screenshot = await posterElement.screenshot({
          type: format,
          encoding: 'base64',
          path: './poster.png',
        });
        console.log(screenshot, 'screenshot')
      } else {
        // 如果是长图，自动计算内容高度
        if (isLongImage) {
          // 等待页面加载完成
          await page.waitForTimeout(1000);

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
          quality: quality,
          fullPage: isLongImage
        });
      }

      // 关闭浏览器
      await browser.close();

      return screenshot;
    } catch (error) {
      console.error('Error generating poster:', error);
      throw new Error('Failed to generate poster');
    }
  }

  /**
   * 创建默认的海报HTML模板
   * @param {Object} content - 海报内容
   * @param {string} content.text - 文本内容
   * @param {string} content.imageUrl - 图片URL
   * @param {string} content.backgroundColor - 背景颜色
   * @returns {string} 生成的HTML字符串
   */
  static createDefaultHtmlTemplate({ text = 'Sample Text', imageUrl = '', backgroundColor = '#ffffff' }) {
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <style>
          body { margin: 0; padding: 20px; background-color: ${backgroundColor}; }
          .poster { width: 100%; height: 100%; position: relative; }
          .text-content { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 32px; color: #333; text-align: center; }
          .image-content { position: absolute; top: 20%; left: 50%; transform: translateX(-50%); width: 200px; height: 200px; object-fit: cover; }
        </style>
      </head>
      <body>
        <div class="poster">
          ${imageUrl ? `<img src="${imageUrl}" class="image-content" />` : ''}
          <div class="text-content">${text}</div>
        </div>
      </body>
      </html>
    `;
  }

  static async createCrystalPoster({ crystalData }) {
    const posterHtml = getCrystalPosterTemplate({ crystalData });
    console.log(posterHtml, 'posterHtml');
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