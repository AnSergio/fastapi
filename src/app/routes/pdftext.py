# src/app/routes/pdftext.py
import io
import base64
import pdfplumber
import PyPDF2
from fastapi import APIRouter, HTTPException
from src.app.schemas.pdftext import PdfTextRequest


router = APIRouter()


@router.post("/pdftext1")
async def on_pdf_text_1(body: PdfTextRequest):
    # print(f"body: {body}")
    pag: int = 0
    tex: str = ""
    encod = body.encod or "utf-8"

    if not body.base64:
        raise HTTPException(status_code=400, detail="base64 é necessários!")

    try:
        pdf_data = base64.b64decode(body.base64)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar os dados: {str(e)}")

    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_data))
        for ind in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[ind]
            text = page.extract_text()
            pag = pag + 1
            if text:
                tex += "\nPagina: " + str(pag) + "\n" + text + "\n"
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar o PDF: {str(e)}")

    try:
        enc = tex.encode(encoding=encod, errors="ignore")
        dec = enc.decode(encod)
        result = {"Paginas": pag, "Text": dec}
        return result

    except UnicodeDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Erro de codificação: {str(e)}")
    except Exception as e:
        try:
            status, detail = str(e).split(": ", 1)
            status = int(status.strip())
        except Exception:
            status = 500
            detail = "Internal Server Error"
        raise HTTPException(status_code=status, detail=detail.strip())


@router.post("/pdftext2")
async def on_pdf_text_2(body: PdfTextRequest):
    # print(f"body: {body}")
    pag: int = 0
    tex: str = ""
    encod = body.encod or "utf-8"

    if not body.base64:
        raise HTTPException(status_code=400, detail="base64 é necessários!")

    try:
        pdf_data = base64.b64decode(body.base64)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar os dados: {str(e)}")

    try:
        with pdfplumber.open(io.BytesIO(pdf_data)) as pdf:
            for page in pdf.pages:
                pag += 1
                text = page.extract_text()
                if text:
                    tex += "\nPagina: " + str(pag) + "\n" + text + " \n \n"
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar o PDF: {str(e)}")

    try:
        enc = tex.encode(encoding=encod, errors="ignore")
        dec = enc.decode(encod)
        result = {"Paginas": pag, "Text": dec}
        return result

    except UnicodeDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Erro de codificação: {str(e)}")
    except Exception as e:
        try:
            status, detail = str(e).split(": ", 1)
            status = int(status.strip())
        except Exception:
            status = 500
            detail = "Internal Server Error"
        raise HTTPException(status_code=status, detail=detail.strip())
