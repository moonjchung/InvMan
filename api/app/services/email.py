from postmarker.core import PostmarkClient
from app.core.config import settings

def send_low_stock_alert(item_name: str, item_sku: str, stock_level: int):
    if not settings.POSTMARK_SERVER_TOKEN:
        print("POSTMARK_SERVER_TOKEN not set, skipping email.")
        return

    postmark = PostmarkClient(server_token=settings.POSTMARK_SERVER_TOKEN)
    postmark.emails.send(
        From="sender@example.com", # Replace with a real sender email
        To="recipient@example.com", # Replace with a real recipient email
        Subject=f"Low Stock Alert: {item_name}",
        TextBody=f"The stock level for item {item_name} (SKU: {item_sku}) is low: {stock_level}.",
    )
