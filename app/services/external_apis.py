"""
External API Services
Handles Brave Search API and Gemini AI API calls
"""
import json
import logging
from typing import List, Dict, Any
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)

class BraveSearchService:
    def __init__(self):
        self.api_key = settings.brave_search_api_key
        self.base_url = settings.brave_search_base_url
        self.headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.api_key
        }
    
    async def search_vulnerabilities(
        self, 
        brand: str, 
        model: str, 
        version: str
    ) -> Dict[str, Any]:
        """
        Search for vulnerability information using Brave Search API
        
        Args:
            brand: Device brand
            model: Device model  
            version: Software version
            
        Returns:
            Search results from Brave API
        """
        try:
            # Construct efficient search query
            query = f'"{brand}" "{model}" "{version}" vulnerability CVE security exploit'
            
            params = {
                "q": query,
                "count": settings.brave_search_count,
                "country": settings.brave_search_country,
                "search_lang": settings.brave_search_search_lang,
                "ui_lang": settings.brave_search_ui_lang,
                "freshness": "py",  # Past year for recent vulnerabilities
                "spellcheck": 1
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.base_url,
                    headers=self.headers,
                    params=params,
                    timeout=settings.vuln_scan_timeout
                )
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"Brave Search returned {len(data.get('web', {}).get('results', []))} results")
                    return data
                else:
                    logger.error(f"Brave Search API error: {response.status_code}")
                    return {}
                        
        except Exception as e:
            logger.error(f"Error calling Brave Search API: {e}")
            return {}


class GeminiAIService:
    def __init__(self):
        self.api_key = settings.gemini_api_key
        self.model = settings.gemini_model
        self.base_url = settings.gemini_base_url
        self.headers = {
            "Content-Type": "application/json"
        }
    
    async def filter_vulnerability_results(
        self, 
        search_results: List[Dict[str, Any]], 
        device_info: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Use Gemini AI to filter and analyze vulnerability search results
        
        Args:
            search_results: Raw search results from Brave Search
            device_info: Device information (brand, model, version)
            
        Returns:
            Filtered and analyzed vulnerability information
        """
        try:
            # Prepare prompt for Gemini
            prompt = self._create_vulnerability_analysis_prompt(search_results, device_info)
            
            # Gemini API request payload
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": settings.gemini_temperature,
                    "maxOutputTokens": settings.gemini_max_tokens,
                    "candidateCount": 1
                }
            }
            
            # Make API call
            url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers=self.headers,
                    json=payload,
                    timeout=settings.vuln_scan_timeout
                )
                if response.status_code == 200:
                    data = response.json()
                    result_text = data["candidates"][0]["content"]["parts"][0]["text"]
                    
                    # Parse JSON response from Gemini
                    try:
                        parsed_result = json.loads(result_text)
                        return parsed_result
                    except json.JSONDecodeError:
                        logger.warning("Failed to parse Gemini response as JSON")
                        return {"vulnerability_found": False, "raw_response": result_text}
                else:
                    logger.error(f"Gemini API error: {response.status_code}")
                    return {"vulnerability_found": False, "error": "API error"}
                        
        except Exception as e:
            logger.error(f"Error calling Gemini AI API: {e}")
            return {"vulnerability_found": False, "error": str(e)}
    
    def _create_vulnerability_analysis_prompt(
        self, 
        search_results: List[Dict[str, Any]], 
        device_info: Dict[str, str]
    ) -> str:
        """Create structured prompt for Gemini AI analysis"""
        
        # Extract relevant text from search results
        search_text = ""
        for result in search_results[:5]:  # Limit to top 5 results
            title = result.get("title", "")
            description = result.get("description", "")
            search_text += f"Title: {title}\nDescription: {description}\n\n"
        
        prompt = f"""
You are a cybersecurity expert analyzing search results for potential vulnerabilities.

DEVICE INFORMATION:
- Brand: {device_info.get('brand', 'Unknown')}
- Model: {device_info.get('model', 'Unknown')}  
- Version: {device_info.get('version', 'Unknown')}

SEARCH RESULTS TO ANALYZE:
{search_text}

TASK:
Analyze the search results and determine if there are legitimate vulnerabilities for this specific device and version.
Filter out false positives, marketing content, and irrelevant information.

RESPONSE FORMAT (JSON only):
{{
    "vulnerability_found": true/false,
    "confidence_score": 0.0-1.0,
    "vulnerabilities": [
        {{
            "cve_id": "CVE-YYYY-XXXXX",
            "severity": "Critical/High/Medium/Low",
            "description": "Brief description",
            "source_url": "URL if available"
        }}
    ],
    "summary": "Brief explanation of findings",
    "false_positives_filtered": 0-10
}}
"""
        return prompt


# Global service instances
brave_search_service = BraveSearchService()
gemini_ai_service = GeminiAIService()
