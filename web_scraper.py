"""
웹 스크래핑 유틸리티 모듈 (test.py 리팩토링)
"""
import logging
from typing import List, Optional
import requests
from lxml import etree
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class WebScraper:
    """웹 스크래핑을 담당하는 클래스"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        
        # 기본 헤더 설정
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_html(self, url: str) -> Optional[str]:
        """URL에서 HTML 콘텐츠를 가져옴"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            logger.info(f"HTML 페이지 로드 성공: {url}")
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"URL 로드 실패 {url}: {e}")
            return None
    
    def get_all_xpaths(self, url: str) -> List[str]:
        """URL의 모든 XPath를 추출"""
        html_content = self.fetch_html(url)
        if not html_content:
            return []
        
        try:
            soup = BeautifulSoup(html_content, 'lxml')
            dom = etree.HTML(str(soup))
            
            xpaths = []
            for element in dom.iter():
                xpath = dom.getpath(element)
                xpaths.append(xpath)
            
            logger.info(f"XPath 추출 완료: {len(xpaths)}개")
            return xpaths
            
        except Exception as e:
            logger.error(f"XPath 추출 실패: {e}")
            return []
    
    def save_xpaths_to_file(self, xpaths: List[str], filename: str = 'xpaths.txt'):
        """XPath 목록을 파일에 저장"""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                for xpath in xpaths:
                    file.write(f"{xpath}\n")
            logger.info(f"XPath 파일 저장 완료: {filename}")
        except Exception as e:
            logger.error(f"XPath 파일 저장 실패: {e}")
            raise
    
    def extract_xpaths_from_url(self, url: str, output_file: str = 'xpaths.txt'):
        """URL에서 모든 XPath를 추출하고 파일로 저장"""
        xpaths = self.get_all_xpaths(url)
        if xpaths:
            self.save_xpaths_to_file(xpaths, output_file)
            logger.info(f"XPath 추출 및 저장 완료: {output_file}")
            return True
        else:
            logger.warning("추출할 XPath가 없습니다")
            return False
    
    def close(self):
        """세션 정리"""
        self.session.close()


class ElementExtractor:
    """특정 요소 추출을 담당하는 클래스"""
    
    def __init__(self, scraper: WebScraper):
        self.scraper = scraper
    
    def extract_links(self, url: str) -> List[dict]:
        """페이지의 모든 링크를 추출"""
        html_content = self.scraper.fetch_html(url)
        if not html_content:
            return []
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            links = []
            
            for link in soup.find_all('a', href=True):
                links.append({
                    'text': link.get_text(strip=True),
                    'href': link['href']
                })
            
            logger.info(f"링크 추출 완료: {len(links)}개")
            return links
            
        except Exception as e:
            logger.error(f"링크 추출 실패: {e}")
            return []
    
    def extract_images(self, url: str) -> List[dict]:
        """페이지의 모든 이미지를 추출"""
        html_content = self.scraper.fetch_html(url)
        if not html_content:
            return []
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            images = []
            
            for img in soup.find_all('img', src=True):
                images.append({
                    'alt': img.get('alt', ''),
                    'src': img['src']
                })
            
            logger.info(f"이미지 추출 완료: {len(images)}개")
            return images
            
        except Exception as e:
            logger.error(f"이미지 추출 실패: {e}")
            return []
    
    def extract_text_by_tag(self, url: str, tag: str) -> List[str]:
        """특정 태그의 텍스트를 모두 추출"""
        html_content = self.scraper.fetch_html(url)
        if not html_content:
            return []
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            texts = []
            
            for element in soup.find_all(tag):
                text = element.get_text(strip=True)
                if text:
                    texts.append(text)
            
            logger.info(f"'{tag}' 태그 텍스트 추출 완료: {len(texts)}개")
            return texts
            
        except Exception as e:
            logger.error(f"텍스트 추출 실패: {e}")
            return []


def extract_xpaths_from_url(url: str, output_file: str = 'xpaths.txt') -> bool:
    """편의 함수: URL에서 XPath 추출 (기존 호환성 유지)"""
    scraper = WebScraper()
    try:
        return scraper.extract_xpaths_from_url(url, output_file)
    finally:
        scraper.close()


if __name__ == "__main__":
    # 예제 사용법
    url = "https://naver.com"
    
    # XPath 추출
    scraper = WebScraper()
    extractor = ElementExtractor(scraper)
    
    try:
        # XPath 추출
        scraper.extract_xpaths_from_url(url, "naver_xpaths.txt")
        
        # 링크 추출
        links = extractor.extract_links(url)
        print(f"추출된 링크 수: {len(links)}")
        
        # 이미지 추출
        images = extractor.extract_images(url)
        print(f"추출된 이미지 수: {len(images)}")
        
        # 제목 태그 추출
        titles = extractor.extract_text_by_tag(url, 'h1')
        print(f"추출된 H1 태그 수: {len(titles)}")
        
    finally:
        scraper.close()


