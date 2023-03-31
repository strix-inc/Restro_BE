from base64 import b64encode
import requests


class UPIService:
    def __init__(self, upi_id: str, name: str) -> None:
        self.upi_id = upi_id

    def generate_upi_qr_code(self, amount: float, note: str, name):
        amount = f"{amount:.2f}"
        res = requests.get(
            "https://upiqr.in/api/qr",
            params={"name": name, "vpa": self.upi_id, "amount": amount, "note": note},
            timeout=5,
        )
        if res.status_code == 200:
            return b64encode(res.content).decode()
