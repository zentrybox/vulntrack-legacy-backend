"""
MongoDB CVE Service
Handles queries to the local CVE database for vulnerability checking
"""

import logging
from typing import Any, Dict, List, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from app.core.config import settings

logger = logging.getLogger(__name__)


class CVEService:
    def __init__(self):
        self.client: Optional[MongoClient[Dict[str, Any]]] = None
        self.database: Optional[Database[Dict[str, Any]]] = None
        self.collection: Optional[Collection[Dict[str, Any]]] = None
        self._connect()

    def _connect(self) -> None:
        """Connect to MongoDB CVE database"""
        try:
            # Try to connect to MongoDB
            connection_url = settings.mongodb_connection_url
            logger.info(f"Attempting to connect to MongoDB: {connection_url}")

            self.client = MongoClient(
                connection_url,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=5000,
            )

            # Test the connection
            self.client.admin.command("ping")

            self.database = self.client[settings.mongodb_db_name]
            self.collection = self.database.cves
            logger.info("Successfully connected to MongoDB CVE database")

        except Exception as e:
            logger.warning(f"MongoDB connection failed: {e}")
            logger.info(
                "CVE service will continue without local database (web search only)"
            )
            self.client = None
            self.database = None
            self.collection = None

    async def search_vulnerabilities_by_version(
        self, brand: str, model: str, version: str
    ) -> List[Dict[str, Any]]:
        """
        Search for known vulnerabilities by device brand, model and version

        Args:
            brand: Device brand (e.g., "Cisco", "Fortinet")
            model: Device model
            version: Software/firmware version

        Returns:
            List of CVE records matching the criteria
        """
        try:
            # Check if MongoDB connection is available
            if self.collection is None:
                logger.warning("MongoDB not connected, returning empty results")
                return []

            # Search query - looking for CVEs that mention the brand, model, and version
            query: Dict[str, Any] = {
                "$and": [
                    {
                        "$or": [
                            {
                                "cve.description.description_data.value": {
                                    "$regex": brand,
                                    "$options": "i",
                                }
                            },
                            {
                                "cve.affects.vendor.vendor_data.vendor_name": {
                                    "$regex": brand,
                                    "$options": "i",
                                }
                            },
                        ]
                    },
                    {
                        "$or": [
                            {
                                "cve.description.description_data.value": {
                                    "$regex": model,
                                    "$options": "i",
                                }
                            },
                            {
                                "cve.affects.vendor.vendor_data.product.product_data.product_name": {
                                    "$regex": model,
                                    "$options": "i",
                                }
                            },
                        ]
                    },
                    {
                        "$or": [
                            {
                                "cve.description.description_data.value": {
                                    "$regex": version,
                                    "$options": "i",
                                }
                            },
                            {
                                "cve.affects.vendor.vendor_data.product.product_data.version.version_data.version_value": version
                            },
                        ]
                    },
                ]
            }

            # Execute query
            results = list(self.collection.find(query).limit(50))

            logger.info(
                f"Found {len(results)} CVE records for {brand} {model} {version}"
            )
            return results

        except Exception as e:
            logger.error(f"Error searching CVE database: {e}")
            return []

    async def search_vulnerabilities_by_keywords(
        self, keywords: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Search for vulnerabilities using general keywords

        Args:
            keywords: List of search keywords

        Returns:
            List of CVE records matching the keywords
        """
        try:
            # Check if MongoDB connection is available
            if self.collection is None:
                logger.warning("MongoDB not connected, returning empty results")
                return []

            # Build OR query for keywords
            keyword_queries: List[Dict[str, Any]] = []
            for keyword in keywords:
                keyword_queries.append(
                    {
                        "cve.description.description_data.value": {
                            "$regex": keyword,
                            "$options": "i",
                        }
                    }
                )

            query: Dict[str, Any] = {"$or": keyword_queries}

            # Execute query
            results = list(self.collection.find(query).limit(30))

            logger.info(f"Found {len(results)} CVE records for keywords: {keywords}")
            return results

        except Exception as e:
            logger.error(f"Error searching CVE database with keywords: {e}")
            return []

    def close_connection(self) -> None:
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")


# Global CVE service instance
cve_service = CVEService()
