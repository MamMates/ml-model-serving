from pydantic import BaseModel, ConfigDict


class Predict(BaseModel):
    category: int = None
    rating: int = None
    price: int = None


class GlobalResponse(BaseModel):
    model_config = ConfigDict(extra='allow')
    status: bool = None
    code: int = None
    message: str = None

    def DefaultOK(**kwargs):
        return GlobalResponse(status=True, code=200, message="OK", **kwargs)

    def DefaultBadRequest(**kwargs):
        return GlobalResponse(status=False, code=400, message="Bad Request", **kwargs)

    def DefaultNotFound(**kwargs):
        return GlobalResponse(status=False, code=404, message="Not Found", **kwargs)

    def DefaultInternalServerError(**kwargs):
        return GlobalResponse(status=False, code=500, message="Internal Server Error", **kwargs)
