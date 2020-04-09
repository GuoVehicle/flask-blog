/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50720
Source Host           : localhost:3306
Source Database       : awesome

Target Server Type    : MYSQL
Target Server Version : 50720
File Encoding         : 65001

Date: 2018-09-07 20:33:48
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for blogs
-- ----------------------------
DROP TABLE IF EXISTS `blogs`;
CREATE TABLE `blogs` (
  `id` varchar(50) NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `user_image` varchar(500) NOT NULL,
  `name` varchar(50) NOT NULL,
  `summary` varchar(200) NOT NULL,
  `content` mediumtext NOT NULL,
  `created_at` double NOT NULL,
  `sort_id` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of blogs
-- ----------------------------
INSERT INTO `blogs` VALUES ('0015351732514203e0ba2d7fde44ea28f6ce5e3a2110e73000', '12', 'guo', 'ss', 'Python New Study', 'python框架搭建 Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', '123456767', '1535169651.42031', '001536210399576b362d1c2e1ec4b4691de84c9b4a12f57000');
INSERT INTO `blogs` VALUES ('001535173282685239ba4bdac2d41ca840e79ddbe325918000', '12', 'guo', 'ss', 'Python New Study', 'python框架搭建 Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', '123456767', '1535169682.6852', '001536210399576b362d1c2e1ec4b4691de84c9b4a12f57000');
INSERT INTO `blogs` VALUES ('001535173288389b2be0930c138425395d90cb961848b1a000', '12', 'guo', 'ss', 'Python New Study', 'python框架搭建 Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', '123456767', '1535169688.3891', '001536210399576b362d1c2e1ec4b4691de84c9b4a12f57000');
INSERT INTO `blogs` VALUES ('00153553390361559afe76e3d314a048ce8b70103f87d52000', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', 'tttt', '../static/img/iiam.jpg', '关于python开发中遇到的问题', '真的问题', 'python如何连接数据库python如何连接数据库python如何连接数据库python如何连接数据库python如何连接数据库python如何连接数据库python如何连接数据库python如何连接数据库python如何连接数据库python如何连接数据库python如何连接数据库', '1535533903.61598', '001536210399576b362d1c2e1ec4b4691de84c9b4a12f57000');
INSERT INTO `blogs` VALUES ('001535534022826e66dba0cd4a047f7bb8e001e02621807000', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', 'tttt', '../static/img/iiam.jpg', 'Python New Study', 'Python New StudyPython New StudyPython New StudyPython New Study', 'Python New StudyPython New StudyPython New StudyPython New Stud阿斯顿撒旦 撒旦撒的yPython New StudyPython New Study', '1535534022.8264', '001536210399576b362d1c2e1ec4b4691de84c9b4a12f57000');
INSERT INTO `blogs` VALUES ('001535534029658a1f645eccbfb496e882cf1ed249d1513000', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', 'tttt', '../static/img/iiam.jpg', '关于python开发中遇到的问题', 'Python New StudyPython New StudyPython New StudyPython New Study', 'Python New StudyPython New StudyPython New StudyPython New Stud阿斯顿撒旦 撒旦撒的yPython New StudyPython New Study', '1535534029.65803', '001536210399576b362d1c2e1ec4b4691de84c9b4a12f57000');
INSERT INTO `blogs` VALUES ('0015355340353183b4b4fceca86478a917ff60f54d68030000', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', 'tttt', '../static/img/iiam.jpg', 'Python New威威撒旦', 'Python New StudyPython New StudyPython New StudyPython New Study', 'Python New StudyPython New StudyPython New StudyPython New Stud阿斯顿撒旦 撒旦撒的yPython New StudyPython New Study', '1535534035.31845', '001536210399576b362d1c2e1ec4b4691de84c9b4a12f57000');
INSERT INTO `blogs` VALUES ('001535534047812d9bbe5e625bc45b9b8e9617003eb88e8000', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', 'tttt', '../static/img/iiam.jpg', '关于python开发中遇到的问题（7）', 'Python New StudyPython New StudyPython New StudyPython New Study', 'Python New StudyPython New StudyPython New StudyPython New Stud阿斯顿撒旦 撒旦撒的yPython New StudyPython New Study', '1535534047.81286', '001536210399576b362d1c2e1ec4b4691de84c9b4a12f57000');
INSERT INTO `blogs` VALUES ('001535534057455574951ad3d7e4361a33cdc97e0c42fdc000', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', 'tttt', '../static/img/iiam.jpg', '关于python开发中遇到的问题（8）', 'Python New StudyPython New StudyPython New StudyPython New Study', 'Python New StudyPython New StudyPython New StudyPython New Stud阿斯顿撒旦 撒旦撒的yPython New StudyPython New Study', '1535534057.45505', '001536210399576b362d1c2e1ec4b4691de84c9b4a12f57000');
INSERT INTO `blogs` VALUES ('0015355340682378fc2a58e1ab74a7384a5cba647e07913000', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', 'tttt', '../static/img/iiam.jpg', '关于python开发中遇到的问题（9）', 'Python New StudyPython New StudyPython New StudyPython New Study', 'Python New StudyPython New StudyPython New StudyPython New Stud阿斯顿撒旦 撒旦撒的yPython New StudyPython New Study', '1535534068.2371', '001536210399576b362d1c2e1ec4b4691de84c9b4a12f57000');
INSERT INTO `blogs` VALUES ('0015355340784745500b5f078d142e5bfee6374b06aa185000', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', 'tttt', '../static/img/iiam.jpg', '关于python开发中遇到的问题（10）', 'Python New StudyPython New StudyPython New StudyPython New Study', 'Python New StudyPython New StudyPython New StudyPython New Stud阿斯顿撒旦 撒旦撒的yPython New StudyPython New Study', '1535534078.47453', '001536210399576b362d1c2e1ec4b4691de84c9b4a12f57000');
INSERT INTO `blogs` VALUES ('0015355340911577695b7f41d144532bb909daf4f6fee68000', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', 'tttt', '../static/img/iiam.jpg', '关于python开发中遇到的问题（11）', 'Python New StudyPython New StudyPython New StudyPython New Study', 'Python New StudyPython New StudyPython New StudyPython New Stud阿斯顿撒旦 撒旦撒的yPython New StudyPython New Study', '1535534091.15731', '001536210399576b362d1c2e1ec4b4691de84c9b4a12f57000');
INSERT INTO `blogs` VALUES ('00153553410434974c6e12125be4fd58c1ef1c5680dfdf2000', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', 'tttt', '../static/img/iiam.jpg', '关于python开发中遇到的问题（分页楼）', 'Python New StudyPython New StudyPython New StudyPython New Study', 'Python New StudyPython New StudyPython New StudyPython New Stud阿斯顿撒旦 撒旦撒的yPython New StudyPython New Study', '1535534104.34976', '001536210399576b362d1c2e1ec4b4691de84c9b4a12f57000');
INSERT INTO `blogs` VALUES ('0015356319098092a5e6e15db264ea694688f4e65f450f1000', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', '总部管理', '../static/img/iiam.jpg', '关于python开发中遇到的问题（13）', '关于python开发中遇到的问题（13）呃呃', '网站部署上线后，是不是总觉得味道淡了点儿！没错，就像廖老师所说：“在移动互联网浪潮席卷而来的今天，一个网站没有上线移动App，出门根本不好意思跟人打招呼”。然而，android手机app要用java开发，苹果手机iOS系统app要用swift等开发，难道又要埋头苦学这些语言吗？别慌，本文教你在已有网站开发编程基础上利用Framework7和Cordova跨平台开发移动App，想想就有些激动呢！\n\n一、Framework7简介\n\nFramework7 是一款免费、开源的移动HTML框架，主要用于开发混合手机App或者网页App，某些应用场景的体验几乎与原生开发的 iOS 和 Android 应用一模一样，同时也是一款不可获取的应用原型快速开发及展示工具。\n\nFramework7 主要的作用就是让你有机会能够使用 HTML，CSS 和 JavaScript 简单明了地开发 iOS 和 Android 应用。Framework7 是完全开放的，它完全没有限制你进行打开脑洞的创造，同时还提供了一些解决方案。\n\n一、Framework7资源下载\n\n使用 Framework7 来构建你的应用，是一件非常简单的事情。首先我们需要下载 Framework7资源包。当然，你也可以跳过这一步，直接使用官方提供的项目模板进行构建项目，例如：starter app templates。\n\n我们可以通过两种方式下载或安装 Framework7：\n\n1. 从 GitHub 下载\n\n我们可以从 Framework7 GitHub repository 下载 Framework7 所需的文件。\n\n2. 通过 NPM 安装\n\nnpm install framework7\n\n从下载好的压缩包里的目录 dist/css 和 dist/js 可以找到我们需要的所有文件\n\n三、 HTML代码UI布局\n\n<!DOCTYPE html>\n<html>\n  <head>\n    <!-- Required meta tags-->\n    <meta charset=\"utf-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no, minimal-ui, viewport-fit=cover\">\n    <meta name=\"apple-mobile-web-app-capable\" content=\"yes\">\n    <!-- Color theme for statusbar -->\n    <meta name=\"theme-color\" content=\"#2196f3\">\n    <!-- Your app title -->\n    <title>My App</title>\n    <!-- Path to Framework7 Library CSS, Material Theme -->\n    <link rel=\"stylesheet\" href=\"path/to/framework7.min.css\">\n    <!-- Path to your custom app styles-->\n    <link rel=\"stylesheet\" href=\"path/to/my-app.css\">\n  </head>\n  <body>\n    <!-- App root element -->\n    <div id=\"app\">\n      <!-- Statusbar overlay -->\n      <div class=\"statusbar\"></div>\n\n      <!-- Your main view, should have \"view-main\" class -->\n      <div class=\"view view-main\">\n        <!-- Initial Page, \"data-name\" contains page name -->\n        <div data-name=\"home\" class=\"page\">\n\n          <!-- Top Navbar -->\n          <div class=\"navbar\">\n            <div class=\"navbar-inner\">\n              <div class=\"title\">Awesome App</div>\n            </div>\n          </div>\n\n          <!-- Toolbar -->\n          <div class=\"toolbar\">\n            <div class=\"toolbar-inner\">\n              <!-- Toolbar links -->\n              <a href=\"#\" class=\"link\">Link 1</a>\n              <a href=\"#\" class=\"link\">Link 2</a>\n            </div>\n          </div>\n\n          <!-- Scrollable page content -->\n          <div class=\"page-content\">\n            <p>Page content goes here</p>\n            <!-- Link to another page -->\n            <a href=\"/about/\">About app</a>\n          </div>\n        </div>\n      </div>\n    </div>\n    <!-- Path to Framework7 Library JS-->\n    <script type=\"text/javascript\" src=\"path/to/framework7.min.js\"></script>\n    <!-- Path to your app js-->\n    <script type=\"text/javascript\" src=\"path/to/my-app.js\"></script>\n  </body>\n</html>\n\n我们只需关注HTML、JS、CSS的编写，即上述代码中的my-app.js、my-app.css以及html代码，而这些是我们网站开发后已经具备的知识。当然，想要让你的App更加引人注目，你得学习下Framework7文档，而且这并不是件难事！下面我们将介绍如何使用Cordova打包App。\n\n四、 Cordova打包App 1. Cordova打包App\n\n安装NPM包管理工具 (未安装请移步官网)，然后终端使用如下命令安装Cordova：\n\nnpm install -g cordova\n\n2. 新建Cordova项目\n\ncordova create firstApp com.cordova.app\n\n上面代码中firstApp是你的项目文件夹名，com.cordova.app是什么意思可以在你的config.xml中找到 (项目文件夹下)，这里你省略这一项也无所谓。\n\n3. 打包各种平台App (以android为例)\n\n首先将你写好的HTML、JS、CSS文件替换掉项目文件夹firstApp下www子文件夹中的文件。然后终端进入项目文件夹添加平台资源后打包App：\n\ncd firstApp\ncordova platform add android\ncordova plugin add [你需要添加的插件]\ncordova build android', '1535631909.80911', '001536210399576b362d1c2e1ec4b4691de84c9b4a12f57000');
INSERT INTO `blogs` VALUES ('001536144501272e0bd6975b0224c498a85950eda0a8326000', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', '总部管理', '../static/img/iiam.jpg', 'net开发的数据库连接问题', 'net开发的数据库连接问题net开发的数据库连接问题net开发的数据库连接问题net开发的数据库连接问题', 'net开发的数据库连接问题net开发的数据库连接问题net开发的数据库连接问题net开发的数据库连接问题net开发的数据库连接问题net开发的数据库连接问题net开发的数据库连接问题net开发的数据库连接问题', '1536144501.27223', '001536210399576b362d1c2e1ec4b4691de84c9b4a12f57000');
INSERT INTO `blogs` VALUES ('0015361511621279fe236ba182c42b0af173de037e209c2000', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', '总部管理', '../static/img/iiam.jpg', '关于python开发中遇到的问题（14）', '为关于python开发中遇到的问题（14）关于python开发中遇到的问题（14）关于python开发中遇到的问题（14）关于python开发中遇到的问题（14）关于python开发中遇到的问题（14）关于python开发中遇到的问题（14）', '关于python开发中遇到的问题（14）v关于python开发中遇到的问题（14）关于python开发中遇到的问题（14）关于python开发中遇到的问题（14）', '1536151162.1274', '001536210399576b362d1c2e1ec4b4691de84c9b4a12f57000');
INSERT INTO `blogs` VALUES ('001536154876165431378d3960745249146ef347687db3d000', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', '总部管理', '../static/img/iiam.jpg', '.NET mvc模式的深刻讨论（1）', '.NET mvc模式的深刻讨论（1）.NET mvc模式的深刻讨论（1）.NET mvc模式的深刻讨论（1）.NET mvc模式的深刻讨论（1）.NET mvc模式的深刻讨论（1）.NET mvc模式的深刻讨论（1）', '.NET mvc模式的深刻讨论（1）.NET mvc模式的深刻讨论（1）.NET mvc模式的深刻讨论（1）.NET mvc模式的深刻讨论（1）.NET mvc模式的深刻讨论（1）.NET mvc模式的深刻讨论（1）.NET mvc模式的深刻讨论（1）.NET mvc模式的深刻讨论（1）.NET mvc模式的深刻讨论（1）.NET mvc模式的深刻讨论（1）', '1536154876.16526', '001536212201186b2ceffa9117649eab225e4208fb6a521000');
INSERT INTO `blogs` VALUES ('00153621224948839335ff1663246509e00ec9c3cf1b5c5000', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', '总部管理', '../static/img/iiam.jpg', '.NET mvc模式的深刻讨论（3）', '.NET mvc模式的深刻讨论（3）.NET mvc模式的深刻讨论（3）.NET mvc模式的深刻讨论（3）.NET mvc模式的深刻讨论（3）.NET mvc模式的深刻讨论（3）.NET mvc模式的深刻讨论（3）.NET mvc模式的深刻讨论（3）', '.NET mvc模式的深刻讨论（3）.NET mvc模式的深刻讨论（3）.NET mvc模式的深刻讨论（3）.NET mvc模式的深刻讨论（3）.NET mvc模式的深刻讨论（3）.NET mvc模式的深刻讨论（3）', '1536212249.48852', '001536212201186b2ceffa9117649eab225e4208fb6a521000');

-- ----------------------------
-- Table structure for comments
-- ----------------------------
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `id` varchar(50) NOT NULL,
  `blog_id` varchar(50) NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `user_image` varchar(500) NOT NULL,
  `content` mediumtext NOT NULL,
  `created_at` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of comments
-- ----------------------------
INSERT INTO `comments` VALUES ('0015354613016393f7d5a12e55f4d8a8094ec5795ae0cf4000', '0015351732514203e0ba2d7fde44ea28f6ce5e3a2110e73000', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', 'tttt', '../static/img/iam.jpg', '我的天啊 这个厉害哈', '1535461301.63901');
INSERT INTO `comments` VALUES ('001535461309479f2af6b0b1dd24ab3a945ea83848bfe33000', '0015351732514203e0ba2d7fde44ea28f6ce5e3a2110e73000', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', 'tttt', '../static/img/iam.jpg', '真的厉害', '1535461309.47983');
INSERT INTO `comments` VALUES ('001535542941225d5c6ce26246e4c3bb22804d7894e7463000', '00153553410434974c6e12125be4fd58c1ef1c5680dfdf2000', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', 'tttt', '../static/img/iiam.jpg', 'zhende lihai', '1535542941.22528');
INSERT INTO `comments` VALUES ('001536218148809351403bc182d4dbea6bdf793396c907a000', '00153621224948839335ff1663246509e00ec9c3cf1b5c5000', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', '总部管理', '../static/img/iiam.jpg', '我的天啊', '1536218148.80931');
INSERT INTO `comments` VALUES ('001536241961155a5c2698f55504fd0a8fad845bfe53bd6000', '00153621224948839335ff1663246509e00ec9c3cf1b5c5000', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', '总部管理', '../static/img/iiam.jpg', '我的天啊是撒', '1536241961.156');
INSERT INTO `comments` VALUES ('00153624595648941d27618445742988b3934f85eed3a74000', '00153621224948839335ff1663246509e00ec9c3cf1b5c5000', '00153561815465632fb5228affd47ff897294328b8684a1000', '我是游客', 'http://www.gravatar.com/avatar/1d852f1a6ab4d70e0a9261f486f2f9ac?d=mm&s=120', '我的天啊', '1536245956.48955');

-- ----------------------------
-- Table structure for sorts
-- ----------------------------
DROP TABLE IF EXISTS `sorts`;
CREATE TABLE `sorts` (
  `id` varchar(50) NOT NULL,
  `class_name` varchar(50) NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `user_image` varchar(500) NOT NULL,
  `created_at` double NOT NULL,
  `updated_at` double NOT NULL,
  `updated_user_id` varchar(50) NOT NULL,
  `updated_user_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sorts
-- ----------------------------
INSERT INTO `sorts` VALUES ('001536210399576b362d1c2e1ec4b4691de84c9b4a12f57000', 'python', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', '总部管理', '../static/img/iiam.jpg', '1536210399.57606', '1536210399.57606', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', '总部管理');
INSERT INTO `sorts` VALUES ('001536212201186b2ceffa9117649eab225e4208fb6a521000', 'NET', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', '总部管理', '../static/img/iiam.jpg', '1536212201.18609', '1536212201.18609', '001535342696216c8b89749100e4525b10ba3eeb4c651aa000', '总部管理');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `passwd` varchar(50) NOT NULL,
  `admin` tinyint(1) NOT NULL,
  `name` varchar(50) NOT NULL,
  `image` varchar(500) NOT NULL,
  `created_at` double NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_email` (`email`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('001535114526395b8ed7acf434741f0bbaa5ae37e64827b000', 'tjzxgdk@163.com', '1234567890', '0', '郭定康啊', '../static/img/iiam.jpg', '1535114526.39598');
INSERT INTO `users` VALUES ('001535342696216c8b89749100e4525b10ba3eeb4c651aa000', 'tzxgdk@134.com', '311afac5f70c611f2384f58eb310fc88489ac2e2', '1', '总部管理', '../static/img/iiam.jpg', '1535342696.21603');
INSERT INTO `users` VALUES ('00153561815465632fb5228affd47ff897294328b8684a1000', 'tjzxgdk@666.com', 'd305c06ce60418c64bb70632c5667663db3b82be', '0', '我是游客', 'http://www.gravatar.com/avatar/1d852f1a6ab4d70e0a9261f486f2f9ac?d=mm&s=120', '1535618154.65693');
