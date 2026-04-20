# Assignment 2 Grading: buenojacob

**Final Score: 39/100 (F)**

## Summary
- Database Models: 6/20
- Task Endpoints: 6/30
- Category Endpoints: 4/15
- Background Tasks: 5/15
- Docker Compose: 18/20

## Detailed Results

### Database Models (6/20)

❌ **DB-01**: Task model has all required fields
   - Score: 0/8
   - Deduction: Cannot create task to verify model fields (-8 pts, critical)

❌ **DB-02**: Category model with unique name constraint
   - Score: 3/6
   - Deduction: Cannot create category (status: no response) (-3 pts, major)

❌ **DB-03**: Task-Category relationship (task belongs to category)
   - Score: 3/6
   - Deduction: Cannot create category to test relationship (-3 pts, major)

### Task Endpoints with Validation (6/30)

❌ **TASK-01**: GET /tasks returns list of all tasks
   - Score: 2/4
   - Deduction: Returns 404 instead of 200 (-2 pts, major)

❌ **TASK-02**: GET /tasks?completed=false filters by completion status
   - Score: 0/4
   - Deduction: Filter query parameter not supported (-4 pts, major)

❌ **TASK-03**: GET /tasks/:id returns single task with category info
   - Score: 0/3
   - Deduction: Returns 404 for existing task (-3 pts, major)

✅ **TASK-04**: GET /tasks/:id returns 404 when not found
   - Score: 2/2
   - Correctly returns 404

❌ **TASK-05**: POST /tasks creates task, returns 201
   - Score: 0/4
   - Deduction: Returns 404 for valid task creation (-4 pts, critical)

❌ **TASK-06**: POST /tasks validates input (title required, length limits)
   - Score: 0/4
   - Deduction: No input validation implemented (-4 pts, major)

❌ **TASK-07**: Validation errors include structured messages
   - Score: 0/2
   - Deduction: No validation error to check message format (-2 pts, major)

❌ **TASK-08**: PUT /tasks/:id updates task, returns 200
   - Score: 0/3
   - Deduction: Returns 404 for PUT update (-3 pts, major)

✅ **TASK-09**: PUT /tasks/:id returns 404 when not found
   - Score: 1/1
   - Correctly returns 404

❌ **TASK-10**: DELETE /tasks/:id deletes task, returns 200 with message
   - Score: 0/2
   - Deduction: Returns 404 for DELETE (-2 pts, major)

✅ **TASK-11**: DELETE /tasks/:id returns 404 when not found
   - Score: 1/1
   - Correctly returns 404

### Category Endpoints (4/15)

❌ **CAT-01**: GET /categories returns categories with task_count
   - Score: 2/5
   - Deduction: Returns 404 instead of 200 (-3 pts, major)

❌ **CAT-02**: GET /categories/:id returns category with its tasks
   - Score: 1/3
   - Deduction: Category not found (may not have been created) (-2 pts, major)

❌ **CAT-03**: POST /categories validates unique name and hex color
   - Score: 0/4
   - Deduction: No category validation implemented (-4 pts, major)

❌ **CAT-04**: DELETE /categories/:id prevents deletion with existing tasks
   - Score: 1/3
   - Deduction: Cannot create category to test deletion protection (-2 pts, major)

### Background Task Processing (5/15)

✅ **BG-01**: Redis and rq worker properly configured
   - Score: 4/4
   - Redis and worker services defined in docker-compose.yml

❌ **BG-02**: notification_queued: true when due_date within 24h
   - Score: 0/5
   - Deduction: POST not responding (-5 pts, critical)

❌ **BG-03**: notification_queued: false when no due_date or > 24h
   - Score: 0/3
   - Deduction: notification_queued not correctly false for non-urgent tasks (-3 pts, major)

❌ **BG-04**: Background job executes (worker logs show reminder)
   - Score: 1/3
   - Worker logs present but no 'Reminder' message found
   - Deduction: Worker running but no reminder message in logs (-2 pts, minor)

### Docker Compose (18/20)

✅ **DOCK-01**: docker-compose.yml defines all 4 services (app, db, redis, worker)
   - Score: 5/5
   - All 4 services defined: ['db', 'redis', 'app', 'worker']

❌ **DOCK-02**: docker-compose up --build runs without errors
   - Score: 6/8
   - docker-compose up --build succeeded, all containers running
   - Deduction: Docker config issue fixed for grading (broken YAML/missing entrypoint/missing compose) (-2 pts, minor)

✅ **DOCK-03**: All services connect properly (app to db+redis, worker to redis)
   - Score: 4/4
   - Connectivity verified through functional endpoint tests

✅ **DOCK-04**: API is accessible and functional on configured port
   - Score: 3/3
   - API accessible at http://127.0.0.1:5050 (port 5050)

## Strengths
- docker-compose.yml defines all 4 services (app, db, redis, worker)
- Redis and rq worker properly configured
- All services connect properly (app to db+redis, worker to redis)
- API is accessible and functional on configured port
- GET /tasks/:id returns 404 when not found

## Areas for Improvement
- docker-compose up --build runs without errors: Docker config issue fixed for grading (broken YAML/missing entrypoint/missing compose)
- Task model has all required fields: Cannot create task to verify model fields
- Category model with unique name constraint: Cannot create category (status: no response)
- Task-Category relationship (task belongs to category): Cannot create category to test relationship
- GET /tasks returns list of all tasks: Returns 404 instead of 200
- GET /tasks?completed=false filters by completion status: Filter query parameter not supported
- GET /tasks/:id returns single task with category info: Returns 404 for existing task
- POST /tasks creates task, returns 201: Returns 404 for valid task creation
- POST /tasks validates input (title required, length limits): No input validation implemented
- Validation errors include structured messages: No validation error to check message format
- PUT /tasks/:id updates task, returns 200: Returns 404 for PUT update
- DELETE /tasks/:id deletes task, returns 200 with message: Returns 404 for DELETE
- GET /categories returns categories with task_count: Returns 404 instead of 200
- GET /categories/:id returns category with its tasks: Category not found (may not have been created)
- POST /categories validates unique name and hex color: No category validation implemented
- DELETE /categories/:id prevents deletion with existing tasks: Cannot create category to test deletion protection
- notification_queued: true when due_date within 24h: POST not responding
- notification_queued: false when no due_date or > 24h: notification_queued not correctly false for non-urgent tasks
- Background job executes (worker logs show reminder): Worker running but no reminder message in logs
