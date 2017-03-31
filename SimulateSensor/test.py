def write_sitemap_file(i):
    try:
        f = open('test.config/config_' + str(int(i / 10)) + '.cfg', 'w')
        f.writelines('128.199.242.5\n')
        f.writelines('31382\n')
        f.writelines('sensor_\n')
        f.writelines('sensor_\n')
        f.writelines(str(i) + '\n')
        f.writelines('60\n')
    except IOError:
        print('Can not open file sitemap\n')
    else:
        f.close()


def write_item_openhab_file(index, index_2):
    try:
        f = open('test.config/openhab.items/demo_{}.items'.format(index), 'w')
        for k in range(index_2, index_2 + 5):
            f.write('Number openhab_pf_{}'.format(str(k)) +
                    ' "Value [%.1f]" {mqtt="<[mqttIn:'+'openhab_pf_{}/temperature'.format(str(k))+':state:default], '+
                    '>[mqttOut:'+'openhab_pf_{}/temperature'.format(str(k))+':state:*:default]"}\n')
    except IOError:
        print('Can not open file item\n')
    else:
        f.close()


j = 1
for i in range(1, 4):
    write_item_openhab_file(i, j)
    j += 5
