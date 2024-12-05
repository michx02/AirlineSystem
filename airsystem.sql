-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Dec 04, 2024 at 12:13 AM
-- Server version: 8.3.0
-- PHP Version: 8.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `airsystem`
--
CREATE DATABASE IF NOT EXISTS `airsystem` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `airsystem`;

-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

DROP TABLE IF EXISTS `airline`;
CREATE TABLE IF NOT EXISTS `airline` (
  `airline_name` varchar(30) NOT NULL,
  PRIMARY KEY (`airline_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`airline_name`) VALUES
('Jet Blue');

-- --------------------------------------------------------

--
-- Table structure for table `airline_staff`
--

DROP TABLE IF EXISTS `airline_staff`;
CREATE TABLE IF NOT EXISTS `airline_staff` (
  `username` varchar(20) NOT NULL,
  `user_password` varchar(20) NOT NULL,
  `first_name` varchar(15) NOT NULL,
  `last_name` varchar(15) NOT NULL,
  `date_of_birth` date NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `airline_staff`
--

INSERT INTO `airline_staff` (`username`, `user_password`, `first_name`, `last_name`, `date_of_birth`) VALUES
('alice123', 'alicepass123', 'Alice', 'Brown', '1988-09-05');

-- --------------------------------------------------------

--
-- Table structure for table `airline_staff_email_address`
--

DROP TABLE IF EXISTS `airline_staff_email_address`;
CREATE TABLE IF NOT EXISTS `airline_staff_email_address` (
  `username` varchar(20) NOT NULL,
  `email_address` varchar(30) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `airline_staff_email_address`
--

INSERT INTO `airline_staff_email_address` (`username`, `email_address`) VALUES
('alice123', 'alice.brown@jetblue.com');

-- --------------------------------------------------------

--
-- Table structure for table `airline_staff_phone_number`
--

DROP TABLE IF EXISTS `airline_staff_phone_number`;
CREATE TABLE IF NOT EXISTS `airline_staff_phone_number` (
  `username` varchar(20) NOT NULL,
  `phone_number` int NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `airline_staff_phone_number`
--

INSERT INTO `airline_staff_phone_number` (`username`, `phone_number`) VALUES
('alice123', 2147483647);

-- --------------------------------------------------------

--
-- Table structure for table `airplane`
--

DROP TABLE IF EXISTS `airplane`;
CREATE TABLE IF NOT EXISTS `airplane` (
  `airline_name` varchar(20) NOT NULL,
  `airplane_id_number` varchar(20) NOT NULL,
  `maintenance_id` varchar(20) DEFAULT NULL,
  `seats` int NOT NULL,
  `manufacturing_company` varchar(20) NOT NULL,
  `model` varchar(20) NOT NULL,
  `manufacturing_date` date NOT NULL,
  `age` int NOT NULL,
  PRIMARY KEY (`airline_name`,`airplane_id_number`),
  KEY `maintenance_id` (`maintenance_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`airline_name`, `airplane_id_number`, `maintenance_id`, `seats`, `manufacturing_company`, `model`, `manufacturing_date`, `age`) VALUES
('Jet Blue', 'A123', 'MNT456', 200, 'Boeing', '737', '2010-03-15', 14),
('Jet Blue', 'B456', 'MNT789', 250, 'Airbus', 'A320', '2012-07-22', 12),
('Jet Blue', 'C789', 'KYG677', 180, 'Boeing', '757', '2015-10-05', 9);

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

DROP TABLE IF EXISTS `airport`;
CREATE TABLE IF NOT EXISTS `airport` (
  `airport_code` varchar(20) NOT NULL,
  `airport_name` varchar(20) NOT NULL,
  `city` varchar(20) NOT NULL,
  `country` varchar(20) NOT NULL,
  `number_of_terminals` int NOT NULL,
  `type` varchar(20) NOT NULL,
  PRIMARY KEY (`airport_code`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`airport_code`, `airport_name`, `city`, `country`, `number_of_terminals`, `type`) VALUES
('001', 'JFK', 'NYC', 'USA', 8, 'Both'),
('002', 'PVG', 'Shanghai', 'China', 5, 'International');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `email_address` varchar(30) NOT NULL,
  `first_name` varchar(15) NOT NULL,
  `last_name` varchar(15) NOT NULL,
  `customer_password` varchar(20) NOT NULL,
  `building_number` int NOT NULL,
  `street` varchar(20) NOT NULL,
  `apartment_number` int NOT NULL,
  `city` varchar(20) NOT NULL,
  `state` varchar(20) NOT NULL,
  `zip` int NOT NULL,
  `passport_number` varchar(20) NOT NULL,
  `passport_exp` date NOT NULL,
  `passport_country` varchar(20) NOT NULL,
  `date_of_birth` date NOT NULL,
  PRIMARY KEY (`email_address`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`email_address`, `first_name`, `last_name`, `customer_password`, `building_number`, `street`, `apartment_number`, `city`, `state`, `zip`, `passport_number`, `passport_exp`, `passport_country`, `date_of_birth`) VALUES
('john.doe@skyhigh.com', 'John', 'Doe', 'securepass123', 123, 'Maple St', 4, 'Brooklyn', 'NY', 11201, 'P12345678', '2030-01-15', 'USA', '1990-02-10'),
('jane.smith@skyhigh.com', 'Jane', 'Smith', 'mypassword456', 456, 'Oak St', 8, 'Queens', 'NY', 11105, 'P87654321', '2031-06-10', 'UK', '1985-07-25'),
('emma.jones@skyhigh.com', 'Emma', 'Jones', 'emmapass789', 789, 'Pine St', 2, 'Manhattan', 'NY', 10019, 'P13579246', '2029-11-20', 'USA', '1995-12-30');

-- --------------------------------------------------------

--
-- Table structure for table `customerphone`
--

DROP TABLE IF EXISTS `customerphone`;
CREATE TABLE IF NOT EXISTS `customerphone` (
  `email_address` varchar(30) NOT NULL,
  `phone_number` int NOT NULL,
  PRIMARY KEY (`email_address`,`phone_number`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `customerphone`
--

INSERT INTO `customerphone` (`email_address`, `phone_number`) VALUES
('emma.jones@skyhigh.com', 2147483647),
('jane.smith@skyhigh.com', 2147483647),
('john.doe@skyhigh.com', 1234567890);

-- --------------------------------------------------------

--
-- Table structure for table `employed_by`
--

DROP TABLE IF EXISTS `employed_by`;
CREATE TABLE IF NOT EXISTS `employed_by` (
  `airline_name` varchar(20) NOT NULL,
  `username` varchar(20) NOT NULL,
  PRIMARY KEY (`airline_name`,`username`),
  KEY `username` (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `employed_by`
--

INSERT INTO `employed_by` (`airline_name`, `username`) VALUES
('Jet Blue', 'alice123');

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

DROP TABLE IF EXISTS `flight`;
CREATE TABLE IF NOT EXISTS `flight` (
  `airline_name` varchar(20) NOT NULL,
  `flight_number` varchar(20) NOT NULL,
  `depart_date` date NOT NULL,
  `depart_time` time NOT NULL,
  `depart_airport_code` varchar(20) NOT NULL,
  `arrival_date` date NOT NULL,
  `arrival_time` time NOT NULL,
  `arrival_airport_code` decimal(5,0) NOT NULL,
  `base_price` decimal(5,2) NOT NULL,
  `flight_status` varchar(20) NOT NULL,
  PRIMARY KEY (`airline_name`,`flight_number`,`depart_date`,`depart_time`),
  KEY `depart_airport_code` (`depart_airport_code`),
  KEY `arrival_airport_code` (`arrival_airport_code`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`airline_name`, `flight_number`, `depart_date`, `depart_time`, `depart_airport_code`, `arrival_date`, `arrival_time`, `arrival_airport_code`, `base_price`, `flight_status`) VALUES
('Jet Blue', 'SH123', '2025-04-01', '15:30:00', '001', '2025-04-01', '18:00:00', 2, 450.00, 'On time'),
('Jet Blue', 'SH456', '2025-04-15', '09:00:00', '002', '2025-04-15', '11:30:00', 1, 350.00, 'Delayed'),
('Jet Blue', 'SH789', '2025-05-10', '12:45:00', '001', '2025-05-10', '15:15:00', 2, 550.00, 'On time');

-- --------------------------------------------------------

--
-- Table structure for table `maintenance`
--

DROP TABLE IF EXISTS `maintenance`;
CREATE TABLE IF NOT EXISTS `maintenance` (
  `maintenance_id` varchar(20) NOT NULL,
  `start_date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_date` date NOT NULL,
  `end_time` time NOT NULL,
  PRIMARY KEY (`maintenance_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `maintenance`
--

INSERT INTO `maintenance` (`maintenance_id`, `start_date`, `start_time`, `end_date`, `end_time`) VALUES
('MNT456', '2024-07-15', '08:00:00', '2024-07-17', '17:00:00'),
('MNT789', '2024-09-01', '07:30:00', '2024-09-02', '15:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `purchase`
--

DROP TABLE IF EXISTS `purchase`;
CREATE TABLE IF NOT EXISTS `purchase` (
  `ticket_id` varchar(20) NOT NULL,
  `email_address` varchar(30) NOT NULL,
  `purchase_time` time NOT NULL,
  `purchase_date` date NOT NULL,
  `card_type` varchar(30) NOT NULL,
  `card_number` varchar(30) NOT NULL,
  `name_on_card` varchar(20) NOT NULL,
  `exp_date` date NOT NULL,
  PRIMARY KEY (`ticket_id`,`email_address`),
  KEY `email_address` (`email_address`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `purchase`
--

INSERT INTO `purchase` (`ticket_id`, `email_address`, `purchase_time`, `purchase_date`, `card_type`, `card_number`, `name_on_card`, `exp_date`) VALUES
('T1001', 'john.doe@skyhigh.com', '08:45:00', '2025-03-20', 'credit', '1234123412341234', 'John Doe', '2025-09-01'),
('T1002', 'jane.smith@skyhigh.com', '10:15:00', '2025-03-22', 'debit', '4321432143214321', 'Jane Smith', '2026-05-15'),
('T1003', 'emma.jones@skyhigh.com', '14:30:00', '2025-04-02', 'credit', '5678567856785678', 'Emma Jones', '2028-12-05');

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
CREATE TABLE IF NOT EXISTS `reviews` (
  `email_address` varchar(20) NOT NULL,
  `airline_name` varchar(20) NOT NULL,
  `flight_number` varchar(20) NOT NULL,
  `depart_date` date NOT NULL,
  `depart_time` time NOT NULL,
  `rating` decimal(2,1) NOT NULL,
  `comment` varchar(4000) DEFAULT NULL,
  PRIMARY KEY (`email_address`,`airline_name`,`flight_number`,`depart_date`,`depart_time`),
  KEY `airline_name` (`airline_name`,`flight_number`,`depart_date`,`depart_time`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `reviews`
--

INSERT INTO `reviews` (`email_address`, `airline_name`, `flight_number`, `depart_date`, `depart_time`, `rating`, `comment`) VALUES
('john.doe@skyhigh.com', 'Jet Blue', 'SH123', '2025-04-01', '15:30:00', 4.5, 'Smooth flight, great service!'),
('jane.smith@skyhigh.c', 'Jet Blue', 'SH456', '2025-04-15', '09:00:00', 3.0, 'Flight delayed, but otherwise good.'),
('emma.jones@skyhigh.c', 'Jet Blue', 'SH789', '2025-05-10', '12:45:00', 5.0, 'Excellent experience!');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
CREATE TABLE IF NOT EXISTS `ticket` (
  `ticket_id` varchar(20) NOT NULL,
  `airline_name` varchar(20) NOT NULL,
  `flight_number` varchar(20) NOT NULL,
  `depart_date` date NOT NULL,
  `depart_time` time NOT NULL,
  `calculated_price` decimal(8,2) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `date_of_birth` date NOT NULL,
  PRIMARY KEY (`ticket_id`),
  KEY `airline_name` (`airline_name`,`flight_number`,`depart_date`,`depart_time`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`ticket_id`, `airline_name`, `flight_number`, `depart_date`, `depart_time`, `calculated_price`, `first_name`, `last_name`, `date_of_birth`) VALUES
('T1001', 'Jet Blue', 'SH123', '2025-04-01', '15:30:00', 450.00, 'John', 'Doe', '1990-02-10'),
('T1002', 'Jet Blue', 'SH456', '2025-04-15', '09:00:00', 350.00, 'Jane', 'Smith', '1985-07-25'),
('T1003', 'Jet Blue', 'SH789', '2025-05-10', '12:45:00', 550.00, 'Emma', 'Jones', '1995-12-30');
--
-- Database: `mydata`
--
CREATE DATABASE IF NOT EXISTS `mydata` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `mydata`;

-- --------------------------------------------------------

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
CREATE TABLE IF NOT EXISTS `client` (
  `ID` char(5) NOT NULL,
  `name` char(200) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `gradepoint`
--

DROP TABLE IF EXISTS `gradepoint`;
CREATE TABLE IF NOT EXISTS `gradepoint` (
  `grade` varchar(2) NOT NULL,
  `point` decimal(3,1) DEFAULT NULL,
  PRIMARY KEY (`grade`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `gradepoint`
--

INSERT INTO `gradepoint` (`grade`, `point`) VALUES
('A', 4.0),
('A-', 3.7),
('B+', 3.3),
('B', 3.0),
('B-', 2.7),
('C+', 2.3),
('C', 2.0),
('C-', 1.7),
('D+', 1.3),
('D', 1.0),
('F', 0.0);
--
-- Database: `university`
--
CREATE DATABASE IF NOT EXISTS `university` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `university`;

-- --------------------------------------------------------

--
-- Table structure for table `advisor`
--

DROP TABLE IF EXISTS `advisor`;
CREATE TABLE IF NOT EXISTS `advisor` (
  `s_ID` varchar(5) NOT NULL,
  `i_ID` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`s_ID`),
  KEY `i_ID` (`i_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `advisor`
--

INSERT INTO `advisor` (`s_ID`, `i_ID`) VALUES
('00128', '45565'),
('12345', '10101'),
('23121', '76543'),
('44553', '22222'),
('45678', '22222'),
('76543', '45565'),
('76653', '98345'),
('98765', '98345'),
('98988', '76766');

-- --------------------------------------------------------

--
-- Table structure for table `classroom`
--

DROP TABLE IF EXISTS `classroom`;
CREATE TABLE IF NOT EXISTS `classroom` (
  `building` varchar(15) NOT NULL,
  `room_number` varchar(7) NOT NULL,
  `capacity` decimal(4,0) DEFAULT NULL,
  PRIMARY KEY (`building`,`room_number`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `classroom`
--

INSERT INTO `classroom` (`building`, `room_number`, `capacity`) VALUES
('Packard', '101', 500),
('Painter', '514', 10),
('Taylor', '3128', 70),
('Watson', '100', 30),
('Watson', '120', 50);

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
CREATE TABLE IF NOT EXISTS `course` (
  `course_id` varchar(8) NOT NULL,
  `title` varchar(50) DEFAULT NULL,
  `dept_name` varchar(20) DEFAULT NULL,
  `credits` decimal(2,0) DEFAULT NULL,
  PRIMARY KEY (`course_id`),
  KEY `dept_name` (`dept_name`)
) ;

--
-- Dumping data for table `course`
--

INSERT INTO `course` (`course_id`, `title`, `dept_name`, `credits`) VALUES
('BIO-101', 'Intro. to Biology', 'Biology', 4),
('BIO-301', 'Genetics', 'Biology', 4),
('BIO-399', 'Computational Biology', 'Biology', 3),
('CS-101', 'Intro. to Computer Science', 'Comp. Sci.', 4),
('CS-190', 'Game Design', 'Comp. Sci.', 4),
('CS-315', 'Robotics', 'Comp. Sci.', 3),
('CS-319', 'Image Processing', 'Comp. Sci.', 3),
('CS-347', 'Database System Concepts', 'Comp. Sci.', 3),
('EE-181', 'Intro. to Digital Systems', 'Elec. Eng.', 3),
('FIN-201', 'Investment Banking', 'Finance', 3),
('HIS-351', 'World History', 'History', 3),
('MU-199', 'Music Video Production', 'Music', 3),
('PHY-101', 'Physical Principles', 'Physics', 4);

-- --------------------------------------------------------

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
CREATE TABLE IF NOT EXISTS `department` (
  `dept_name` varchar(20) NOT NULL,
  `building` varchar(15) DEFAULT NULL,
  `budget` decimal(12,2) DEFAULT NULL,
  PRIMARY KEY (`dept_name`)
) ;

--
-- Dumping data for table `department`
--

INSERT INTO `department` (`dept_name`, `building`, `budget`) VALUES
('Biology', 'Watson', 90000.00),
('Comp. Sci.', 'Taylor', 100000.00),
('Elec. Eng.', 'Taylor', 85000.00),
('Finance', 'Painter', 120000.00),
('History', 'Painter', 50000.00),
('Music', 'Packard', 80000.00),
('Physics', 'Watson', 70000.00);

-- --------------------------------------------------------

--
-- Table structure for table `gradepoint`
--

DROP TABLE IF EXISTS `gradepoint`;
CREATE TABLE IF NOT EXISTS `gradepoint` (
  `grade` varchar(2) NOT NULL,
  `point` decimal(3,1) DEFAULT NULL,
  PRIMARY KEY (`grade`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `gradepoint`
--

INSERT INTO `gradepoint` (`grade`, `point`) VALUES
('A', 4.0),
('A-', 3.7),
('B+', 3.3),
('B', 3.0),
('B-', 2.7),
('C+', 2.3),
('C', 2.0),
('C-', 1.7),
('D+', 1.3),
('D', 1.0),
('F', 0.0);

-- --------------------------------------------------------

--
-- Table structure for table `instructor`
--

DROP TABLE IF EXISTS `instructor`;
CREATE TABLE IF NOT EXISTS `instructor` (
  `ID` varchar(5) NOT NULL,
  `name` varchar(20) NOT NULL,
  `dept_name` varchar(20) DEFAULT NULL,
  `salary` decimal(8,2) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `dept_name` (`dept_name`)
) ;

--
-- Dumping data for table `instructor`
--

INSERT INTO `instructor` (`ID`, `name`, `dept_name`, `salary`) VALUES
('10101', 'Srinivasan', 'Comp. Sci.', 65000.00),
('12121', 'Wu', 'Finance', 90000.00),
('15151', 'Mozart', 'Music', 40000.00),
('22222', 'Einstein', 'Physics', 95000.00),
('32343', 'El Said', 'History', 60000.00),
('33456', 'Gold', 'Physics', 87000.00),
('45565', 'Katz', 'Comp. Sci.', 75000.00),
('58583', 'Califieri', 'History', 62000.00),
('76543', 'Singh', 'Finance', 80000.00),
('76766', 'Crick', 'Biology', 72000.00),
('83821', 'Brandt', 'Comp. Sci.', 92000.00),
('98345', 'Kim', 'Elec. Eng.', 80000.00);

-- --------------------------------------------------------

--
-- Table structure for table `prereq`
--

DROP TABLE IF EXISTS `prereq`;
CREATE TABLE IF NOT EXISTS `prereq` (
  `course_id` varchar(8) NOT NULL,
  `prereq_id` varchar(8) NOT NULL,
  PRIMARY KEY (`course_id`,`prereq_id`),
  KEY `prereq_id` (`prereq_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `prereq`
--

INSERT INTO `prereq` (`course_id`, `prereq_id`) VALUES
('BIO-301', 'BIO-101'),
('BIO-399', 'BIO-101'),
('CS-190', 'CS-101'),
('CS-315', 'CS-101'),
('CS-319', 'CS-101'),
('CS-347', 'CS-101'),
('EE-181', 'PHY-101');

-- --------------------------------------------------------

--
-- Table structure for table `section`
--

DROP TABLE IF EXISTS `section`;
CREATE TABLE IF NOT EXISTS `section` (
  `course_id` varchar(8) NOT NULL,
  `sec_id` varchar(8) NOT NULL,
  `semester` varchar(6) NOT NULL,
  `year` decimal(4,0) NOT NULL,
  `building` varchar(15) DEFAULT NULL,
  `room_number` varchar(7) DEFAULT NULL,
  `time_slot_id` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`course_id`,`sec_id`,`semester`,`year`),
  KEY `building` (`building`,`room_number`)
) ;

--
-- Dumping data for table `section`
--

INSERT INTO `section` (`course_id`, `sec_id`, `semester`, `year`, `building`, `room_number`, `time_slot_id`) VALUES
('BIO-101', '1', 'Summer', 2009, 'Painter', '514', 'B'),
('BIO-301', '1', 'Summer', 2010, 'Painter', '514', 'A'),
('CS-101', '1', 'Fall', 2009, 'Packard', '101', 'H'),
('CS-101', '1', 'Spring', 2010, 'Packard', '101', 'F'),
('CS-190', '1', 'Spring', 2009, 'Taylor', '3128', 'E'),
('CS-190', '2', 'Spring', 2009, 'Taylor', '3128', 'A'),
('CS-315', '1', 'Spring', 2010, 'Watson', '120', 'D'),
('CS-319', '1', 'Spring', 2010, 'Watson', '100', 'B'),
('CS-319', '2', 'Spring', 2010, 'Taylor', '3128', 'C'),
('CS-347', '1', 'Fall', 2009, 'Taylor', '3128', 'A'),
('EE-181', '1', 'Spring', 2009, 'Taylor', '3128', 'C'),
('FIN-201', '1', 'Spring', 2010, 'Packard', '101', 'B'),
('HIS-351', '1', 'Spring', 2010, 'Painter', '514', 'C'),
('MU-199', '1', 'Spring', 2010, 'Packard', '101', 'D'),
('PHY-101', '1', 'Fall', 2009, 'Watson', '100', 'A');

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
CREATE TABLE IF NOT EXISTS `student` (
  `ID` varchar(5) NOT NULL,
  `name` varchar(20) NOT NULL,
  `dept_name` varchar(20) DEFAULT NULL,
  `tot_cred` decimal(3,0) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `dept_name` (`dept_name`)
) ;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`ID`, `name`, `dept_name`, `tot_cred`) VALUES
('00128', 'Zhang', 'Comp. Sci.', 102),
('12345', 'Shankar', 'Comp. Sci.', 32),
('19991', 'Brandt', 'History', 80),
('23121', 'Chavez', 'Finance', 110),
('44553', 'Peltier', 'Physics', 56),
('45678', 'Levy', 'Physics', 46),
('54321', 'Williams', 'Comp. Sci.', 54),
('55739', 'Sanchez', 'Music', 38),
('70557', 'Snow', 'Physics', 0),
('76543', 'Brown', 'Comp. Sci.', 58),
('76653', 'Aoi', 'Elec. Eng.', 60),
('98765', 'Bourikas', 'Elec. Eng.', 98),
('98988', 'Tanaka', 'Biology', 120);

-- --------------------------------------------------------

--
-- Stand-in structure for view `studentgpa`
-- (See below for the actual view)
--
DROP VIEW IF EXISTS `studentgpa`;
CREATE TABLE IF NOT EXISTS `studentgpa` (
`dept_name` varchar(20)
,`gpa` decimal(31,5)
,`id` varchar(5)
);

-- --------------------------------------------------------

--
-- Table structure for table `takes`
--

DROP TABLE IF EXISTS `takes`;
CREATE TABLE IF NOT EXISTS `takes` (
  `ID` varchar(5) NOT NULL,
  `course_id` varchar(8) NOT NULL,
  `sec_id` varchar(8) NOT NULL,
  `semester` varchar(6) NOT NULL,
  `year` decimal(4,0) NOT NULL,
  `grade` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`ID`,`course_id`,`sec_id`,`semester`,`year`),
  KEY `course_id` (`course_id`,`sec_id`,`semester`,`year`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `takes`
--

INSERT INTO `takes` (`ID`, `course_id`, `sec_id`, `semester`, `year`, `grade`) VALUES
('00128', 'CS-101', '1', 'Fall', 2009, 'A'),
('00128', 'CS-347', '1', 'Fall', 2009, 'A-'),
('12345', 'CS-101', '1', 'Fall', 2009, 'C'),
('12345', 'CS-190', '2', 'Spring', 2009, 'A'),
('12345', 'CS-315', '1', 'Spring', 2010, 'A'),
('12345', 'CS-347', '1', 'Fall', 2009, 'A'),
('19991', 'HIS-351', '1', 'Spring', 2010, 'B'),
('23121', 'FIN-201', '1', 'Spring', 2010, 'C+'),
('44553', 'PHY-101', '1', 'Fall', 2009, 'B-'),
('45678', 'CS-101', '1', 'Fall', 2009, 'F'),
('45678', 'CS-101', '1', 'Spring', 2010, 'B+'),
('45678', 'CS-319', '1', 'Spring', 2010, 'B'),
('54321', 'CS-101', '1', 'Fall', 2009, 'A-'),
('54321', 'CS-190', '2', 'Spring', 2009, 'B+'),
('55739', 'MU-199', '1', 'Spring', 2010, 'A-'),
('76543', 'CS-101', '1', 'Fall', 2009, 'A'),
('76543', 'CS-319', '2', 'Spring', 2010, 'A'),
('76653', 'EE-181', '1', 'Spring', 2009, 'C'),
('98765', 'CS-101', '1', 'Fall', 2009, 'C-'),
('98765', 'CS-315', '1', 'Spring', 2010, 'B'),
('98988', 'BIO-101', '1', 'Summer', 2009, 'A'),
('98988', 'BIO-301', '1', 'Summer', 2010, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `teaches`
--

DROP TABLE IF EXISTS `teaches`;
CREATE TABLE IF NOT EXISTS `teaches` (
  `ID` varchar(5) NOT NULL,
  `course_id` varchar(8) NOT NULL,
  `sec_id` varchar(8) NOT NULL,
  `semester` varchar(6) NOT NULL,
  `year` decimal(4,0) NOT NULL,
  PRIMARY KEY (`ID`,`course_id`,`sec_id`,`semester`,`year`),
  KEY `course_id` (`course_id`,`sec_id`,`semester`,`year`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `teaches`
--

INSERT INTO `teaches` (`ID`, `course_id`, `sec_id`, `semester`, `year`) VALUES
('10101', 'CS-101', '1', 'Fall', 2009),
('10101', 'CS-315', '1', 'Spring', 2010),
('10101', 'CS-347', '1', 'Fall', 2009),
('12121', 'FIN-201', '1', 'Spring', 2010),
('15151', 'MU-199', '1', 'Spring', 2010),
('22222', 'PHY-101', '1', 'Fall', 2009),
('32343', 'HIS-351', '1', 'Spring', 2010),
('45565', 'CS-101', '1', 'Spring', 2010),
('45565', 'CS-319', '1', 'Spring', 2010),
('76766', 'BIO-101', '1', 'Summer', 2009),
('76766', 'BIO-301', '1', 'Summer', 2010),
('83821', 'CS-190', '1', 'Spring', 2009),
('83821', 'CS-190', '2', 'Spring', 2009),
('83821', 'CS-319', '2', 'Spring', 2010),
('98345', 'EE-181', '1', 'Spring', 2009);

-- --------------------------------------------------------

--
-- Table structure for table `time_slot`
--

DROP TABLE IF EXISTS `time_slot`;
CREATE TABLE IF NOT EXISTS `time_slot` (
  `time_slot_id` varchar(4) NOT NULL,
  `day` varchar(1) NOT NULL,
  `start_hr` decimal(2,0) NOT NULL,
  `start_min` decimal(2,0) NOT NULL,
  `end_hr` decimal(2,0) DEFAULT NULL,
  `end_min` decimal(2,0) DEFAULT NULL,
  PRIMARY KEY (`time_slot_id`,`day`,`start_hr`,`start_min`)
) ;

--
-- Dumping data for table `time_slot`
--

INSERT INTO `time_slot` (`time_slot_id`, `day`, `start_hr`, `start_min`, `end_hr`, `end_min`) VALUES
('A', 'M', 8, 0, 8, 50),
('A', 'W', 8, 0, 8, 50),
('A', 'F', 8, 0, 8, 50),
('B', 'M', 9, 0, 9, 50),
('B', 'W', 9, 0, 9, 50),
('B', 'F', 9, 0, 9, 50),
('C', 'M', 11, 0, 11, 50),
('C', 'W', 11, 0, 11, 50),
('C', 'F', 11, 0, 11, 50),
('D', 'M', 13, 0, 13, 50),
('D', 'W', 13, 0, 13, 50),
('D', 'F', 13, 0, 13, 50),
('E', 'T', 10, 30, 11, 45),
('E', 'R', 10, 30, 11, 45),
('F', 'T', 14, 30, 15, 45),
('F', 'R', 14, 30, 15, 45),
('G', 'M', 16, 0, 16, 50),
('G', 'W', 16, 0, 16, 50),
('G', 'F', 16, 0, 16, 50),
('H', 'W', 10, 0, 12, 30);

-- --------------------------------------------------------

--
-- Structure for view `studentgpa`
--
DROP TABLE IF EXISTS `studentgpa`;

DROP VIEW IF EXISTS `studentgpa`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `studentgpa`  AS SELECT `student`.`ID` AS `id`, `student`.`dept_name` AS `dept_name`, (sum((`course`.`credits` * `gradepoint`.`point`)) / sum(`course`.`credits`)) AS `gpa` FROM ((((`takes` join `student` on((`takes`.`ID` = `student`.`ID`))) join `section` on(((`takes`.`course_id` = `section`.`course_id`) and (`takes`.`sec_id` = `section`.`sec_id`)))) join `course` on((`section`.`course_id` = `course`.`course_id`))) join `gradepoint` on((`takes`.`grade` = `gradepoint`.`grade`))) GROUP BY `student`.`ID`, `student`.`dept_name` ;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
