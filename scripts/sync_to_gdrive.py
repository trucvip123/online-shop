import os
import sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle
import logging

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gdrive_sync.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Các quyền cần thiết
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_credentials():
    """Lấy credentials từ file hoặc tạo mới nếu cần."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def upload_file(service, file_path, folder_id=None):
    """Upload một file lên Google Drive."""
    file_name = os.path.basename(file_path)
    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    
    logging.info(f'File {file_name} đã được upload thành công. File ID: {file.get("id")}')
    return file.get('id')

def sync_folder(service, local_folder, drive_folder_id=None):
    """Đồng bộ toàn bộ thư mục lên Google Drive."""
    for root, dirs, files in os.walk(local_folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                upload_file(service, file_path, drive_folder_id)
            except Exception as e:
                logging.error(f'Lỗi khi upload file {file_path}: {str(e)}')

def main():
    try:
        # Lấy credentials
        creds = get_credentials()
        service = build('drive', 'v3', credentials=creds)
        
        # Đường dẫn đến thư mục media
        media_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media')
        
        # ID của thư mục trên Google Drive (nếu có)
        drive_folder_id = None  # Thay thế bằng ID thư mục của bạn nếu cần
        
        # Thực hiện đồng bộ
        logging.info('Bắt đầu đồng bộ dữ liệu...')
        sync_folder(service, media_folder, drive_folder_id)
        logging.info('Đồng bộ hoàn tất!')
        
    except Exception as e:
        logging.error(f'Lỗi: {str(e)}')
        sys.exit(1)

if __name__ == '__main__':
    main() 