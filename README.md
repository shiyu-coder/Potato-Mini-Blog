# Potato Mini Blog
施宇 191250119

![](https://img.shields.io/badge/Django-2.2-brightgreen.svg)![](https://img.shields.io/badge/Python-3.7-yellowgreen)![](https://img.shields.io/badge/Gunicorn-20.0.4-blue)![](https://img.shields.io/badge/Ubuntu-20.04.1-orange)![](https://img.shields.io/badge/MySQL-8.0.23-red)![](https://img.shields.io/badge/Nginx-1.18.0-lightgrey)

## 项目用途

Potato Mini Blog是一款迷你博客平台，麻雀虽小五脏俱全，用户不但可以在这里浏览文章，给他人的博文点赞，也可以自己注册成为用户，撰写文章并在评论区发表评论。博客平台的为响应式网页，已对常见设备显示器规格进行适配。

众所周知，南京某大学的教服系统的服务器是土豆做的，本博客平台使用的9.5块一个月的学生优惠服务器相较而言，就是迷你小土豆了，因而名为迷你土豆博客平台。

项目的整个开发历时3周，现已进行部署到：<i>http://101.132.136.117/home/</i>

源代码见：<i>https://github.com/shiyu-coder/Potato-Mini-Blog</i>

## 技术栈

### 前端

#### 编程语言

前端界面使用HTML，CSS和Javascript语言进行搭建，HTML负责网页内容和基本结构，CSS负责UI样式，Javascript负责将用户请求传送到后端并将后端数据在HTML界面中展示，同时也负责一些前端UI动态特效的实现工作

#### UI样式库

前端主要使用Bootstrap进行搭建响应式网页，部分图标、字体库和CSS框架使用Font Awesome、FancyBox和Fontastic等实现。

#### Javascript库

Javascript库是实现前端交互和动态效果的主要手段，包含DOM操作，ajax异步get和post请求封装实现、页面渲染刷新等。但许多Javascript库文件通常有数百kb大小，在宽带紧张的环境下会拖慢页面的加载速度。本项目主要使用了jQuery、Layer等js库实现

### 后端

后端使用Django2框架实现

### HTTP服务

静态文件请求使用nginx进行监听处理，动态文件请求使用gunicorn负责监听处理

### 数据库

数据库使用mysql数据库

### 开发环境及工具

本项目开发过程中使用的IDE有pycharm、vscode（用于写前端代码）、dreamweaver（写前端代码）

mysql数据库使用NaviCat 15进行一些配置工作、本地调试采用Django自带服务器

### 部署

本项目在Windows10上进行开发工作，部署到阿里云服务器上，具体服务端配置如下：

镜像信息：Ubuntu 20.04

CPU：1核；内存：2GB；系统盘：40GB

## 思路与设计

本项目采用Django2模板设计方法，采用MVT模式（模型、视图和模板）进行开发。主要包含以下功能：

### 浏览文章

用户访问文章列表界面后，后端获取到当前页数等信息，经过文章的筛选后通过Django-paginator模块（负责进行翻页显示管理）获取当前页的文章信息并返回插入到前端模板中展现给用户

### 点赞

点赞数量保存在服务器数据库中，点赞校验数据（判断是否已点过赞）保存在浏览器端的LocalStorage中，因此每个浏览器对每篇文章只允许点赞一次。点赞不要求用户登录，不允许重复点赞。点赞校验数据借助Javascript对LocalStorage进行存取，而点赞数量的更新则通过ajax请求完成

### 用户注册

用户在博客平台主页填写并提交注册表单，前端会通过Javascript对两次输入密码是否相同等内容进行检查，检查无误后将注册表单提交到后端，后端对用户名是否已重复等内容进行检查

### 用户登录

用户在登录界面填写并提交登录信息表单，后端对用户名和密码进行核实，正确后进入登陆状态，否则返回错误信息

### 用户注销

用户确定注销后，后端删除数据库中的用户信息

### 用户管理个人信息

用户编辑并提交个人信息表单，后端接收到表单后用表单中的信息对用户原有个人信息进行更新。

### 撰写文章

用户进去文章编辑界面，撰写文章并填写文章标题、标签、分类等信息，同时上传封面图后，后端在数据库中写入新的文章信息。文章正文支持富文本markdown格式，同时支持markdown语法和常见富文本选项（图片、媒体等信息）。

### 多级评论

多级评论通过Django-mptt模块利用树结构进行表示，根节点是一级品论，其他节点是次级评论。考虑到如果嵌套的层级过多，反而会导致结构混乱，并且难以排版。所以这里限制评论最多只能两级，超过两级的评论一律重置为两级。在html中，利用中序遍历算法对评论进行罗列与布局。

回复评论通过Django-ckeditor模块支持富文本输入，整个评论的编辑、发送和更新过程通过ajax完成。

### 文章搜索

用户可以通过在输入框输入关键字进行搜索，后端获取到用户的输入后会对数据库中每篇文章的标题和正文中进行搜索，返回搜索到的文章信息。具体搜索逻辑通过Django提供的Q对象完成

### 消息提醒

通过django-notifications模块实现，当用户对其他用户的文章进行点赞或对其进行评论时，会写入消息通知，并且在该用户登录时通过用户名旁的“小红点”进行提示。

## 运行效果

### 主页

![1](\image\1.png)

### 文章列表页

![2](\image\2.png)

### 文章详情

![3](D:\software_engineering\Potato Mini Blog\image\3.png)

### 用户下拉框

<img src="\image\4.png" alt="4" style="zoom:80%;" />

### 编辑文章界面

<img src="\image\5.png" alt="5" style="zoom:80%;" />

### 搜索界面

<img src="\image\6.png" alt="6" style="zoom:80%;" />

### 登录界面

<img src="\image\7.png" alt="7" style="zoom:80%;" />

### 后台管理界面

<img src="\image\8.png" alt="8" style="zoom:80%;" />

### 响应式界面

完整显示时：

<img src="\image\9.png" alt="9" style="zoom:80%;" />

移动端显示时：

<img src="\image\10.png" alt="10" style="zoom:80%;" />

展开列表：

<img src="\image\11.png" alt="11" style="zoom:80%;" />

