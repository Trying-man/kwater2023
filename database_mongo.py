import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from dotenv import load_dotenv
import logging

load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB 연결 설정
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("MONGO_DATABASE", "news_collector")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "articles")

# MongoDB 클라이언트 (동기)
mongo_client = None
database = None
collection = None

# MongoDB 클라이언트 (비동기)
async_mongo_client = None
async_database = None
async_collection = None

def get_mongo_client():
    """동기 MongoDB 클라이언트를 반환합니다."""
    global mongo_client
    if mongo_client is None:
        try:
            mongo_client = MongoClient(MONGO_URL)
            logger.info(f"MongoDB 연결 성공: {MONGO_URL}")
        except Exception as e:
            logger.error(f"MongoDB 연결 실패: {e}")
            raise
    return mongo_client

def get_database():
    """데이터베이스를 반환합니다."""
    global database
    if database is None:
        client = get_mongo_client()
        database = client[DATABASE_NAME]
    return database

def get_collection():
    """컬렉션을 반환합니다."""
    global collection
    if collection is None:
        db = get_database()
        collection = db[COLLECTION_NAME]
    return collection

async def get_async_mongo_client():
    """비동기 MongoDB 클라이언트를 반환합니다."""
    global async_mongo_client
    if async_mongo_client is None:
        try:
            async_mongo_client = AsyncIOMotorClient(MONGO_URL)
            logger.info(f"비동기 MongoDB 연결 성공: {MONGO_URL}")
        except Exception as e:
            logger.error(f"비동기 MongoDB 연결 실패: {e}")
            raise
    return async_mongo_client

async def get_async_database():
    """비동기 데이터베이스를 반환합니다."""
    global async_database
    if async_database is None:
        client = await get_async_mongo_client()
        async_database = client[DATABASE_NAME]
    return async_database

async def get_async_collection():
    """비동기 컬렉션을 반환합니다."""
    global async_collection
    if async_collection is None:
        db = await get_async_database()
        async_collection = db[COLLECTION_NAME]
    return async_collection

def create_indexes():
    """컬렉션에 인덱스를 생성합니다."""
    try:
        collection = get_collection()
        
        # URL 기반 중복 방지 인덱스
        collection.create_index("url", unique=True)
        
        # 날짜 기반 검색 인덱스
        collection.create_index("published_at")
        collection.create_index("created_at")
        
        # 감정 분석 인덱스
        collection.create_index("sentiment")
        
        # 텍스트 검색 인덱스 (제목과 내용)
        collection.create_index([("title", "text"), ("content", "text")])
        
        # 개별 필드 인덱스 (정규식 검색용)
        collection.create_index("title")
        collection.create_index("content")
        
        logger.info("MongoDB 인덱스 생성 완료")
    except Exception as e:
        logger.error(f"인덱스 생성 실패: {e}")

def close_connection():
    """MongoDB 연결을 종료합니다."""
    global mongo_client, async_mongo_client
    if mongo_client:
        mongo_client.close()
        mongo_client = None
    if async_mongo_client:
        async_mongo_client.close()
        async_mongo_client = None
    logger.info("MongoDB 연결 종료")
