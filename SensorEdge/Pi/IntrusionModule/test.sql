CREATE TABLE IF NOT EXISTS intrusions(
	edgeconnector numeric not null,
	intrudate datetime default CURRENT_TIMESTAMP,
	videofile text not null,
	uploaded numeric default 0
);
CREATE TABLE IF NOT EXISTS settings(
	globalalarmtime numeric not null, 
	forcedalarmtime numeric not null, 
	motiondetection numeric not null, 
	updated datetime default CURRENT_TIMESTAMP
);



