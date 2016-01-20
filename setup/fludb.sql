prompt >> Starting up
startup
alter session set "_ORACLE_SCRIPT"=true;
prompt >> Dropping fludb user
drop user fludb cascade;
prompt >> Creating fludb...

prompt >> Creating tablespace
CREATE TABLESPACE FLUDB DATAFILE 'fludb.dbf' SIZE 1G reuse AUTOEXTEND ON nologging;

prompt >> Creating user
CREATE USER fludb IDENTIFIED BY flushot
	DEFAULT TABLESPACE FLUDB
	QUOTA UNLIMITED ON FLUDB;

prompt >> Assiging privileges
grant dba to fludb;
grant ALTER ANY PROCEDURE to fludb;
grant ALTER SYSTEM to fludb;
grant CREATE ANY PROCEDURE to fludb;
grant CREATE PROCEDURE to fludb;
grant CREATE TABLE to fludb;
grant DEBUG ANY PROCEDURE to fludb;
grant DEBUG CONNECT SESSION to fludb;
grant EXECUTE ANY PROCEDURE to fludb;
grant UNLIMITED TABLESPACE to fludb;

prompt >> creating staging directory
!mkdir /home/oracle/fludb_staging
create or replace directory fludb_directory as '/home/oracle/fludb_staging';
grant all on directory fludb_directory to fludb;
quit
