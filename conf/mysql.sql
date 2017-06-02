--
-- Table structure for table `users`
--
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(32) NOT NULL,
  `grp` varchar(32) NOT NULL,
  `email` varchar(128) NOT NULL,
  `mobile` varchar(16) NOT NULL,
  `pw_hash` text NOT NULL,
  `admin` boolean NOT NULL,
  `creationdate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `login` (`login`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `events`
--
DROP TABLE IF EXISTS `events`;
CREATE TABLE `events` (
  `eid` int(11) NOT NULL AUTO_INCREMENT,
  `module` varchar(32) NOT NULL,
  `user` varchar(32) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `msg` text NOT NULL,
  `status` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`eid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `spaces`
--
DROP TABLE IF EXISTS `spaces`;
CREATE TABLE `spaces` (
  `sid` varchar(80) NOT NULL,
  `uid` int(11) NOT NULL,
  `name` varchar(128) NOT NULL,
  `status` varchar(32) DEFAULT NULL,
  `severity` varchar(32) DEFAULT NULL,
  `birthday` date NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`sid`, `uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `sEvents`
--
DROP TABLE IF EXISTS `sEvents`;
CREATE TABLE `sEvents` (
  `seid` int(11) NOT NULL AUTO_INCREMENT,
  `sid` varchar(80) NOT NULL,
  `uid` int(11) NOT NULL,
  `msg` text NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`seid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `files`
--
DROP TABLE IF EXISTS `files`;
CREATE TABLE `files` (
  `fid` int(11) NOT NULL AUTO_INCREMENT,
  `sid` varchar(80) NOT NULL,
  `name` varchar(32) NOT NULL,
  `path` varchar(128) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`fid`, `sid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


