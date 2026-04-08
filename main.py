from fastapi import FastAPI, UploadFile, File, HTTPException
from transformers import pipeline
from PIL import Image
import io
import torch
import nest_asyncio
import matplotlib.pyplot as plt
from fastapi.staticfiles import StaticFiles
import os

# Tạo thư mục lưu kết quả 
os.makedirs("outputs", exist_ok=True)

app = FastAPI()

# Cho phép truy cập thư mục ảnh qua URL
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# Khởi tạo model
depth_estimator = pipeline("depth-estimation", model="Intel/dpt-large")

@app.get("/")
def read_root():
    # Giới thiệu hệ thống
    return {
        "project": "2D-to-3D Depth Estimator API",
        "description": "API ước tính độ sâu từ ảnh 2D hỗ trợ làm game assets",
    }

@app.get("/health")
def health_check():
    # Kiểm tra trạng thái
    return {"status": "healthy", "model": "Intel/dpt-large", "device": "cuda" if torch.cuda.is_available() else "cpu"}

@app.post("/predict")
async def predict(file: UploadFile = File(None)):
    # Kiểm tra dữ liệu đầu vào và xử lý lỗi
    if file is None:
        raise HTTPException(status_code=400, detail="Lỗi: Vui lòng tải lên một file ảnh.")

    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Lỗi: Định dạng file không phải là hình ảnh.")

    try:
        # Đọc ảnh từ request
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")

        # Suy luận (Inference)
        result = depth_estimator(image)
        depth_map = result["predicted_depth"]

        # Tạo tên file và lưu heatmap
        pure_filename = os.path.basename(file.filename)
        heatmap_filename = f"heatmap_{pure_filename}.png"
        heatmap_path = os.path.join("outputs", heatmap_filename)
    
        depth_numpy = depth_map.cpu().numpy()
        plt.imsave(heatmap_path, depth_numpy, cmap='magma')

        # Trả kết quả JSON
        return {
            "status": "success",
            "filename": file.filename,
            "heatmap_path": f"/outputs/{heatmap_filename}", # Đường dẫn tải heatmap
            "depth_map_info": {
                "width": depth_map.shape[1],
                "height": depth_map.shape[0],
                "max_depth": float(torch.max(depth_map)),
                "min_depth": float(torch.min(depth_map))
            }
        }
    except Exception as e:
        # Xử lý lỗi trong quá trình suy luận
        return {"status": "error", "message": str(e)}
