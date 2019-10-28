from src.presenter import socket_presenter
from src.input.smart_input import smart_input


def show(udp=False):
    _execute(_collect_config(), udp)


def _collect_config():
    ip_response = socket_presenter.get_ip(smart_input("Ip: "))
    while not ip_response.valid:
        ip_response = socket_presenter.get_ip(
            smart_input(f'{ip_response.error}: '))

    port_response = socket_presenter.get_port(smart_input("Port: "))
    while not port_response.valid:
        port_response = socket_presenter.get_port(
            smart_input(f'{port_response.error}: '))

    timeout_response = socket_presenter.get_timeout(smart_input(
        f'Timeout(o, default: {socket_presenter.DEFAULT_TIMEOUT}): '))
    while not timeout_response.valid:
        timeout_response = socket_presenter.get_timeout(
            smart_input(f'{timeout_response.error}: '))

    rate_response = socket_presenter.get_rate(
        smart_input("Rate(or 0 if data should be send once):"))
    while not rate_response.valid:
        rate_response = socket_presenter.get_rate(
            smart_input(f'{rate_response.error}: '))

    data_response = socket_presenter.collect_data(smart_input)
    while not data_response.valid:
        print(data_response.error)
        data_response = socket_presenter.collect_data(smart_input)

    return socket_presenter.SocketRequestConfig(ip_response.data,
                                                port_response.data,
                                                rate_response.data,
                                                data_response.data,
                                                timeout=timeout_response.data,
                                                data_consumer=lambda x: print(
                                                    str(x)),
                                                interruption=lambda: smart_input())


def _execute(config, udp):
    if config.rate > 0:
        print('Listening to responses, press enter to stop.')
    else:
        print('Received response:')
    if udp:
        socket_presenter.execute_udp_request(config)
    else:
        socket_presenter.execute_tcp_request(config)
    _repeat_or_exit(config, udp)


def _repeat_or_exit(config, udp):
    print()
    repeat = smart_input('Change data and keep sending?(y/n): ')
    print()
    if repeat.lower() == 'y':
        data_response = socket_presenter.collect_data(smart_input)
        while not data_response.valid:
            print(data_response.error)
            data_response = socket_presenter.collect_data(smart_input)
        config.data = data_response.data
        _execute(config, udp)
