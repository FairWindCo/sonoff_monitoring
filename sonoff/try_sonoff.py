import sonoff

if __name__ == '__main__':

    devices = []
    try:
        s = sonoff.Sonoff('dima@tsarsky.com', 'Sonoff123@', 'eu')
        s.update_devices()
        devices = s.get_devices()
        print(devices)
    except Exception as e:
        print('EX ' + e)