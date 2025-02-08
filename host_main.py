from serialcomms.serial_host import host_mainloop

if __name__ == '__main__':
    host_mainloop(onreceive=lambda x: print(x))
