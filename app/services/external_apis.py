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
            # Construct efficient search query for vulnerability research
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
              # Correct URL for Brave Search API
            url = f"{self.base_url}/web/search"
            
            logger.info(f"🔍 Brave Search Request:")
            logger.info(f"  URL: {url}")
            logger.info(f"  Query: {query}")
            logger.info(f"  Headers: {self.headers}")
            logger.info(f"  Params: {params}")
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers=self.headers,
                    params=params,
                    timeout=settings.vuln_scan_timeout
                )
                
                logger.info(f"📡 Brave Search Response:")
                logger.info(f"  Status Code: {response.status_code}")
                logger.info(f"  Headers: {dict(response.headers)}")
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"📄 Brave Search Response Body:")
                    logger.info(f"  Raw JSON: {data}")
                    
                    # Log successful response with correct structure
                    result_count = len(data.get('web', {}).get('results', []))
                    logger.info(f"✅ Brave Search returned {result_count} web results")
                    
                    # Log each result for debugging
                    for i, result in enumerate(data.get('web', {}).get('results', [])[:3]):
                        logger.info(f"  Result {i+1}: {result.get('title', 'No title')}")
                        logger.info(f"  URL {i+1}: {result.get('url', 'No URL')}")
                    
                    return data
                elif response.status_code == 401:
                    logger.error("❌ Brave Search API: Invalid API key")
                    logger.error(f"Response body: {response.text}")
                    return {"error": "invalid_api_key"}
                elif response.status_code == 429:
                    logger.error("❌ Brave Search API: Rate limit exceeded")
                    logger.error(f"Response body: {response.text}")
                    return {"error": "rate_limit_exceeded"}
                else:
                    logger.error(f"❌ Brave Search API error: {response.status_code}")
                    logger.error(f"Response body: {response.text}")
                    return {"error": f"api_error_{response.status_code}"}
                        
        except httpx.TimeoutException:
            logger.error("Brave Search API timeout")
            return {"error": "timeout"}
        except Exception as e:
            logger.error(f"Error calling Brave Search API: {e}")
            return {"error": str(e)}


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
            
            logger.info(f"🤖 Gemini AI Request:")
            logger.info(f"  URL: {url}")
            logger.info(f"  Model: {self.model}")
            logger.info(f"  Prompt length: {len(prompt)} characters")
            logger.info(f"  Search results count: {len(search_results)}")
            logger.info(f"  Device: {device_info}")
            logger.info(f"  Payload: {payload}")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers=self.headers,
                    json=payload,
                    timeout=settings.vuln_scan_timeout
                )
                
                logger.info(f"🧠 Gemini AI Response:")
                logger.info(f"  Status Code: {response.status_code}")
                logger.info(f"  Headers: {dict(response.headers)}")
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"📄 Gemini AI Response Body:")
                    logger.info(f"  Raw JSON: {data}")
                    
                    result_text = data["candidates"][0]["content"]["parts"][0]["text"]
                    logger.info(f"📝 Gemini Generated Text:")
                    logger.info(f"  Text: {result_text}")
                    
                    # Parse JSON response from Gemini
                    try:
                        parsed_result = json.loads(result_text)
                        logger.info(f"✅ Gemini JSON parsed successfully:")
                        logger.info(f"  Parsed result: {parsed_result}")
                        return parsed_result
                    except json.JSONDecodeError as json_error:
                        logger.error(f"❌ Failed to parse Gemini response as JSON: {json_error}")
                        logger.error(f"  Raw text: {result_text}")
                        return {"vulnerability_found": False, "raw_response": result_text}
                else:
                    logger.error(f"❌ Gemini API error: {response.status_code}")
                    logger.error(f"Response body: {response.text}")
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
