## TRƯỜNG ĐẠI HỌC THUỶ LỢI **KHOA CÔNG NGHỆ THÔNG TIN** BẢN TÓM TẮT ĐỀ CƯƠNG ĐỒ ÁN TỐT NGHIỆP 

## **Tên đề tài: Xây dựng luồng xử lý dữ liệu và quy trình vận hành mô hình học máy giám sát đội robot di động tự hành trong nhà máy** 

_Sinh viên thực hiện_ : Lê Đoàn Dương _Lớp_ : 64TTNT.NB _Mã sinh viên:_ 2251262592 _Số điện thoại:_ 0376248404 _Email:_ 2251262592@e.tlu.edu.vn _Giáo viên hướng dẫn_ : PGS.Ts Nguyễn Quang Hoan 

## **TÓM TẮT ĐỀ TÀI** 

Đồ án tập trung giải quyết thách thức về quản trị dữ liệu phân mảnh và sự suy giảm hiệu năng của mô hình Trí tuệ nhân tạo (Model Decay) trong quá trình vận hành biên đội robot di động tự hành (AMR) tại các nhà máy thông minh. Để giải quyết vấn đề này, đề tài tiến hành thiết kế và xây dựng một hệ thống khép kín (End-to-End) kết hợp giữa luồng xử lý dữ liệu (Data Pipeline) tối ưu chi phí và quy trình vận hành học máy (MLOps). Cụ thể, hệ thống ứng dụng mô hình thị giác máy tính học sâu để suy luận tại biên (Edge AI) nhằm phát hiện vật cản; toàn bộ nhật ký vận hành và hình ảnh sau đó được đẩy về một hồ dữ liệu (Data Lake) trung tâm. Quá trình trích xuất và biến đổi dữ liệu (ETL) được tự động hóa thông qua kiến trúc phân tích trực tiếp (In-process OLAP), giúp tiết kiệm tối đa tài nguyên máy chủ. Điểm nhấn khoa học của đồ án nằm ở cơ chế giám sát độ tin cậy (Confidence Score) của AI theo thời gian thực; hệ thống có khả năng nhận diện hiện tượng trôi dạt dữ liệu (Data Drift) khi robot gặp vật thể lạ, từ đó cô lập dữ liệu bất thường nhằm kích hoạt vòng lặp học chủ động (Active Learning). Kết quả kỳ vọng là một giải pháp giám sát tập trung, tự động hóa toàn bộ vòng đời dữ liệu từ biên lên đám mây, đảm bảo sự bền vững cho mô hình AI và tối ưu hạ tầng cho doanh nghiệp. 

## **CÁC MỤC TIÊU CHÍNH** 

Để giải quyết bài toán đặt ra, đồ án hướng tới 5 mục tiêu cụ thể sau: 

1. Thiết kế luồng dữ liệu đầu cuối (End-to-End Data Pipeline): Xây dựng kiến trúc hạ tầng tự động thu thập, truyền tải và tập trung hóa dữ liệu vận hành (tọa độ, trạng thái thiết bị, hình ảnh camera) từ biên đội robot tự hành lên hồ dữ liệu (Data Lake) trên nền tảng điện toán đám mây. 

2. Triển khai Trí tuệ nhân tạo tại biên (Edge AI): Ứng dụng mô hình thị giác máy tính học sâu trực tiếp tại thiết bị robot để nhận diện chướng ngại vật; đảm bảo khả năng phản hồi tức thì và tiết kiệm băng thông mạng công nghiệp. 

3. Tối ưu hóa quy trình xử lý dữ liệu (ETL): Áp dụng kiến trúc phân tích trực tiếp (In-process OLAP) thay thế cho các hệ thống phân tán truyền thống nhằm làm sạch, biến đổi và tổng hợp dữ liệu lớn, giúp tối ưu hóa tài nguyên máy chủ và chi phí hạ tầng. 

4. Xây dựng quy trình vận hành học máy (MLOps): Tích hợp cơ chế giám sát hiệu năng AI theo thời gian thực; tự động phát hiện hiện tượng trôi dạt dữ liệu (Data Drift) khi robot đối mặt với môi trường lạ, từ đó cô lập hình ảnh nhiễu để kích hoạt vòng lặp học chủ động (Active Learning). 

5. Trực quan hóa và giám sát tập trung: Phát triển hệ thống bảng điều khiển (Dashboard) hiển thị luồng dữ liệu thời gian thực, cảnh báo an toàn vận hành và trạng thái "sức khỏe" của mô hình AI, phục vụ công tác quản trị toàn diện. 

## **KẾT QUẢ DỰ KIẾN** 

Sau quá trình nghiên cứu và triển khai, đồ án dự kiến sẽ mang lại các kết quả cụ thể (Deliverables) như sau: 

1. Hệ thống luồng dữ liệu đám mây (Cloud-based Data Pipeline) hoàn chỉnh: Một hệ thống phần mềm đóng gói (Containerized) được triển khai trên máy chủ đám mây, có khả năng tiếp nhận, lưu trữ và xử lý tự động hàng nghìn bản ghi dữ liệu (log tọa độ, trạng thái, hình ảnh) mỗi phút từ các thiết bị biên giả lập. 

2. Mô hình AI nhận diện vật cản tại biên: Một mô hình thị giác máy tính học sâu được tối ưu hóa để chạy trực tiếp trên thiết bị biên (Edge Device). Mô hình có khả năng nhận diện chính xác các chướng ngại vật phổ biến trong nhà máy và trích xuất siêu dữ liệu (metadata) cùng độ tin cậy (Confidence Score) theo thời gian thực. 

3. Cơ chế tự động hóa MLOps: Một luồng quy trình vận hành giám sát AI thành công, có khả năng tự động nhận diện hiện tượng trôi dạt dữ liệu (Data Drift). Hệ thống sẽ tự động phân loại và cô lập ít nhất 90% các hình ảnh gây bối rối cho mô hình vào hồ dữ liệu (Data Lake) để phục vụ quá trình tái huấn luyện. 

4. Bảng điều khiển giám sát thời gian thực (Real-time Dashboard): Giao diện quản trị trực quan hiển thị bản đồ di chuyển của biên đội robot, trạng thái tiêu 

hao năng lượng, cảnh báo va chạm và biểu đồ theo dõi "sức khỏe" của mô hình AI. 

5. Báo cáo đánh giá hiệu năng hệ thống: Bản phân tích và so sánh các chỉ số về tài nguyên (RAM, CPU usage) và độ trễ (Latency) khi ứng dụng kiến trúc xử lý trực tiếp (In-process OLAP) so với các giải pháp dữ liệu phân tán truyền thống, chứng minh tính khả thi về mặt tối ưu chi phí hạ tầng. 

## **TIẾN ĐỘ THỰC HIỆN** 

|**TT**|**Thời gian**|**Nội dung công việc**|**Kết quả dự kiến đạt được**|
|---|---|---|---|
|1|Tuần 1 - 2|Nghiên cứu tổng quan và<br>thiết kế hệ thống|Sơ đồ kiến trúc tổng thể;<br>Tài liệu đặc tả yêu cầu hệ<br>thống và lược đồ dữ liệu.|
|2|Tuần 3 - 4|Thiết lập môi trường và<br>triển khai AI tại biên|Môi trường máy chủ sẵn<br>sàng; Script giả lập hoạt<br>động; AI nhận diện được<br>chướng ngại vật cơ bản.|



||||||||
|---|---|---|---|---|---|---|
||||||Cấu trúc thư mục Data||
||3|Tuần|5 - 6|Xây dựng phân hệ thu<br>thập và lưu trữ dữ liệu|Lake hoàn thiện; Dữ liệu<br>thô liên tục được đẩy lên||
||||||hệ thống.||
||||||Luồng ETL tự động chạy||
||4|Tuần|7 - 8|Phát triển luồng xử lý dữ<br>liệu (ETL Pipeline)|theo chu kỳ; Dữ liệu được<br>làm sạch và lưu dưới định||
||||||dạng tối ưu phân tích.||
||5|Tuần|9 - 10|Tích hợp quy trình<br>MLOps và Active<br>Learning|Hệ thống cảnh báo Data<br>Drift hoạt động; Dữ liệu<br>nhiễu được phân loại tự<br>động vào khu vực riêng.||
||||||Dashboard hiển thị bản đồ||
||6|Tuần<br>12|11 -|Phát triển Bảng điều khiển<br>(Dashboard) và Kiểm thử|và biểu đồ trực quan; Bảng<br>số liệu báo cáo hiệu năng||
||||||hệ thống.||
||||||||



Cuốn thuyết minh đồ án Tuần 13 - Tổng kết, hoàn thiện cáo hoàn chỉnh; Slide thuyết 7 14 cáo trình; Kịch bản chạy thực tế trước hội đồng. 

## **TÀI LIỆU THAM KHẢO** 

[1] Reis, J., & Housley, M. (2022). _Fundamentals of Data Engineering: Plan and Build Robust Data Systems_ . O'Reilly Media. (Tài liệu nền tảng về thiết kế và xây dựng luồng dữ liệu - Data Pipeline chuyên nghiệp). 

[2] Kreuzberger, D., Kühl, N., & Hirschl, S. (2023). "Machine Learning Operations (MLOps): Overview, Definition, and Architecture". _IEEE Access, 11_ , 31866-31879. (Bài báo khoa học cung cấp định nghĩa chuẩn và kiến trúc vòng lặp MLOps, Data Drift). 

[3] Raasveldt, M., & Mühleisen, H. (2019). "DuckDB: an Embeddable Analytical Database". _Proceedings of the 2019 International Conference on Management of Data (SIGMOD)_ , 1981–1984. (Nghiên cứu gốc từ những nhà sáng lập DuckDB, minh chứng cho phương pháp In-process OLAP). 

[4] Jocher, G., Chaurasia, A., & Qiu, J. (2023). _Ultralytics YOLOv8_ . Truy xuất từ kho lưu trữ mã nguồn mở GitHub: https://github.com/ultralytics/ultralytics (Tài liệu và mã nguồn gốc của mô hình thị giác máy tính YOLOv8 áp dụng cho Edge AI). 

[5] Lu, J., Liu, A., Dong, F., Gu, F., Gama, J., & Zhang, G. (2018). "Learning under Concept Drift: A Review". _IEEE Transactions on Knowledge and Data Engineering, 31_ (12), 2346-2363. (Tài liệu học thuật chuyên sâu về hiện tượng trôi dạt dữ liệu - Data/Concept Drift và cơ chế học chủ động). 

