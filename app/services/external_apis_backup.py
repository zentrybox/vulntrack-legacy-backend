"""
External API Services
Handles Brave Search API and Gemini AI API calls
"""

import asyncio
import json
import logging
import time
from typing import Any, Dict, List

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
            "X-Subscription-Token": self.api_key,
        }
        # Rate limiting: 1 request per second for Brave Search API
        self._last_request_time = 0.0
        self._rate_limit_delay = 1.0  # 1 second between requests

    async def _wait_for_rate_limit(self):
        """Ensure we don't exceed the rate limit of 1 request per second"""
        current_time = time.time()
        time_since_last_request = current_time - self._last_request_time

        if time_since_last_request < self._rate_limit_delay:
            sleep_time = self._rate_limit_delay - time_since_last_request
            logger.info(
                f"⏳ Rate limiting: waiting {sleep_time:.2f} seconds before next Brave Search request"
            )
            await asyncio.sleep(sleep_time)

        self._last_request_time = time.time()

    async def search_vulnerabilities(
        self, brand: str, model: str, version: str
    ) -> Dict[str, Any]:
        """
        Search for vulnerability information using Brave Search API

        Args:
            brand: Device brand
            model: Device model
            version: Software version        Returns:
            Search results from Brave API
        """
        # Apply rate limiting before making the request
        await self._wait_for_rate_limit()

        try:  # Construct efficient search query for vulnerability research
            query = (
                f'"{brand}" "{model}" "{version}" vulnerability CVE security exploit'
            )

            params: Dict[str, Any] = {
                "q": query,
                "count": settings.brave_search_count,
                "freshness": "py",  # Past year for recent vulnerabilities
                "result_filter": "web",  # Only web results
            }

            # Construct the full URL for web search
            url = f"{self.base_url}/web/search"

            logger.info("🔍 Brave Search Request:")
            logger.info(f"  URL: {url}")
            logger.info(f"  Query: {query}")
            logger.info(f"  Headers: {self.headers}")
            logger.info(f"  Params: {params}")

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers=self.headers,
                    params=params,
                    timeout=settings.vuln_scan_timeout,
                )

                logger.info("📡 Brave Search Response:")
                logger.info(f"  Status Code: {response.status_code}")
                logger.info(f"  Headers: {dict(response.headers)}")

                if response.status_code == 200:
                    data = response.json()
                    logger.info("📄 Brave Search Response Body:")
                    logger.info(f"  Raw JSON: {data}")

                    # Log successful response with correct structure
                    result_count = len(data.get("web", {}).get("results", []))
                    logger.info(f"✅ Brave Search returned {result_count} web results")
                    # Log each result for debugging
                    for i, result in enumerate(
                        data.get("web", {}).get("results", [])[:3]
                    ):
                        logger.info(
                            f"  Result {i + 1}: {result.get('title', 'No title')}"
                        )
                        logger.info(f"  URL {i + 1}: {result.get('url', 'No URL')}")

                    return data
                elif response.status_code == 301:
                    logger.error("❌ Brave Search API: URL redirect (301)")
                    logger.error(f"Response body: {response.text}")
                    logger.error(
                        "💡 Check if the API URL is correct - might need different endpoint"
                    )
                    return {
                        "error": "url_redirect",
                        "details": "API URL might be incorrect",
                    }
                elif response.status_code == 401:
                    logger.error("❌ Brave Search API: Invalid API key")
                    logger.error(f"Response body: {response.text}")
                    return {"error": "invalid_api_key"}

                elif response.status_code == 429:
                    logger.error("❌ Brave Search API: Rate limit exceeded")
                    logger.error(f"Response body: {response.text}")

                    # Try to parse the response to get rate limit info
                    try:
                        rate_limit_info = response.json()
                        logger.error(f"📊 Rate limit details: {rate_limit_info}")
                        if "meta" in rate_limit_info.get("error", {}):
                            meta = rate_limit_info["error"]["meta"]
                            logger.error(
                                f"💡 Rate limit: {meta.get('rate_current', 'N/A')}/{meta.get('rate_limit', 'N/A')} requests"
                            )
                            logger.error(
                                f"💡 Quota: {meta.get('quota_current', 'N/A')}/{meta.get('quota_limit', 'N/A')} total"
                            )
                    except (json.JSONDecodeError, KeyError, AttributeError):
                        pass

                    # Wait longer before potential retry
                    logger.info("⏳ Waiting additional time due to rate limit...")
                    await asyncio.sleep(2.0)  # Wait 2 seconds on rate limit

                    return {
                        "error": "rate_limit_exceeded",
                        "details": "Request rate limit exceeded. Try again later.",
                        "retry_after": 2.0,
                    }
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
        self.headers = {"Content-Type": "application/json"}

    async def filter_vulnerability_results(
        self, search_results: List[Dict[str, Any]], device_info: Dict[str, str]
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
            prompt = self._create_vulnerability_analysis_prompt(
                search_results, device_info
            )

            # Gemini API request payload
            payload: Dict[str, Any] = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": settings.gemini_temperature,
                    "maxOutputTokens": settings.gemini_max_tokens,
                    "candidateCount": 1,
                },
            }
            # Make API call
            url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"

            logger.info("🤖 Gemini AI Request:")
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
                    timeout=settings.vuln_scan_timeout,
                )

                logger.info("🧠 Gemini AI Response:")
                logger.info(f"  Status Code: {response.status_code}")
                logger.info(f"  Headers: {dict(response.headers)}")

                if response.status_code == 200:
                    data = response.json()
                    logger.info("📄 Gemini AI Response Body:")
                    logger.info(f"  Raw JSON: {data}")

                    result_text = data["candidates"][0]["content"]["parts"][0]["text"]
                    logger.info("📝 Gemini Generated Text:")
                    logger.info(
                        f"  Text: {result_text}"
                    )  # Parse JSON response from Gemini (handle markdown code blocks)
                    try:
                        # Try to extract JSON from markdown code blocks if present
                        clean_text = result_text.strip()
                        if clean_text.startswith("```json") and clean_text.endswith(
                            "```"
                        ):
                            # Extract JSON from markdown code block
                            clean_text = clean_text[
                                7:-3
                            ].strip()  # Remove ```json and ```
                        elif clean_text.startswith("```") and clean_text.endswith(
                            "```"
                        ):
                            # Extract from generic code block
                            clean_text = clean_text[3:-3].strip()

                        parsed_result = json.loads(clean_text)
                        logger.info("✅ Gemini JSON parsed successfully:")
                        logger.info(f"  Parsed result: {parsed_result}")
                        return parsed_result
                    except json.JSONDecodeError as json_error:
                        logger.error(
                            f"❌ Failed to parse Gemini response as JSON: {json_error}"
                        )
                        logger.error(f"  Raw text: {result_text}")
                        return {
                            "vulnerability_found": False,
                            "error": "json_parse_error",
                            "raw_response": result_text,
                        }
                else:
                    logger.error(f"❌ Gemini API error: {response.status_code}")
                    logger.error(f"Response body: {response.text}")
                    return {"vulnerability_found": False, "error": "API error"}

        except Exception as e:
            logger.error(f"Error calling Gemini AI API: {e}")
            return {"vulnerability_found": False, "error": str(e)}

    def _create_vulnerability_analysis_prompt(
        self, search_results: List[Dict[str, Any]], device_info: Dict[str, str]
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
- Brand: {device_info.get("brand", "Unknown")}
- Model: {device_info.get("model", "Unknown")}
- Version: {device_info.get("version", "Unknown")}

SEARCH RESULTS TO ANALYZE:
{search_text}

TASK:
Analyze the search results and determine if there are legitimate vulnerabilities for this specific device and version.
Filter out false positives, marketing content, and irrelevant information.

IMPORTANT: Respond with ONLY pure JSON. Do NOT use markdown code blocks or backticks.

RESPONSE FORMAT (pure JSON only):
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
