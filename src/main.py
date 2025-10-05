from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .service import router

app = FastAPI(
    title='K-PaaS 2025 Image Service',
    summary='Image Service for K-PaaS 2025',
    docs_url='/',
)

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(router.router)