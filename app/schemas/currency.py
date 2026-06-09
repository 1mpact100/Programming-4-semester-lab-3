from datetime import date

from pydantic import BaseModel, ConfigDict

class CurrencyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    code: str
    name: str

class CurrencyRateRead(BaseModel):
    currency_code: str
    currency_name: str
    date: date
    rate: float

class CurrenciesUpdateResult(BaseModel):
    updated_currencies: int
    updated_rates: int
