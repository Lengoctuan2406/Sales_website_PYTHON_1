-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 28, 2023 at 01:12 PM
-- Server version: 5.7.31
-- PHP Version: 7.1.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `meow_shop`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
CREATE TABLE IF NOT EXISTS `accounts` (
  `account_id` int(5) NOT NULL AUTO_INCREMENT,
  `account_name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `email` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `password` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `account_address` text COLLATE utf8_unicode_ci,
  `gender` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `phone` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `avatar` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `role` int(1) DEFAULT NULL,
  `block` int(1) DEFAULT NULL,
  `created_date_account` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_date_account` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`account_id`, `account_name`, `email`, `password`, `date_of_birth`, `account_address`, `gender`, `phone`, `avatar`, `role`, `block`, `created_date_account`, `update_date_account`) VALUES
(1, 'Lê Ngọc Tuấn', 'lengoctuan2406@gmail.com', '123456789(Tuan)', '2001-06-27', 'Hà Nội', 'Male', '0564789546', 'avatar1.png', 1, 0, '2022-06-27 15:05:00', '2023-05-26 00:00:00'),
(2, 'Lê Hoàng Khoa', 'hoangkhoa47@gmail.com', '123456789(Tuan)', '1995-06-14', 'Xã Cổ Loa, Huyện Đông Anh, Thành phố Hà Nội.', 'Male', '0358745698', 'avatar2.png', 1, 0, '2022-06-27 15:05:00', '2022-06-27 15:05:00'),
(3, 'Nguyễn Hồng Loan', 'hongloan28@gmail.com', '123456789(Tuan)', '2001-07-13', 'xã Tiến Thắng, huyện Mê Linh, Tp Hà Nội', 'Female', '0548256587', 'avatar3.png', 1, 0, '2022-06-27 15:05:00', '2022-06-27 15:05:00'),
(4, 'Lê Hồng Ngọc', 'hongngoc46@gmail.com', '123456789(Tuan)', '1998-03-17', 'xã Phúc Lâm, huyện Mỹ Đức, Tp. Hà Nội', 'Female', '0956857259', 'avatar4.png', 0, 0, '2022-06-27 15:05:00', '2023-05-27 00:00:00'),
(5, 'Nguyễn Mai Linh', 'mailinh25@gmail.com', '123456789(Tuan)', '1976-03-09', '61 Lê Văn Lương, P. Trung Hòa, Q. Cầu Giấy, TP. Hà', 'Female', '0586965487', 'avatar5.png', 0, 0, '2022-06-27 15:05:00', '2022-06-27 15:05:00'),
(6, 'Mai Hông Ngọc', 'hongngoc49@gmail.com', '123456789(Tuan)', '1995-05-11', 'X. Đa Tốn, H. Gia Lâm, TP. Hà Nội', 'Female', '0958587458', 'avatar6.png', 0, 0, '2022-06-27 15:05:00', '2022-06-27 15:05:00'),
(7, 'Lê Thanh Linh', 'thanhlinh76@gmail.com', '123456789(Tuan)', '1997-08-07', 'thôn Quỳnh Đô, Xã Vĩnh Quỳnh, Huyện Thanh Trì, Thành phố Hà Nội', 'Female', '0658745465', 'avatar7.png', 0, 0, '2022-06-27 15:05:00', '2022-06-27 15:05:00'),
(8, 'Lê Thanh Như', 'thanhnhu5@gmail.com', '123456789(Tuan)', '1998-05-12', 'P. Nhân Chính, Q. Thanh Xuân, TP. Hà Nội', 'Female', '0258985879', 'avatar8.png', 0, 0, '2022-06-27 15:05:00', '2022-06-27 15:05:00'),
(9, 'Lê Như Ngọc', 'nhungoc29@gmail.com', '123456789(Tuan)', '1996-02-12', 'Xã Thủy Xuân Tiên, Huyện Chương Mỹ, Thành phố Hà Nội', 'Female', '0258565475', 'avatar9.png', 0, 0, '2022-06-27 15:05:00', '2022-06-27 15:05:00'),
(10, 'Đỗ Thị Mai', 'domai28@gmaiil.com', '123456789(Tuan)', '1990-04-13', 'Xã Trung Tú, Huyện Ứng Hòa, Thành phố Hà Nội', 'Female', '0258985478', 'avatar10.png', 0, 0, '2022-06-27 15:05:00', '2022-06-27 15:05:00'),
(11, 'Trần Hồng Trang', 'hongtrang37@gmail.com', '123456789(Tuan)', '1999-06-10', 'xã Đại Thịnh, H. Mê Linh, Tp. Hà Nội (Ngã 3 Thường Lệ)', 'Female', '0589875489', 'avatar11.png', 0, 0, '2022-06-27 15:05:00', '2022-06-27 15:05:00'),
(12, 'Đỗ Khánh Linh', 'khanhlinh58@gmail.com', '123456789(Tuan)', '2000-02-07', 'Xã Phụng Thượng, Huyện Phúc Thọ, Thành phố Hà Nội', 'Female', '0695453216', 'avatar12.png', 0, 0, '2022-06-27 15:05:00', '2022-06-27 15:05:00'),
(13, 'Trần Ngọc Anh', 'ngocanh25@gmai.com', '123456789(Tuan)', '2000-02-08', 'Phường Thổ Quan, Quận Đống Đa, TP Hà Nội', 'Female', '0956254897', 'avatar13.png', 0, 0, '2022-06-27 15:05:00', '2022-06-27 15:05:00'),
(14, 'Trần Bảo Linh', 'baolinh57@gmail.com', '123456789(Tuan)', '1996-04-12', 'Xã Trung Tú, Huyện Ứng Hòa, Thành phố Hà Nội', 'Female', '0626512651', 'avatar14.png', 0, 0, '2022-06-27 15:05:00', '2022-06-27 15:05:00'),
(15, 'Nguyễn Quốc Hùng', 'quochung96@gmail.com', '123456789(Tuan)', '1996-07-12', 'Xuân Phương, Vân Canh, Từ Liêm , Hà Nội', 'Male', '0489465131', 'avatar15.png', 0, 0, '2022-06-27 15:05:00', '2022-06-27 15:05:00'),
(16, 'Kiều Chí Thành', 'chithanhnh@gmail.com', '123456789(Tuan)', '1996-07-20', '1174 Đường Láng, P. Láng thượng, Q. Đống Đa, TP. Hà Nội', 'Male', '0589685475', 'avatar16.png', 0, 0, '2022-06-27 15:05:00', '2022-06-27 15:05:00'),
(17, 'Trương Công Lập', 'conglapknt@gmail.com', '123456789(Tuan)', '1997-02-20', 'Xã Thủy Xuân Tiên, Huyện Chương Mỹ, Thành phố Hà Nội', 'Male', '0256454121', 'avatar17.png', 0, 0, '2022-06-27 15:05:00', '2022-06-27 15:05:00'),
(18, 'Hà  Ðức Quang', 'ducquang2@gmail.com', '123456789(Tuan)', '1993-04-01', 'P. Nhân Chính, Q. Thanh Xuân, TP. Hà Nội ', 'Male', '0546853541', 'avatar18.png', 0, 0, '2022-06-27 15:05:00', '2022-06-27 15:05:00'),
(19, 'Tiền Hoài Vỹ', 'hoaivy@gmail.com', '123456789(Tuan)', '1990-05-01', 'Thôn Cấn Thượng, Xã Cấn Hữu, Huyện Quốc Oai, Thành phố Hà Nội', 'Male', '0256485156', 'avatar19.png', 0, 0, '2022-06-27 15:05:00', '2022-06-27 15:05:00'),
(20, 'Đường Thanh Nhàn', 'thanhnhan@gmail.com', '123456789(Tuan)', '1996-05-20', 'P. Đông Ngạc, Q. Bắc Từ Liêm, TP. Hà Nội (ngã 3 Tân Xuân - Đông Ngạc)', 'Female', '0256485135', 'avatar20.png', 0, 0, '2022-06-27 15:05:00', '2022-06-27 15:05:00'),
(22, 'Tống Khánh Vi', 'khanhvi@gmail.com', '123456789(Tuan)', '1994-04-05', 'TT. Liên Quan, H. Thạch Thất, Tp. Hà Nội', 'Female', '0369524568', 'avatar22.png', 0, 0, '2022-06-27 15:05:00', '2022-06-27 15:05:00'),
(23, 'Lư Hồng Quế', 'hongque@gmail.com', '123456789(Tuan)', '1997-06-13', 'Thôn Tràng An, TT. Chúc Sơn, H. Chương Mỹ, TP. Hà Nội', 'Female', '0368547895', 'avatar23.png', 0, 0, '2022-06-27 15:05:00', '2023-05-27 00:00:00'),
(24, 'Đàm Thục Ðoan', 'thucdoan@gmail.com', '123456789(Tuan)', '1999-03-08', 'Tờ bản đồ số 10, thôn 5, xã Hạ Bằng, huyện Thạch Thất, thành phố Hà Nội', 'Female', '0358515152', 'avatar24.png', 0, 0, '2022-06-27 15:05:00', '2022-06-27 15:05:00'),
(25, 'Viên Quỳnh Dung', 'quynhdung@gmail.com', '123456789(Tuan)', '1996-03-08', 'Xã Hiền Ninh, Huyện Sóc Sơn, Thành phố Hà Nội', 'Female', '0259874256', 'avatar25.png', 0, 0, '2022-06-27 15:05:00', '2022-06-27 15:05:00');

-- --------------------------------------------------------

--
-- Table structure for table `carts`
--

DROP TABLE IF EXISTS `carts`;
CREATE TABLE IF NOT EXISTS `carts` (
  `cart_id` int(5) NOT NULL AUTO_INCREMENT,
  `account_id` int(5) DEFAULT NULL,
  `product_id` int(5) DEFAULT NULL,
  `cart_quantity` int(10) DEFAULT NULL,
  PRIMARY KEY (`cart_id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `carts`
--

INSERT INTO `carts` (`cart_id`, `account_id`, `product_id`, `cart_quantity`) VALUES
(17, 8, 26, 1),
(18, 10, 5, 1),
(21, 4, 1, 5),
(22, 4, 2, 1),
(28, 8, 8, 1);

-- --------------------------------------------------------

--
-- Table structure for table `count_others`
--

DROP TABLE IF EXISTS `count_others`;
CREATE TABLE IF NOT EXISTS `count_others` (
  `count_other_id` int(5) NOT NULL AUTO_INCREMENT,
  `count_other_name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `count_other` int(10) DEFAULT NULL,
  PRIMARY KEY (`count_other_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `count_others`
--

INSERT INTO `count_others` (`count_other_id`, `count_other_name`, `count_other`) VALUES
(1, 'account_online', 0),
(2, 'products', 29),
(3, 'customers', 17),
(4, 'employees', 4),
(5, 'suppliers', 5);

-- --------------------------------------------------------

--
-- Table structure for table `count_sales`
--

DROP TABLE IF EXISTS `count_sales`;
CREATE TABLE IF NOT EXISTS `count_sales` (
  `count_sales_id` int(5) NOT NULL AUTO_INCREMENT,
  `product_id` int(5) DEFAULT NULL,
  `count_sale` int(10) DEFAULT NULL,
  PRIMARY KEY (`count_sales_id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `count_sales`
--

INSERT INTO `count_sales` (`count_sales_id`, `product_id`, `count_sale`) VALUES
(1, 1, 3),
(2, 2, 10),
(3, 3, 0),
(4, 4, 0),
(5, 5, 1),
(6, 6, 2),
(7, 7, 2),
(8, 8, 2),
(9, 9, 2),
(10, 10, 0),
(11, 11, 0),
(12, 12, 0),
(13, 13, 0),
(14, 14, 0),
(15, 14, 0),
(16, 15, 0),
(17, 16, 0),
(18, 17, 0),
(19, 18, 0),
(20, 18, 0),
(21, 19, 0),
(22, 20, 0),
(23, 21, 0),
(24, 22, 0),
(25, 23, 0),
(26, 24, 3),
(27, 25, 7),
(28, 26, 0),
(29, 28, 0),
(30, 29, 0),
(31, 31, 0);

-- --------------------------------------------------------

--
-- Table structure for table `coupons`
--

DROP TABLE IF EXISTS `coupons`;
CREATE TABLE IF NOT EXISTS `coupons` (
  `coupon_id` int(5) NOT NULL AUTO_INCREMENT,
  `coupon_name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `discount` int(10) DEFAULT NULL,
  PRIMARY KEY (`coupon_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `coupons`
--

INSERT INTO `coupons` (`coupon_id`, `coupon_name`, `discount`) VALUES
(1, 'Decrease 5%', 5),
(2, 'Decrease 10%', 10),
(3, 'Decrease 15%', 15),
(4, 'Decrease 20%', 20),
(5, 'Decrease 25%', 25),
(6, 'Decrease 30%', 30),
(7, 'Decrease 35%', 35),
(8, 'Decrease 40%', 40),
(9, 'Decrease 45%', 45),
(10, 'Decrease 50%', 50);

-- --------------------------------------------------------

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
CREATE TABLE IF NOT EXISTS `employees` (
  `employee_id` int(5) NOT NULL AUTO_INCREMENT,
  `account_id` int(5) DEFAULT NULL,
  `employee_position` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`employee_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `employees`
--

INSERT INTO `employees` (`employee_id`, `account_id`, `employee_position`) VALUES
(2, 22, 'sale'),
(3, 23, 'sale'),
(4, 24, 'sale'),
(5, 25, 'sale'),
(6, 30, 'Manager');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
CREATE TABLE IF NOT EXISTS `orders` (
  `order_id` int(5) NOT NULL AUTO_INCREMENT,
  `account_id` int(5) DEFAULT NULL,
  `order_product_all_id` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `order_all_quantity` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `order_total` double DEFAULT NULL,
  `order_name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `order_address` text COLLATE utf8_unicode_ci,
  `order_phone` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `order_notes` text COLLATE utf8_unicode_ci,
  `date_invoice_order` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `order_status_id` int(5) DEFAULT NULL,
  PRIMARY KEY (`order_id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`order_id`, `account_id`, `order_product_all_id`, `order_all_quantity`, `order_total`, `order_name`, `order_address`, `order_phone`, `order_notes`, `date_invoice_order`, `order_status_id`) VALUES
(1, 4, '2', '1', 3.1255, 'Lê Hồng Ngọc', 'xã Phúc Lâm, huyện Mỹ Đức, Tp. Hà Nội', '0956857259', '', '2022-06-27 17:22:18', 2),
(2, 4, '8', '1', 3.1255, 'Lê Hồng Ngọc', 'xã Phúc Lâm, huyện Mỹ Đức, Tp. Hà Nội', '0956857259', '', '2022-06-28 11:56:24', 2),
(4, 4, '6', '1', 31, 'Lê Hồng Ngọc', 'xã Phúc Lâm, huyện Mỹ Đức, Tp. Hà Nội', '0956857259', '', '2022-06-29 17:28:50', 3),
(6, 4, '1', '1', 21, 'Lê Hồng Ngọc', 'xã Phúc Lâm, huyện Mỹ Đức, Tp. Hà Nội', '0956857259', '', '2022-06-27 17:35:56', 1),
(8, 5, '1', '1', 24, 'Nguyễn Mai Linh', '61 Lê Văn Lương, P. Trung Hòa, Q. Cầu Giấy, TP. Hà', '0586965487', '', '2022-06-27 17:38:06', 2),
(9, 5, '2', '2', 10, 'Nguyễn Mai Linh', '61 Lê Văn Lương, P. Trung Hòa, Q. Cầu Giấy, TP. Hà', '0586965487', '', '2022-06-27 17:38:39', 1),
(11, 5, '2', '1', 20, 'Nguyễn Mai Linh', '61 Lê Văn Lương, P. Trung Hòa, Q. Cầu Giấy, TP. Hà', '0586965487', '', '2022-06-27 17:39:09', 3),
(12, 5, '1', '1', 20, 'Nguyễn Mai Linh', '61 Lê Văn Lương, P. Trung Hòa, Q. Cầu Giấy, TP. Hà', '0586965487', '', '2022-06-27 17:40:09', 3),
(13, 6, '25', '1', 20, 'Mai Hông Ngọc', 'X. Đa Tốn, H. Gia Lâm, TP. Hà Nội', '0958587458', '', '2022-06-27 17:42:47', 3),
(14, 6, '2,8', '1,1', 20, 'Mai Hông Ngọc', 'X. Đa Tốn, H. Gia Lâm, TP. Hà Nội', '0958587458', '', '2022-06-27 17:43:12', 3),
(18, 6, '20', '1', 20, 'Mai Hông Ngọc', 'X. Đa Tốn, H. Gia Lâm, TP. Hà Nội', '0958587458', '', '2022-06-27 18:01:07', 1),
(20, 6, '26', '1', 20, 'Mai Hông Ngọc', 'X. Đa Tốn, H. Gia Lâm, TP. Hà Nội', '0958587458', '', '2022-06-27 18:03:38', 1),
(21, 7, '5', '1', 20, 'Lê Thanh Linh', 'thôn Quỳnh Đô, Xã Vĩnh Quỳnh, Huyện Thanh Trì, Thà', '0658745465', '', '2022-06-27 18:04:55', 1),
(22, 7, '6', '1', 20, 'Lê Thanh Linh', 'thôn Quỳnh Đô, Xã Vĩnh Quỳnh, Huyện Thanh Trì, Thà', '0658745465', '', '2022-06-27 18:05:13', 3),
(23, 7, '1,7', '1,1', 20, 'Lê Thanh Linh', 'thôn Quỳnh Đô, Xã Vĩnh Quỳnh, Huyện Thanh Trì, Thà', '0658745465', '', '2022-06-27 18:05:31', 1),
(24, 7, '24', '1', 20, 'Lê Thanh Linh', 'thôn Quỳnh Đô, Xã Vĩnh Quỳnh, Huyện Thanh Trì, Thà', '0658745465', '', '2022-06-27 18:06:03', 3),
(25, 7, '27', '1', 20, 'Lê Thanh Linh', 'thôn Quỳnh Đô, Xã Vĩnh Quỳnh, Huyện Thanh Trì, Thà', '0658745465', '', '2022-06-27 18:06:20', 1),
(26, 8, '9', '1', 20, 'Lê Thanh Như', 'P. Nhân Chính, Q. Thanh Xuân, TP. Hà Nội', '0258985879', '', '2022-06-27 19:14:29', 3),
(27, 8, '29', '1', 20, 'Lê Thanh Như', 'P. Nhân Chính, Q. Thanh Xuân, TP. Hà Nội', '0258985879', '', '2022-06-27 19:14:47', 1),
(28, 8, '24', '1', 20, 'Lê Thanh Như', 'P. Nhân Chính, Q. Thanh Xuân, TP. Hà Nội', '0258985879', '', '2022-06-27 19:15:10', 1),
(29, 10, '7', '2', 20, 'Đỗ Thị Mai', 'Xã Trung Tú, Huyện Ứng Hòa, Thành phố Hà Nội', '0258985478', '', '2022-06-27 19:15:58', 1),
(30, 10, '4', '2', 20, 'Đỗ Thị Mai', 'Xã Trung Tú, Huyện Ứng Hòa, Thành phố Hà Nội', '0258985478', '', '2022-06-27 19:16:14', 1),
(31, 10, '25', '2', 20, 'Đỗ Thị Mai', 'Xã Trung Tú, Huyện Ứng Hòa, Thành phố Hà Nội', '0258985478', '', '2022-06-27 19:16:36', 3),
(32, 11, '9', '2', 20, 'Trần Hồng Trang', 'xã Đại Thịnh, H. Mê Linh, Tp. Hà Nội (Ngã 3 Thường', '0589875489', '', '2022-06-27 19:17:13', 1),
(33, 11, '7', '2', 20, 'Trần Hồng Trang', 'xã Đại Thịnh, H. Mê Linh, Tp. Hà Nội (Ngã 3 Thường', '0589875489', '', '2022-06-27 19:17:35', 4),
(34, 11, '27', '2', 20, 'Trần Hồng Trang', 'xã Đại Thịnh, H. Mê Linh, Tp. Hà Nội (Ngã 3 Thường', '0589875489', '', '2022-06-27 19:17:47', 1),
(35, 12, '1', '1', 20, 'Đỗ Khánh Linh', 'Xã Phụng Thượng, Huyện Phúc Thọ, Thành phố Hà Nội', '0695453216', '', '2022-06-27 19:19:14', 3),
(36, 12, '8', '2', 20, 'Đỗ Khánh Linh', 'Xã Phụng Thượng, Huyện Phúc Thọ, Thành phố Hà Nội', '0695453216', '', '2022-06-27 19:19:25', 1),
(37, 12, '24', '2', 20, 'Đỗ Khánh Linh', 'Xã Phụng Thượng, Huyện Phúc Thọ, Thành phố Hà Nội', '0695453216', '', '2022-06-27 19:19:38', 3),
(38, 5, '25,26,2', '1,1,1', 20, 'Nguy?n Mai Linh', '', '0586965487', '', '2023-05-26 13:01:04', 1),
(39, 4, '5,25', '1,1', 20, 'Lê Hồng Ngọc', 'xã Phúc Lâm, huyện Mỹ Đức, Tp. Hà Nội', '0956857259', '', '2023-05-26 13:01:53', 1),
(40, 4, '5,25,2', '1,1,3', 20, 'Lê Hồng Ngọc', 'xã Phúc Lâm, huyện Mỹ Đức, Tp. Hà Nội, 12', '0956857259', '', '2023-05-26 13:16:43', 1),
(41, 4, '5,25,2', '1,1,3', 20, 'Lê Hồng Ngọc', 'xã Phúc Lâm, huyện Mỹ Đức, Tp. Hà Nội', '0956857259', '', '2023-05-26 13:20:30', 3),
(44, 1, '2', '4', 20, 'Nguyn Minh Hong', 'Hng Lc Hu Lc Thanh Ha', '056478954767', '', '2023-05-26 17:22:46', 3),
(45, 5, '31', '3', 20, 'Nguyễn Mai Linh', '61 Lê Văn Lương, P. Trung Hòa, Q. Cầu Giấy, TP. Hà', '0586965487', '', '2023-05-28 01:51:09', 1),
(46, 7, '8,20', '2,1', 20, 'Lê Thanh Linh', 'thôn Quỳnh Đô, Xã Vĩnh Quỳnh, Huyện Thanh Trì, Thành phố Hà Nội', '0658745465', 'Gửi tận nhà cho tôi', '2023-05-28 12:55:26', 4),
(47, 7, '23', '3', 20, 'Lê Thanh Linh', 'thôn Quỳnh Đô, Xã Vĩnh Quỳnh, Huyện Thanh Trì, Thành phố Hà Nội', '0658745465', 'Gửi tận nhà', '2023-05-28 12:58:32', 1),
(48, 7, '25,9', '2,1', 20, 'Lê Thanh Linh', 'thôn Quỳnh Đô, Xã Vĩnh Quỳnh, Huyện Thanh Trì, Thành phố Hà Nội', '0658745465', '', '2023-05-28 12:59:03', 3);

-- --------------------------------------------------------

--
-- Table structure for table `order_status`
--

DROP TABLE IF EXISTS `order_status`;
CREATE TABLE IF NOT EXISTS `order_status` (
  `order_status_id` int(5) NOT NULL AUTO_INCREMENT,
  `order_status_name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`order_status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `order_status`
--

INSERT INTO `order_status` (`order_status_id`, `order_status_name`) VALUES
(1, 'Waiting'),
(2, 'Delivery'),
(3, 'Completely'),
(4, 'Pending');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
CREATE TABLE IF NOT EXISTS `products` (
  `product_id` int(5) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `product_type_id` int(5) DEFAULT NULL,
  `supplier_id` int(5) DEFAULT NULL,
  `product_quantity` int(10) DEFAULT NULL,
  `product_description` mediumtext COLLATE utf8_unicode_ci,
  `product_price` double DEFAULT NULL,
  `product_image_1` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `product_image_2` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `product_image_3` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `product_name`, `product_type_id`, `supplier_id`, `product_quantity`, `product_description`, `product_price`, `product_image_1`, `product_image_2`, `product_image_3`) VALUES
(1, 'True Hemp™ Treats – Calming by True Leaf', 1, 2, 200, '<div>We know the difficulty of seeing our pets stressed from loud noises, separation anxiety and even our own mood swings.</div><div>This unique formulation incorporates hemp leaf, green tea, chamomile and lemon balm to help reduce tension and bring True Hemp™ CALMING to our most sensitive companions.</div><div><br></div>', 3.29, 'product1-hinh1.jpg', 'product1-hinh2.jpg', 'empty_product.png'),
(2, 'Cat Stocking with mix of cat toys and treats', 1, 2, 200, '<div>With christmas on the horizon it’s time to get your kitties the purrfect Cat Stocking filled with cat goodies! ?</div><div>Each stocking contains a mixture of cat toys and one bag of treats with a total value of £14 – £17.00 and the toys &amp; treats have been carefully selected by your very own Santa Claws Nubia</div><div>PLEASE NOTE WE HAVE A RANDOM SELECTION OF STOCKINGS NOW; HIGH QUALITY BUT IT WAS DIFFICULT TO GET SUFFICIENT STOCK IN THE SAME DESIGN!!!! PHOTO FOR REFERENCE PURPOSE ONLY AT THIS POINT!</div>', 14, 'product2-hinh1.jpg', 'product2-hinh2.jpg', 'empty_product.png'),
(3, 'Ziwipeak Daily Cat Cuisine Cans Lamb 85g', 1, 3, 200, '<div>A single-protein option for cats with protein allergies or sensitivities. Ziwi Lamb is sourced only from local New Zealand farms, ensuring the animals are free-ranging, grass-fed and finished.</div><div>3% New Zealand Green Mussel is included as a natural source of glucosamine and chondroitin, and inclusion of 7% cold-washed tripe increases palatability and aids in healthy digestion.</div><div>Out of stock</div>', 1.69, 'product3-hinh1.jpg', 'product3-hinh2.jpg', 'empty_product.png'),
(4, 'Oliver & Nubia Lucky Bags', 1, 3, 200, '<div>By popular demand we’ve now added our cat show lucky bags online. Please note that currently for Online they are delivered in a sealed grey bag due to supplier issues for the craft bags.</div><div>Each bag comes with a special selection of toys and treats purveyed by their Meowjesty King Oliver &amp; Queen Nubia.</div><div><br></div>', 15, 'product4-hinh1.jpg', 'product4-hinh2.jpg', 'product4-hinh3.jpg'),
(5, 'Newflands Hoki Bites-15grams', 1, 3, 200, 'Newflands Hoki Bites are freeze dried Hoki which are cut into small 10 mm x 10 mm cubes. They are wonderful training aides and can be easily placed in your pockets and broken into smaller portions for small dogs and cats.', 5.99, 'product5-hinh1.jpg', 'product5-hinh2.jpg', 'product5-hinh3.jpg'),
(6, 'Ziwi Peak Air Dried Cuisine Pouches Lamb 1000g', 1, 2, 200, '<div>A single-protein option for cats with protein allergies or sensitivities. Ziwi Lamb is sourced only from local New Zealand farms, ensuring the animals are free-ranging, grass-fed and finished.</div><div>For the perfect finishing touch, we add kelp as a natural vitamin and mineral source, and New Zealand Green Mussel for natural glucosamine and chondroitin.</div>', 29.99, 'product6-hinh1.jpg', 'product6-hinh2.jpg', 'product6-hinh3.jpg'),
(7, 'MycAni – Chill mal – Calming Product for Cats', 1, 2, 200, '<div>Chill mal is for all of our cats who should take a more relaxed approach to life. Panic on New Year’s Eve, excitement during car journeys, preparing for a move… The list of situations our kitties experience stress is endless. And for all the cats who find it difficult to deal with such changes and challenges in everyday life, we have developed this mixture.</div><div>We experience more and more often that cats cannot deal with our stressful everyday life and react with fear. Animals from abroad in particular can have major problems when suddenly no longer living on the street but in a 2-room apartment in the big city. Completely new influences can be really frightening! Chill out can help your cat regulate itself better.</div><div>Of course, chilling does not replace spending time with your cat, but should be used in addition.</div>', 30, 'product7-hinh1.jpg', 'product7-hinh2.jpg', 'empty_product.png'),
(8, 'Newflands Hoki Bites-60grams', 1, 2, 200, 'Newflands Hoki Bites are freeze dried Hoki which are cut into small 10 mm x 10 mm cubes. They are wonderful training aides and can be easily placed in your pockets and broken into smaller portions for small dogs and cats.', 15, 'product8-hinh1.jpg', 'product8-hinh2.jpg', 'empty_product.png'),
(9, 'Newflands Hoki Gravy', 1, 3, 200, 'Newflands Hoki Gravy is a super tasty and palatable sauce to tempt even the fussiest of eaters.&nbsp; Generously mix in with your fur baby’s food or medication to enhance the flavour and encourage them to eat.&nbsp; Comes in a 315ml squirt bottle.', 17, 'product9-hinh1.jpg', 'product9-hinh2.png', 'product9-hinh3.jpg'),
(10, 'PetAlive Natural Homeopathic Cushex-M Liquid', 2, 4, 200, '35% off your first Repeat Delivery', 36.35, 'product10-hinh1.png', 'product10-hinh2.png', 'empty_product.png'),
(11, 'Gabapentin Capsul', 2, 1, 200, 'Gabapentin’s anti-seizure capabilities have met with mixed reviews among veterinary neurologists. For pain control, gabapentin is usually used in conjunction with other pain relievers that may later be tapered away.', 0.1, 'product11-hinh1.jpg', 'product11-hinh2.jpg', 'empty_product.png'),
(12, 'Salix (Furosemide) Tablet', 2, 1, 200, 'Salix (Furosemide Tablets) is primarily used to treat heart failure and pulmonary edema (lung fluid). It is also used to treat some electrolyte imbalances, such as high calcium and high potassium levels.', 0.19, 'product12-hinh1.jpg', 'product12-hinh2.jpg', 'empty_product.png'),
(13, 'Latanoprost Ophthalmic Solution 0.005% 2.5 ml', 2, 1, 200, 'Latanoprost Ophthalmic Solution 0.005% 2.5 ml GENERIC for brand (Xalatan) reduces pressure in the eye by increasing the amount of fluid that drains from the eye. Xalatan is used to treat glaucoma and high pressure in the eye(s).', 12.19, 'product13-hinh1.png', 'product13-hinh2.png', 'empty_product.png'),
(14, 'Ketorolac Tromethamine 0.5% Ophthalmic Solution', 2, 1, 200, 'Ketorolac Tromethamine is the generic for the human ophthalmic solution, Acuvail. It is a Non-Steroidal Anti-Inflammatory Drug (NSAID) that decreases inflammation. It is often used to decrease inflammation and pain after eye surgeries and for pets with cataracts, but it can be used for a wide variety of eye disorders.', 7.19, 'product14-hinh1.png', 'empty_product.png', 'empty_product.png'),
(16, 'Flurbiprofen 0.03% Ophthalmic Drops, 2.5 ml', 2, 1, 200, 'Flurbiprofen 0.03% Ophthalmic Drops is a nonsteroidal anti-inflammatory drug (NSAID) used to treat inflammation of the eyes in dogs and cats. It may also be used to lessen complications of eye surgery and inhibit constriction of the pupil. Available in a 2.5 ml dropper bottle.&nbsp;&nbsp;<br>', 25.19, 'product15-hinh1.png', 'product15-hinh2.png', 'empty_product.png'),
(17, 'Zymox Otic', 2, 1, 200, 'Zymox is for the treatment of acute and chronic otitis externa due to bacterial, viral and yeast infections. Zymox is highly effective in the treatment of bacterial, fungal and yeast infections including Staphylococcus, Pseudomonas, Proteus and Malassezia.', 19.99, 'product16-hinh1.png', 'product16-hinh2.jpg', 'empty_product.png'),
(18, 'Dasuquin with MSM for Dogs', 2, 2, 200, 'Dasuquin with MSM is a new breed of joint health supplement from Nutramax the maker of Cosequin. Dasuquin is a tasty chewable tablet for dogs that goes beyond standard glucosamine supplements.', 44.99, 'product17-hinh1.png', 'product17-hinh2.png', 'product17-hinh3.png'),
(20, 'Zymox Plus Otic 1.0% Hydrocortisone', 2, 3, 200, 'Zymox Plus Otic 1.0% Hydrocortisone in an advanced formula that treats chronic otitis externa caused by bacterial and yeast infections in dogs and cats. Zymox Plus Otic is recommended for recurring otitis infections or the infections that won&#039;t resolve. Zymox Plus Otic contains a biofilm reducing formula that works on resistant microbes quicker and more effectively. Same broad spectrum antibacterial, antifungal properties PLUS biofilm reduction.&amp;nbsp;&lt;br&gt;', 33.49, 'product18-hinh1.png', 'product18-hinh2.png', 'empty_product.png'),
(21, 'Necoichi – Dining Tray (Double)', 3, 4, 200, 'Serve your feline friend’s food in style on this Necoichi Single Dining Tray! This beautiful white mealtime accessory is made from porcelain for a high-quality finish and helps protect your floors from spills. It has the outline of a kitty’s head in the center, 3 paw prints on the side and an image of a crown in another corner with text inside that says, “Happy Dining.” This tray is conveniently dishwasher-safe, microwave-safe and made to FDA standards with zero lead or cadmium. So, serve up a purr-worthy meal on this porcelain beauty!&lt;br&gt;', 24.49, 'product19-hinh1.jpg', 'product19-hinh2.jpg', 'product19-hinh3.jpg'),
(22, 'Necoichi – Portable Stress-Free Cat Pen', 3, 2, 200, 'The Necoichi Portable Stress Free Cat Cage is like a portable cat hotel and multi-purpose carrier in one versatile and stylish design. Offering cats a place to curl up whether you’re at home or away, it provides a comforting and secure escape during travel, when guests are over, while moving, and more. It’s also an excellent way to transport cats in the car, with a easy-open design that pops right open and features built-in seat belt straps—making it convenience at its very cutest. The two mesh panel sides allow for breathability and visibility, and can also be rolled down when it’s quiet time.', 41.99, 'product20-hinh1.jpg', 'product20-hinh2.jpg', 'product20-hinh3.jpg'),
(23, 'Pet Airs – Elizabethan Collar', 3, 1, 200, 'Pet Airs – makes the unloved but often necessary protective collar as comfortable as possible for animal patients.', 8, 'product21-hinh1.jpg', 'product21-hinh2.jpg', 'empty_product.png'),
(24, 'Rotho Lunch Box & Storage Box', 3, 2, 200, 'Cute cat themed lockable storage box – click closure for secure hold – ideal for storing treats, utensils or a lunch sandwich.', 3.49, 'product22-hinh1.jpg', 'product22-hinh2.jpg', 'empty_product.png'),
(25, 'Necoichi – Extra Tall Raised Cat Water Bowl', 3, 1, 198, 'Give your kitty the utmost comfort during hydration with the Necoichi Raised Cat Water Bowl. By raising the water to his level instead of forcing him to bend down, it makes for easier drinking and swallowing—and it’s also great for cats with arthritis, by reducing neck strain. The inner lip means no spills, and there are even measuring lines for ease of portion control and to keep track of how much your cat is drinking. Plus, the design just so happens to be adorable!', 33.49, 'product23-hinh1.jpg', 'product23-hinh2.jpg', 'product23-hinh3.jpg'),
(26, 'ZenClipper – The Worry Free NailClipper for Pets', 3, 3, 200, 'Zen Clipper a revolutionary new pet nail clipper (claw clipper) that is designed to clip just the tip of the nail! It’s completely silent and will ensure that you never hit the quick of your pet again.', 23.49, 'product24-hinh1.jpg', 'product24-hinh2.jpg', 'product24-hinh3.jpg'),
(27, 'Kat Zen Pads – The Purrfect Cat Bed for Your Felin', 3, 4, 200, 'These cat sleeping pads are handmade in the UK using high-quality cotton fabric imported from Japan together with a British Made fleece lining for the back to turn any flooring, shelf or other areas into the purrfect cat zen meditation hotspot!', 15.49, 'product25-hinh1.jpg', 'product25-hinh2.jpg', 'product25-hinh3.jpg'),
(28, 'Aïkiou Cat Toys for Cat Treats', 3, 2, 200, 'Cats are designed by nature for hunting. When you use a treat dispenser like the cat treat mouse or fish, your cat can now have fun hunting for their food. Its size is just perfect as it respects the same size as a real mouse.', 15.49, 'product26-hinh1.jpg', 'product26-hinh2.jpg', 'product26-hinh3.jpg'),
(29, 'Jerrys Designer Cat Cave WITH airholes', 3, 2, 200, 'Are you looking for one that will last for the lifetime of your furry friend? Look no further as this fabulous cave is the purrfect solution.&lt;br&gt;', 67.49, 'product27-hinh1.jpg', 'product27-hinh2.jpg', 'product27-hinh3.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `product_types`
--

DROP TABLE IF EXISTS `product_types`;
CREATE TABLE IF NOT EXISTS `product_types` (
  `product_type_id` int(5) NOT NULL AUTO_INCREMENT,
  `product_type_name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `coupon_id` int(5) DEFAULT NULL,
  PRIMARY KEY (`product_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `product_types`
--

INSERT INTO `product_types` (`product_type_id`, `product_type_name`, `coupon_id`) VALUES
(1, 'Nutritious FOOD', 2),
(2, 'Hygiene, care', 1),
(3, 'Utensils and accessories', 1);

-- --------------------------------------------------------

--
-- Table structure for table `suppliers`
--

DROP TABLE IF EXISTS `suppliers`;
CREATE TABLE IF NOT EXISTS `suppliers` (
  `supplier_id` int(5) NOT NULL AUTO_INCREMENT,
  `supplier_name` varchar(50) DEFAULT NULL,
  `supplier_email` varchar(50) DEFAULT NULL,
  `supplier_address` text,
  `supplier_phone` varchar(20) DEFAULT NULL,
  `supplier_avatar` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`supplier_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `suppliers`
--

INSERT INTO `suppliers` (`supplier_id`, `supplier_name`, `supplier_email`, `supplier_address`, `supplier_phone`, `supplier_avatar`) VALUES
(1, 'Hoa Tien Company', 'hoatienct2523@gmail.com', 'quận Thanh Khê thành phố Đà Nẵng, thuộc số 303 đường Trường Chinh.', '0586985458', 'supplier1.png'),
(2, 'Thanh Trung Service ', 'thanhtrungsv56@gmail.com', 'thị xã Dĩ An tỉnh Bình Dương. Số 09 đường Nguyễn Trãi.', '0909155657', 'supplier2.png'),
(3, 'Pet Mart Company', 'petmartcompany@gmail.com', 'quận Hai Bà Trưng, thành phố Hà Nội. Cụ thể là số 3, Đại Cồ Việt.', '0982334556', 'supplier3.png'),
(4, 'Petcare Service', 'petcareservice@gmail.com', 'Quận 2, thành phố Hồ Chí Minh, Cụ thể là phường Thảo Điền, 124 A đường Xuân Thủy.', '0908101110', 'supplier4.png'),
(5, 'Nobipet Company', 'nobiopetcompany@gmail.com', 'Thanh Khê Đông, thành phố Đà Nẵng số 169 Cù Chính Lan.', '0973405754', 'supplier5.png');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
