# from fastapi import FastAPI
# from app.core.middleware import add_middleware
# from app.core.scheduler import start_scheduler, shutdown_scheduler, register_jobs
#
# def create_app() -> FastAPI:
#     app = FastAPI()
#
#     add_middleware(app)
#
#     @app.on_event("startup")
#     async def startup():
#         register_jobs()
#         start_scheduler()
#
#     @app.on_event("shutdown")
#     async def shutdown():
#         shutdown_scheduler()
#
#     return app
#
# app = create_app()
