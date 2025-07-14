# TAT API - เที่ยวไทยคนละครึ่ง

---

## ข้อมูลผู้จัดทำ
- ชื่อ: นายรัชชานนท์ กุลภัทรากร  
- รหัสนักศึกษา: 6510110730  

## วิธีติดตั้งและรันระบบ
```bash
# Install dependencies
poetry install

# Run development server
poetry run fastapi dev src/main.py

# Run test
poetry run pytest tests/test_user.py -v
poetry run pytest tests/test_province.py -v

```

- หลังจากรันเซิร์ฟเวอร์แล้ว สามารถเข้าใช้งาน API Docs ได้ที่:
- Swagger UI: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc
