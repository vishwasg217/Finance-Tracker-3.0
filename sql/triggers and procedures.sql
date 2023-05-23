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
returns table(tid varchar(25), tdate date, sender text, rec text, amt int, t varchar(10), cat varchar(25))
language plpgsql
as $$
begin
return query
select r.transaction_id,r.trans_date, replace(sender_id, auid, u.username), replace(receiver_id, auid, u.username), r.amount, ca.type, ca.category_name
from record r
join users u
on (r.sender_id = u.uid or r.receiver_id=u.uid)
join category ca
on r.cat_id = ca.category_id
where (r.sender_id = auid or r.receiver_id = auid)
and r.trans_date between sel_date and current_date
order by r.trans_date desc;
end;
$$;

select * from rec('abc123', '2021-09-01');


create or replace function inc_line_chart(auid varchar(25))
returns table(t date, s bigint, tar integer)
language plpgsql
as $$ 
begin 
return query
	select date_trunc('month', r.trans_date)::date, sum(r.amount), u.savings_target
	from record r
	join users u
	on r.receiver_id = u.uid
	and r.receiver_id = auid
	group by date_trunc('month', r.trans_date), u.savings_target
	order by date_trunc('month', r.trans_date), u.savings_target;
end
$$;

select * from inc_line_chart('abc123');

create or replace function exp_line_chart(auid varchar(25))
returns table(t date, s bigint, tar integer)
language plpgsql
as $$ 
begin 
return query
	select date_trunc('month', r.trans_date)::date, sum(r.amount), u.savings_target
	from record r
	join users u
	on r.sender_id = u.uid
	and r.sender_id = auid
	group by date_trunc('month', r.trans_date), u.savings_target
	order by date_trunc('month', r.trans_date), u.savings_target;
end
$$;

select * from exp_line_chart('abc123');

create or replace function cat_line_chart(auid varchar(25), cat varchar(25))
returns table(t date, s bigint)
language plpgsql
as $$ 
begin 
return query
	select date_trunc('month', r.trans_date)::date, sum(r.amount)
	from record r
	join category ca
	on ca.category_id = r.cat_id
	where ca.category_name = cat
	and (r.sender_id = 'abc123' or r.receiver_id = 'abc123')
	group by date_trunc('month', r.trans_date)
	order by date_trunc('month', r.trans_date);
end;
$$;

select * from cat_line_chart('abc123', 'Salary');


create or replace function inc_pie_chart(auid varchar(25), d date)
returns table(cat varchar(25), s bigint)
language plpgsql
as $$
begin
return query
	select ca.category_name, sum(r.amount)
	from record r
	join category ca
	on r.cat_id = ca.category_id
	where r.receiver_id = auid
	and r.trans_date between d and current_date
	group by ca.category_name;
end;
$$;

select * from inc_pie_chart('abc123', '2021-01-01');

create or replace function exp_pie_chart(auid varchar(25), d date)
returns table(cat varchar(25), s bigint)
language plpgsql
as $$
begin
return query
	select ca.category_name, sum(r.amount)
	from record r
	join category ca
	on r.cat_id = ca.category_id
	where r.sender_id = auid
	and r.trans_date between d and current_date
	group by ca.category_name;
end;
$$;

select * from exp_pie_chart('abc123', '2021-01-01');


create or replace function cashflow(auid varchar(25), d date)
returns table(co bigint, s bigint)
language plpgsql
as $$
begin
return query
	select count(r.transaction_id), sum(r.amount)
	from record r
	join category ca
	on ca.category_id = r.cat_id
	where (r.sender_id = auid or r.receiver_id = auid)
	and r.trans_date between d and current_date
	group by ca.type
	order by ca.type desc;
end;
$$;

select * from cashflow('abc123', '2020-05-04');







