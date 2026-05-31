-- Профилактика битых text-индексов после смены версии/collation PostgreSQL
ALTER DATABASE shortlink REFRESH COLLATION VERSION;
