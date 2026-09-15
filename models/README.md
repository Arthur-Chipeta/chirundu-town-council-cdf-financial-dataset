# OCR model

`en_PP-OCRv3_rec_infer.onnx` is the English recognition model published by RapidAI. It is used with `rapidocr-onnxruntime==1.4.4`.

Source: https://huggingface.co/spaces/RapidAI/RapidOCR/blob/main/models/text_rec/en_PP-OCRv3_rec_infer.onnx

If the file is missing, run this from the project folder in PowerShell:

```powershell
New-Item -ItemType Directory -Force models
Invoke-WebRequest 'https://huggingface.co/spaces/RapidAI/RapidOCR/resolve/main/models/text_rec/en_PP-OCRv3_rec_infer.onnx' -OutFile 'models/en_PP-OCRv3_rec_infer.onnx'
```

The OCR model reads text; it does not supply council data. Council data comes from the downloaded PDF.
