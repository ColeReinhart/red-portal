DROP TABLE IF EXISTS submissions;
DROP TABLE IF EXISTS assignments;
DROP TABLE IF EXISTS users_sessions;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id bigserial PRIMARY KEY,
    email text UNIQUE NOT NULL,
    password text NOT NULL,
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student'))
);


CREATE TABLE courses(
	course_id bigserial PRIMARY KEY,
	teacher_id bigint REFERENCES users (id),
	course_number varchar(10) UNIQUE,
	course_name text NOT NULL,
	course_info text
);

CREATE TABLE sessions (
    session_id bigserial PRIMARY KEY,
    letter varchar(1) NOT NULL,
    session_time varchar(100) NOT NULL,
    course_id bigint REFERENCES courses (course_id)
);

CREATE TABLE users_sessions (
  student bigint REFERENCES users (id) NOT NULL,
  session bigint REFERENCES sessions (session_id) NOT NULL,
  CONSTRAINT users_sessions_key PRIMARY KEY (student, session)
);

--what if we have user data in users table which courses relies on, then what?
CREATE TABLE assignments(
	assignment_id bigserial PRIMARY KEY,
	session_id bigint REFERENCES sessions (session_id),
	assignment_name text NOT NULL,
	assignment_info text,
  assignment_type text,
  total_points smallint
);

-- CREATE TABLE grades (
--     id bigserial PRIMARY KEY,
--     assignment_id bigint REFERENCES assignments (assignment_id),
--     student_id bigint REFERENCES users (id),
--     grade decimal NOT NULL,
--     letter varchar(1),
--     CONSTRAINT unique_assignment_student UNIQUE (assignment_id, student_id)
-- );

CREATE TABLE submissions (
    id bigserial PRIMARY KEY,
    assignment_id bigint REFERENCES assignments (assignment_id),
    student_id bigint REFERENCES users (id),
    points smallint,
    letter varchar(1),
    filename text,
    CONSTRAINT unique_assignment_student UNIQUE (assignment_id, student_id)
);
