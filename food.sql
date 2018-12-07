/*
Navicat MySQL Data Transfer

Source Server         : 阿里云-food用户
Source Server Version : 50722
Source Host           : 47.106.96.179:3306
Source Database       : food

Target Server Type    : MYSQL
Target Server Version : 50722
File Encoding         : 65001

Date: 2018-12-07 16:45:42
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for lb_food
-- ----------------------------
DROP TABLE IF EXISTS `lb_food`;
CREATE TABLE `lb_food` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `class1_id` int(11) NOT NULL,
  `class2_id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `comment_num` int(11) DEFAULT NULL,
  `popularity_num` int(11) DEFAULT NULL,
  `step_num` int(11) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `logo` varchar(255) DEFAULT NULL,
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
  `url` varchar(255) DEFAULT NULL,
  `total_page` int(11) DEFAULT '0',
  `current_page` int(11) DEFAULT '0',
  `tag` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for lb_food_copy
-- ----------------------------
DROP TABLE IF EXISTS `lb_food_copy`;
CREATE TABLE `lb_food_copy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `level` tinyint(4) NOT NULL DEFAULT '1',
  `insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
