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


# j = 1
# for i in range(1, 4):
#     write_item_openhab_file(i, j)
#     j += 5

def gen_sensor_item(start, end, type, freq, prefix):
    for i in range(start, end+1):
        print('{type},{type}_pf_{prefix}_{index},{type}_pf_{prefix}_{index}/temperature,{freq}'.format(
            type=type, index=i, freq=freq, prefix=prefix
        ))

def gen_onem2m_item(start, end, prefix):
    print('[')
    for i in range(start, end+1):
        item = dict()
        item['item_name'] = 'onem2m_pf_{prefix}_{index}'.format(index=i, prefix=prefix)
        item['item_type'] = '1'
        item['topic'] = 'onem2m_pf_{prefix}_{index}/temperature'.format(index=i, prefix=prefix)
        if i == end:
            print('{}'.format(item))
        else:
            print('{},'.format(item))
    print(']')

def gen_openhab_item(start, end):
    for i in range(start, end + 1):
        print('String openhab_pf_'+str(i)+' "[%s]" {mqtt="<[mqttIn:openhab_pf_'+str(i)+'/temperature:state:default], >[mqttOut:openhab_pf_'+str(i)+'/temperature:state:*:default]"}')

def gen_topic(start, end, type, prefix):
    for i in range(start, end+1):
        print('{type}_pf_{prefix}_{index}/temperature'.format(
            type=type, index=i, prefix=prefix
        ))

# for i in range(16, 31):
    # item = dict()
    # item['item_name'] = 'onem2m_pf_{}'.format(i)
    # item['item_type'] = '1'
    # item['topic'] = 'onem2m_pf_{}/temperature'.format(i)
    # print('{},'.format(item))
    # print('String openhab_pf_'+str(i)+' "[%s]" {mqtt="<[mqttIn:openhab_pf_'+str(i)+'/temperature:state:default], >[mqttOut:openhab_pf_'+str(i)+'/temperature:state:*:default]"}')
# gen_sensor_item(1, 50, 'onem2m', 10, 5)
# gen_onem2m_item(1, 50, 5)
# gen_openhab_item()
gen_topic(1,50,'onem2m',5)