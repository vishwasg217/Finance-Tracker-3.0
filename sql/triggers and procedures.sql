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


create or replace function cashflow(auid varchar(25), sel_date date)
returns table(ct bigint, s bigint)
language plpgsql
as $$
begin
return query
	select count(r.transaction_id), sum(r.amount)
	from record r
	join category ca
	on ca.category_id = r.cat_id
	where r.sender_id = auid
	and r.trans_date between sel_date and current_date
	group by ca.type
	order by ca.type desc;
end
$$;
select * from cashflow('abc123', '2020-05-04');

create or replace function line_chart(auid varchar(25), t_type varchar(10))
returns table(t date, s bigint, tar integer)
language plpgsql
as $$ 
begin 
return query
	select date_trunc('month', r.trans_date)::date, sum(r.amount), u.savings_target
	from record r
	join category ca
	on ca.category_id = r.cat_id
	join users u
	on r.sender_id = u.uid
	where ca.type = t_type
	and r.sender_id = auid
	group by date_trunc('month', r.trans_date), u.savings_target
	order by date_trunc('month', r.trans_date), u.savings_target;
end
$$;

select * from line_chart('abc123', 'income');



