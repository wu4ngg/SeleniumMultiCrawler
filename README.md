<div align=center>
  <h1>Selenium Multi Crawler</h1>
  <p>Dụng cụ crawl sản phẩm từ Google, Lazada dựa trên dữ liệu Excel</p>
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
  <img src="https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white"/>
</div>

## Chức năng
- Giao diện người dùng được xây dựng bằng Tkinter.
- Chọn file từ file system và crawl Lazada, Google bằng file đó. [Mẫu Excel](https://github.com/user-attachments/files/17644004/danh_sach_san_pham.xlsx)
- Xuất file excel kết quả đã crawl, sắp xếp theo từng sheet theo các từ khóa trên file excel đầu vào
- Tìm kiếm trên kết quả đã crawl trên giao diện
## Nhược điểm
- Chỉ chấp nhận dữ liệu Excel theo mẫu.
- Không có biện pháp lách giao diện kiểm tra Robot của Lazada.
## Tải về
Build code đi bro.
## Cách build và khởi chạy
### Bước 1: Lấy project về
Để có thể truy cập vào mã nguồn và build, cần phải tải project về máy. Các bước tải như sau:
- Trên tất cả nền tảng:
```
git clone https://github.com/wu4ngg/SeleniumMultiCrawler
cd SeleniumMultiCrawler
```
### Bước 2: Tạo môi trường Python
Môi trường ảo Python (virtual environment) giúp chúng ta cài đặt các dependency và thực thi code ở mức độ project, giúp việc quản lý các phiên bản python và các dependency dễ dàng hơn. Sau đây là các bước khởi tạo môi trường ảo Python:\
**Trước khi khởi tạo môi trường ảo, hãy cài đặt Python 3.12+.**
- Trên tất cả nền tảng
```
python -m venv .venv
```
- Trên Windows:
```
.venv\Scripts\activate
```
- Trên MacOS/Linux:
```
source myenv/bin/activate
```
### Bước 3: Cài đặt dependencies
Các dependencies đã được lưu trữ trong 1 file requirements.txt duy nhất, sau đây là câu lệnh thực thi việc cài dependencies từ file này:
```
pip install -r requirements.txt
```
### Bước 4: Chạy code
```
python main.py
```
### Where exe?
Ko.
