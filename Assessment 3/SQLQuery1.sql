-- We first check if the database exists, and drop it if it does.
IF DB_ID('student') IS NOT NULL
	BEGIN
		PRINT 'Database exists - dropping.';
		USE master;
		ALTER DATABASE student SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
		DROP DATABASE student;
	END
GO
-- Now that we are sure the database does not exist, we create it.
PRINT 'Creating database...';
CREATE DATABASE student;
GO
-- We activate the created database.
USE student;
GO
-- Create course_info table to hold course information.
PRINT 'Creating course info table...';

CREATE TABLE course_info(	
	course_code			CHAR(3) NOT NULL,
	course_name			VARCHAR(25) NOT NULL,
	year_start_offer	INT NOT NULL,
	year_end_offer		INT NULL,
	course_coordinator_name	VARCHAR(25) NULL,
	course_coordinator_email	VARCHAR(50) NULL,
	course_coordinator_phone	VARCHAR(20) NULL,

	CONSTRAINT course_pk PRIMARY KEY (course_code),
	CONSTRAINT course_name_uk UNIQUE (course_name)
);

-- Create student_info table to hold student information.
PRINT 'Creating student info table...';

CREATE TABLE student_info(	
	person_id		BIGINT NOT NULL IDENTITY(20241201,1),
	first_name		VARCHAR(20) NOT NULL,
	last_name		VARCHAR(20) NOT NULL,
	email			VARCHAR(50) NOT NULL,
	mobile_phone	VARCHAR(20) NOT NULL,
	stu_course_code	CHAR(3) NOT NULL,
	unit_attempted	TINYINT	NOT NULL,
	unit_completed	TINYINT NOT NULL,
	course_status	VARCHAR(50) NOT NULL,

	CONSTRAINT student_pk PRIMARY KEY (person_id),
	CONSTRAINT student_course_fk FOREIGN KEY (stu_course_code) REFERENCES course_info(course_code),
	CONSTRAINT student_email_uk UNIQUE (email),
	CONSTRAINT student_phone_uk UNIQUE (mobile_phone),
	CONSTRAINT unit_attempted_check CHECK (unit_attempted <=30)
);

-- Create student_unit table to hold results of each unit of students.
PRINT 'Creating student_unit table...';

CREATE TABLE student_unit(	
	record_id	INT NOT NULL IDENTITY,
	person_id	BIGINT NOT NULL,
	unit_code	VARCHAR(20) NOT NULL,
	unit_title	VARCHAR(30) NOT NULL,
	result_score	DECIMAL(4,1) NOT NULL,
	result_grade	VARCHAR(2) NOT NULL,
	year_attempted	INT NOT NULL,
	semester_attempted	TINYINT NOT NULL,

	CONSTRAINT student_unit_pk PRIMARY KEY (record_id),
	CONSTRAINT student_unit_person_fk FOREIGN KEY (person_id) REFERENCES student_info(person_id),
	CONSTRAINT student_unit_result_score_check CHECK (result_score BETWEEN 0 AND 100),
	CONSTRAINT student_unit_result_grade_check CHECK (result_grade IN ('F', 'P', 'CR', 'D', 'HD')),
	CONSTRAINT student_unit_semester_attempted_check CHECK (semester_attempted IN ('1', '2'))
);

--  Now that the database tables have been created, we can populate them with data

--  Populate the course_info table.
PRINT 'Populating course_info table...';

INSERT INTO course_info
VALUES	('U65', 'Computer Science', 1989, NULL, 'Course_cor1 PERSON1', 'cc.PERSON1@my.oust.edu.au', '2024010201'),
		('U67', 'Information Technology', 1992, NULL, 'Course_cor2 PERSON2', 'cc.PERSON2@my.oust.edu.au', '2024010202'),
		('Y89', 'Cyber Security', 1998, NULL, 'Course_cor3 PERSON3', 'cc.PERSON3@my.oust.edu.au', '2024010203'),
		('Y84', 'Data Science', 2012, NULL, 'Course_cor4 PERSON14', 'cc.PERSON14@my.oust.edu.au', '2024010204'),
		('K22', 'Physics', 1983, NULL, 'Course_cor5 PERSON62', 'cc.PERSON62@my.oust.edu.au', '2024010205'),
		('E37', 'Tertiery Education', 1983, 2022, NULL, NULL, NULL);

-- call query to see values inserted 
SELECT * FROM course_info;

--  Populate the student_info table.
PRINT 'Populating student_info table...';

INSERT INTO student_info
VALUES	('Jim', 'MAX', 'j.max@our.oust.edu.au', '2024120201', 'U65', 30, 24, 'completed'),
		('Jit', 'MAX', 'jt.max@our.oust.edu.au', '2024120202', 'U65', 24, 24, 'completed'),
		('Late', 'MAX', 'l.max@our.oust.edu.au', '2024120203', 'U65', 28, 24, 'completed'),
		('Rep', 'SMITH', 'r.smith@our.oust.edu.au', '2024120204', 'U65', 26, 24, 'completed'),
		('Paul', 'Landan', 'p.landan@our.oust.edu.au', '2024120205', 'U67', 27, 24, 'completed'),
		('Peter', 'London', 'p.london@our.oust.edu.au', '2024120206', 'U67', 26, 24, 'completed'),
		('John', 'Turner', 'j.turner@our.oust.edu.au', '2024120207', 'Y84', 27, 24, 'completed'),
		('Jim', 'XIAO', 'j.XIAO@our.oust.edu.au', '2024120208', 'Y84', 17, 15, 'In Progress');

-- call query to see values inserted 
SELECT * FROM student_info;

--  Populate the student_unit table.
PRINT 'Populating student_unit table...';

INSERT INTO student_unit
VALUES	(20241201, 'Unit_01', 'Unit_title_001', 100, 'HD', 2019, 1),
		(20241201, 'Unit_02', 'Unit_title_002', 67.6, 'CR', 2019, 1),
		(20241201, 'Unit_03', 'Unit_title_003', 64.6, 'CR', 2019, 1),
		(20241201, 'Unit_04', 'Unit_title_004', 80.2, 'HD', 2019, 1),
		(20241201, 'Unit_05', 'Unit_title_005', 90, 'HD', 2019, 2),
		(20241201, 'Unit_06', 'Unit_title_006', 55, 'P', 2019, 2),
		(20241201, 'Unit_07', 'Unit_title_007', 60.8, 'CR', 2019, 2),
		(20241201, 'Unit_08', 'Unit_title_008', 85.2, 'HD', 2019, 2),
		(20241201, 'Unit_09', 'Unit_title_009', 68.2, 'CR', 2020, 1),
		(20241201, 'Unit_10', 'Unit_title_010', 68.3, 'CR', 2020, 1),
		(20241201, 'Unit_11', 'Unit_title_011', 56.7, 'P', 2020, 1),
		(20241201, 'Unit_12', 'Unit_title_012', 38.9, 'F', 2020, 1),
		(20241201, 'Unit_12', 'Unit_title_012', 77.5, 'D', 2020, 2),
		(20241201, 'Unit_14', 'Unit_title_014', 76.2, 'D', 2020, 2),
		(20241201, 'Unit_15', 'Unit_title_015', 81.3, 'HD', 2020, 2),
		(20241201, 'Unit_16', 'Unit_title_016', 46.2, 'F', 2020, 2),
		(20241201, 'Unit_16', 'Unit_title_016', 81.7, 'HD', 2021, 1),
		(20241201, 'Unit_18', 'Unit_title_018', 43.3, 'F', 2021, 1),
		(20241201, 'Unit_18', 'Unit_title_018', 77.3, 'D', 2021, 1),
		(20241201, 'Unit_20', 'Unit_title_020', 42.8, 'F', 2021, 1),
		(20241201, 'Unit_20', 'Unit_title_020', 45.4, 'F', 2021, 2),
		(20241201, 'Unit_20', 'Unit_title_020', 90.9, 'HD', 2021, 2),
		(20241201, 'Unit_23', 'Unit_title_023', 71.1, 'D', 2021, 2),
		(20241201, 'Unit_24', 'Unit_title_024', 92.6, 'HD', 2021, 2),
		(20241201, 'Unit_25', 'Unit_title_025', 74.1, 'D', 2022, 1),
		(20241201, 'Unit_26', 'Unit_title_026', 94.6, 'HD', 2022, 1),
		(20241201, 'Unit_27', 'Unit_title_027', 56.9, 'P', 2022, 1),
		(20241201, 'Unit_28', 'Unit_title_028', 40.6, 'F', 2022, 1),
		(20241201, 'Unit_28', 'Unit_title_028', 82.7, 'HD', 2022, 2),
		(20241201, 'Unit_30', 'Unit_title_030', 99.9, 'HD', 2022, 2),
		(20241202, 'Unit_01', 'Unit_title_001', 74, 'D', 2021, 1),
		(20241202, 'Unit_02', 'Unit_title_002', 95.3, 'HD', 2021, 1),
		(20241202, 'Unit_03', 'Unit_title_003', 92.3, 'HD', 2021, 1),
		(20241202, 'Unit_04', 'Unit_title_004', 67.3, 'CR', 2021, 1),
		(20241202, 'Unit_06', 'Unit_title_006', 90.9, 'HD', 2021, 2),
		(20241202, 'Unit_07', 'Unit_title_007', 71.1, 'D', 2021, 2),
		(20241202, 'Unit_08', 'Unit_title_008', 52.6, 'P', 2021, 2),
		(20241202, 'Unit_09', 'Unit_title_009', 74.1, 'D', 2021, 2),
		(20241202, 'Unit_10', 'Unit_title_010', 94.6, 'HD', 2022, 1),
		(20241202, 'Unit_11', 'Unit_title_011', 56.9, 'P', 2022, 1),
		(20241202, 'Unit_12', 'Unit_title_012', 56.6, 'P', 2022, 1),
		(20241202, 'Unit_13', 'Unit_title_013', 76.4, 'D', 2022, 1),
		(20241202, 'Unit_14', 'Unit_title_014', 58.5, 'P', 2022, 2),
		(20241202, 'Unit_16', 'Unit_title_016', 62.4, 'CR', 2022, 2),
		(20241202, 'Unit_18', 'Unit_title_018', 67, 'CR', 2022, 2),
		(20241202, 'Unit_19', 'Unit_title_019', 74.4, 'D', 2022, 2),
		(20241202, 'Unit_20', 'Unit_title_020', 74.9, 'D', 2023, 1),
		(20241202, 'Unit_21', 'Unit_title_021', 53, 'P', 2023, 1),
		(20241202, 'Unit_23', 'Unit_title_023', 52.8, 'P', 2023, 1),
		(20241202, 'Unit_24', 'Unit_title_024', 65.7, 'CR', 2023, 1),
		(20241202, 'Unit_25', 'Unit_title_025', 84.3, 'HD', 2023, 2),
		(20241202, 'Unit_26', 'Unit_title_026', 87.7, 'HD', 2023, 2),
		(20241202, 'Unit_27', 'Unit_title_027', 72.9, 'D', 2023, 2),
		(20241202, 'Unit_30', 'Unit_title_030', 93, 'HD', 2023, 2),
		(20241203, 'Unit_01', 'Unit_title_001', 22.2, 'F', 2020, 1),
		(20241203, 'Unit_01', 'Unit_title_001', 83.8, 'HD', 2020, 2),
		(20241203, 'Unit_03', 'Unit_title_003', 75.8, 'D', 2020, 1),
		(20241203, 'Unit_04', 'Unit_title_004', 92.1, 'HD', 2020, 1),
		(20241203, 'Unit_05', 'Unit_title_005', 64.6, 'CR', 2020, 1),
		(20241203, 'Unit_06', 'Unit_title_006', 80.3, 'HD', 2020, 2),
		(20241203, 'Unit_07', 'Unit_title_007', 56.3, 'P', 2020, 2),
		(20241203, 'Unit_08', 'Unit_title_008', 82.8, 'HD', 2020, 2),
		(20241203, 'Unit_09', 'Unit_title_009', 33.6, 'F', 2021, 1),
		(20241203, 'Unit_09', 'Unit_title_009', 75.9, 'D', 2021, 2),
		(20241203, 'Unit_11', 'Unit_title_011', 80.1, 'HD', 2021, 1),
		(20241203, 'Unit_12', 'Unit_title_012', 69.8, 'CR', 2021, 1),
		(20241203, 'Unit_12', 'Unit_title_012', 26.5, 'F', 2021, 2),
		(20241203, 'Unit_12', 'Unit_title_012', 57.8, 'P', 2022, 1),
		(20241203, 'Unit_14', 'Unit_title_014', 87.8, 'HD', 2021, 2),
		(20241203, 'Unit_16', 'Unit_title_016', 11.5, 'F', 2021, 2),
		(20241203, 'Unit_16', 'Unit_title_016', 79, 'D', 2022, 1),
		(20241203, 'Unit_18', 'Unit_title_018', 73, 'D', 2022, 1),
		(20241203, 'Unit_19', 'Unit_title_019', 75, 'D', 2022, 1),
		(20241203, 'Unit_20', 'Unit_title_020', 89, 'HD', 2022, 1),
		(20241203, 'Unit_21', 'Unit_title_021', 50.6, 'P', 2022, 2),
		(20241203, 'Unit_22', 'Unit_title_022', 71.7, 'D', 2022, 2),
		(20241203, 'Unit_23', 'Unit_title_023', 77.8, 'D', 2022, 2),
		(20241203, 'Unit_24', 'Unit_title_024', 75.7, 'D', 2022, 2),
		(20241203, 'Unit_25', 'Unit_title_025', 52, 'P', 2023, 1),
		(20241203, 'Unit_26', 'Unit_title_026', 67.7, 'CR', 2023, 1),
		(20241203, 'Unit_27', 'Unit_title_027', 75.9, 'D', 2023, 1),
		(20241203, 'Unit_30', 'Unit_title_030', 71.7, 'D', 2023, 1),
		(20241204, 'Unit_01', 'Unit_title_001', 71.6, 'D', 2020, 1),
		(20241204, 'Unit_02', 'Unit_title_002', 65.2, 'CR', 2020, 1),
		(20241204, 'Unit_03', 'Unit_title_003', 72.8, 'D', 2020, 1),
		(20241204, 'Unit_04', 'Unit_title_004', 75.9, 'D', 2020, 1),
		(20241204, 'Unit_05', 'Unit_title_005', 65.4, 'CR', 2020, 2),
		(20241204, 'Unit_06', 'Unit_title_006', 70.8, 'D', 2020, 2),
		(20241204, 'Unit_07', 'Unit_title_007', 81.7, 'HD', 2020, 2),
		(20241204, 'Unit_08', 'Unit_title_008', 72.7, 'D', 2020, 2),
		(20241204, 'Unit_09', 'Unit_title_009', 58.9, 'P', 2021, 1),
		(20241204, 'Unit_10', 'Unit_title_010', 53.5, 'P', 2021, 1),
		(20241204, 'Unit_11', 'Unit_title_011', 59, 'P', 2021, 1),
		(20241204, 'Unit_13', 'Unit_title_013', 68.7, 'CR', 2021, 1),
		(20241204, 'Unit_14', 'Unit_title_014', 83.1, 'HD', 2021, 2),
		(20241204, 'Unit_15', 'Unit_title_015', 52, 'P', 2021, 2),
		(20241204, 'Unit_16', 'Unit_title_016', 55.5, 'P', 2021, 2),
		(20241204, 'Unit_18', 'Unit_title_018', 56.9, 'P', 2021, 2),
		(20241204, 'Unit_19', 'Unit_title_019', 67, 'CR', 2022, 1),
		(20241204, 'Unit_21', 'Unit_title_021', 68, 'CR', 2022, 1),
		(20241204, 'Unit_22', 'Unit_title_022', 55.3, 'P', 2022, 1),
		(20241204, 'Unit_23', 'Unit_title_023', 78.1, 'D', 2022, 1),
		(20241204, 'Unit_25', 'Unit_title_025', 46.5, 'F', 2022, 2),
		(20241204, 'Unit_25', 'Unit_title_025', 50.7, 'P', 2022, 2),
		(20241204, 'Unit_27', 'Unit_title_027', 45, 'F', 2022, 2),
		(20241204, 'Unit_27', 'Unit_title_027', 75.4, 'D', 2023, 1),
		(20241204, 'Unit_29', 'Unit_title_029', 68.3, 'CR', 2023, 1),
		(20241204, 'Unit_30', 'Unit_title_030', 76.9, 'D', 2023, 1),
		(20241205, 'Unit_01', 'Unit_title_001', 70, 'D', 2019, 1),
		(20241205, 'Unit_02', 'Unit_title_002', 80.5, 'HD', 2019, 1),
		(20241205, 'Unit_03', 'Unit_title_003', 60.1, 'CR', 2019, 1),
		(20241205, 'Unit_04', 'Unit_title_004', 54.9, 'P', 2019, 1),
		(20241205, 'Unit_05', 'Unit_title_005', 23.6, 'F', 2019, 2),
		(20241205, 'Unit_05', 'Unit_title_005', 51.6, 'P', 2020, 1),
		(20241205, 'Unit_07', 'Unit_title_007', 42.3, 'F', 2019, 2),
		(20241205, 'Unit_07', 'Unit_title_007', 86.3, 'HD', 2020, 1),
		(20241205, 'Unit_49', 'Unit_title_049', 60.9, 'CR', 2019, 2),
		(20241205, 'Unit_50', 'Unit_title_050', 53.2, 'P', 2019, 2),
		(20241205, 'Unit_51', 'Unit_title_051', 81.9, 'HD', 2020, 1),
		(20241205, 'Unit_52', 'Unit_title_052', 52.1, 'P', 2020, 1),
		(20241205, 'Unit_53', 'Unit_title_053', 86.9, 'HD', 2020, 2),
		(20241205, 'Unit_54', 'Unit_title_054', 55.3, 'P', 2020, 2),
		(20241205, 'Unit_55', 'Unit_title_055', 55.9, 'P', 2020, 2),
		(20241205, 'Unit_56', 'Unit_title_056', 55.7, 'P', 2021, 1),
		(20241205, 'Unit_58', 'Unit_title_058', 62.9, 'CR', 2021, 1),
		(20241205, 'Unit_59', 'Unit_title_059', 84, 'HD', 2021, 1),
		(20241205, 'Unit_61', 'Unit_title_061', 76.1, 'D', 2021, 1),
		(20241205, 'Unit_62', 'Unit_title_062', 65, 'CR', 2021, 2),
		(20241205, 'Unit_63', 'Unit_title_063', 74.9, 'D', 2021, 2),
		(20241205, 'Unit_64', 'Unit_title_064', 83.8, 'HD', 2021, 2),
		(20241205, 'Unit_65', 'Unit_title_065', 74.3, 'D', 2021, 2),
		(20241205, 'Unit_66', 'Unit_title_066', 56.8, 'P', 2022, 1),
		(20241205, 'Unit_67', 'Unit_title_067', 53.7, 'P', 2022, 1),
		(20241205, 'Unit_68', 'Unit_title_068', 42.8, 'F', 2022, 1),
		(20241205, 'Unit_68', 'Unit_title_068', 76.8, 'D', 2022, 2),
		(20241206, 'Unit_01', 'Unit_title_001', 65.9, 'CR', 2018, 1),
		(20241206, 'Unit_02', 'Unit_title_002', 52.6, 'P', 2018, 1),
		(20241206, 'Unit_03', 'Unit_title_003', 61.9, 'CR', 2018, 1),
		(20241206, 'Unit_04', 'Unit_title_004', 53.1, 'P', 2018, 1),
		(20241206, 'Unit_05', 'Unit_title_005', 51.5, 'P', 2018, 2),
		(20241206, 'Unit_07', 'Unit_title_007', 55.4, 'P', 2018, 2),
		(20241206, 'Unit_08', 'Unit_title_008', 62.5, 'CR', 2018, 2),
		(20241206, 'Unit_10', 'Unit_title_010', 64.4, 'CR', 2018, 2),
		(20241206, 'Unit_41', 'Unit_title_041', 50.7, 'P', 2019, 1),
		(20241206, 'Unit_42', 'Unit_title_042', 54.4, 'P', 2019, 1),
		(20241206, 'Unit_43', 'Unit_title_043', 62.7, 'CR', 2019, 1),
		(20241206, 'Unit_44', 'Unit_title_044', 56.4, 'P', 2019, 1),
		(20241206, 'Unit_45', 'Unit_title_045', 50.5, 'P', 2019, 2),
		(20241206, 'Unit_46', 'Unit_title_046', 80.5, 'HD', 2019, 2),
		(20241206, 'Unit_48', 'Unit_title_048', 62.7, 'CR', 2019, 2),
		(20241206, 'Unit_49', 'Unit_title_049', 57.8, 'P', 2019, 2),
		(20241206, 'Unit_60', 'Unit_title_060', 71.2, 'D', 2020, 1),
		(20241206, 'Unit_61', 'Unit_title_061', 55.7, 'P', 2020, 1),
		(20241206, 'Unit_62', 'Unit_title_062', 51.1, 'P', 2020, 1),
		(20241206, 'Unit_63', 'Unit_title_063', 41, 'F', 2020, 1),
		(20241206, 'Unit_63', 'Unit_title_063', 62.7, 'CR', 2020, 2),
		(20241206, 'Unit_66', 'Unit_title_066', 56.3, 'P', 2020, 2),
		(20241206, 'Unit_67', 'Unit_title_067', 60, 'CR', 2020, 2),
		(20241206, 'Unit_68', 'Unit_title_068', 54.5, 'P', 2021, 1),
		(20241206, 'Unit_69', 'Unit_title_069', 47.5, 'F', 2021, 1),
		(20241206, 'Unit_69', 'Unit_title_069', 58.2, 'P', 2021, 2),
		(20241207, 'Unit_01', 'Unit_title_001', 50.1, 'P', 2020, 1),
		(20241207, 'Unit_02', 'Unit_title_002', 56.8, 'P', 2020, 1),
		(20241207, 'Unit_03', 'Unit_title_003', 58.4, 'P', 2020, 1),
		(20241207, 'Unit_04', 'Unit_title_004', 62.6, 'CR', 2020, 1),
		(20241207, 'Unit_05', 'Unit_title_005', 58.4, 'P', 2020, 2),
		(20241207, 'Unit_06', 'Unit_title_006', 83.9, 'HD', 2020, 2),
		(20241207, 'Unit_07', 'Unit_title_007', 52.1, 'P', 2020, 2),
		(20241207, 'Unit_08', 'Unit_title_008', 48.3, 'F', 2021, 1),
		(20241207, 'Unit_08', 'Unit_title_008', 64.2, 'CR', 2021, 2),
		(20241207, 'Unit_70', 'Unit_title_070', 68.9, 'CR', 2021, 1),
		(20241207, 'Unit_71', 'Unit_title_071', 69.3, 'CR', 2021, 1),
		(20241207, 'Unit_72', 'Unit_title_072', 79.6, 'D', 2021, 2),
		(20241207, 'Unit_73', 'Unit_title_073', 70.9, 'D', 2021, 2),
		(20241207, 'Unit_74', 'Unit_title_074', 71.2, 'D', 2021, 2),
		(20241207, 'Unit_75', 'Unit_title_075', 78, 'D', 2022, 1),
		(20241207, 'Unit_76', 'Unit_title_076', 48, 'F', 2022, 1),
		(20241207, 'Unit_76', 'Unit_title_076', 76.8, 'D', 2022, 2),
		(20241207, 'Unit_79', 'Unit_title_079', 60, 'CR', 2022, 1),
		(20241207, 'Unit_80', 'Unit_title_080', 61, 'CR', 2022, 2),
		(20241207, 'Unit_81', 'Unit_title_081', 36.1, 'F', 2022, 2),
		(20241207, 'Unit_81', 'Unit_title_081', 62, 'CR', 2023, 1),
		(20241207, 'Unit_84', 'Unit_title_084', 78.5, 'D', 2022, 2),
		(20241207, 'Unit_85', 'Unit_title_085', 76.8, 'D', 2023, 1),
		(20241207, 'Unit_86', 'Unit_title_086', 53, 'P', 2023, 1),
		(20241207, 'Unit_88', 'Unit_title_088', 60.6, 'CR', 2023, 2),
		(20241207, 'Unit_89', 'Unit_title_089', 75.2, 'D', 2023, 2),
		(20241207, 'Unit_90', 'Unit_title_090', 63.1, 'CR', 2023, 2),
		(20241208, 'Unit_01', 'Unit_title_001', 54, 'P', 2022, 1),
		(20241208, 'Unit_02', 'Unit_title_002', 92.1, 'HD', 2022, 1),
		(20241208, 'Unit_03', 'Unit_title_003', 72.3, 'D', 2022, 1),
		(20241208, 'Unit_04', 'Unit_title_004', 34.5, 'F', 2022, 1),
		(20241208, 'Unit_04', 'Unit_title_004', 53, 'P', 2022, 2),
		(20241208, 'Unit_06', 'Unit_title_006', 56.4, 'P', 2022, 2),
		(20241208, 'Unit_07', 'Unit_title_007', 98.6, 'HD', 2022, 2),
		(20241208, 'Unit_08', 'Unit_title_008', 56.7, 'P', 2023, 1),
		(20241208, 'Unit_09', 'Unit_title_009', 67, 'CR', 2023, 1),
		(20241208, 'Unit_70', 'Unit_title_070', 42.2, 'F', 2023, 1),
		(20241208, 'Unit_70', 'Unit_title_070', 51.2, 'P', 2023, 2),
		(20241208, 'Unit_72', 'Unit_title_072', 92.9, 'HD', 2023, 2),
		(20241208, 'Unit_73', 'Unit_title_073', 77.1, 'D', 2023, 2),
		(20241208, 'Unit_74', 'Unit_title_074', 71.5, 'D', 2024, 1),
		(20241208, 'Unit_87', 'Unit_title_087', 97.7, 'HD', 2024, 1),
		(20241208, 'Unit_89', 'Unit_title_089', 61.2, 'CR', 2024, 1),
		(20241208, 'Unit_90', 'Unit_title_090', 99.9, 'HD', 2024, 1);

-- call query to see values inserted 
SELECT * FROM student_unit;