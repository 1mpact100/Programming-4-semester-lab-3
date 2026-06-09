import httpx


CBR_XML = """<?xml version="1.0" encoding="windows-1251"?>
<ValCurs Date="09.06.2026" name="Foreign Currency Market">
    <Valute ID="R01235">
        <NumCode>840</NumCode>
        <CharCode>USD</CharCode>
        <Nominal>1</Nominal>
        <Name>Доллар США</Name>
        <Value>79,1234</Value>
    </Valute>
    <Valute ID="R01020A">
        <NumCode>944</NumCode>
        <CharCode>AZN</CharCode>
        <Nominal>10</Nominal>
        <Name>Азербайджанских манатов</Name>
        <Value>465,0000</Value>
    </Valute>
</ValCurs>
""".encode("cp1251")


class FakeAsyncClient:
    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        pass

    async def get(self, url):
        request = httpx.Request("GET", url)
        return httpx.Response(200, content=CBR_XML, request=request)


def test_user_crud(client):
    response = client.post(
        "/users/",
        json={"username": "alice", "email": "alice@example.com"},
    )
    assert response.status_code == 201
    user_id = response.json()["id"]

    duplicate = client.post(
        "/users/",
        json={"username": "alice", "email": "another@example.com"},
    )
    assert duplicate.status_code == 409

    updated = client.put(
        f"/users/{user_id}",
        json={"email": "new@example.com"},
    )
    assert updated.status_code == 200
    assert updated.json()["email"] == "new@example.com"

    assert client.get("/users/").json()[0]["username"] == "alice"
    assert client.delete(f"/users/{user_id}").status_code == 200
    assert client.get(f"/users/{user_id}").status_code == 404


def test_currency_update_rate_and_subscription(client, monkeypatch):
    monkeypatch.setattr("app.services.currency.httpx.AsyncClient", FakeAsyncClient)

    updated = client.post("/currencies/update")
    assert updated.status_code == 200
    assert updated.json() == {"updated_currencies": 2, "updated_rates": 2}

    currencies = client.get("/currencies/").json()
    assert [currency["code"] for currency in currencies] == ["AZN", "USD"]

    rate = client.get("/currencies/AZN/rate")
    assert rate.status_code == 200
    assert rate.json()["rate"] == 46.5

    user = client.post(
        "/users/",
        json={"username": "bob", "email": "bob@example.com"},
    ).json()
    request = {"user_id": user["id"], "currency_code": "usd"}

    subscription = client.post("/subscriptions/", json=request)
    assert subscription.status_code == 201
    assert client.post("/subscriptions/", json=request).status_code == 409

    user_with_subscriptions = client.get(f"/users/{user['id']}").json()
    assert user_with_subscriptions["subscriptions"][0]["code"] == "USD"

    assert client.request("DELETE", "/subscriptions/", json=request).status_code == 200
    assert client.request("DELETE", "/subscriptions/", json=request).status_code == 404


def test_subscription_requires_exactly_one_currency_identifier(client):
    invalid = client.post(
        "/subscriptions/",
        json={"user_id": 1, "currency_id": 1, "currency_code": "USD"},
    )
    assert invalid.status_code == 422
