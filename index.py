import requests
import os
import hashlib
from urllib.parse import urlparse
from pathlib import Path

def main():
    """
    Ubuntu Image Fetcher - A tool for mindfully collecting images from the web
    Embodies Ubuntu principles: Community, Respect, Sharing, Practicality
    """
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    # Get URL from user
    url = input("Please enter the image URL: ").strip()
    
    if not url:
        print("✗ No URL provided. Ubuntu thrives on connection.")
        return
    
    try:
        # Create directory if it doesn't exist (Ubuntu principle: Sharing)
        os.makedirs("Fetched_Images", exist_ok=True)
        
        # Fetch the image with proper headers (Ubuntu principle: Respect)
        headers = {
            'User-Agent': 'Ubuntu-Image-Fetcher/1.0 (Educational Purpose)'
        }
        
        print("Connecting to the global community...")
        response = requests.get(url, timeout=10, headers=headers, stream=True)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Check if the content is actually an image
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            print(f"⚠ Warning: Content type is '{content_type}', not an image")
            proceed = input("Continue anyway? (y/N): ").lower()
            if proceed != 'y':
                print("Operation cancelled. Respect for data types maintained.")
                return
        
        # Extract filename from URL or generate one (Ubuntu principle: Practicality)
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # If no filename in URL, generate one based on content type
        if not filename or '.' not in filename:
            extension = get_extension_from_content_type(content_type) or '.jpg'
            filename = f"ubuntu_image_{hash(url) % 10000}{extension}"
        
        # Ensure safe filename (Ubuntu principle: Respect)
        filename = sanitize_filename(filename)
        filepath = os.path.join("Fetched_Images", filename)
        
        # Check for duplicate files (Ubuntu principle: Sharing - avoid waste)
        if os.path.exists(filepath):
            print(f"⚠ File {filename} already exists")
            choice = input("Overwrite? (y/N): ").lower()
            if choice != 'y':
                # Generate unique filename
                base, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(filepath):
                    filename = f"{base}_{counter}{ext}"
                    filepath = os.path.join("Fetched_Images", filename)
                    counter += 1
                print(f"Saving as {filename} instead")
        
        # Save the image in chunks (Ubuntu principle: Respect for resources)
        file_size = int(response.headers.get('content-length', 0))
        if file_size > 50 * 1024 * 1024:  # 50MB limit
            print(f"⚠ Large file detected: {file_size / (1024*1024):.1f}MB")
            proceed = input("Continue download? (y/N): ").lower()
            if proceed != 'y':
                print("Download cancelled. Bandwidth conservation practiced.")
                return
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        # Verify the download
        actual_size = os.path.getsize(filepath)
        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
        print(f"✓ File size: {actual_size / 1024:.1f} KB")
        
        if file_size > 0 and actual_size != file_size:
            print("⚠ Warning: File size mismatch - download may be incomplete")
        
        print("\nConnection strengthened. Community enriched.")
        print("Ubuntu: 'I am because we are' - Thank you for being part of our community.")
        
    except requests.exceptions.ConnectionError:
        print("✗ Connection error: Unable to reach the server")
        print("Ubuntu wisdom: Sometimes connections take time to establish")
    except requests.exceptions.Timeout:
        print("✗ Timeout error: Server took too long to respond")
        print("Ubuntu wisdom: Patience is a virtue, but sometimes we must try again")
    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP error: {e}")
        print("Ubuntu wisdom: Not all paths lead to sharing, but we respect the journey")
    except requests.exceptions.RequestException as e:
        print(f"✗ Request error: {e}")
        print("Ubuntu wisdom: Every failure teaches us something valuable")
    except PermissionError:
        print("✗ Permission denied: Cannot write to the directory")
        print("Ubuntu wisdom: Respect the system's boundaries")
    except Exception as e:
        print(f"✗ An unexpected error occurred: {e}")
        print("Ubuntu wisdom: In diversity there is beauty and strength")

def get_extension_from_content_type(content_type):
    """Extract file extension from content type"""
    extensions = {
        'image/jpeg': '.jpg',
        'image/jpg': '.jpg',
        'image/png': '.png',
        'image/gif': '.gif',
        'image/webp': '.webp',
        'image/bmp': '.bmp',
        'image/svg+xml': '.svg',
        'image/tiff': '.tiff'
    }
    return extensions.get(content_type.lower())

def sanitize_filename(filename):
    """Sanitize filename to prevent security issues"""
    # Remove or replace dangerous characters
    dangerous_chars = '<>:"/\\|?*'
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    
    return filename

def handle_multiple_urls():
    """Challenge 1: Handle multiple URLs at once"""
    print("\n=== Ubuntu Image Fetcher - Batch Mode ===")
    print("Enter multiple URLs (one per line). Press Enter twice when done.\n")
    
    urls = []
    while True:
        url = input("URL: ").strip()
        if not url:
            break
        urls.append(url)
    
    if not urls:
        print("No URLs provided.")
        return
    
    print(f"\nProcessing {len(urls)} URLs...")
    successful = 0
    
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Processing: {url}")
        # Here you would call a modified version of the main download logic
        # Implementation left as exercise
        
    print(f"\nBatch complete: {successful}/{len(urls)} successful downloads")

def check_file_safety(url, response):
    """Challenge 2: Safety precautions for unknown sources"""
    safety_checks = []
    
    # Check file size
    file_size = int(response.headers.get('content-length', 0))
    if file_size > 100 * 1024 * 1024:  # 100MB
        safety_checks.append(f"Large file: {file_size / (1024*1024):.1f}MB")
    
    # Check content type
    content_type = response.headers.get('content-type', '')
    if not content_type.startswith('image/'):
        safety_checks.append(f"Unexpected content type: {content_type}")
    
    # Check URL reputation (basic check)
    suspicious_domains = ['suspicious.com', 'malware.net']  # Example
    domain = urlparse(url).netloc.lower()
    if any(sus in domain for sus in suspicious_domains):
        safety_checks.append(f"Potentially suspicious domain: {domain}")
    
    return safety_checks

def prevent_duplicates(filepath):
    """Challenge 3: Prevent downloading duplicate images"""
    if not os.path.exists(filepath):
        return False
    
    print(f"File {os.path.basename(filepath)} already exists")
    
    # Could also implement hash-based duplicate detection
    # by calculating SHA256 of existing files
    
    return True

def check_important_headers(response):
    """Challenge 4: Check important HTTP headers"""
    important_headers = {
        'content-length': 'File size',
        'content-type': 'Content type',
        'last-modified': 'Last modified',
        'server': 'Server info',
        'content-encoding': 'Encoding',
        'cache-control': 'Cache policy'
    }
    
    print("\n=== HTTP Headers Analysis ===")
    for header, description in important_headers.items():
        value = response.headers.get(header)
        if value:
            print(f"{description}: {value}")

if __name__ == "__main__":
    main()
    
