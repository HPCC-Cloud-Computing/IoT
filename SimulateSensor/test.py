def write_sitemap_file(i):
    try:
        f = open('config/config_'+str(int(i/10))+'.cfg', 'w')
        f.writelines('128.199.242.5\n')
        f.writelines('31382\n')
        f.writelines('sensor_\n')
        f.writelines('sensor_\n')
        f.writelines(str(i)+'\n')
        f.writelines('60\n')
    except IOError:
        print('Can not open file sitemap\n')
    else:
        f.close()

for i in range(1, 11):
    write_sitemap_file(i*10)