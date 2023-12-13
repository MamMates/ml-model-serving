from pydantic import BaseModel


class Predict(BaseModel):
    category: int = None
    rating: int = None
    price: int = None


class GlobalResponse(BaseModel):
    status: bool = None
    code: int = None
    message: str = None
    data: dict = None

    def DefaultOK(data: dict = {}):
        return GlobalResponse(status=True, code=200, message="OK", data=data)

    def DefaultBadRequest():
        return GlobalResponse(status=False, code=400, message="Bad Request", data={})

    def DefaultNotFound():
        return GlobalResponse(status=False, code=404, message="Not Found", data={})

    def DefaultInternalServerError():
        return GlobalResponse(status=False, code=500, message="Internal Server Error", data={})
