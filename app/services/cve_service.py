"""
MongoDB CVE Service
Handles queries to the local CVE database for vulnerability checking
"""
from typing import List, Dict, Any, Optional
from pymongo import MongoClient
from pymongo.collection import Collection
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class CVEService:
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.database = None
        self.collection: Optional[Collection] = None
        self._connect()
    
    def _connect(self):
        """Connect to MongoDB CVE database"""
        try:
            self.client = MongoClient(settings.mongodb_connection_url)
            self.database = self.client[settings.mongodb_db_name]
            self.collection = self.database.cves
            logger.info("Connected to MongoDB CVE database")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    async def search_vulnerabilities_by_version(
        self, 
        brand: str, 
        model: str, 
        version: str
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
            # Search query - looking for CVEs that mention the brand, model, and version
            query = {
                "$and": [
                    {
                        "$or": [
                            {"cve.description.description_data.value": {"$regex": brand, "$options": "i"}},
                            {"cve.affects.vendor.vendor_data.vendor_name": {"$regex": brand, "$options": "i"}}
                        ]
                    },
                    {
                        "$or": [
                            {"cve.description.description_data.value": {"$regex": model, "$options": "i"}},
                            {"cve.affects.vendor.vendor_data.product.product_data.product_name": {"$regex": model, "$options": "i"}}
                        ]
                    },
                    {
                        "$or": [
                            {"cve.description.description_data.value": {"$regex": version, "$options": "i"}},
                            {"cve.affects.vendor.vendor_data.product.product_data.version.version_data.version_value": version}
                        ]
                    }
                ]
            }
            
            # Execute query
            results = list(self.collection.find(query).limit(50))
            
            logger.info(f"Found {len(results)} CVE records for {brand} {model} {version}")
            return results
            
        except Exception as e:
            logger.error(f"Error searching CVE database: {e}")
            return []
    
    async def search_vulnerabilities_by_keywords(
        self, 
        keywords: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Search for vulnerabilities using general keywords
        
        Args:
            keywords: List of search keywords
            
        Returns:
            List of CVE records matching the keywords
        """
        try:
            # Build OR query for keywords
            keyword_queries = []
            for keyword in keywords:
                keyword_queries.append({
                    "cve.description.description_data.value": {"$regex": keyword, "$options": "i"}
                })
            
            query = {"$or": keyword_queries}
            
            # Execute query
            results = list(self.collection.find(query).limit(30))
            
            logger.info(f"Found {len(results)} CVE records for keywords: {keywords}")
            return results
            
        except Exception as e:
            logger.error(f"Error searching CVE database with keywords: {e}")
            return []
    
    def close_connection(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

# Global CVE service instance
cve_service = CVEService()
