from fastapi import APIRouter, UploadFile, File, HTTPException

from .. import APIResponse

from .service import generate_letter_with_image

router = APIRouter(
    prefix="/image-service",
    tags=["image-service"],
    responses={404: {"description": "Not found"}},
)

@router.get("/health", response_model=APIResponse)
async def health():
    return APIResponse(
        status=200,
        status_text="OK",
        data={"status": "healthy"},
        message="Service is healthy"
    )

@router.post("/generate-letter", response_model=APIResponse)
async def generate_letter(file: UploadFile = File(...)):
    try:
        # validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")

        # read image data
        image_data = await file.read()

        # process image and generate letter
        result = generate_letter_with_image(image_data, file.filename)

        if not result:
            raise HTTPException(status_code=500, detail="Failed to process image and generate letter")

        image_url, letter = result

        return APIResponse(
            status=200,
            status_text="OK",
            data={
                "image_url": image_url,
                "object_key": f"images/{file.filename}",
                "filename": file.filename,
                "letter": letter
            },
            message="Letter generated successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Letter generation failed: {str(e)}")