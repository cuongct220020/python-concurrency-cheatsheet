# Báo cáo chuyên sâu: Làm chủ Python Multiprocessing (Đa tiến trình)

## Mục lục
  * [1. Tổng quan về Python Process](#1-tổng-quan-về-python-process)
  * [2. Chạy một hàm trong tiến trình (Functional Approach)](#2-chạy-một-hàm-trong-tiến-trình-functional-approach)
  * [3. Mở rộng lớp Process (OOP Approach)](#3-mở-rộng-lớp-process-oop-approach)
  * [4. Các phương thức khởi động (Process Start Methods)](#4-các-phương-thức-khởi-động-process-start-methods)
  * [5. Thuộc tính của tiến trình (Instance Attributes)](#5-thuộc-tính-của-tiến-trình-instance-attributes)
  * [6. Các tiện ích (Process Utilities)](#6-các-tiện-ích-process-utilities)
  * [7. Đồng bộ hoá dữ liệu (Synchronization Primitives)](#7-đồng-bộ-hoá-dữ-liệu-synchronization-primitives)
  * [8. Các thực hành tốt nhất (Best Practices)](#8-các-thực-hành-tốt-nhất-best-practices)
  * [9. Các lỗi thường gặp](#9-các-lỗi-thường-gặp)


## 1. Tổng quan về Python Process

Trong Computer Science, Tiến trình (Process) là một instance của chương trình máy tính đang được thực thi. 
Trong Python, mỗi tiến trình chạy một phiên bản riêng biệt của trình thông dịch Python (Python Interpreter).
* Mỗi tiến trình có không gian bộ nhớ riêng (memory space).
* Chúng độc lập hoàn toàn với nhau, biến thay đổi ở tiến trình này không ảnh hưởng trực tiếp đến tiến trình khác. 

**So sánh Thread (Luồng) và Process (Tiến trình)**

Đây là sự phân biệt quan trọng nhất khi tối ưu hiệu năng:

| Đặc điểm | Thread (Đa luồng) | Process (Đa tiến trình) |
|----------|-------------------|------------------------|
| **Không gian bộ nhớ** | Chia sẻ (Shared Memory) | Riêng biệt (Isolated Memory) |
| **Chi phí khởi tạo** | Thấp (Lightweight) | Cao (Heavyweight - cần sao chép môi trường) |
| **GIL (Global Interpreter Lock)** | Bị ảnh hưởng. Chỉ 1 thread chạy mã Python tại 1 thời điểm | Bỏ qua GIL. Các tiến trình chạy song song thực sự trên nhiều nhân CPU |
| **Trường hợp sử dụng** | I/O Bound (Mạng, File, Database) | CPU Bound (Tính toán nặng, Xử lý ảnh, ML) |
| **Giao tiếp** | Dễ dàng (biến chung). Cần Lock để an toàn | Phức tạp hơn (cần Queue, Pipe, Manager) |


**Vòng đời của tiến trình**

Một tiến trình Python trải qua các giai đoạn:
1. **Khởi tạo (Creation):** Đối tượng `Process` được tạo. 
2. **Bắt đầu (Start):** Phương thức `start()` được gọi, hệ điều hành cấp phát tài nguyên (PID) và chạy phương thức `run()`.
3. **Thực thi (Running):** Mã lệnh bên trong hàm `target` được thực thi. 
4. **Kết thúc (Termination):** Hàm `target()` hoàn tất hoặc gặp lỗi, hoặc bị dừng cưỡng bức. Tài nguyên được giải phóng, nhưng mã thoát (exit code) vẫn được giữ lại. 
5. **Đóng (Closure):** Tiến trình cha gọi `join()` để đọc mã thoát và dọn dẹp hoàn toàn dấu vết của tiến trình con. 

**Tiến trình con (Child) và Cha (Parent)**
* **Parent Process:** Tiến trình tạo ra tiến trình khác. Thường là `MainProcess`.
* **Child Process:** Tiến trình được tạo ra. Nó có thể kế thừa một số tài nguyên từ cha tuỳ thuộc vào phương thức khởi động (Start Method).


## 2. Chạy một hàm trong tiến trình (Functional Approach)

Cách đơn giản nhất để sử dụng multiprocessing là chạy một hàm cụ thể trong một tiến trình riêng biệt.

**Cách thực hiện:** Sử dụng lớp `multiprocessing.Process`. Bạn cần truyền hàm cần chạy vào tham số `target`.  
* **Lưu ý quan trọng:** Luôn đặt code khởi tạo bên trong khối `if __name__ == '__main__'`: để tránh lỗi đệ quy vô hạn trên Window/MacOS.

```Python
import multiprocessing
import time

def task():
    print('Tiến trình con đang chạy...')
    time.sleep(1)
    print('Tiến trình con hoàn tất.')

if __name__ == '__main__':
    # Tạo tiến trình
    p = multiprocessing.Process(target=task)
    # Bắt đầu
    p.start()
    print('Tiến trình chính đang chờ...')
    # Chờ tiến trình con kết thúc
    p.join()
```

**Ví dụ với tham số (Arguments):** Truyền tham số cho hàm thông qua `args` (tuple) hoặc `kwargs` (dictionary). Dữ liệu này sẽ được **Pickle** (tuần tự hoá) để gửi sáng tiến trình con.

```Python
def greeting(name, delay):
    time.sleep(delay)
    print(f"Xin chào {name} từ tiến trình con!")

if __name__ == '__main__':
    p = multiprocessing.Process(target=greeting, args=('Nam', 0.5))
    p.start()
    p.join()
```

## 3. Mở rộng lớp Process (OOP Approach)

Đối với các lớp tác vụ phức tạp cần quản lý trạng thái, bạn nên tạo class kế thừa từ `multiprocessing.Process`.

**Cách thực hiện:**
1. Tạo class kế thừa `multiprocessing.Process`.
2. Ghi đè phương thức `run()`. Đây là nơi chứa logic sẽ chạy trong tiến trình mới.
3. (Tuỳ chọn) Ghi đè `__init__` để nhận tham số, nhớ gọi `super().__init__()`. 

```Python
import multiprocessing

class WorkerProcess(multiprocessing.Process):
    def __init__(self, name):
        super().__init__()
        self.worker_name = name

    def run(self):
        print(f"Worker {self.worker_name} đang xử lý công việc...")

if __name__ == '__main__':
    worker = WorkerProcess("A-1")
    worker.start()
    worker.join()
```

**Trả về giá trị từ Class:** Phương thức `run()` không thể trả về giá trị (return) trực tiếp cho tiến trình cha. 
Giải pháp là sử dụng **Shared Memory** hoặc **Queue** được truyền vào `__init__`.

## 4. Các phương thức khởi động (Process Start Methods)

Python cung cấp 3 cách hệ điều hành tạo ra một tiến trình mới. Việc chọn phương thức ảnh hưởng đến hiệu năng và tính tương thích. 

**Các phương thức:**

1. `spawn` (Mặc định trên Windows & MacOS)
* Khởi động một trình thông dịch Python hoàn toàn mới. 
* Chậm hơn do phải nạp lại thư viện. 
* An toàn nhất, không kế thừa trạng thái rác từ cha. 

2. `fork` (Mặc định trên Linux cũ)
* Sử dụng `os.fork()`. Sao chép toàn bộ bộ nhớ của cha sang con (Copy-on-Write). 
* Rất nhanh. 
* **Nguy hiểm:** Có thể gây deadlock nếu tiến trình cha đang giữ Lock hoặc sử dụng thread không an toàn. 

3. `forkserver`:
* Khởi tạo một server process đặc biệt để tạo các process con sau đó. 
* Cân bằng giữa tốc độ và an toàn. 

**Cách thay đổi:** Sử dụng `multiprocessing.set_start_method('spawn')` ngay đầu chương trình, trong khối `if __name__ == 'main'`.


## 5. Thuộc tính của tiến trình (Instance Attributes)
Các thuộc tính quan trọng để quản lý và giám sát: 
* `p.name`: Tên của tiến trình (ví dụ: `Process-1`). Có thể đặc tên tuỳ ý để dễ debug. 
* `p.pid`: Process ID (Mã định danh tiến trình của hệ điều hành). `None` trước khi start. 
* `p.daemon`:
  * `True`: Tiến trình nền. Sẽ bỉ huỷ ngay lập tức nếu tiến trình cha kết thúc. Không được phép tạo tiến trình con. 
  * `False` (Mặc định): Chương trình chỉ thoát khi tất cả tiến trình non-daemon kết thúc.
* `p.is_alive()`: Trả về `True` nếu tiến trình đang chạy. 
* `p.exitcode`:
  * `None`: Chứa kết thúc. 
  * `0`: Thành công
  * `> 0`: Lỗi (ví dụ 1)
  * `< 0`: Bị kill bởi tiến hiệu (Ví dụ: -9 là SIGKILL).

## 6. Các tiện ích (Process Utilities)
* `multiprocessing.active_children()`: Danh sách các tiến trình con đang chạy. 
* `multiprocessing.cpu_count()`: Số lượng nhân CPU (logical cores). Dùng để quyết định số lượng process tối ưu. 
* `multiprocessing.current_process()`: Lấy đối tượng process hiện tại đạng chạy dòng code đó. 
* `multiprocessing.parent_process()`: Lấy đối tượng process cha. 

## 7. Đồng bộ hoá dữ liệu (Synchronization Primitives)

Khi nhiều tiến trình cùng truy cập tài nguyên (như file, in ra màn hình), cần cơ chế khoá để tránh xung đột. 


* **Lock (Mutex - Mutual Exclusion):** Chỉ cho phép một tiến trình truy cập đoạn mã tại một thời điểm. 

```Python
lock = multiprocessing.Lock()
with lock:
    # Critical Section
    print("Chỉ một process được in dòng này tại một thời điểm")
```

* **RLock (Reentrant Lock):** Giống Lock, nhưng cho phép cùng một tiến trình `acquire` khóa nhiều lần mà không bị treo chính nó (thường dùng trong đệ quy).


* **Semaphore:** Cho phép tối đa N tiến trình truy cập tài nguyên cùng lúc. Ví dụ: Giới hạn chỉ 4 process cùng kết nối Database.

```Python
sem = multiprocessing.Semaphore(4)
with sem:
    # Kết nối DB
```

* **Event**: Cơ chế giao tiếp đơn giản. Một tiến trình phát tín hiệu (`set()`), các tiến trình khác chờ (`wait()`).
```Python
event = multiprocessing.Event()
# Process 1
event.wait() # Chờ
# Process 2
event.set() # Đánh thức Process 1
```

* **Barrier**: Đồng bộ hóa một nhóm các tiến trình. Tất cả phải đến điểm hẹn (wait()) thì mới được cùng đi tiếp.

## 8. Các thực hành tốt nhất (Best Practices)

1. **Luôn dùng Context Managers:** Sử dụng `with Pool() as p:` để đảm bảo tài nguyên được dọn dẹp kể cả khi lỗi. 
2. **Sử dụng Timeouts:** Khi gọi `join()` hoặc `get()` từ Queue, nên có timeout để tránh chương trình bị treo vĩnh viễn (deadlock).
3. **Bảo vệ điểm nhập (`if __name__ == 'main'`):** Bắt buộc trên Windows/macOS để tránh lỗi "RuntieError Starting New Processes".
4. **Ưu tiên Message Passing (Queue/Pipe):** Hạn chế dùng Lock/Shared Memory (Value/Array) vì khó debug. Hãy giao tiếp bằng cách gửi tin nhắn.
5. **Shared ctypes:** Nếu bắt buộc chia sẻ mảng lớn (như numpy array), hãy dùng multiprocessing.Array hoặc SharedMemory để tránh copy dữ liệu tốn RAM.

## 9. Các lỗi thường gặp

1. RuntimeError: An attempt has been made to start a new process...:
* **Nguyên nhân:** Thiếu `if __name__ == '__main__':`.
* **Khắc phục:** Đưa mã `start()` vào trong khối main guard.


2. print() không hiển thị:
* **Nguyên nhân:** Buffer của stdout chưa được xả (flush) hoặc nhiều process tranh chấp I/O.
* **Khắc phục:** Dùng `print(..., flush=True)` hoặc dùng một Queue chuyên dụng để log.

3. Lỗi Pickle:
* **Nguyên nhân:** Cố gắng truyền các đối tượng không thể tuần tự hóa (như lambda function, database connection) qua `args` của Process.
* **Khắc phục:** Chỉ truyền dữ liệu thuần (list, dict, string), khởi tạo connection bên trong `run()`.