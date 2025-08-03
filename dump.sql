CREATE TABLE IF NOT EXISTS `t_market` (
  `market_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(1000) DEFAULT NULL,
  `headers` json DEFAULT NULL,
  `cookies` json DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`market_id`)
);
CREATE TABLE IF NOT EXISTS `t_job` (
  `job_id` int NOT NULL AUTO_INCREMENT,
  `start` datetime DEFAULT NULL,
  `finish` datetime DEFAULT NULL,
  `script` varchar(300) DEFAULT NULL,
  `params` text,
  `market_id` int DEFAULT NULL,
  `result` text,
  PRIMARY KEY (`job_id`),
  KEY `t_job_t_market_FK` (`market_id`),
  CONSTRAINT `t_job_t_market_FK` FOREIGN KEY (`market_id`) REFERENCES `t_market` (`market_id`)
);
CREATE TABLE IF NOT EXISTS `u_discount_wb` (
  `discount_wb_id` bigint NOT NULL AUTO_INCREMENT,
  `job_id` int NOT NULL,
  `nm_id` bigint DEFAULT NULL,
  `vendor_code` varchar(100) DEFAULT NULL,
  `discount_on_site` int DEFAULT NULL,
  PRIMARY KEY (`discount_wb_id`),
  KEY `u_discount_wb_t_job_FK` (`job_id`),
  CONSTRAINT `u_discount_wb_t_job_FK` FOREIGN KEY (`job_id`) REFERENCES `t_job` (`job_id`)
);
