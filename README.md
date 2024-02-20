# Tóm tắt

Thấy được tầm quan trọng của bộ phận quản trị nhân sự đối với doanh nghiệp, dự án này tập trung xây dựng website phân tích dữ liệu, ứng dụng các yếu tố của Data Science trong lĩnh vực quản trị nhân sự để giúp các nhà quản lý kịp thời ra các quyết định quan trọng, khai thác tiềm năng về nguồn nhân lực. Từ đó giúp giảm các chi phí ẩn do việc thay đổi nhân sự, tạo ra môi trường có thể cộng tác lâu dài với nhân viên.

Dự án sẽ sử dụng 2 mô hình machine learning để dự đoán khả năng thăng tiến, và khả năng nghỉ việc của nhân viên, đồng thời diễn tả các trường thông tin quan trọng trong lĩnh vực quản trị nhân sự nói chung và các yếu tố liên quan tới kết quả dự đoán nói riêng, một yếu tố quan trọng là khả năng cập nhập dữ liệu theo thời gian thực. Dự án sẽ đi từ bước thu thập data từ S3 bucket để tạo kho chứa raw data trên Snowflake, sau đó xây dựng logic dữ liệu tạo Data Warehouse và Data Mart, cuối cùng biểu đồ hóa xây dựng dashboard và chức năng dự đoán trên nền tảng Website.

Phần cuối bài báo các đề cập tới kiến thức và quá trình lựa chọn, tìm hiểu các lĩnh vực và công cụ cần thiết để hoàn thành dự án, cũng như tổng kết về các hạn chế cũng như hướng phát triển của dự án trong tương lai.

## Khái quát hệ thống
### Kiến trúc tổng thể Data Warehouse
Kho dữ liệu (DW hoặc DWH) là một hệ thống phức tạp lưu trữ dữ liệu được sử dụng cho việc dự báo, báo cáo và phân tích dữ liệu. Nó liên quan đến việc thu thập, làm sạch và biến đổi dữ liệu từ các luồng dữ liệu khác nhau và tải nó vào các bảng Dimensiona/Fact


<img src="https://github.com/Lilili2214/DataScienceWebBased_humanrousces/blob/main/images/Picture14.png" width="100%" height="100%">

## Biểu đồ thành phần 
Trong hệ thống sẽ có các thành phần sau tương tác với nhau:
-	Streamlit: được sử dụng như một lớp frontend, nơi người dùng có thể tương tác với ứng dụng.
-	FastAPI: được sử dụng như một lớp backend, nơi nó xử lý các yêu cầu từ frontend (Streamlit), truy vấn nguồn dữ liệu và trả về kết quả.
-	Nguồn Dữ liệu (Data Layer): đây là nơi lưu trữ và quản lý dữ liệu. FastAPI sẽ truy vấn nguồn dữ liệu này để lấy thông tin cần thiết để xử lý các yêu cầu từ frontend.

<img src="https://github.com/Lilili2214/DataScienceWebBased_humanrousces/blob/main/images/Picture15.png" width="100%" height="100%">


## Data Model
<img src="https://github.com/Lilili2214/DataScienceWebBased_humanrousces/blob/main/images/Picture20.png" width="100%" height="100%">

<img src="https://github.com/Lilili2214/DataScienceWebBased_humanrousces/blob/main/images/Picture16.png" 

## Use Case 
<img src="https://github.com/Lilili2214/DataScienceWebBased_humanrousces/blob/main/images/Picture21.png" width="100%" height="100%">

# For more detail, Please download Report file, images of the result stored inside 'images' folder
