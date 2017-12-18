from harmonicIO.processing_engine import batch


def process_data(message_bytes):
    print(len(message_bytes))


batch.listen_for_tasks(process_data)
