import json

sockets = []

def web_socket_do_extra_handshake(request):
    pass

def web_socket_transfer_data(request):
    global sockets
    
    while True:
        try:
            incoming = json.loads(request.ws_stream.receive_message())
            
            if 'is_admin' in incoming and incoming['is_admin']:
                request.ws_stream.send_message("sending message to "+str(len(sockets))+" sockets!")
                delete_queue = []
                for i in range(len(sockets)):
                    if sockets[i]._request.client_terminated or sockets[i]._request.server_terminated:
                        delete_queue.append(i)
                for i in range(len(delete_queue)):
                    del sockets[delete_queue[i]]
                request.ws_stream.send_message("there are now "+str(len(sockets))+" sockets!")
                for i in range(len(sockets)):
                    try:
                        sockets[i].send_message(json.dumps({
                            'is_enabled': incoming['is_enabled']
                        }))
                    except:
                        pass
            else:
                sockets += [request.ws_stream]
        except Exception as inst:
            request.ws_stream.send_message(inst.__str__())