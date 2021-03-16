/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 50725
 Source Host           : localhost:3306
 Source Schema         : tiantidb

 Target Server Type    : MySQL
 Target Server Version : 50725
 File Encoding         : 65001

 Date: 16/03/2021 21:40:21
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id`, `permission_id`) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id`, `codename`) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 49 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add admin', 7, 'add_admin');
INSERT INTO `auth_permission` VALUES (26, 'Can change admin', 7, 'change_admin');
INSERT INTO `auth_permission` VALUES (27, 'Can delete admin', 7, 'delete_admin');
INSERT INTO `auth_permission` VALUES (28, 'Can view admin', 7, 'view_admin');
INSERT INTO `auth_permission` VALUES (29, 'Can add student', 8, 'add_student');
INSERT INTO `auth_permission` VALUES (30, 'Can change student', 8, 'change_student');
INSERT INTO `auth_permission` VALUES (31, 'Can delete student', 8, 'delete_student');
INSERT INTO `auth_permission` VALUES (32, 'Can view student', 8, 'view_student');
INSERT INTO `auth_permission` VALUES (33, 'Can add contest', 9, 'add_contest');
INSERT INTO `auth_permission` VALUES (34, 'Can change contest', 9, 'change_contest');
INSERT INTO `auth_permission` VALUES (35, 'Can delete contest', 9, 'delete_contest');
INSERT INTO `auth_permission` VALUES (36, 'Can view contest', 9, 'view_contest');
INSERT INTO `auth_permission` VALUES (37, 'Can add group', 10, 'add_group');
INSERT INTO `auth_permission` VALUES (38, 'Can change group', 10, 'change_group');
INSERT INTO `auth_permission` VALUES (39, 'Can delete group', 10, 'delete_group');
INSERT INTO `auth_permission` VALUES (40, 'Can view group', 10, 'view_group');
INSERT INTO `auth_permission` VALUES (41, 'Can add sign', 11, 'add_sign');
INSERT INTO `auth_permission` VALUES (42, 'Can change sign', 11, 'change_sign');
INSERT INTO `auth_permission` VALUES (43, 'Can delete sign', 11, 'delete_sign');
INSERT INTO `auth_permission` VALUES (44, 'Can view sign', 11, 'view_sign');
INSERT INTO `auth_permission` VALUES (45, 'Can add cert', 12, 'add_cert');
INSERT INTO `auth_permission` VALUES (46, 'Can change cert', 12, 'change_cert');
INSERT INTO `auth_permission` VALUES (47, 'Can delete cert', 12, 'delete_cert');
INSERT INTO `auth_permission` VALUES (48, 'Can view cert', 12, 'view_cert');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id`, `group_id`) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id`) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id`, `permission_id`) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id`) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label`, `model`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (12, 'certms', 'cert');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (9, 'contestms', 'contest');
INSERT INTO `django_content_type` VALUES (10, 'contestms', 'group');
INSERT INTO `django_content_type` VALUES (11, 'contestms', 'sign');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (7, 'userms', 'admin');
INSERT INTO `django_content_type` VALUES (8, 'userms', 'student');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 22 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2021-03-14 17:56:52.973656');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2021-03-14 17:56:53.076774');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2021-03-14 17:56:53.382283');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2021-03-14 17:56:53.460264');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2021-03-14 17:56:53.466852');
INSERT INTO `django_migrations` VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2021-03-14 17:56:53.546491');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2021-03-14 17:56:53.582518');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0003_alter_user_email_max_length', '2021-03-14 17:56:53.624859');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0004_alter_user_username_opts', '2021-03-14 17:56:53.631972');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0005_alter_user_last_login_null', '2021-03-14 17:56:53.663735');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0006_require_contenttypes_0002', '2021-03-14 17:56:53.666705');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2021-03-14 17:56:53.673123');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0008_alter_user_username_max_length', '2021-03-14 17:56:53.729648');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2021-03-14 17:56:53.769194');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0010_alter_group_name_max_length', '2021-03-14 17:56:53.814838');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0011_update_proxy_permissions', '2021-03-14 17:56:53.821691');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2021-03-14 17:56:53.866486');
INSERT INTO `django_migrations` VALUES (18, 'certms', '0001_initial', '2021-03-14 17:56:53.890055');
INSERT INTO `django_migrations` VALUES (19, 'userms', '0001_initial', '2021-03-14 17:56:53.932837');
INSERT INTO `django_migrations` VALUES (20, 'contestms', '0001_initial', '2021-03-14 17:56:54.000939');
INSERT INTO `django_migrations` VALUES (21, 'sessions', '0001_initial', '2021-03-14 17:56:54.195779');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('3o02osdkw3tc0rltbwfm3jfm58tte7d3', '.eJxNjtEOgyAMRX9l6fMcLWxG-BlDlBgWFKOwF-O_r2Jmlvaht7097QZ-bUMc_ASG7lCqNq9uAbOB7UdWvi-jUywxuD9puy7mKYEBiRKb1xORGg2_8WRHdkNnmXGtfGyKjAeR5xBtL45r4uyKYhHJjXPLQEJFNYdSpEk_3rMbLgx_mnyhH8YKVUX1TaJBzQn7_gUOCkPK:1lM9I1:6qTuEoNPPTuOntBqfScgVeE-eWPOh51ObjVzsrk-1bo', '2021-03-30 20:59:13.346608');
INSERT INTO `django_session` VALUES ('7e8u9n6x8ia8j51js7h384yn9webzz0u', '.eJxdj80OgjAQhN9lz8b-18LJk69BGrsaDFDSLsaE8O5WBA_edr-dnczM0Oami_d2gFodYJ2aKWOCeoZMU9MGqPVhHQffI9RAmEnDFxF2hQhTWeOMrZzZOPa-7XbtOeTbMYfbduv9I6Y_n4CjT_QHh1iA5MJyviP_9LQ-s2nsog_sE5V9KSuCgAMxwn5sJJeCK6GENieu1UkfH-N9c8n4KhaXbbv6VDqCVdJIY52rjFvrVHveSBR_0ZblDYPfYM4:1lLybw:ia4gm-DRZD59uHsbnAuU5j3KdPn0RkVceAey9aphU8U', '2021-03-30 09:35:04.340392');
INSERT INTO `django_session` VALUES ('ig04k1agc8vr1qxobvwe1f91fdkv7l0b', 'eyJpc19sb2dpbiI6MCwibG9naW5fdXNlciI6bnVsbH0:1lM8j5:kbkyC2yNPwQCtG-12D-ZslUJlAXlHUIJKLK_Om6Mfxw', '2021-03-30 20:23:07.017804');
INSERT INTO `django_session` VALUES ('u5f90jk8lgx5cwwqkckpr22vcdg898xn', '.eJw1kE2OgzAMhe-SdVWcPydhNas5wyyQUIBQURWCIBmNVPXu41C6sRz7y7Ofn2za20e8TQur5YUdWZv3sLH6yfaU22lgtbkc6eLnwGrWZDsY3WTNcWDvTgoPanAtUCtjnVZnPcx-OjrScae0UNx8cZTXPs4nMft73A5Ro2UR7TQ0WY2BNxkBxxMbwuq39B7eeeo54L7QiJQjipNbIjECOAJ8Sv7Xp2NElddH9ENV3FXvakXAEJZUpTCvrQDBQXKkiNJwsNf7Gm6nzB7-SOP7fPV-o7swFKDpk3MWpLDSyp-PrZhSPNbVnQvlYiOZoz1HirYni87bnkwbThWjgGwYtIp4XRgVAAoJpty5R_Z6_QOVNYEj:1lM9Pb:zD6ngbu4mBCBEpqtjA2uBhhkOr5mLIVoBZHT0XpGrNM', '2021-03-30 21:07:03.204215');

-- ----------------------------
-- Table structure for tt_admin
-- ----------------------------
DROP TABLE IF EXISTS `tt_admin`;
CREATE TABLE `tt_admin`  (
  `admin_id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_account` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `admin_pwd` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `admin_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `admin_role` int(11) NOT NULL,
  `admin_logtime` datetime(6) NOT NULL,
  `admin_avator` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`admin_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tt_admin
-- ----------------------------
INSERT INTO `tt_admin` VALUES (1, '202085400189', '123456', 'caid', 1, '2021-03-16 20:59:13.344614', '/upload/user/avator/admin/default_avator.jpg');

-- ----------------------------
-- Table structure for tt_cert
-- ----------------------------
DROP TABLE IF EXISTS `tt_cert`;
CREATE TABLE `tt_cert`  (
  `cert_id` int(11) NOT NULL AUTO_INCREMENT,
  `cert_imgurl` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `cert_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `cert_userx` int(11) NOT NULL,
  `cert_usery` int(11) NOT NULL,
  `cert_levelx` int(11) NOT NULL,
  `cert_levely` int(11) NOT NULL,
  `cert_qrcodex` int(11) NOT NULL,
  `cert_qrcodey` int(11) NOT NULL,
  `cert_teachx` int(11) NOT NULL,
  `cert_teachy` int(11) NOT NULL,
  PRIMARY KEY (`cert_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tt_cert
-- ----------------------------
INSERT INTO `tt_cert` VALUES (1, '/upload/cert/template/temp_20210316205945047.png', '天梯赛', 1, 1, 1, 1, 1, 1, 1, 1);

-- ----------------------------
-- Table structure for tt_contest
-- ----------------------------
DROP TABLE IF EXISTS `tt_contest`;
CREATE TABLE `tt_contest`  (
  `con_id` int(11) NOT NULL AUTO_INCREMENT,
  `con_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `con_time` datetime(6) NOT NULL,
  `con_signtime` datetime(6) NOT NULL,
  `con_endtime` datetime(6) NOT NULL,
  `con_place` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `con_rule` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `con_environ` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `con_lang` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `con_level` int(11) NOT NULL,
  `con_signlink` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `con_certid` int(11) NOT NULL,
  `con_createrid` int(11) NOT NULL,
  PRIMARY KEY (`con_id`) USING BTREE,
  INDEX `tt_contest_con_certid_d9f8b960_fk_tt_cert_cert_id`(`con_certid`) USING BTREE,
  INDEX `tt_contest_con_createrid_cfe09ad1_fk_tt_admin_admin_id`(`con_createrid`) USING BTREE,
  CONSTRAINT `tt_contest_con_certid_d9f8b960_fk_tt_cert_cert_id` FOREIGN KEY (`con_certid`) REFERENCES `tt_cert` (`cert_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `tt_contest_con_createrid_cfe09ad1_fk_tt_admin_admin_id` FOREIGN KEY (`con_createrid`) REFERENCES `tt_admin` (`admin_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tt_contest
-- ----------------------------
INSERT INTO `tt_contest` VALUES (1, '天梯赛-兰州理工大学校内选拔赛', '2021-11-13 00:00:00.000000', '2021-03-13 00:00:00.000000', '2021-11-12 00:00:00.000000', '图书馆', '<p><p><p><ol><li>竞赛时长为 3 小时竞赛中 3 个不同组别使用同一套题目，在同一时间，</li></ol><p><ol><li>按照统一评分规则进行比赛。参赛队员须自行准备竞赛需要的机器和环境，参</li></ol><p><ol><li>赛现场除竞赛用机外，仅可以出现无计算功能的铅笔或水笔，以及空白草稿纸若干张。</li></ol><p><ol><li>可以使用本地的代码调试工具，但仅可用于独立完成解题代码的现场编写、调试与提交。</li></ol><p><ol><li>参赛队员须首先按照<a href=\"https://pintia.cn/download-oms-client?tab=self-check\">OMS用户自测流程</a>完成本地竞赛条件测试，可参考教学视频<a href=\"https://www.bilibili.com/video/BV1cV41167iS/\">如何搞定OMS监考系统</a>参赛队员在竞赛过程中须自己设法保证竞赛用机、联络手机的正常运转，以及网络的畅通。因队员自己的设备故障造成的影响，由队员自行承担后果。</li></ol><p><ol><li>线下参赛的队员仅可以携带无计算功能的铅笔或水笔入场。不能携带任何可用计算机处理的软件或数据(不允许任何私人携带的存储设备或计算器)。不能携带包括无线电接收器、移动电话等在内的任何类型的通讯工具。</li></ol><p><ol><li>在竞赛中，参赛队员不得和竞赛专家委员会指定的工作人员以外的人交谈。竞赛的预定时长为 3 小时，但当竞赛进行一定时间后，竞赛专家委员会主任可以因为出现不可预见的事件而调整比赛时长，一旦比赛时长发生改变，须及时地用统一方式通告所有参赛队员。当线下参赛的队员出现诸如擅自移动赛场中的设备，未经授权修改比赛软硬件，干扰他人比赛等妨碍比赛正常进行的行为时，都将被竞赛专家委员会剥夺参赛资格。</li><li>以下为明令禁止的事项。当参赛队员违背下列禁则时，将被竞赛专家委员会剥夺参赛资格禁止使用虚拟机。禁止使用双屏，无论第二屏幕是否开启。禁止佩戴耳机等电子设备。赛过程中禁止触碰 USB 接口。除通过 OMS 客户端访问比赛指定题目集外，禁止以任何形式访问任何网站。禁止使用任何形式的即时通信工具。禁止打开任何事先存储在机器上的电子资料以及任何纸质资料。禁止与监考老师以外的任何人交谈。禁止拒绝监考老师的检查要求。严禁在检查过程中擅自关闭摄像头、监考客户端。</li></ol></p></p></p></p></p></p></p><ol><li>其他关于线上竞赛的细则详见附件4“线上参赛须知”。</li></ol></p></p>', 'JDK1.5', 'Java;Python;C', 3, '', 1, 1);

-- ----------------------------
-- Table structure for tt_group
-- ----------------------------
DROP TABLE IF EXISTS `tt_group`;
CREATE TABLE `tt_group`  (
  `group_id` int(11) NOT NULL AUTO_INCREMENT,
  `group_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `group_motto` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `group_conid` int(11) NOT NULL,
  PRIMARY KEY (`group_id`) USING BTREE,
  INDEX `tt_group_group_conid_45a8a042_fk_tt_contest_con_id`(`group_conid`) USING BTREE,
  CONSTRAINT `tt_group_group_conid_45a8a042_fk_tt_contest_con_id` FOREIGN KEY (`group_conid`) REFERENCES `tt_contest` (`con_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for tt_sign
-- ----------------------------
DROP TABLE IF EXISTS `tt_sign`;
CREATE TABLE `tt_sign`  (
  `sign_id` int(11) NOT NULL AUTO_INCREMENT,
  `sign_lang` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `sign_state` int(11) NOT NULL,
  `sign_certpath` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `sign_total` int(11) NULL DEFAULT NULL,
  `sign_detial` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `sign_level` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `sign_teach` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `sign_conid` int(11) NOT NULL,
  `sign_groupid` int(11) NULL DEFAULT NULL,
  `sign_stuid` int(11) NOT NULL,
  PRIMARY KEY (`sign_id`) USING BTREE,
  INDEX `tt_sign_sign_conid_70221c9b_fk_tt_contest_con_id`(`sign_conid`) USING BTREE,
  INDEX `tt_sign_sign_stuid_ab78be5b_fk_tt_student_stu_id`(`sign_stuid`) USING BTREE,
  INDEX `tt_sign_sign_groupid_38801a33_fk_tt_group_group_id`(`sign_groupid`) USING BTREE,
  CONSTRAINT `tt_sign_sign_conid_70221c9b_fk_tt_contest_con_id` FOREIGN KEY (`sign_conid`) REFERENCES `tt_contest` (`con_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `tt_sign_sign_groupid_38801a33_fk_tt_group_group_id` FOREIGN KEY (`sign_groupid`) REFERENCES `tt_group` (`group_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `tt_sign_sign_stuid_ab78be5b_fk_tt_student_stu_id` FOREIGN KEY (`sign_stuid`) REFERENCES `tt_student` (`stu_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for tt_student
-- ----------------------------
DROP TABLE IF EXISTS `tt_student`;
CREATE TABLE `tt_student`  (
  `stu_id` int(11) NOT NULL AUTO_INCREMENT,
  `stu_no` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `stu_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `stu_pwd` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `stu_tel` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `stu_email` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `stu_major` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `stu_depart` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `stu_avator` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `stu_sex` varchar(2) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `stu_motto` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `stu_card` varchar(18) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`stu_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
