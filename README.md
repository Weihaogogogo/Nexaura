# SEO Article Backend - 云服务器部署版本

这是 SEO 文章生成系统的云服务器部署版本，只包含运行所需的核心文件。

## 包含的文件和目录

### 后端核心文件
- `app.py` - Flask 应用入口
- `config.py` - 配置文件
- `exts.py` - Flask 扩展
- `requirements_production.txt` - 生产环境依赖

### 后端核心目录
- `blueprints/` - 路由蓝图
- `utils/` - 工具函数
- `models/` - 数据模型

### 前端构建产物
- `fronted/dist/` - 前端构建后的静态文件

## 部署说明

1. 将代码拉取到云服务器
2. 使用云服务器上的 Docker 配置文件进行部署
3. 前端静态文件位于 `fronted/dist/` 目录

## 仓库说明

此仓库使用白名单模式的 `.gitignore`，只保留云服务器运行必需的文件，排除了：
- 开发工具文件
- 文档文件
- Docker 配置文件（云服务器有自己的配置）
- 环境配置文件
- 其他部署相关脚本 