use pricing;
drop table if exists price_competitive;
create table if not exists price_competitive (
	ID INT(11) NOT NULL AUTO_INCREMENT,
    item_id varchar(225),
    item_name varchar(225),
    farm_price varchar(45),
    farm_unit varchar(45),
    market_name varchar(225),
    market_item_name varchar(225),
    market_item_id varchar(225),
    market_price varchar(225),
    market_unit varchar(45),
    market_zipcode varchar(45),
    market_price_date varchar(225),
    is_item_same varchar(45),
    is_competitive varchar(45)
);
