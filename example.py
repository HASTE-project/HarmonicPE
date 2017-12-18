from harmonicPE.daemon import listen_for_tasks


def process_data(message_bytes):
    print(len(message_bytes))


listen_for_tasks(process_data)
