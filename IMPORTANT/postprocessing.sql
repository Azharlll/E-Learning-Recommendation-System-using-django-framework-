create table Postprocessing_tab(
Unnamed0 int(3),
Unnamed01 int(3),
Unnamed011 int(3),
Surname varchar(20),

Firstname varchar(20),
Institution varchar(20),
Department varchar(20),
Emailaddress varchar(20),
State varchar(20),

Startedon varchar(20),
Completed varchar(20),
Timetaken varchar(20),
Grade350 varchar(20),
Q1M5 int(3),
Q2M5 int(3),

Q3M10 int(3),
Q4M10 int(3),
Q5M15 int(3),
Q6M15 int(3),
Q7M15 int(3),
Q8M20 int(3),
Q9M20 int(3),
Q10M5 int(3),

Q11M5 int(3),
Q12M10 int(3),
Q13M10 int(3),
Q14M15 int(3),
Q15M15 int(3),
Q16M15 int(3),
Q17M20 int(3),

Q18M20 int(3),
Q19M5 int(3),
Q20M5 int(3),
Q21M5 int(3),
Q22M5 int(3),
Q23M5 int(3),
Q24M5 int(3),

Q25M5 int(3),
Q26M5 int(3),
Q27M5 int(3),
Q28M5 int(3),
Q29M5 int(3),
Q30M5 int(3),
Q31M2 int(3),
Q32M2 int(3),

Q33M2 int(3),
Q34M2 int(3),
Q35M2 int(3),
Q36M10 int(3),
Q37M10 int(3),
Q38M30 int(3),
v_seeking int(3),
v_pauses int(3),

v_replay int(3),
a_seeking int(3),
a_pauses int(3),
a_replay int(3),
p_seeking int(3),
p_pauses int(3),
p_replay int(3),

VocabTotal int(3),
GrammarTotal int(3),
ReadingTotal int(3),
ComputerTotal int(3),
WritingTotal int(3),

VideoTotal int(3),
AudioTotal int(3),
PPTTotal int(3),
VocabSection int(3),
GrammarSection int(3),

ReadingSection int(3),
ComputerSection int(3),
WritingSection int(3),
VideoSection int(3),
AudioSection int(3),

PPTSection int(3),
VocabLabel  varchar(20),
GrammarLabel  varchar(20),
ReadingLabel  varchar(20),

ComputerLabel  varchar(20),
WritingLabel  varchar(20),
VideoLabel  varchar(20),
AudioLabel varchar(20),

PPTLabel varchar(20));

LOAD DATA  LOCAL INFILE '/home/tesla/MyWorld/Work/Works_6/WebWorks/Site2/Part1/E-learning (New)/English11.csv'
INTO TABLE Postprocessing_tab
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
