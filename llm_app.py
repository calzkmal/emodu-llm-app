from ollama import Client
from os import environ as env

async def handle_conversation(emosi, penguatan, pendekatan):

    # Change this setup
    metadata = {
        'role': 'user',
        'emosi': emosi,
        'penguatan': penguatan,
        'pendekatan': pendekatan
    }

    role = metadata['role']
    content = (
        "Anda adalah model bahasa yang bertugas membuat satu kalimat penguatan kepada siswa berdasarkan data berikut:\n\n"
        f"1. Emosi: {metadata['emosi']}\n"
        "   - Kategori emosi yang sedang dirasakan siswa.\n\n"
        f"2. Penguatan: {metadata['penguatan']}\n"
        "   - Jenis penguatan untuk memotivasi siswa.\n\n"
        f"3. Pendekatan: {metadata['pendekatan']}\n"
        "   - Pendekatan berbasis ARCS Model untuk menentukan gaya bahasa yang relevan.\n\n"
        "Instruksi tambahan:\n"
        "- Kalimat harus memiliki maksimal 100 karakter.\n"
        "- Tambahkan emoji di akhir kalimat untuk memberikan kesan ceria dan mendukung suasana.\n"
        "- Jangan menambahkan penjelasan, instruksi, atau detail apapun di luar kalimat penguatan.\n\n"
    )

    client = Client(host=f"{env['CLIENT_API']}")
    response = client.chat(model="calzkmal/emodu-llm", messages=[
        {
            'role': role,
            'content': content
        }
    ])

    try:
        result = response['message']['content']  
    except KeyError:
        raise ValueError("Response format error, missing 'message' or 'content' keys.")
    
    return result