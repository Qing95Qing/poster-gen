#!/bin/bash

# 安装Git
sudo yum install -y git

# 安装Node.js (使用NodeSource仓库)
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs

# 验证安装
echo "Git版本: $(git --version)"
echo "Node.js版本: $(node --version)"
echo "npm版本: $(npm --version)"

echo "安装完成!"