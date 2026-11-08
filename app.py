from fastapi import Depends, FastAPI
from auth import get_current_active_user
from routes.user import router as user_router
from routes.details import router as details_router
from routes.households import router as household_router


app = FastAPI()
app.include_router(user_router)
app.include_router(details_router)
app.include_router(household_router)