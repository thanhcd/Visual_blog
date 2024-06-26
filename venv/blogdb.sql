-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th4 02, 2024 lúc 04:35 AM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
-- Phiên bản PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `blogdb`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `account`
--

CREATE TABLE `account` (
  `AccID` int(11) NOT NULL,
  `PermissionID` varchar(10) NOT NULL,
  `Account` varchar(50) NOT NULL,
  `Password` varchar(50) NOT NULL,
  `Email` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `account`
--

INSERT INTO `account` (`AccID`, `PermissionID`, `Account`, `Password`, `Email`) VALUES
(1, '0', 'thanh', '123', ''),
(5, '1', 'thanh', '123', ''),
(6, '1', 'thang', '123', ''),
(7, '1', 'test2', '123', 'fia27975@nezid.com'),
(8, '1', 'test3', '123', 'chauducthanh08@gmail.com'),
(9, '1', 'test4', '123', 'hten4567@gmail.com');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `admin`
--

CREATE TABLE `admin` (
  `AccID` int(11) NOT NULL,
  `ADname` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `blog`
--

CREATE TABLE `blog` (
  `BlogID` int(11) NOT NULL,
  `AccID` int(11) NOT NULL,
  `Content` mediumtext NOT NULL,
  `Image` mediumtext NOT NULL,
  `TotalLikes` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `blog`
--

INSERT INTO `blog` (`BlogID`, `AccID`, `Content`, `Image`, `TotalLikes`) VALUES
(3, 7, 'que mira bobo\r\n', '432768240_410487704962589_8045077667653422121_n.jpg', 0),
(4, 7, 'nó lực vl, thề!', '3489939-71145948-2560-1440.jpg', 0),
(6, 7, 'địt mẹ code lồn ', 'lehmann1200.jpg', 0),
(11, 7, 'ádasdasdasd', '77711_v9_bc.jpg', 0);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `blog_comment`
--

CREATE TABLE `blog_comment` (
  `BlogID` int(10) NOT NULL,
  `CommentID` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `blog_comment`
--

INSERT INTO `blog_comment` (`BlogID`, `CommentID`) VALUES
(3, 17),
(4, 10),
(4, 20),
(6, 21);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `blog_like_test`
--

CREATE TABLE `blog_like_test` (
  `BlogID` int(10) NOT NULL,
  `AccID` int(11) NOT NULL,
  `Likes` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `blog_like_test`
--

INSERT INTO `blog_like_test` (`BlogID`, `AccID`, `Likes`) VALUES
(3, 7, 1),
(4, 7, 1),
(4, 9, 1),
(11, 7, 1),
(11, 9, 1);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `comment`
--

CREATE TABLE `comment` (
  `CommentID` int(10) NOT NULL,
  `AccID` int(11) NOT NULL,
  `Comment` mediumtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `comment`
--

INSERT INTO `comment` (`CommentID`, `AccID`, `Comment`) VALUES
(10, 8, 'bbb'),
(17, 9, 'cũng bình thường ấy mà!'),
(20, 8, 'ấdasdasdfghfghfg'),
(21, 9, 'qeu mỉa bobo');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `permission`
--

CREATE TABLE `permission` (
  `PermissionID` varchar(10) NOT NULL,
  `Permission` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `permission`
--

INSERT INTO `permission` (`PermissionID`, `Permission`) VALUES
('0', 'admin'),
('1', 'user');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `user`
--

CREATE TABLE `user` (
  `AccID` int(11) NOT NULL,
  `Username` varchar(50) NOT NULL,
  `Date` date NOT NULL,
  `Phone` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `user`
--

INSERT INTO `user` (`AccID`, `Username`, `Date`, `Phone`) VALUES
(7, 'ducthanh', '2024-03-26', 2147483647),
(8, 'xinthong0147', '2024-03-26', 2147483647),
(9, 'anh 7 tạ', '2024-03-27', 2147483647);

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`AccID`),
  ADD KEY `PermissionID` (`PermissionID`);

--
-- Chỉ mục cho bảng `admin`
--
ALTER TABLE `admin`
  ADD UNIQUE KEY `AccID` (`AccID`);

--
-- Chỉ mục cho bảng `blog`
--
ALTER TABLE `blog`
  ADD PRIMARY KEY (`BlogID`),
  ADD KEY `AccID` (`AccID`);

--
-- Chỉ mục cho bảng `blog_comment`
--
ALTER TABLE `blog_comment`
  ADD KEY `BlogID` (`BlogID`,`CommentID`);

--
-- Chỉ mục cho bảng `blog_like_test`
--
ALTER TABLE `blog_like_test`
  ADD UNIQUE KEY `BlogID` (`BlogID`,`AccID`);

--
-- Chỉ mục cho bảng `comment`
--
ALTER TABLE `comment`
  ADD PRIMARY KEY (`CommentID`);

--
-- Chỉ mục cho bảng `permission`
--
ALTER TABLE `permission`
  ADD PRIMARY KEY (`PermissionID`);

--
-- Chỉ mục cho bảng `user`
--
ALTER TABLE `user`
  ADD UNIQUE KEY `AccID` (`AccID`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `account`
--
ALTER TABLE `account`
  MODIFY `AccID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT cho bảng `blog`
--
ALTER TABLE `blog`
  MODIFY `BlogID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT cho bảng `comment`
--
ALTER TABLE `comment`
  MODIFY `CommentID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `account`
--
ALTER TABLE `account`
  ADD CONSTRAINT `account_ibfk_1` FOREIGN KEY (`PermissionID`) REFERENCES `permission` (`PermissionID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
