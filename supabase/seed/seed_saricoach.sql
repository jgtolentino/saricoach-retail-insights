-- Insert Store
insert into stores (name, owner_name) 
values ('Sari-Sari Store #1', 'Maria') 
on conflict do nothing;

-- Insert Metrics for Today (Assuming today is the demo day, usually you use dynamic dates in prod)
insert into daily_metrics (store_id, date, volume, revenue, avg_basket_size, avg_duration_seconds)
values 
(1, (now() at time zone 'Asia/Manila')::date, 649, 135785.00, 2.4, 42)
on conflict (store_id, date) do update 
set volume = EXCLUDED.volume, revenue = EXCLUDED.revenue;

-- Insert Chart Data (Hourly)
-- Clear existing for today to avoid dupes/mess
delete from hourly_traffic where store_id = 1 and date = (now() at time zone 'Asia/Manila')::date;

insert into hourly_traffic (store_id, date, hour_of_day, volume)
values 
(1, (now() at time zone 'Asia/Manila')::date, 8, 45),
(1, (now() at time zone 'Asia/Manila')::date, 10, 120),
(1, (now() at time zone 'Asia/Manila')::date, 12, 160),
(1, (now() at time zone 'Asia/Manila')::date, 14, 90),
(1, (now() at time zone 'Asia/Manila')::date, 16, 140),
(1, (now() at time zone 'Asia/Manila')::date, 18, 190);

-- Insert AI Insights
delete from daily_insights where store_id = 1 and date = (now() at time zone 'Asia/Manila')::date;

insert into daily_insights (store_id, date, insights, coach_message)
values 
(1, (now() at time zone 'Asia/Manila')::date, 
 ARRAY['Peak traffic detected between 5:00 PM and 7:00 PM.', 'Coke Zero stocks are critically low (3 units left).'], 
 'Traffic is surging in the late afternoon. Consider moving high-margin snacks near the counter for the 5 PM rush.'
);
