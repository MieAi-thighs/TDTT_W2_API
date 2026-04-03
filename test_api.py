import requests
import json
import os

os.makedirs("outputs", exist_ok=True)

BASE_URL = "https://boxhi-34-168-205-108.run.pinggy-free.link" # Thay link đường dẫn của bạn ở đây
API_URL = f"{BASE_URL}/predict"  
IMAGE_PATH = ["test_img/test_3.jpg", "test_img/test_4.jpg"]

def test_depth_estimation():
    print(f"Đang gửi yêu cầu tới: {API_URL}...")
    
    for img in IMAGE_PATH:
        try:
            # Mở file ảnh ở chế độ binary
            with open(img, "rb") as image_file:
                # Gửi POST request kèm file
                files = {"file": (os.path.basename(img), image_file, "image/jpeg")}
                response = requests.post(API_URL, files=files)
                
                # Kiểm tra kết quả
                if response.status_code == 200:
                    result = response.json()
                    print(f"\n Kết quả từ Server cho '{img}':")
                    print(json.dumps(result, indent=4, ensure_ascii=False))
                    
                    # Trích xuất thông tin quan trọng để báo cáo
                    info = result.get("depth_map_info", {})
                    print(f"\n--- THÔNG SỐ TRÍCH XUẤT ---")
                    print(f"- Kích thước: {info.get('width')}x{info.get('height')}")
                    print(f"- Độ sâu lớn nhất: {info.get('max_depth')}")
                    print(f"- Độ sâu nhỏ nhất: {info.get('min_depth')}")

                    # Lưu heatmap vào folder outputs
                    if result.get("status") == "success":
                        path_on_server = result["heatmap_path"]
                        download_url = f"{BASE_URL}{path_on_server}"
                        img_data = requests.get(download_url).content
                        
                        # Lưu vào folder outputs của bạn
                        save_name = os.path.join("outputs", f"heatmap_{os.path.basename(img)}")
                        with open(save_name, "wb") as f_out:
                            f_out.write(img_data)
                        print(f"Đã lưu: {save_name}")
                    else:
                        print(f"Lỗi từ Server: {result.get('message')}")
                else:
                    print(f" Lỗi Server: {response.status_code}")
                    print(response.text)
                    
        except FileNotFoundError:
            print(f" Lỗi: Không tìm thấy file ảnh '{img}'")
        except Exception as e:
            print(f" Lỗi kết nối: {e}")

if __name__ == "__main__":
    test_depth_estimation()