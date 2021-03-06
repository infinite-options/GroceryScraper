#!/bin/bash
# Type password when prompted to access the MySQL console for Infinite Options RDS

function usage () {
    echo "usage:";
    echo "--login, -l: log onto mysql server"
    echo "--create-groceries-table, -c: drop and create table in database, use with caution";
    echo "--create-price_competitive-table, -cp: drop and create table in database, use with caution";
    exit 1;
}

if [[ $# -eq 1 ]]; then
    case $1 in
    -l | --login)
        mysql -h io-mysqldb8.cxjnrciilyjq.us-west-1.rds.amazonaws.com -u admin -D sf -p
        exit 1
        ;;
    -c | --create-pricing-tables)
        mysql -h io-mysqldb8.cxjnrciilyjq.us-west-1.rds.amazonaws.com -u admin -D sf -p < create_groceries_in_sf.sql
        exit 1
        ;;
    -cp | --create-price_competitive-table)
        mysql -h io-mysqldb8.cxjnrciilyjq.us-west-1.rds.amazonaws.com -u admin -D sf -p < create_price_competitive_in_sf.sql
        exit 1
    *)
        usage
        ;;
    esac
else
    usage;
fi

