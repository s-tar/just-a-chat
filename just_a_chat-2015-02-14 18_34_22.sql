-- --------------------------------------------------------
-- Хост:                         127.0.0.1
-- Версия сервера:               5.5.25 - MySQL Community Server (GPL)
-- ОС Сервера:                   Win32
-- HeidiSQL Версия:              9.1.0.4867
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Дамп структуры для таблица chaty.s_chat
CREATE TABLE IF NOT EXISTS `s_chat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `deleted` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- Дамп данных таблицы chaty.s_chat: ~1 rows (приблизительно)
DELETE FROM `s_chat`;
/*!40000 ALTER TABLE `s_chat` DISABLE KEYS */;
INSERT INTO `s_chat` (`id`, `name`, `deleted`) VALUES
	(1, 'Demo chat', 0);
/*!40000 ALTER TABLE `s_chat` ENABLE KEYS */;


-- Дамп структуры для таблица chaty.s_chat_user
CREATE TABLE IF NOT EXISTS `s_chat_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chat_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы chaty.s_chat_user: ~0 rows (приблизительно)
DELETE FROM `s_chat_user`;
/*!40000 ALTER TABLE `s_chat_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `s_chat_user` ENABLE KEYS */;


-- Дамп структуры для таблица chaty.s_community
CREATE TABLE IF NOT EXISTS `s_community` (
  `cm_id` int(11) NOT NULL AUTO_INCREMENT,
  `cm_alias` varchar(50) DEFAULT NULL,
  `cm_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`cm_id`),
  UNIQUE KEY `Индекс 2` (`cm_alias`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- Дамп данных таблицы chaty.s_community: ~2 rows (приблизительно)
DELETE FROM `s_community`;
/*!40000 ALTER TABLE `s_community` DISABLE KEYS */;
INSERT INTO `s_community` (`cm_id`, `cm_alias`, `cm_name`) VALUES
	(1, 'fb', 'Facebook'),
	(2, 'vk', 'Vkontakte');
/*!40000 ALTER TABLE `s_community` ENABLE KEYS */;


-- Дамп структуры для таблица chaty.s_message
CREATE TABLE IF NOT EXISTS `s_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `chat_id` int(11) NOT NULL,
  `text` text NOT NULL,
  `data` text,
  `datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_system` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы chaty.s_message: ~0 rows (приблизительно)
DELETE FROM `s_message`;
/*!40000 ALTER TABLE `s_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `s_message` ENABLE KEYS */;


-- Дамп структуры для таблица chaty.s_user
CREATE TABLE IF NOT EXISTS `s_user` (
  `usr_id` int(11) NOT NULL AUTO_INCREMENT,
  `usr_email` varchar(50) DEFAULT NULL,
  `usr_password` varchar(50) DEFAULT NULL,
  `usr_firstname` varchar(50) DEFAULT NULL,
  `usr_lastname` varchar(50) DEFAULT NULL,
  `usr_photo` varchar(255) DEFAULT NULL,
  `usr_photo_s` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`usr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы chaty.s_user: ~0 rows (приблизительно)
DELETE FROM `s_user`;
/*!40000 ALTER TABLE `s_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `s_user` ENABLE KEYS */;


-- Дамп структуры для таблица chaty.s_user_community
CREATE TABLE IF NOT EXISTS `s_user_community` (
  `ucm_id` int(11) NOT NULL AUTO_INCREMENT,
  `usr_id` int(11) DEFAULT NULL,
  `cm_id` int(11) DEFAULT NULL,
  `ucm_external_id` varchar(255) DEFAULT NULL,
  `ucm_additional_data` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ucm_id`),
  KEY `FK_s_user_community_s_user` (`usr_id`),
  KEY `FK_s_user_community_s_community` (`cm_id`),
  CONSTRAINT `FK_s_user_community_s_community` FOREIGN KEY (`cm_id`) REFERENCES `s_community` (`cm_id`),
  CONSTRAINT `FK_s_user_community_s_user` FOREIGN KEY (`usr_id`) REFERENCES `s_user` (`usr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы chaty.s_user_community: ~0 rows (приблизительно)
DELETE FROM `s_user_community`;
/*!40000 ALTER TABLE `s_user_community` DISABLE KEYS */;
/*!40000 ALTER TABLE `s_user_community` ENABLE KEYS */;


-- Дамп структуры для таблица chaty.s_user_role
CREATE TABLE IF NOT EXISTS `s_user_role` (
  `usrr_id` int(11) NOT NULL AUTO_INCREMENT,
  `usr_id` int(11) DEFAULT NULL,
  `usrr_code` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`usrr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- Дамп данных таблицы chaty.s_user_role: ~0 rows (приблизительно)
DELETE FROM `s_user_role`;
/*!40000 ALTER TABLE `s_user_role` DISABLE KEYS */;
/*!40000 ALTER TABLE `s_user_role` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
