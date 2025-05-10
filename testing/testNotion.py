from notion_client import Client

# Ganti dengan token yang kamu dapat dari Notion
notion = Client(auth="ntn_R41196194289OGrjVTfXm2LbnU4WxSJp8errI3HSiQw54G")
DATABASE_ID = "1d00f58c676480aa97fae8dc09c6f8b4"

# Query isi database
response = notion.databases.query(database_id=DATABASE_ID)

# Tambahkan data
new_page = notion.pages.create(
    parent={"database_id": DATABASE_ID},
    properties={
        "Nama Murid": {
            "title": [
                {"text": {"content": "Test1"}}
            ]
        },
        "Nomer WA Murid": {
            "rich_text": [
                {"text": {"content": "0814536729"}}
            ]
        },
        "Tutor": {
            "rich_text": [
                {"text": {"content": "Pak Ahmad"}}
            ]
        },
        "Nomer WA Tutor": {
            "rich_text": [
                {"text": {"content": "0896452171"}}
            ]
        },
        "Mata Kuliah": {
            "select": {
                "name": "Kalkulus 2"
            }
        },
        "Jadwal": {
            "rich_text": [
                {"text": {"content": "21 April 09.00-11.00"}}
            ]
        },
        "Status": {
            "select": {
                "name": "Belum"
            }
        }
    }
)

print("Data berhasil ditambahkan ke Notion 🎉")