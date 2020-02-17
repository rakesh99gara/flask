-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 17, 2020 at 04:08 PM
-- Server version: 5.6.33-0ubuntu0.14.04.1-log
-- PHP Version: 5.5.9-1ubuntu4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `riktam_assignment_4_blog`
--

-- --------------------------------------------------------

--
-- Table structure for table `comments`
--

CREATE TABLE IF NOT EXISTS `comments` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(225) NOT NULL,
  `comment` text NOT NULL,
  `post_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `post_id` (`post_id`),
  KEY `user_id` (`user_id`),
  FULLTEXT KEY `name` (`name`),
  FULLTEXT KEY `name_2` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=22 ;

--
-- Dumping data for table `comments`
--

INSERT INTO `comments` (`id`, `name`, `comment`, `post_id`, `user_id`, `created_at`, `updated_at`) VALUES
(10, 'ranjeet', 'django is very good', 7, 2, '2020-02-12 12:07:52', '2020-02-12 12:07:52'),
(14, 'riktamtech', 'very good', 10, 3, '2020-02-13 07:20:42', '2020-02-13 07:20:42'),
(15, 'riktamtech', 'flask is good', 6, 3, '2020-02-13 13:34:09', '2020-02-13 13:34:09');

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE IF NOT EXISTS `posts` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=16 ;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`id`, `title`, `content`, `user_id`, `created_at`, `updated_at`) VALUES
(6, 'about flask', 'Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries.[3] It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions. However, Flask supports extensions that can add application features as if they were implemented in Flask itself. Extensions exist for object-relational mappers, form validation, upload handling, various open authentication technologies and several common framework related tools. Extensions are updated far more frequently than the core Flask program.[4]\r\n\r\nApplications that use the Flask framework include Pinterest and LinkedIn.[5][6] ', 3, '2020-02-12 11:42:00', '2020-02-12 11:42:50'),
(7, 'django', 'Django is a Python-based free and open-source web framework, which follows the model-template-view (MTV) architectural pattern.It is maintained by the Django Software Foundation (DSF), an independent organization established as a non-profit.\r\n\r\nDjango''s primary goal is to ease the creation of complex, database-driven websites. The framework emphasizes reusability and "pluggability" of components, less code, low coupling, rapid development, and the principle of don''t repeat yourself.Python is used throughout, even for settings files and data models. Django also provides an optional administrative create, read, update and delete interface that is generated dynamically through introspection and configured via admin models. ', 2, '2020-02-12 12:06:15', '2020-02-12 12:06:57'),
(9, 'Java (programming language)', 'Java is a general-purpose programming language that is class-based, object-oriented, and designed to have as few implementation dependencies as possible. It is intended to let application developers write once, run anywhere (WORA),[15] meaning that compiled Java code can run on all platforms that support Java without the need for recompilation.[16] Java applications are typically compiled to bytecode that can run on any Java virtual machine (JVM) regardless of the underlying computer architecture. The syntax of Java is similar to C and C++, but it has fewer low-level facilities than either of them. As of 2019, Java was one of the most popular programming languages in use according to GitHub,[17][18] particularly for client-server web applications, with a reported 9 million developers.[19]\r\n\r\nJava was originally developed by James Gosling at Sun Microsystems (which has since been acquired by Oracle) and released in 1995 as a core component of Sun Microsystems'' Java platform. The original and reference implementation Java compilers, virtual machines, and class libraries were originally released by Sun under proprietary licenses. As of May 2007, in compliance with the specifications of the Java Community Process, Sun had relicensed most of its Java technologies under the GNU General Public License. Meanwhile, others have developed alternative implementations of these Sun technologies, such as the GNU Compiler for Java (bytecode compiler), GNU Classpath (standard libraries), and IcedTea-Web (browser plugin for applets). ', 8, '2020-02-12 13:19:57', '2020-02-12 13:19:57'),
(10, 'SQL', 'SQL (/??s?kju???l/ (About this soundlisten) S-Q-L,[4] /?si?kw?l/ "sequel"; Structured Query Language)[5][6][7] is a domain-specific language used in programming and designed for managing data held in a relational database management system (RDBMS), or for stream processing in a relational data stream management system (RDSMS). It is particularly useful in handling structured data, i.e. data incorporating relations among entities and variables.\r\n\r\nSQL offers two main advantages over older read–write APIs such as ISAM or VSAM. Firstly, it introduced the concept of accessing many records with one single command. Secondly, it eliminates the need to specify how to reach a record, e.g. with or without an index.\r\n\r\nOriginally based upon relational algebra and tuple relational calculus, SQL consists of many types of statements,[8] which may be informally classed as sublanguages, commonly: a data query language (DQL),[a] a data definition language (DDL),[b] a data control language (DCL), and a data manipulation language (DML).[c][9] The scope of SQL includes data query, data manipulation (insert, update and delete), data definition (schema creation and modification), and data access control. Although SQL is essentially a declarative language (4GL), it includes also procedural elements. ', 3, '2020-02-13 07:20:30', '2020-02-13 07:20:30'),
(11, 'PHP', '\r\nPHPPHP-logo.svg\r\nParadigm	Imperative, functional, object-oriented, procedural, reflective\r\nDesigned by	Rasmus Lerdorf\r\nDeveloper	The PHP Development Team, Zend Technologies\r\nFirst appeared	1995; 25 years ago[1]\r\nStable release	\r\n7.4.2[2] / January 21, 2020; 22 days ago\r\nTyping discipline	Dynamic, weak\r\n\r\nsince version 7.0:\r\nGradual[3]\r\nImplementation language	C (primarily; some components C++)\r\nOS	Unix-like, Windows\r\nLicense	PHP License (most of Zend engine under Zend Engine License)\r\nFilename extensions	.php, .phtml, .php3, .php4, .php5, .php7, .phps, .php-s, .pht, .phar\r\nWebsite	www.php.net\r\nMajor implementations\r\nZend Engine, HHVM, Phalanger, Quercus, Parrot\r\nInfluenced by\r\nPerl, C, C++, Java, Tcl,[1] JavaScript, Hack[4]\r\nInfluenced\r\nHack\r\n\r\n    PHP Programming at Wikibooks\r\n\r\nPHP is a popular general-purpose scripting language that is especially suited to web development[5]. It was originally created by Rasmus Lerdorf in 1994;[6] the PHP reference implementation is now produced by The PHP Group.[7] PHP originally stood for Personal Home Page,[6] but it now stands for the recursive initialism PHP: Hypertext Preprocessor.[8]\r\n\r\nPHP code may be executed with a command line interface (CLI), embedded into HTML code, or used in combination with various web template systems, web content management systems, and web frameworks. PHP code is usually processed by a PHP interpreter implemented as a module in a web server or as a Common Gateway Interface (CGI) executable. The web server outputs the results of the interpreted and executed PHP code, which may be any type of data, such as generated HTML code or binary image data. PHP can be used for many programming tasks outside of the web context, such as standalone graphical applications[9] and robotic drone control.[10]\r\n\r\nThe standard PHP interpreter, powered by the Zend Engine, is free software released under the PHP License. PHP has been widely ported and can be deployed on most web servers on almost every operating system and platform, free of charge.[11]\r\n\r\nThe PHP language evolved without a written formal specification or standard until 2014, with the original implementation acting as the de facto standard which other implementations aimed to follow. Since 2014, work has gone on to create a formal PHP specification.[12] ', 3, '2020-02-13 13:33:15', '2020-02-13 13:33:15'),
(12, 'Laravel', 'Taylor Otwell created Laravel as an attempt to provide a more advanced alternative to the CodeIgniter framework, which did not provide certain features such as built-in support for user authentication and authorization. Laravel''s first beta release was made available on June 9, 2011, followed by the Laravel 1 release later in the same month. Laravel 1 included built-in support for authentication, localisation, models, views, sessions, routing and other mechanisms, but lacked support for controllers that prevented it from being a true MVC framework.[1]\r\n\r\nLaravel 2 was released in September 2011, bringing various improvements from the author and community. Major new features included the support for controllers, which made Laravel 2 a fully MVC-compliant framework, built-in support for the inversion of control (IoC) principle, and a templating system called Blade. As a downside, support for third-party packages was removed in Laravel 2.[1]\r\n\r\nLaravel 3 was released in February 2012 with a set of new features including the command-line interface (CLI) named Artisan, built-in support for more database management systems, database migrations as a form of version control for database layouts, support for handling events, and a packaging system called Bundles. An increase of Laravel''s userbase and popularity lined up with the release of Laravel 3.[1] ', 3, '2020-02-13 13:44:11', '2020-02-13 13:44:11');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `email` varchar(45) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=16 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `password`, `created_at`, `updated_at`) VALUES
(2, 'ranjeet@gmail.com', 'pbkdf2:sha256:150000$jA0BGRr8$e7b094362c2f455c9ec531800ec3624b27ec47139d33f56287f77388552f20e5', '2020-02-12 11:40:15', '2020-02-12 11:41:15'),
(3, 'riktamtech@gmail.com', 'pbkdf2:sha256:150000$GmGGAOyE$8aa2a79c3b841de003201465578db7e20e8e628334fbd138947a8cfa09c0d459', '2020-02-12 11:40:15', '2020-02-12 11:41:15'),
(8, 'lingaiah@gmail.com', 'pbkdf2:sha256:150000$xOUqYTeb$70132cb06bcae13c19b25c71ac74ca74aa91f97caa6b619c376084f9c11a38f3', '2020-02-12 13:17:44', '2020-02-12 13:17:44');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`),
  ADD CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `posts`
--
ALTER TABLE `posts`
  ADD CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
