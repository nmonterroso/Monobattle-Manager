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
				for i in range(len(sockets)):
					if sockets[i] is None or sockets[i]._request.client_terminated or sockets[i]._request.server_terminated:
						sockets[i] = None
					else:
						try:
							sockets[i].send_message(json.dumps({
								'is_enabled': incoming['is_enabled']
							}))
						except:
							sockets[i] = None
							pass

				while sockets.count(None) > 0:
					sockets.remove(None)
			else:
				sockets.append(request.ws_stream)
				request.ws_stream.send_message(json.dumps({
					'ack': True
				}))
		except Exception as inst:
			request.ws_stream.send_message(inst.__str__())


def display_sockets(socket):
	global sockets
	for i in range(len(sockets)):
		if sockets[i] is None:
			socket.send_message(str(i) + " is None")
		else:
			socket.send_message(str(i) + " is NOT None")