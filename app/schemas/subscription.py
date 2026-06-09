from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

class SubscriptionRequest(BaseModel):
    user_id: int = Field(gt=0)
    currency_id: int | None = Field(default=None, gt=0)
    currency_code: str | None = None
    
    @field_validator("currency_code")
    @classmethod
    def validate_currency_code(cls, value: str | None) -> str | None:
        if value is None:
            return value
        
        value = value.strip().upper()
        
        if not value:
            raise ValueError("Currency code cannot be empty")
        
        return value
    
    @model_validator(mode="after")
    def validate_currency_identifier(self):
        identifiers = (self.currency_id is not None, self.currency_code is not None)

        if sum(identifiers) != 1:
            raise ValueError("Provide exactly one of currency_id or currency_code")
        
        return self

class SubscriptionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    user_id: int
    currency_id: int
