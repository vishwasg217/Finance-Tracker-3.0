select * from record;

select r.transaction_id,r.trans_date, u.username, r.receiver_id, r.amount, r.type, c.category_name
from record r
join users u
on r.sender_id = u.uid 
join category c
on r.cat_id = c.category_id
order by r.trans_date asc;

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
as "net income";
