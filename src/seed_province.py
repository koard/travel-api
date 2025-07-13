import asyncio
from src import models
from src.models import Province
from sqlmodel import select


province_data = [
    # เมืองหลัก (is_secondary=False)
    ("กรุงเทพมหานคร", False), ("เชียงใหม่", False), ("ขอนแก่น", False),
    ("นครราชสีมา", False), ("ชลบุรี", False), ("ภูเก็ต", False),
    ("สุราษฎร์ธานี", False), ("พิษณุโลก", False), ("นครศรีธรรมราช", False),
    ("สงขลา", False), ("นนทบุรี", False), ("ปทุมธานี", False),
    ("ระยอง", False), ("อุดรธานี", False), ("เชียงราย", False),
    ("ลำปาง", False), ("พระนครศรีอยุธยา", False), ("นครสวรรค์", False),
    ("สระบุรี", False), ("สมุทรปราการ", False), ("ราชบุรี", False),
    ("เพชรบุรี", False),

    # เมืองรอง (is_secondary=True)
    ("กำแพงเพชร", True), ("ชัยนาท", True), ("อุทัยธานี", True), ("อุตรดิตถ์", True),
    ("สุโขทัย", True), ("ตาก", True), ("เพชรบูรณ์", True), ("พิจิตร", True),
    ("นครนายก", True), ("ปราจีนบุรี", True), ("สระแก้ว", True), ("จันทบุรี", True),
    ("ตราด", True), ("กาญจนบุรี", True), ("ประจวบคีรีขันธ์", True), ("สมุทรสงคราม", True),
    ("สมุทรสาคร", True), ("นครปฐม", True), ("สิงห์บุรี", True), ("ลพบุรี", True),
    ("อ่างทอง", True), ("มหาสารคาม", True), ("ร้อยเอ็ด", True), ("ยโสธร", True),
    ("กาฬสินธุ์", True), ("อำนาจเจริญ", True), ("หนองบัวลำภู", True), ("หนองคาย", True),
    ("บึงกาฬ", True), ("สกลนคร", True), ("นครพนม", True), ("มุกดาหาร", True),
    ("ศรีสะเกษ", True), ("อุบลราชธานี", True), ("เลย", True), ("ชัยภูมิ", True),
    ("สุรินทร์", True), ("บุรีรัมย์", True), ("แพร่", True), ("พะเยา", True),
    ("น่าน", True), ("ลำพูน", True), ("แม่ฮ่องสอน", True), ("สตูล", True),
    ("พังงา", True), ("กระบี่", True), ("ตรัง", True), ("ระนอง", True),
    ("พัทลุง", True), ("ชุมพร", True), ("ปัตตานี", True), ("ยะลา", True),
    ("นราธิวาส", True),
]

async def seed_provinces_once():
    await models.init_db()
    async for session in models.get_session():
        # เช็คก่อนว่ามีข้อมูลแล้วหรือยัง
        result = await session.exec(select(Province))
        if result.first():
            print("Provinces already seeded.")
            return

        for name, is_secondary in province_data:
            session.add(Province(name=name, is_secondary=is_secondary))
        await session.commit()
        print("✅ Seeded 77 provinces.")
    await models.close_db()