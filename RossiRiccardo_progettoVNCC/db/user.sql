USE bucketlist;

CREATE TABLE bucketlist.tbl_user (
  user_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  user_name LONGTEXT NULL,
  user_username LONGTEXT NULL,
  user_password LONGTEXT NULL,
  PRIMARY KEY (user_id)
);

DELIMITER //
CREATE DEFINER='root'@'localhost' PROCEDURE sp_createUser(IN p_name LONGTEXT, IN p_username LONGTEXT, IN p_password LONGTEXT)
BEGIN
	IF (select exists(select 1 from tbl_user where user_username = p_username)) THEN
		select 'Username Exists !!';
	ELSE
		INSERT INTO tbl_user(user_name, user_username, user_password) VALUES(p_name, p_username, p_password);
	END IF;
END//
DELIMITER ;


