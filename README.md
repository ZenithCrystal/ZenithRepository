# AI新闻聚合器

这是一个自动收集当天AI领域最新新闻并整理成网页的工具。通过多种搜索引擎和新闻源获取最新AI相关资讯，并将其整合到一个美观、易于阅读的HTML页面中。

## 功能特点

- **自动搜集当天的AI相关新闻**：每日自动从多个来源获取最新AI领域动态
- **多来源新闻收集**：支持Google、Bing等多个搜索引擎和专业AI新闻网站
- **智能内容整理**：自动提取新闻标题、摘要和链接，避免重复内容
- **美观的HTML页面展示**：使用现代化设计生成易于阅读的新闻页面
- **响应式设计**：自适应不同设备屏幕尺寸，包括手机、平板和电脑
- **分类展示**：根据新闻内容和来源进行智能分类
- **离线阅读支持**：生成的HTML文件可以保存并离线查看
- **定制化选项**：可以通过修改配置调整新闻来源和展示方式
- **定制化选项**：可以通过修改配置调整新闻来源和展示方式
- **新闻分类展示**：根据新闻内容和来源进行智能分类
- **离线阅读支持**：生成的HTML文件可以保存并离线查看
- **新闻内容翻译**：将新闻标题自动翻译成中文

## 系统要求

- Python 3.6 或更高版本
- 互联网连接（用于获取新闻）
- 支持HTML5的现代浏览器（用于查看生成的新闻页面）

## 安装步骤

### 1. 安装Python

确保已安装Python 3.6或更高版本。可以从[Python官网](https://www.python.org/downloads/)下载并安装。

安装时，请确保勾选「Add Python to PATH」选项，这样可以在命令行中直接使用Python和pip命令。

![Python安装示例](https://www.python.org/static/community_logos/python-logo.png)

### 2. 下载项目

您可以通过以下方式获取项目代码：

- 克隆Git仓库（如果有）
- 下载项目ZIP包并解压
- 直接复制项目文件到本地文件夹

### 3. 验证Python安装

打开命令提示符（CMD）或PowerShell，输入以下命令验证Python是否正确安装：

```
python --version
```

您应该看到类似于`Python 3.9.5`的输出，版本号可能会有所不同。

### 4. 安装依赖包

有多种方式安装所需的依赖包：

#### 方式一：使用requirements.txt文件（推荐）

此文件包含了项目运行所需的所有依赖库，包括 `requests` (用于网络请求), `beautifulsoup4` (用于解析HTML), 以及 `deep-translator` (用于将新闻标题翻译成中文)。

在项目目录下，打开命令提示符或PowerShell，运行：

```
python -m pip install -r requirements.txt
```

如果上述命令出错，可以尝试：

```
py -m pip install -r requirements.txt
```

#### 方式二：直接安装必要的包

```
python -m pip install requests==2.31.0 beautifulsoup4==4.12.2
```

或

```
py -m pip install requests==2.31.0 beautifulsoup4==4.12.2
```

## 使用方法

### 基本使用

运行以下命令启动AI新闻聚合器：

```
python ai_news_aggregator.py
```

如果上述命令无法运行，请尝试：

```
py ai_news_aggregator.py
```

程序将自动：
1. 搜集当天的AI新闻（这可能需要几分钟时间）
2. 生成HTML页面（ai_news.html）
3. 在控制台输出HTML文件的路径

生成的HTML文件可以直接在浏览器中打开查看。

### 高级使用

#### 使用高级新闻收集器

项目还提供了一个高级版本的新闻收集器，具有更多功能：

```
python advanced_ai_news_collector.py
```

或使用便捷的运行脚本：

```
python run_ai_news_collector.py
```

#### 自定义新闻来源

您可以通过编辑`ai_news_aggregator.py`文件中的`news_sources`列表来添加或修改新闻来源。

#### 调整搜索关键词

可以修改`queries`列表来自定义搜索关键词，以获取更符合您兴趣的AI新闻。

#### 定时自动运行

您可以使用操作系统的任务计划功能（如Windows的任务计划程序或Linux的cron）设置定时任务，每天自动运行新闻聚合器。

**Windows示例（创建批处理文件）：**

创建一个名为`run_daily.bat`的文件，内容如下：

```batch
@echo off
cd /d %~dp0
python ai_news_aggregator.py
```

然后在任务计划程序中设置每天运行此批处理文件。

## 文件说明

- `ai_news_aggregator.py`: 主程序脚本，负责收集和整理新闻
- `advanced_ai_news_collector.py`: 高级版新闻收集器，提供更多功能
- `run_ai_news_collector.py`: 便捷的运行脚本
- `template.html`: HTML页面模板，定义了生成页面的基本结构
- `style.css`: 页面样式文件，控制生成页面的外观
- `requirements.txt`: 项目依赖列表，用于快速安装所需包 (包括 `requests`, `beautifulsoup4`, `deep-translator`)
- `ai_news.html`: 程序生成的新闻页面（运行后生成）

## 自定义页面样式

如果您想修改生成的新闻页面的外观，可以编辑`style.css`文件。该文件包含了控制页面布局、颜色、字体等样式的CSS代码。

## 常见问题解决

### 无法识别pip命令

如果遇到「pip不是内部或外部命令」的错误，请尝试以下方法：

1. 使用`python -m pip`代替直接使用`pip`
2. 检查Python是否已添加到系统PATH中
3. 重新打开命令提示符或PowerShell
4. 如果使用的是虚拟环境，确保已激活该环境

### 代理连接问题

如果在安装依赖包时遇到类似以下的代理错误：

```
ProxyError('Cannot connect to proxy.', NewConnectionError(...): Failed to establish a new connection: [WinError 10061] 由于目标计算机积极拒绝，无法连接。
```

请尝试以下解决方法：

1. **临时禁用代理**：在命令行中执行以下命令临时禁用代理设置

   ```
   # Windows CMD
   set HTTP_PROXY=
   set HTTPS_PROXY=
   
   # Windows PowerShell
   $env:HTTP_PROXY=""
   $env:HTTPS_PROXY=""
   ```

2. **使用--no-proxy参数**：安装时添加--no-proxy参数

   ```
   python -m pip install -r requirements.txt --no-proxy
   ```

3. **修改pip配置**：创建或编辑pip.ini文件（Windows）

   文件位置：`%APPDATA%\pip\pip.ini`或`%USERPROFILE%\pip\pip.ini`
   
   添加以下内容：
   ```
   [global]
   proxy = 
   ```

4. **检查系统代理设置**：检查并更正Windows系统代理设置

### 新闻获取失败

如果程序无法获取新闻，可能是由于以下原因：

1. **网络连接问题**：检查您的互联网连接是否正常
2. **搜索引擎限制**：某些搜索引擎可能会限制频繁的自动查询，可以尝试：
   - 减少查询频率
   - 使用不同的搜索引擎
   - 添加更多备用新闻源
3. **用户代理问题**：某些网站可能会拒绝特定的用户代理，可以尝试修改代码中的请求头

### HTML页面显示异常

如果生成的HTML页面显示不正常，可能是由于以下原因：

1. **模板文件丢失**：确保`template.html`文件存在且内容完整
2. **样式文件丢失**：确保`style.css`文件存在且内容完整
3. **浏览器兼容性**：尝试使用不同的现代浏览器（如Chrome、Firefox、Edge等）

### 其他问题

- 本工具依赖网络连接获取新闻，请确保您的网络连接稳定
- 爬取的内容仅供参考，请遵守相关法律法规和网站的使用条款
- 如遇到网络限制问题，可能需要调整代码中的请求头或使用代理
- 如果您遇到其他问题，可以尝试查看程序输出的错误信息，或者搜索相关解决方案

## 项目贡献

欢迎对本项目进行改进和贡献！您可以通过以下方式参与：

- 提交bug报告或功能建议
- 改进代码和文档
- 添加新的新闻源或功能

## 许可证

本项目采用开源许可证，您可以自由使用、修改和分发，但请遵守相关法律法规。

## 免责声明

- 本工具仅用于学习和研究目的
- 使用本工具获取的新闻内容版权归原作者或网站所有
- 使用本工具时请遵守相关法律法规和网站的使用条款
- 开发者不对使用本工具产生的任何后果负责