-- 更新 drag_events 表结构，添加 user_id 字段

-- 如果表已存在，添加 user_id 字段
ALTER TABLE drag_events ADD COLUMN IF NOT EXISTS user_id TEXT;

-- 如果表不存在，创建新表
CREATE TABLE IF NOT EXISTS drag_events (
    id SERIAL PRIMARY KEY,
    count INTEGER NOT NULL,
    user_id TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL
);

-- 为 user_id 字段创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_drag_events_user_id ON drag_events(user_id);

-- 为 timestamp 字段创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_drag_events_timestamp ON drag_events(timestamp);

-- 为 count 字段创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_drag_events_count ON drag_events(count);