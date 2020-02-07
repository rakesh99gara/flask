# flask
## basic example folder
### database table 
CREATE TABLE `tbl_user` (
  `user_id` bigint NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) DEFAULT NULL,
  `user_email` varchar(45) DEFAULT NULL,
  `user_password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `tbl_user` */

insert  into `tbl_user`(`user_id`,`user_name`,`user_email`,`user_password`) values 
(1,'Soumitra Roy Sarkar','contact@roytuts.com','pbkdf2:sha256:50000$obX7AAZv$61ba4f743eff5113433a3fd249896deed4120e9a83deaf166477ca5fb74fcd49');

##crud

### database table
CREATE TABLE `tbl_user` (
  `user_id` bigint NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) DEFAULT NULL,
  `user_email` varchar(45) DEFAULT NULL,
  `user_password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `tbl_user` */

insert  into `tbl_user`(`user_id`,`user_name`,`user_email`,`user_password`) values 
(1,'Soumitra Roy Sarkar','contact@roytuts.com','pbkdf2:sha256:50000$obX7AAZv$61ba4f743eff5113433a3fd249896deed4120e9a83deaf166477ca5fb74fcd49');
