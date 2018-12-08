/*
Navicat MySQL Data Transfer

Source Server         : 阿里云
Source Server Version : 50722
Source Host           : 47.106.96.179:3306
Source Database       : food

Target Server Type    : MYSQL
Target Server Version : 50722
File Encoding         : 65001

Date: 2018-12-08 17:57:03
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for lb_cook_process
-- ----------------------------
DROP TABLE IF EXISTS `lb_cook_process`;
CREATE TABLE `lb_cook_process` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `food_id` int(11) DEFAULT NULL COMMENT '菜谱id',
  `step` int(11) DEFAULT NULL COMMENT '步骤排序',
  `img_url` varchar(255) DEFAULT NULL COMMENT '图片，多个逗号隔开',
  `content` varchar(500) DEFAULT NULL COMMENT '描述',
  `insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=208 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for lb_food
-- ----------------------------
DROP TABLE IF EXISTS `lb_food`;
CREATE TABLE `lb_food` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `class1_id` int(11) NOT NULL COMMENT '一级分类id',
  `class2_id` int(11) NOT NULL COMMENT '二级分类id',
  `name` varchar(255) DEFAULT NULL COMMENT '菜谱名称',
  `comment_num` int(11) DEFAULT NULL COMMENT '评论数量',
  `popularity_num` int(11) DEFAULT NULL COMMENT '人气数量',
  `step_num` int(11) DEFAULT NULL COMMENT '烹饪步骤数量',
  `html_url` varchar(255) DEFAULT NULL COMMENT '美食杰菜谱html地址',
  `logo_url` varchar(255) DEFAULT NULL COMMENT 'logo地址',
  `thumbnail_url` varchar(255) DEFAULT NULL COMMENT '列表缩略图地址',
  `is_spider_detail` tinyint(4) DEFAULT '0' COMMENT '是否爬取详情',
  `final_img_url` varchar(500) DEFAULT NULL COMMENT '成品图',
  `materials_desc` varchar(500) DEFAULT NULL COMMENT '用料描述',
  `suitable_label` varchar(255) DEFAULT NULL COMMENT '标签',
  `cooking_skill` varchar(500) DEFAULT NULL COMMENT '烹饪技巧',
  `user_grade` varchar(255) DEFAULT NULL COMMENT '用户等级',
  `user_avatar_url` varchar(255) DEFAULT NULL,
  `user_url` varchar(255) DEFAULT NULL COMMENT '用户地址',
  `user_id` int(11) DEFAULT NULL COMMENT '用户id',
  `favorite_num` int(11) DEFAULT NULL COMMENT '收藏数量',
  `ready_time` varchar(255) DEFAULT NULL COMMENT '准备时长',
  `cooking_time` varchar(255) DEFAULT NULL COMMENT '烹饪时长',
  `people_num` varchar(255) DEFAULT NULL COMMENT '适用人数',
  `cooking_difficulty` varchar(255) DEFAULT NULL COMMENT '烹饪难度',
  `cooking_taste` varchar(255) DEFAULT NULL COMMENT '口味',
  `cooking_method` varchar(255) DEFAULT NULL COMMENT '烹饪方法',
  `insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61133 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for lb_food_
-- ----------------------------
DROP TABLE IF EXISTS `lb_food_`;
CREATE TABLE `lb_food_` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `level` tinyint(4) NOT NULL DEFAULT '1',
  `insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for lb_food_class
-- ----------------------------
DROP TABLE IF EXISTS `lb_food_class`;
CREATE TABLE `lb_food_class` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `level` tinyint(4) NOT NULL DEFAULT '1',
  `insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `class_url` varchar(255) DEFAULT NULL COMMENT '分类地址',
  `total_page` int(11) DEFAULT '0',
  `current_page` int(11) DEFAULT '0',
  `tag` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=154 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for lb_food_comment
-- ----------------------------
DROP TABLE IF EXISTS `lb_food_comment`;
CREATE TABLE `lb_food_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `food_id` int(11) DEFAULT NULL,
  `user_name` varchar(255) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `user_avatar_url` varchar(255) NOT NULL,
  `user_url` varchar(255) DEFAULT '1',
  `content` varchar(500) NOT NULL,
  `comment_time` datetime NOT NULL,
  `insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for lb_food_material
-- ----------------------------
DROP TABLE IF EXISTS `lb_food_material`;
CREATE TABLE `lb_food_material` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL COMMENT '名称',
  `class1_id` int(11) DEFAULT NULL COMMENT '一级分类id',
  `class2_id` int(11) DEFAULT NULL COMMENT '二级分类id',
  `taboo_people` varchar(255) DEFAULT NULL COMMENT '禁忌人群',
  `suitable_people` varchar(255) DEFAULT NULL COMMENT '适宜人群',
  `taboo_label` varchar(255) DEFAULT NULL COMMENT '禁忌标签',
  `suitable_label` varchar(255) DEFAULT NULL COMMENT '适宜标签',
  `alias` varchar(255) DEFAULT NULL COMMENT '别名',
  `description` varchar(500) DEFAULT NULL,
  `dosage_suggest` varchar(255) DEFAULT NULL COMMENT '食量建议',
  `html_url` varchar(255) DEFAULT NULL COMMENT '美食杰材料html地址',
  `logo_url` varchar(255) DEFAULT NULL COMMENT 'logo地址',
  `insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1558 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for lb_food_material_assoc
-- ----------------------------
DROP TABLE IF EXISTS `lb_food_material_assoc`;
CREATE TABLE `lb_food_material_assoc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `food_id` int(11) DEFAULT NULL,
  `material_id` int(11) DEFAULT NULL,
  `thumbnail_url` varchar(255) DEFAULT NULL COMMENT '缩略图',
  `dosage` varchar(255) DEFAULT NULL COMMENT '用量',
  `tag` varchar(255) DEFAULT NULL COMMENT '用途 主料 辅料等',
  `name` varchar(255) NOT NULL COMMENT '名称',
  `insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=166 DEFAULT CHARSET=utf8;
