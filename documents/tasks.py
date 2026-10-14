import time
from celery import shared_task


@shared_task
def notify_new_document(document_id):
    from .models import Document
    doc = Document.objects.select_related('asset').get(pk=document_id)
    time.sleep(5)  # simulacija spore obrade
    message = f"Novi dokument '{doc.title}' (v{doc.version}) dodat na '{doc.asset.name}'"
    print(message)
    return message