# Fast_api_organizer



# Note :
 FastOrganize Plan
────────────────────────────

MOVE
app/users.py
→ app/routes/users.py

Reason:
Detected FastAPI route

MOVE
app/user_schema.py
→ app/schemas/user_schema.py

Reason:
Detected Pydantic schema

MOVE
app/user.py
→ app/models/user.py

Reason:
Detected SQLAlchemy model
# WorkFlow:
                   PROJECT
                    │
                    ↓
                 Scanner
                    │
                    ↓
                AST Analyzer
                    │
                    ↓
              FileAnalysis
                 /      \
                ↓        ↓
          Classifier   Imports
              │           │
              ↓           ↓
          File Role    Resolver
              │           │
              └─────┬─────┘
                    ↓
             Dependency Graph
                    │
                    ↓
          Reverse Dependencies
                    │
                    ↓
                 Planner
                    │
                    ↓
                MovePlan
                    │
             ┌──────┴──────┐
             ↓             ↓
        Import Rewriter  Executor
             │             │
             └──────┬──────┘
                    ↓
              Organized Project
