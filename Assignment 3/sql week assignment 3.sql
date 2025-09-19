
use season;

-- Create the Projects table
CREATE TABLE Projects (
    ProjectID INT PRIMARY KEY,
    ProjectName VARCHAR(100),
    StartDate DATE,
    EndDate DATE,
    Budget DECIMAL(10,2)   -- Fixed the DECIMAL issue
);

-- Insert 5 rows into Projects
INSERT INTO Projects VALUES (1, 'Website Design', '2025-01-01', '2025-06-30', 50000.00);
INSERT INTO Projects VALUES (2, 'Mobile Application', '2025-02-15', '2025-08-15', 75000.00);
INSERT INTO Projects VALUES (3, 'Data Migration', '2025-03-01', '2025-07-31', 62000.00);
INSERT INTO Projects VALUES (4, 'Cloud Deployment', '2025-04-10', '2025-10-15', 88000.00);
INSERT INTO Projects VALUES (5, 'AI Chatbot', '2025-05-05', '2025-09-20', 95000.00);
select * from projects;

-- Drop table if it already exists (to avoid duplicate errors)
DROP TABLE IF EXISTS Tasks;

-- Create Tasks table
CREATE TABLE Tasks (
    TaskID INT PRIMARY KEY,
    ProjectID INT,
    TaskName VARCHAR(100),
    AssignedTo VARCHAR(50),
    Status VARCHAR(20),
    FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID)
);

-- Insert 5 rows into Tasks
INSERT INTO Tasks VALUES
(1, 1, 'Design Homepage', 'Alice', 'Completed'),
(2, 1, 'Setup Database', 'Bob', 'In Progress'),
(3, 2, 'UI Wireframes', 'Charlie', 'Completed'),
(4, 3, 'Data Backup', 'David', 'In Progress'),
(5, 4, 'Cloud Configuration', 'Eva', 'Pending');
select * from Tasks;

-- Create Teams Table
CREATE TABLE Teams (
    TeamID INT PRIMARY KEY,
    TeamName VARCHAR(50),
    Leader VARCHAR(50),
    MembersCount INT,
    Location VARCHAR(50)
);

-- Insert 5 rows into Teams
INSERT INTO Teams VALUES
(1, 'Design Team', 'Alice', 5, 'New York'),
(2, 'Development Team', 'Bob', 8, 'San Francisco'),
(3, 'AI Team', 'Charlie', 6, 'Boston'),
(4, 'Cloud Team', 'David', 7, 'Chicago'),
(5, 'Marketing Team', 'Eva', 4, 'Los Angeles');
select * from Teams;

WITH TaskCounts AS (
    SELECT 
        ProjectID,
        COUNT(*) AS total_tasks,
        SUM(CASE WHEN Status = 'Completed' THEN 1 ELSE 0 END) AS completed_tasks
    FROM Tasks
    GROUP BY ProjectID
)
SELECT 
    p.ProjectName,
    t.total_tasks,
    t.completed_tasks
FROM Projects p
JOIN TaskCounts t ON p.ProjectID = t.ProjectID;

WITH TaskCounts AS (
    SELECT 
        AssignedTo,
        COUNT(*) AS total_tasks,
        ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS rn
    FROM Tasks
    GROUP BY AssignedTo
)
SELECT AssignedTo, total_tasks
FROM TaskCounts
WHERE rn <= 2;

-- Alter table to add due_date (if not already added)
ALTER TABLE Tasks ADD Due_Date DATE;

-- Sample updates (5 rows)
UPDATE Tasks SET Due_Date = '2025-03-01' WHERE TaskID = 1;
UPDATE Tasks SET Due_Date = '2025-04-15' WHERE TaskID = 2;
UPDATE Tasks SET Due_Date = '2025-09-21' WHERE TaskID = 3;
UPDATE Tasks SET Due_Date = '2025-09-20' WHERE TaskID = 4;
UPDATE Tasks SET Due_Date = '2025-12-01' WHERE TaskID = 5;
select * from  Tasks;
SELECT 
    TaskID,
    ProjectID,
    TaskName,
    Due_Date
FROM Tasks t
WHERE Due_Date < (
    SELECT AVG(Due_Date)
    FROM Tasks
    WHERE ProjectID = t.ProjectID
);
SELECT ProjectID, ProjectName, Budget
FROM Projects
WHERE Budget = (
    SELECT MAX(Budget)
    FROM Projects
);

SELECT 
    p.ProjectName,
    COUNT(*) AS total_tasks,
    SUM(CASE WHEN t.Status = 'Completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.Status = 'Completed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS completion_percentage
FROM Projects p
JOIN Tasks t ON p.ProjectID = t.ProjectID
GROUP BY p.ProjectName;

SELECT 
    AssignedTo,
    TaskName,
    COUNT(*) OVER (PARTITION BY AssignedTo) AS task_count_per_person
FROM Tasks
ORDER BY AssignedTo;

SELECT 
    t.TaskID,
    t.TaskName,
    t.AssignedTo,
    t.Status,
    t.Due_Date,
    p.ProjectName
FROM Tasks t
JOIN Projects p ON t.ProjectID = p.ProjectID
JOIN Teams tm ON t.AssignedTo = tm.Leader
WHERE t.Status <> 'Completed'
  AND t.Due_Date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 15 DAY);

UPDATE Tasks 
SET Due_Date = '2025-09-12' 
WHERE TaskID = 2;

SELECT 
    p.ProjectID,
    p.ProjectName
FROM Projects p
LEFT JOIN Tasks t ON p.ProjectID = t.ProjectID
WHERE t.TaskID IS NULL;

CREATE TABLE model_training(

    training_id INT PRIMARY KEY,
    project_id INT,
    model_name VARCHAR(100),
    accuracy DECIMAL(5,2),
    training_date DATE,
    FOREIGN KEY (project_id) REFERENCES Projects(ProjectID)
);

-- Insert 5 sample rows
INSERT INTO Model_Training VALUES
(1, 3, 'Chatbot_v1', 85.50, '2025-05-01'),
(2, 3, 'Chatbot_v2', 90.00, '2025-06-01'),
(3, 4, 'CloudPredictor_v1', 88.75, '2025-07-01'),
(4, 4, 'CloudPredictor_v2', 92.00, '2025-08-01'),
(5, 2, 'MobileAI_v1', 80.25, '2025-06-15');
SELECT 
    p.ProjectName,
    m.model_name AS best_model,
    m.accuracy
FROM Model_Training m
JOIN Projects p ON m.project_id = p.ProjectID
WHERE (m.project_id, m.accuracy) IN (
    SELECT project_id, MAX(accuracy)
    FROM Model_Training
    GROUP BY project_id
)
ORDER BY p.ProjectName;

CREATE TABLE Data_Sets (
    dataset_id INT PRIMARY KEY,
    project_id INT,
    dataset_name VARCHAR(100),
    size_gb DECIMAL(10,2),
    last_updated DATE,
    FOREIGN KEY (project_id) REFERENCES Projects(ProjectID)
);

-- Insert 5 sample rows
INSERT INTO Data_Sets VALUES
(1, 1, 'User Logs_2023', 9.50, '2025-08-29'),
(2, 2, 'TransactionData_Q1', 42.10, '2025-08-15'),
(3, 3, 'ChatHistory_v2', 8.00, '2025-11-14'),
(4, 4, 'MobileUsageStats', 12.50, '2025-07-03'),
(5, 5, 'AppFeedback', 5.90, '2025-08-17');

SELECT 
    p.ProjectID,
    p.ProjectName,
    d.dataset_name,
    d.size_gb,
    d.last_updated
FROM Projects p
JOIN Data_Sets d ON p.ProjectID = d.project_id
WHERE d.size_gb > 10
  AND d.last_updated BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND CURDATE()
ORDER BY p.ProjectName;






