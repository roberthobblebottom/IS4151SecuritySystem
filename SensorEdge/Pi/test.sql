CREATE TABLE IF NOT EXISTS intrusions(
	edgeconnector numeric not null,
	intrudate datetime default CURRENT_TIMESTAMP,
	videofile text not null,
	uploaded numeric default 0
);
