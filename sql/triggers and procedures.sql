create or replace procedure acc_bal(auid varchar(25))
language sql
as $$
	update users 
	set account_balance = (
	select
		(
			select sum(amount)
			from record
			where type = 'income'
		)
		-
		(
			select sum(amount)
			from record
			where type = 'expense'
		)
	as "net income")
	where uid = auid;
$$;



create or replace function rec(auid varchar(25), sel_date date)
returns table(tid varchar(25), tdate date, usr varchar(20), rec varchar(20), amt int, t char(10), cat varchar(25))
language plpgsql
as $$
begin
return query
select r.transaction_id,r.trans_date, u.username, r.receiver_id, r.amount, r.type, ca.category_name
from record r
join users u
on r.sender_id = u.uid 
join category ca
on r.cat_id = ca.category_id
where r.sender_id = auid
and r.trans_date between sel_date and current_date
order by r.trans_date desc;
end;
$$;

select * from rec('abc123', '2021-09-01');


create or replace function rec_stats(auid varchar(25), sel_date date)
returns table(inc int, exp int)
language plpgsql
as $$
declare inc1 int;
declare exp1 int;
begin
	
	select sum(amount) into inc1
	from record r
	where type = 'income'
	and r.sender_id = auid
	and r.trans_date between sel_date and current_date;
	
	select sum(amount) into exp1
	from record r
	where type = 'expense'
	and r.sender_id = auid
	and r.trans_date between sel_date and current_date;
	
return query select coalesce(inc1, 0) as inc, coalesce(exp1, 0) as inc;
end;
$$;

select rec_stats('abc123', '2023-01-29');

call update_acc_bal('abc123');


-- create or replace function pie_chart(auid varchar(25), sel_date date)
-- returns table(tid varchar(25), tdate date, usr varchar(20), rec varchar(20), amt int, t char(10), cat varchar(25))
-- language plpgsql
-- as $$
-- begin
-- return query
	select r.cat_id, ca.category_name, sum(r.amount)
	from record r
	join category ca
	on r.cat_id = ca.category_id
	group by r.cat_id;

