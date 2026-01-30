# 宇宙探索项目 - 用户系统说明

## 用户识别机制

### 前端实现

1. **用户 ID 生成**
   - 首次访问时自动生成唯一用户 ID
   - 格式：`user_<timestamp>_<random_string>`
   - 示例：`user_1704067200000_abc123xyz`

2. **用户 ID 存储**
   - 使用 `localStorage` 持久化存储
   - 用户关闭浏览器后重新打开仍保持相同 ID
   - 清除浏览器缓存会生成新 ID

3. **自动上报**
   - 每次拖曳事件都会携带用户 ID
   - 后端记录每个用户的拖曳行为

### 后端 API

#### 1. 上报拖曳事件
```http
POST /api/drag
Content-Type: application/json

{
  "count": 20,
  "user_id": "user_1704067200000_abc123xyz"
}
```

#### 2. 获取用户统计
```http
GET /api/user/{user_id}
```

返回示例：
```json
{
  "user_id": "user_1704067200000_abc123xyz",
  "total_drags": 45,
  "max_count": 20,
  "first_drag": "2024-01-01T10:00:00",
  "last_drag": "2024-01-01T12:30:00"
}
```

#### 3. 获取排行榜
```http
GET /api/leaderboard
```

返回示例：
```json
{
  "leaderboard": [
    {
      "user_id": "user_1704067200000_abc123xyz",
      "max_count": 100,
      "total_drags": 250
    },
    {
      "user_id": "user_1704067200001_def456uvw",
      "max_count": 80,
      "total_drags": 180
    }
  ]
}
```

## 数据库设置

### 1. 创建表结构

在 Supabase SQL 编辑器中执行以下 SQL：

```sql
-- 创建 drag_events 表
CREATE TABLE IF NOT EXISTS drag_events (
    id SERIAL PRIMARY KEY,
    count INTEGER NOT NULL,
    user_id TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_drag_events_user_id ON drag_events(user_id);
CREATE INDEX IF NOT EXISTS idx_drag_events_timestamp ON drag_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_drag_events_count ON drag_events(count);
```

或者直接执行项目中的 `database_schema.sql` 文件。

### 2. 表结构说明

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键，自增 |
| count | INTEGER | 拖曳次数 |
| user_id | TEXT | 用户唯一标识 |
| timestamp | TIMESTAMP | 事件时间戳 |

## 使用场景

### 1. 用户行为分析
- 追踪每个用户的探索次数
- 分析用户活跃度和使用频率
- 了解用户在页面的停留时间

### 2. 排行榜功能
- 展示探索次数最多的用户
- 激励用户更多参与
- 增强社交互动

### 3. 个性化体验
- 根据用户历史行为调整触发器
- 为不同用户定制不同的操作
- 记录用户的成就和里程碑

### 4. 数据统计
- 统计总用户数
- 分析用户留存率
- 生成使用报告

## 扩展功能

### 添加用户信息

可以扩展 `drag_events` 表，添加更多用户信息：

```sql
ALTER TABLE drag_events ADD COLUMN IF NOT EXISTS ip_address TEXT;
ALTER TABLE drag_events ADD COLUMN IF NOT EXISTS user_agent TEXT;
ALTER TABLE drag_events ADD COLUMN IF NOT EXISTS browser TEXT;
ALTER TABLE drag_events ADD COLUMN IF NOT EXISTS device TEXT;
```

### 创建独立的用户表

```sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL,
    last_seen TIMESTAMP NOT NULL,
    total_drags INTEGER DEFAULT 0,
    max_count INTEGER DEFAULT 0
);
```

### 添加成就系统

```sql
CREATE TABLE IF NOT EXISTS achievements (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    achievement_type TEXT NOT NULL,
    achieved_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES drag_events(user_id)
);
```

## 注意事项

1. **隐私保护**
   - 用户 ID 是随机生成的，不包含个人信息
   - 如需收集更多信息，请遵守隐私法规
   - 考虑添加隐私政策说明

2. **性能优化**
   - 已为常用查询字段创建索引
   - 大量用户时考虑分页查询
   - 定期清理过期数据

3. **数据安全**
   - 确保 Supabase API 密钥安全
   - 使用环境变量存储敏感信息
   - 定期备份数据库

## 测试

### 测试用户 ID 生成

打开浏览器控制台，执行：
```javascript
localStorage.getItem('user_id')
```

### 测试 API 调用

```bash
# 获取用户统计
curl http://localhost:8000/api/user/user_1704067200000_abc123xyz

# 获取排行榜
curl http://localhost:8000/api/leaderboard
```