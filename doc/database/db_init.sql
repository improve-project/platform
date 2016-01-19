--
-- Database: `analysis`
--
CREATE DATABASE IF NOT EXISTS `analysis` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `analysis`;

DROP TABLE IF EXISTS `Analyses`;
CREATE TABLE IF NOT EXISTS `Analyses` (
  `AnalysisTaskID` varchar(255) CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL,
  `allowedOrganizations` text CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL,
  `Username` text CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL,
  `TaskName` text CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL,
  `AnalysisModule` text CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL,
  `AnalysisResult` text CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL,
  `Status` text CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL,
  `Notification` text CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL,
  `ConfigurationParameters` text CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL,
  `Started` bigint(20) NOT NULL,
  `Ended` bigint(20) NOT NULL,
  PRIMARY KEY (`AnalysisTaskID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Database: `exercises`
--
CREATE DATABASE IF NOT EXISTS `exercises` DEFAULT CHARACTER SET utf8 COLLATE utf8_swedish_ci;
USE `exercises`;

DROP TABLE IF EXISTS `Exercise`;
CREATE TABLE IF NOT EXISTS `Exercise` (
  `ExerciseID` varchar(255) COLLATE utf8_swedish_ci NOT NULL,
  `allowedOrganizations` text COLLATE utf8_swedish_ci NOT NULL,
  `Name` tinytext COLLATE utf8_swedish_ci NOT NULL,
  `Description` text COLLATE utf8_swedish_ci NOT NULL,
  `Settings` mediumtext COLLATE utf8_swedish_ci NOT NULL,
  PRIMARY KEY (`ExerciseID`),
  UNIQUE KEY `ExerciseID` (`ExerciseID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

DROP TABLE IF EXISTS `ExerciseResult`;
CREATE TABLE IF NOT EXISTS `ExerciseResult` (
  `ExerciseResultID` varchar(255) COLLATE utf8_swedish_ci NOT NULL,
  `ExerciseID` varchar(255) COLLATE utf8_swedish_ci NOT NULL,
  `DataIDs` mediumtext COLLATE utf8_swedish_ci NOT NULL,
  `allowedOrganizations` text COLLATE utf8_swedish_ci NOT NULL,
  `Started` int(11) NOT NULL,
  `Ended` int(11) NOT NULL,
  `Settings` mediumtext COLLATE utf8_swedish_ci NOT NULL,
  `Values` longtext COLLATE utf8_swedish_ci NOT NULL,
  `Progress` text COLLATE utf8_swedish_ci NOT NULL,
  PRIMARY KEY (`ExerciseResultID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

DROP TABLE IF EXISTS `PatientCondition`;
CREATE TABLE IF NOT EXISTS `PatientCondition` (
  `PatientConditionID` varchar(255) COLLATE utf8_swedish_ci NOT NULL,
  `Label` tinytext COLLATE utf8_swedish_ci NOT NULL,
  `Description` text COLLATE utf8_swedish_ci NOT NULL,
  `OfficialMedicalCode` tinytext COLLATE utf8_swedish_ci NOT NULL,
  `allowedOrganizations` text COLLATE utf8_swedish_ci NOT NULL,
  PRIMARY KEY (`PatientConditionID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

DROP TABLE IF EXISTS `PatientInformation`;
CREATE TABLE IF NOT EXISTS `PatientInformation` (
  `PatientInformationID` varchar(255) COLLATE utf8_swedish_ci NOT NULL,
  `BodyWeight` double NOT NULL,
  `BodyHeight` double NOT NULL,
  `UpperBodyDominantSide` enum('Right','Left') COLLATE utf8_swedish_ci NOT NULL,
  `LowerBodyDominantSide` enum('Right','Left') COLLATE utf8_swedish_ci NOT NULL,
  `BirthYear` year(4) NOT NULL,
  `Gender` enum('Male','Female','None') COLLATE utf8_swedish_ci NOT NULL,
  `allowedOrganizations` text COLLATE utf8_swedish_ci NOT NULL,
  PRIMARY KEY (`PatientInformationID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

DROP TABLE IF EXISTS `RehabilitationSet`;
CREATE TABLE IF NOT EXISTS `RehabilitationSet` (
  `RehabilitationSetID` varchar(255) COLLATE utf8_swedish_ci NOT NULL,
  `allowedOrganizations` text COLLATE utf8_swedish_ci NOT NULL,
  `ExerciseResultIDs` mediumtext COLLATE utf8_swedish_ci NOT NULL,
  `PatientConditionIDs` text COLLATE utf8_swedish_ci NOT NULL,
  `PatientInformationID` varchar(255) COLLATE utf8_swedish_ci NOT NULL,
  PRIMARY KEY (`RehabilitationSetID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;


--
-- Database: `patients`
--
CREATE DATABASE IF NOT EXISTS `patients` DEFAULT CHARACTER SET utf8 COLLATE utf8_swedish_ci;
USE `patients`;

DROP TABLE IF EXISTS `Patient`;
CREATE TABLE IF NOT EXISTS `Patient` (
  `PatientID` varchar(255) COLLATE utf8_swedish_ci NOT NULL,
  `AllowedOrganizations` text COLLATE utf8_swedish_ci NOT NULL,
  `RehabilitationSets` text COLLATE utf8_swedish_ci NOT NULL,
  `ExtID` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`PatientID`),
  UNIQUE KEY `ExtID` (`ExtID`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci AUTO_INCREMENT=101 ;


--
-- Database: `sensors`
--
CREATE DATABASE IF NOT EXISTS `sensors` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `sensors`;

DROP TABLE IF EXISTS `Data`;
CREATE TABLE IF NOT EXISTS `Data` (
  `DataID` varchar(255) NOT NULL,
  `DeviceID` varchar(255) NOT NULL,
  `allowedOrganizations` text NOT NULL,
  `Samples` longtext NOT NULL,
  `Created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`DataID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `Device`;
CREATE TABLE IF NOT EXISTS `Device` (
  `DeviceID` varchar(255) NOT NULL,
  `allowedOrganizations` text NOT NULL,
  `Name` tinytext CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL,
  `Type` tinytext CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL,
  `Description` text CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL,
  `AxisCount` tinyint(4) NOT NULL,
  `ValueUnit` tinytext NOT NULL,
  `ValueUnitAbbreviation` tinytext NOT NULL,
  `DefaultValue` double NOT NULL,
  `MaximumValue` double NOT NULL,
  `MinimumValue` double NOT NULL,
  PRIMARY KEY (`DeviceID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Database: `users`
--
CREATE DATABASE IF NOT EXISTS `users` DEFAULT CHARACTER SET utf8 COLLATE utf8_swedish_ci;
USE `users`;

DROP TABLE IF EXISTS `Organization`;
CREATE TABLE IF NOT EXISTS `Organization` (
  `OrganizationID` varchar(255) COLLATE utf8_swedish_ci NOT NULL,
  `Name` tinytext COLLATE utf8_swedish_ci NOT NULL,
  `UserIDs` mediumtext COLLATE utf8_swedish_ci NOT NULL,
  `UserGroupIDs` text COLLATE utf8_swedish_ci NOT NULL,
  PRIMARY KEY (`OrganizationID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

DROP TABLE IF EXISTS `User`;
CREATE TABLE IF NOT EXISTS `User` (
  `UserID` varchar(255) COLLATE utf8_swedish_ci NOT NULL,
  `organizationID` text COLLATE utf8_swedish_ci NOT NULL,
  `FirstName` tinytext COLLATE utf8_swedish_ci NOT NULL,
  `LastName` tinytext COLLATE utf8_swedish_ci NOT NULL,
  `UserName` varchar(255) COLLATE utf8_swedish_ci NOT NULL,
  `Password` tinytext COLLATE utf8_swedish_ci NOT NULL,
  `AccessToken` text COLLATE utf8_swedish_ci NOT NULL,
  `JobTitle` tinytext COLLATE utf8_swedish_ci NOT NULL,
  `PatientIDs` mediumtext COLLATE utf8_swedish_ci NOT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `UserName` (`UserName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

DROP TABLE IF EXISTS `UserGroup`;
CREATE TABLE IF NOT EXISTS `UserGroup` (
  `UserGroupID` varchar(255) COLLATE utf8_swedish_ci NOT NULL,
  `Name` tinytext COLLATE utf8_swedish_ci NOT NULL,
  `PermissionLevel` double NOT NULL,
  `organizationID` text COLLATE utf8_swedish_ci NOT NULL,
  `UserIDs` mediumtext COLLATE utf8_swedish_ci NOT NULL,
  PRIMARY KEY (`UserGroupID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;



/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
