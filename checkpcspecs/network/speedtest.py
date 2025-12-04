"""Speed test functionality."""

import logging
from dataclasses import dataclass
from typing import Optional

import speedtest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


@dataclass
class SpeedTestResult:
    """Result of a speed test."""
    download: float  # Mbps
    upload: float  # Mbps
    success: bool
    error: Optional[str] = None


class SpeedTester:
    """Handles internet speed testing with multiple fallback methods."""

    @staticmethod
    def _test_standard() -> tuple[float, float]:
        """Standard speedtest method."""
        sp = speedtest.Speedtest()
        download = round(sp.download() / (10 ** 6), 2)
        upload = round(sp.upload() / (10 ** 6), 2)
        return download, upload

    @staticmethod
    def _test_secure() -> tuple[float, float]:
        """Secure speedtest method (backup)."""
        sp = speedtest.Speedtest(secure=True)
        download = round(sp.download() / (10 ** 6), 2)
        upload = round(sp.upload() / (10 ** 6), 2)
        return download, upload

    @staticmethod
    def _test_fallback() -> tuple[float, float]:
        """Fallback speed test using file download."""
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        # Download test
        url = 'https://speed.hetzner.de/100MB.bin'
        try:
            response = session.get(url, stream=True, timeout=30)
            total_length = int(response.headers.get('content-length', 0))
            
            import time
            start = time.time()
            downloaded = 0
            
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    downloaded += len(chunk)
            
            elapsed = time.time() - start
            download = round((downloaded * 8) / (elapsed * 10**6), 2)  # Mbps
            
            # Simple upload test (POST small data)
            start = time.time()
            test_data = b'0' * (1024 * 1024)  # 1MB
            response = session.post('https://httpbin.org/post', data=test_data, timeout=30)
            elapsed = time.time() - start
            upload = round((len(test_data) * 8) / (elapsed * 10**6), 2)  # Mbps
            
            return download, upload
        finally:
            session.close()

    @classmethod
    def test(cls) -> SpeedTestResult:
        """Run speed test with multiple fallback methods.
        
        Returns:
            SpeedTestResult with download/upload speeds in Mbps
        """
        methods = [
            ('standard', cls._test_standard),
            ('secure', cls._test_secure),
            ('fallback', cls._test_fallback)
        ]

        for method_name, method in methods:
            try:
                logger.info(f"Attempting speed test using {method_name} method")
                download, upload = method()
                logger.info(f"Speed test successful: {download} Mbps down, {upload} Mbps up")
                return SpeedTestResult(
                    download=download,
                    upload=upload,
                    success=True
                )
            except Exception as e:
                logger.warning(f"Speed test method '{method_name}' failed: {e}")
                continue

        logger.error("All speed test methods failed")
        return SpeedTestResult(
            download=-1,
            upload=-1,
            success=False,
            error="All speed test methods failed"
        )
