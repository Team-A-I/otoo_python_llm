async def ocr_text(client, image: bytes, analysis_type: str):
    return await client.ocrvision(image, analysis_type)
