from harmonicPE.daemon import listen_for_tasks


def process_data(message_bytes):
    # Format of binary message representing task for distributed execution is specific to your application.
    print('message was bytes: ' + str(len(message_bytes)))


# Start the daemon to listen for tasks:
listen_for_tasks(process_data)
