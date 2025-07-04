# Vue 3 + TypeScript + Vite

This template should help get you started developing with Vue 3 and TypeScript in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about the recommended Project Setup and IDE Support in the [Vue Docs TypeScript Guide](https://vuejs.org/guide/typescript/overview.html#project-setup).

# SEO Article Generator Frontend

SEO文章生成器前端项目，基于Vue 3 + TypeScript + Vite构建。

## 功能特性

### 文章导出功能

在文章详情页面，用户可以选择以下几种导出方式：

1. **Markdown格式** - 导出原始的Markdown文件
2. **HTML格式文章（嵌入图片）** - 导出将图片转为base64嵌入的HTML文件，无需外部依赖
3. **HTML+图片包** - 导出包含HTML文件和图片文件夹的压缩包，适合离线查看

#### 图片处理方案

**方案一：Base64嵌入图片**
- 将所有图片转换为base64编码直接嵌入HTML中
- 优点：单个文件包含所有内容，无外部依赖
- 缺点：文件较大，加载可能较慢

**方案二：压缩包下载**
- 创建包含HTML文件和images文件夹的ZIP压缩包
- HTML中使用相对路径引用图片 (`images/image_1_xxx.jpg`)
- 包含README.txt说明文件
- 优点：文件结构清晰，图片质量无损失
- 缺点：需要解压使用

## 安装与运行

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

## 技术栈

- Vue 3 + TypeScript
- Vite
- Ant Design Vue / Element Plus
- JSZip - 用于创建压缩包
- FileSaver.js - 用于文件下载
- Vue I18n - 国际化支持

## 项目结构

```
src/
├── views/app/articles/
│   └── ArticleDetailPage.vue    # 文章详情页面，包含新的导出功能
├── locales/                     # 多语言文件
├── services/api/               # API服务层
└── components/                 # 组件库
```

## 图片下载功能实现

### 核心函数

1. `convertImageToBase64()` - 将图片URL转换为base64编码
2. `extractImageUrls()` - 从HTML中提取所有图片URL  
3. `downloadImageAsBlob()` - 下载图片为Blob格式
4. `downloadContent()` - 主要下载逻辑，支持多种格式

### 使用示例

用户在文章详情页面点击"下载文章"按钮，选择相应的导出格式即可自动下载。

## 开发说明

### 新增依赖

```bash
npm install jszip file-saver
npm install --save-dev @types/file-saver
```

### 浏览器兼容性

- Base64图片嵌入：支持所有现代浏览器
- 文件下载：需要支持HTML5 download属性的浏览器
- Canvas图片处理：需要支持Canvas API的浏览器

### 注意事项

1. 图片跨域问题：使用`crossOrigin = 'anonymous'`处理
2. 大文件处理：Base64嵌入会增加文件大小约33%
3. 错误处理：对图片加载失败进行容错处理

## 更新日志

### 2024-xx-xx
- ✨ 新增文章导出功能，支持三种格式：Markdown、HTML（嵌入图片）、HTML+图片包
- 🔧 添加图片base64嵌入和压缩包下载功能
- 🌐 完善多语言支持

---

更多功能请查看 [功能文档](./docs/)
