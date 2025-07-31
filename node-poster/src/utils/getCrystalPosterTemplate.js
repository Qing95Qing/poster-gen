const FONT_URL = 'https://zhuluoji.cn-sh2.ufileos.com/resources/%E8%83%A1%E6%99%93%E6%B3%A2%E6%B5%AA%E6%BC%AB%E5%AE%8B.ttf';
const POSTER_BG_IMAGE = "https://zhuluoji.cn-sh2.ufileos.com/images-frontend/poster/poster-background-image.png";
const POSTER_BOTTOM_LOGO = "https://zhuluoji.cn-sh2.ufileos.com/images-frontend/poster/poster-bottom-rccode.png";
const CRYSTAL_MATERIAL = "https://zhuluoji.cn-sh2.ufileos.com/images-frontend/poster/crystal-material.png";
const WEAR_TIP_ICON = "https://zhuluoji.cn-sh2.ufileos.com/images-frontend/poster/wear-tip-icon.svg";
const BRAND_LOGO = "https://zhuluoji.cn-sh2.ufileos.com/images-frontend/poster/brand-logo.png"

const getElementConfig = (type) => {
    const configs = {
      金: {
        textColor: "#662900",
        iconUrl: 'https://zhuluoji.cn-sh2.ufileos.com/images-frontend/wu-xing/jin-icon.png',
        bgUrl: 'https://zhuluoji.cn-sh2.ufileos.com/images-frontend/wu-xing/jin-bg.png'
        
      },
      火: {
        textColor: "#930002",
        iconUrl: 'https://zhuluoji.cn-sh2.ufileos.com/images-frontend/wu-xing/huo-icon.png',
        bgUrl: 'https://zhuluoji.cn-sh2.ufileos.com/images-frontend/wu-xing/huo-bg.png'
      },
      水: {
        textColor: "#007193",
        iconUrl: 'https://zhuluoji.cn-sh2.ufileos.com/images-frontend/wu-xing/shui-icon.png',
        bgUrl: 'https://zhuluoji.cn-sh2.ufileos.com/images-frontend/wu-xing/shui-bg.png'
      },
      土: {
        textColor: "#7F6340",
        iconUrl: 'https://zhuluoji.cn-sh2.ufileos.com/images-frontend/wu-xing/tu-icon.png',
        bgUrl: 'https://zhuluoji.cn-sh2.ufileos.com/images-frontend/wu-xing/tu-bg.png'
      },
      木: {
        textColor: "#609349",
        iconUrl: 'https://zhuluoji.cn-sh2.ufileos.com/images-frontend/wu-xing/mu-icon.png',
        bgUrl: 'https://zhuluoji.cn-sh2.ufileos.com/images-frontend/wu-xing/mu-bg.png'
      },
    };
    return configs[type] || configs.金;
  };

export default function getCrystalPosterTemplate({crystalData}) {

    const wuxingConfig = getElementConfig(crystalData?.word_info?.rizhu || crystalData?.word_info?.wuxing?.[0] || '金');
    return `
    <html lang="zh-CN">

<head>
    <meta charset="UTF-8">
    <meta name="divport" content="width=device-width, initial-scale=1.0">
    <title>海报</title>
    <style>
        /* 引入自定义字体 */
        @font-face {
            font-family: 'HuXiaoBoSong';
            src: url(${FONT_URL}) format('truetype');
            font-weight: normal;
            font-style: normal;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Arial', sans-serif;
        }

        body {
            background-color: #f5f5f5;
            padding: 20px;
        }

        .poster {
            position: relative;
            width: 430px;
            height: fit-content;
            padding-bottom: 126px;
            padding-top: 42px;
            margin: 0 auto;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
            background-image: url(${POSTER_BG_IMAGE});
            background-size: 100% 100%;
            background-repeat: repeat;
        }

        .poster::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 136px;
            background-image: url(${POSTER_BOTTOM_LOGO});
            background-size: 100% 100%;
            background-repeat: no-repeat;
        }

        .content-card-wrapper {
            width: 346px;
            padding: 2px;
            border-radius: 10px;
            background: linear-gradient(180deg, #aeaba836 0, #ffffffb8 75%, #ffffff52 100%);
        }

        .content-card {
            position: relative;
            width: 100%;
            height: 100%;
            border-radius: 8px;
            background-color: #fff;
            overflow: hidden;
        }

        .main-image-container {
            position: relative;
            width: 100%;
            height: 256px;
            flex-shrink: 0;
        }

        .main-image-container::before {
            content: '';
            position: absolute;
            height: 31px;
            width: 76px;
            top: 0;
            right: 0;
            background: url(${BRAND_LOGO});
            background-size: 100% 100%;
            background-repeat: no-repeat;
        }

        .main-image-container::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 77px;
            flex-shrink: 0;
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.00) 0%, #FFF 100%);
        }

        .main-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .content-container {
            position: relative;
            top: -12px;
            padding: 0 24px 20px;
            display: flex;
            flex-direction: column;
        }

        .design-no {
            font-family: 'Noto Sans SC', sans-serif;
            color: #1F1722;
            font-size: 11px;
            font-weight: 300;
            font-style: normal;
            line-height: 135%;
            opacity: 0.8;
        }

        .design-title {
            color: #1F1722;
            font-family: 'HuXiaoBoSong', 'Noto Sans SC', sans-serif;
            font-size: 40px;
            font-style: normal;
            font-weight: 400;
            /* 100% */
            letter-spacing: 3px;
            margin-top: 4px;
            margin-bottom: 6px;
        }

        .design-desc-container {
            width: 100%;
            display: flex;
            align-items: flex-start;
            gap: 32px;
        }

        .design-desc-right {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 16px;
            /* 左边部分根据剩余宽度分配 */
        }

        .design-desc-right-top {
            width: 100%;
            color: #1F1722;
            text-align: justify;
            font-size: 12px;
            font-style: normal;
            font-weight: 300;
            line-height: 150%;
            opacity: 0.6;
        }

        .design-desc-right-bottom {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .design-desc-right-bottom-title {
            display: flex;
            align-items: center;
            gap: 4px;
            color: #1F1722;
            text-align: justify;
            font-size: 12px;
            font-style: normal;
            font-weight: 500;
            line-height: 135%;
            /* 16.2px */
            letter-spacing: 1px;
        }

        .title-image {
            width: 16px;
            height: 16px;
        }

        .design-desc-right-bottom-content {
            color: #1F1722;
            text-align: justify;
            font-family: "Noto Sans SC";
            font-size: 12px;
            font-style: normal;
            font-weight: 300;
            line-height: 150%;
            opacity: 0.6;
            /* 16.5px */
        }

        .design-desc-left {
            flex: 0 0 auto;
            position: relative;
            /* 右边部分固定宽高 */
            width: 64px;
            height: 164px;
        }

        .wuxing-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .wuxing-content {
            position: absolute;
            top: 0;
            left: 0;
            width: 64px;
            height: 164px;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            gap: 8px;
            padding: 12px;
        }

        .wuxing-content-right {
            display: flex;
            flex-direction: column;
            gap: 12px;
            align-items: center;
            height: 100%;

        }

        .wuxing-icon {
            width: 22px;
            height: 22px;
        }

        .wuxing-text {
            font-family: "Source Han Serif CN", serif;
            font-weight: 600;
            font-size: 14px;
            text-align: justify;
            margin: 0;
            height: 80%;
            letter-spacing: 4px;
            writing-mode: vertical-lr;
        }

        .wuxing-description {
            font-family: "Source Han Serif CN", serif;
            font-weight: 300;
            font-size: 12px;
            text-align: left;
            width: 100%;
            height: 100%;
            max-width: 80px;
            word-wrap: break-word;
            opacity: 0.6;
            writing-mode: vertical-lr;
            letter-spacing: 2px;
        }

        .crystal-list-container {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .crystal-list {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        .crystal-card {
            width: 100%;
            display: flex;
            align-items: center;
            gap: 4px;
            padding: 6px 12px;
            background: #F9F9F9;
            border-radius: 4px;
            flex: 1;
        }

        .crystal-image-container {
            display: flex;
            justify-content: stretch;
            align-items: stretch;
            gap: 10px;
            padding: 0 2px;
            width: 19px;
            height: 19px;
        }

        .crystal-image {
            width: 16px;
            height: 16px;
        }

        .crystal-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 6px;
            flex: 1;
        }

        .crystal-name {
            font-weight: 400;
            font-size: 12px;
            text-align: center;
            color: #1f1722;
        }

        .crystal-effect {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .crystal-effect-line {
            width: 1px;
            height: 12px;
            background: #e2dcd6;
        }

        .crystal-effect-text {
            font-family: "Noto Sans SC", sans-serif;
            font-weight: 400;
            font-size: 12px;
            text-align: center;
            color: #1f1722;
            opacity: 0.6;
            white-space: nowrap;
        }
    </style>
</head>

<body>
    <div class="poster" id="poster">
        <div class="content-card-wrapper">
            <div class="content-card">
                <div class="main-image-container">
                    <img class="main-image" src=${crystalData?.image_url} alt="海报主图">
                </div>
                <div class="content-container">
                    <div class="design-no">
                        设计编号：${crystalData?.id}
                    </div>
                    <div class="design-title">
                        ${crystalData?.word_info?.name}
                    </div>
                    <div class="design-desc-container">
                        <div class="design-desc-right">
                            <div class="design-desc-right-top">
                                ${crystalData?.word_info?.recommendation_text}
                            </div>
                            <div class="design-desc-right-bottom">
                                <div class="design-desc-right-bottom-title">
                                    <img src=${WEAR_TIP_ICON} class="title-image" />
                                    <div>佩戴指南</div>
                                </div>
                                <div class="design-desc-right-bottom-content">
                                    天然水晶佩戴一段时间后建议定期净化噢~可以用清水冲洗或在月光下放置一晚，以保持水晶的能量纯净和光泽度。
                                </div>
                            </div>
                        </div>
                        <div class="design-desc-left">
                            <img class="wuxing-image" src=${wuxingConfig.bgUrl} />
                            <div class="wuxing-content">
                                <div class="wuxing-content-right">
                                    <img class="wuxing-icon" src=${wuxingConfig.iconUrl} />
                                    <div class="wuxing-text" style="color: ${wuxingConfig.textColor}">
                                        日干为${crystalData?.word_info?.rizhu}
                                    </div>
                                </div>
                                <div class="wuxing-description" style="color: ${wuxingConfig.textColor}">
                                    五行属性喜${crystalData?.word_info?.wuxing?.join('、')}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="crystal-list-container">
                        <div class="design-desc-right-bottom-title">
                            <img src=${CRYSTAL_MATERIAL} class="title-image" />    
                            <div>水晶材料</div>
                        </div>
                        <div class="crystal-list">
                        ${crystalData?.word_info?.bead_ids_deduplication?.map((item) => `
                            <div class="crystal-card">
                                <div class="crystal-image-container">
                                    <img src="${item.image_url}"
                                        class="crystal-image" />
                                </div>
                                <div class="crystal-content">
                                    <div class="crystal-name">
                                        ${item.name}「${item.wuxing}」
                                    </div>
                                    <div class="crystal-effect">
                                        <div class="crystal-effect-line"></div>
                                        <div class="crystal-effect-text">${item.function}</div> 
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        </div>
</body>

</html>
  `;
}