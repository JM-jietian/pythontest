// 绕过TracerPid检测
var ByPassTracerPid = function () {
    var fgetsPtr = Module.findExportByName('libc.so', 'fgets');
    var fgets = new NativeFunction(fgetsPtr, 'pointer', ['pointer', 'int', 'pointer']);
    Interceptor.replace(fgetsPtr, new NativeCallback(function (buffer, size, fp) {
        var retval = fgets(buffer, size, fp);
        var bufstr = Memory.readUtf8String(buffer);
        if (bufstr.indexOf('TracerPid:') > -1) {
            Memory.writeUtf8String(buffer, 'TracerPid:\t0');
            console.log('tracerpid replaced: ' + Memory.readUtf8String(buffer));
        }
        return retval;
    }, 'pointer', ['pointer', 'int', 'pointer']));
};

// 获取调用链
function getStackTrace() {
    var Exception = Java.use('java.lang.Exception');
    var ins = Exception.$new('Exception');
    var straces = ins.getStackTrace();
    if (undefined == straces || null == straces) {
        return;
    }
    var result = '';
    for (var i = 0; i < straces.length; i++) {
        var str = '   ' + straces[i].toString();
        result += str + '\r\n';
    }
    Exception.$dispose();
    return result;
}

function get_format_time() {
    var myDate = new Date();

    return myDate.getFullYear() + '-' + myDate.getMonth() + '-' + myDate.getDate() + ' ' + myDate.getHours() + ':' + myDate.getMinutes() + ':' + myDate.getSeconds();
}

//告警发送
function alertSend(action, messages, arg) {
    var _time = get_format_time();
    send({
        'type': 'notice',
        'time': _time,
        'action': action,
        'messages': messages,
        'arg': arg,
        'stacks': getStackTrace()
    });
}

// 增强健壮性，避免有的设备无法使用 Array.isArray 方法
if (!Array.isArray) {
    Array.isArray = function (arg) {
        return Object.prototype.toString.call(arg) === '[object Array]';
    };
}

// hook方法
function hookMethod(targetClass, targetMethod, targetArgs, action, messages) {
    try {
        var _Class = Java.use(targetClass);
    } catch (e) {
        return false;
    }

    if (targetMethod == '$init') {
        var overloadCount = _Class.$init.overloads.length;
        for (var i = 0; i < overloadCount; i++) {
            _Class.$init.overloads[i].implementation = function () {
                var temp = this.$init.apply(this, arguments);
                // 是否含有需要过滤的参数
                var argumentValues = Object.values(arguments);
                if (Array.isArray(targetArgs) && targetArgs.length > 0 && !targetArgs.every(item => argumentValues.includes(item))) {
                    return null;
                }
                var arg = '';
                for (var j = 0; j < arguments.length; j++) {
                    arg += '参数' + j + '：' + JSON.stringify(arguments[j]) + '\r\n';
                }
                if (arg.length == 0) arg = '无参数';
                else arg = arg.slice(0, arg.length - 1);
                alertSend(action, messages, arg);
                return temp;
            }
        }
    } else {
        try {
            var overloadCount = _Class[targetMethod].overloads.length;
        } catch (e) {
            console.log(e)
            console.log('[*] hook(' + targetMethod + ')方法失败,请检查该方法是否存在！！！');
            return false;
        }
        for (var i = 0; i < overloadCount; i++) {
            _Class[targetMethod].overloads[i].implementation = function () {
                var temp = this[targetMethod].apply(this, arguments);
                // 是否含有需要过滤的参数
                var argumentValues = Object.values(arguments);
                if (Array.isArray(targetArgs) && targetArgs.length > 0 && !targetArgs.every(item => argumentValues.includes(item))) {
                    return null;
                }
                var arg = '';
                for (var j = 0; j < arguments.length; j++) {
                    arg += '参数' + j + '：' + JSON.stringify(arguments[j]) + '\r\n';
                }
                if (arg.length == 0) arg = '无参数';
                else arg = arg.slice(0, arg.length - 1);
                alertSend(action, messages, arg);
                return temp;
            }
        }
    }
    return true;
}

// hook方法(去掉不存在方法）
function hook(targetClass, methodData) {
    try {
        var _Class = Java.use(targetClass);
    } catch (e) {
        return false;
    }
    var methods = _Class.class.getDeclaredMethods();
    _Class.$dispose;
    // 排查掉不存在的方法，用于各个android版本不存在方法报错问题。
    methodData.forEach(function (methodData) {
        for (var i in methods) {
            if (methods[i].toString().indexOf('.' + methodData['methodName'] + '(') != -1 || methodData['methodName'] == '$init') {
                hookMethod(targetClass, methodData['methodName'], methodData['args'], methodData['action'], methodData['messages']);
                break;
            }
        }
    });
}

// hook获取其他app信息api，排除app自身
function hookApplicationPackageManagerExceptSelf(targetMethod, action) {
    var _ApplicationPackageManager = Java.use('android.app.ApplicationPackageManager');
    try {
        try {
            var overloadCount = _ApplicationPackageManager[targetMethod].overloads.length;
        } catch (e) {
            return false;
        }
        for (var i = 0; i < overloadCount; i++) {
            _ApplicationPackageManager[targetMethod].overloads[i].implementation = function () {
                var temp = this[targetMethod].apply(this, arguments);
                var arg = '';
                for (var j = 0; j < arguments.length; j++) {
                    if (j === 0) {
                        var string_to_recv;
                        send({'type': 'app_name', 'data': arguments[j]});
                        recv(function (received_json_object) {
                            string_to_recv = received_json_object.my_data;
                        }).wait();
                    }
                    arg += '参数' + j + '：' + JSON.stringify(arguments[j]) + '\r\n';
                }
                if (arg.length == 0) arg = '无参数';
                else arg = arg.slice(0, arg.length - 1);
                if (string_to_recv) {
                    alertSend(action, targetMethod + '获取的数据为：' + temp, arg);
                }
                return temp;
            }
        }
    } catch (e) {
        console.log(e);
        return
    }


}

// 申请权限
function checkRequestPermission() {
    var action = '申请权限';

    //老项目
    hook('android.support.v4.app.ActivityCompat', [
        {'methodName': 'requestPermissions', 'action': action, 'messages': '申请具体权限看"参数1"'}
    ]);

    hook('androidx.core.app.ActivityCompat', [
        {'methodName': 'requestPermissions', 'action': action, 'messages': '申请具体权限看"参数1"'}
    ]);
}

// 获取电话相关信息
function getPhoneState() {
    var action = '获取电话相关信息';

    hook('android.telephony.TelephonyManager', [
        // Android 8.0
        {'methodName': 'getDeviceId', 'action': action, 'messages': '获取IMEI'},
        // Android 8.1、9   android 10获取不到
        {'methodName': 'getImei', 'action': action, 'messages': '获取IMEI'},

        {'methodName': 'getMeid', 'action': action, 'messages': '获取MEID'},
        {'methodName': 'getLine1Number', 'action': action, 'messages': '获取电话号码标识符'},
        {'methodName': 'getSimSerialNumber', 'action': action, 'messages': '获取IMSI/iccid'},
        {'methodName': 'getSubscriberId', 'action': action, 'messages': '获取IMSI'},
        {'methodName': 'getSimOperator', 'action': action, 'messages': '获取MCC/MNC'},
        {'methodName': 'getNetworkOperator', 'action': action, 'messages': '获取MCC/MNC'},
        {'methodName': 'getSimCountryIso', 'action': action, 'messages': '获取SIM卡国家代码'},

        {'methodName': 'getCellLocation', 'action': action, 'messages': '获取电话当前位置信息'},
        {'methodName': 'getAllCellInfo', 'action': action, 'messages': '获取电话当前位置信息'},
        {'methodName': 'requestCellInfoUpdate', 'action': action, 'messages': '获取基站信息'},
        {'methodName': 'getServiceState', 'action': action, 'messages': '获取sim卡是否可用'},
    ]);

    // 电信卡cid lac
    hook('android.telephony.cdma.CdmaCellLocation', [
        {'methodName': 'getBaseStationId', 'action': action, 'messages': '获取基站cid信息'},
        {'methodName': 'getNetworkId', 'action': action, 'messages': '获取基站lac信息'}
    ]);

    // 移动联通卡 cid/lac
    hook('android.telephony.gsm.GsmCellLocation', [
        {'methodName': 'getCid', 'action': action, 'messages': '获取基站cid信息'},
        {'methodName': 'getLac', 'action': action, 'messages': '获取基站lac信息'}
    ]);

    // 短信
    hook('android.telephony.SmsManager', [
        {'methodName': 'sendTextMessageInternal', 'action': action, 'messages': '获取短信信息-发送短信'},
        {'methodName': 'getDefault', 'action': action, 'messages': '获取短信信息-发送短信'},
        {'methodName': 'sendTextMessageWithSelfPermissions', 'action': action, 'messages': '获取短信信息-发送短信'},
        {'methodName': 'sendMultipartTextMessageInternal', 'action': action, 'messages': '获取短信信息-发送短信'},
        {'methodName': 'sendDataMessage', 'action': action, 'messages': '获取短信信息-发送短信'},
        {'methodName': 'sendDataMessageWithSelfPermissions', 'action': action, 'messages': '获取短信信息-发送短信'},
    ]);

}

// 系统信息(AndroidId/标识/content敏感信息)
function getSystemData() {
    var action = '获取系统信息';

    hook('android.provider.Settings$Secure', [
        {'methodName': 'getString', 'args': ['android_id'], 'action': action, 'messages': '获取安卓ID'}
    ]);
    hook('android.provider.Settings$System', [
        {'methodName': 'getString', 'args': ['android_id'], 'action': action, 'messages': '获取安卓ID'}
    ]);


    hook('android.os.Build', [
        {'methodName': 'getSerial', 'action': action, 'messages': '获取设备序列号'},
    ]);

    hook('android.app.admin.DevicePolicyManager', [
        {'methodName': 'getWifiMacAddress', 'action': action, 'messages': '获取mac地址'},
    ]);

    hook('android.content.ClipboardManager', [
        {'methodName': 'getPrimaryClip', 'action': action, 'messages': '读取剪切板信息'},
        {'methodName': 'setPrimaryClip', 'action': action, 'messages': '写入剪切板信息'},
    ]);

    hook('android.telephony.UiccCardInfo', [
        {'methodName': 'getIccId', 'action': action, 'messages': '读取手机IccId信息'},
    ]);

    //小米
    hook('com.android.id.impl.IdProviderImpl', [
        {'methodName': 'getUDID', 'action': action, 'messages': '读取小米手机UDID'},
        {'methodName': 'getOAID', 'action': action, 'messages': '读取小米手机OAID'},
        {'methodName': 'getVAID', 'action': action, 'messages': '读取小米手机VAID'},
        {'methodName': 'getAAID', 'action': action, 'messages': '读取小米手机AAID'},
    ]);

    //三星
    hook('com.samsung.android.deviceidservice.IDeviceIdService$Stub$Proxy', [
        {'methodName': 'getOAID', 'action': action, 'messages': '读取三星手机OAID'},
        {'methodName': 'getVAID', 'action': action, 'messages': '读取三星手机VAID'},
        {'methodName': 'getAAID', 'action': action, 'messages': '读取三星手机AAID'},
    ]);

    hook('repeackage.com.samsung.android.deviceidservice.IDeviceIdService$Stub$Proxy', [
        {'methodName': 'getOAID', 'action': action, 'messages': '读取三星手机OAID'},
        {'methodName': 'getVAID', 'action': action, 'messages': '读取三星手机VAID'},
        {'methodName': 'getAAID', 'action': action, 'messages': '读取三星手机AAID'},
    ]);

    //OPPO
    hook('com.coloros.service.oaid.IDeviceIDService', [
        {'methodName': 'getOAID', 'action': action, 'messages': '读取OPPO手机OAID'},
        {'methodName': 'getVAID', 'action': action, 'messages': '读取OPPO手机VAID'},
        {'methodName': 'getAAID', 'action': action, 'messages': '读取OPPO手机AAID'},
    ]);

    //获取content敏感信息
    try {
        // 通讯录内容
        var ContactsContract = Java.use('android.provider.ContactsContract');
        var contact_authority = ContactsContract.class.getDeclaredField('AUTHORITY').get('java.lang.Object');
    } catch (e) {
        console.log(e)
    }
    try {
        // 日历内容
        var CalendarContract = Java.use('android.provider.CalendarContract');
        var calendar_authority = CalendarContract.class.getDeclaredField('AUTHORITY').get('java.lang.Object');
    } catch (e) {
        console.log(e)
    }
    try {
        // 浏览器内容
        var BrowserContract = Java.use('android.provider.BrowserContract');
        var browser_authority = BrowserContract.class.getDeclaredField('AUTHORITY').get('java.lang.Object');
    } catch (e) {
        console.log(e)
    }
    try {
        // 相册内容
        var MediaStore = Java.use('android.provider.MediaStore');
        var media_authority = MediaStore.class.getDeclaredField('AUTHORITY').get('java.lang.Object');
    } catch (e) {
        console.log(e)
    }
    try {
        var ContentResolver = Java.use('android.content.ContentResolver');
        var queryLength = ContentResolver.query.overloads.length;
        for (var i = 0; i < queryLength; i++) {
            ContentResolver.query.overloads[i].implementation = function () {
                var temp = this.query.apply(this, arguments);
                if (arguments[0].toString().indexOf(contact_authority) != -1) {
                    alertSend(action, '获取手机通信录内容', '');
                } else if (arguments[0].toString().indexOf(calendar_authority) != -1) {
                    alertSend(action, '获取日历内容', '');
                } else if (arguments[0].toString().indexOf(browser_authority) != -1) {
                    alertSend(action, '获取浏览器内容', '');
                } else if (arguments[0].toString().indexOf(media_authority) != -1) {
                    alertSend(action, '获取相册内容', '');
                }
                return temp;
            }
        }
    } catch (e) {
        console.log(e);
        return
    }
}

//获取其他app信息
function getPackageManager() {
    var action = '获取其他app信息';

    hook('android.content.pm.PackageManager', [
        {'methodName': 'getInstalledPackages', 'action': action, 'messages': 'APP获取了其他app信息'},
        {'methodName': 'getInstalledApplications', 'action': action, 'messages': 'APP获取了其他app信息'}
    ]);

    hook('android.app.ApplicationPackageManager', [
        {'methodName': 'getInstalledPackages', 'action': action, 'messages': 'APP获取了其他app信息'},
        {'methodName': 'getInstalledApplications', 'action': action, 'messages': 'APP获取了其他app信息'},
        {'methodName': 'queryIntentActivities', 'action': action, 'messages': 'APP获取了其他app信息'},
    ]);

    hook('android.app.ActivityManager', [
        {'methodName': 'getRunningAppProcesses', 'action': action, 'messages': '获取了正在运行的App'},
        {'methodName': 'getRunningServiceControlPanel', 'action': action, 'messages': '获取了正在运行的服务面板'},
    ]);
    //需排除应用本身
    hookApplicationPackageManagerExceptSelf('getApplicationInfo', action);
    hookApplicationPackageManagerExceptSelf('getPackageInfoAsUser', action);
    hookApplicationPackageManagerExceptSelf('getInstallerPackageName', action);
}

// 获取位置信息
function getGSP() {
    var action = '获取位置信息';

    hook('android.location.LocationManager', [
        {'methodName': 'requestLocationUpdates', 'action': action, 'messages': action},
        {'methodName': 'getLastKnownLocation', 'action': action, 'messages': action},
        {'methodName': 'getBestProvider', 'action': action, 'messages': action},
        {'methodName': 'getGnssHardwareModelName', 'action': action, 'messages': action},
        {'methodName': 'getGnssYearOfHardware', 'action': action, 'messages': action},
        {'methodName': 'getProvider', 'action': action, 'messages': action},
        {'methodName': 'requestSingleUpdate', 'action': action, 'messages': action},
        {'methodName': 'getCurrentLocation', 'action': action, 'messages': action},
    ]);

    hook('android.location.Location', [
        {'methodName': 'getAccuracy', 'action': action, 'messages': action},
        {'methodName': 'getAltitude', 'action': action, 'messages': action},
        {'methodName': 'getBearing', 'action': action, 'messages': action},
        {'methodName': 'getBearingAccuracyDegrees', 'action': action, 'messages': action},
        {'methodName': 'getElapsedRealtimeNanos', 'action': action, 'messages': action},
        {'methodName': 'getExtras', 'action': action, 'messages': action},
        {'methodName': 'getLatitude', 'action': action, 'messages': action},
        {'methodName': 'getLongitude', 'action': action, 'messages': action},
        {'methodName': 'getProvider', 'action': action, 'messages': action},
        {'methodName': 'getSpeed', 'action': action, 'messages': action},
        {'methodName': 'getSpeedAccuracyMetersPerSecond', 'action': action, 'messages': action},
        {'methodName': 'getTime', 'action': action, 'messages': action},
        {'methodName': 'getVerticalAccuracyMeters', 'action': action, 'messages': action},
    ]);

    hook('android.location.Geocoder', [
        {'methodName': 'getFromLocation', 'action': action, 'messages': action},
        {'methodName': 'getFromLocationName', 'action': action, 'messages': action},
    ]);

}

// 调用摄像头(hook，防止静默拍照)
function getCamera() {
    var action = '调用摄像头';

    hook('android.hardware.Camera', [
        {'methodName': 'open', 'action': action, 'messages': action},
    ]);

    hook('android.hardware.camera2.CameraManager', [
        {'methodName': 'openCamera', 'action': action, 'messages': action},
    ]);

    hook('androidx.camera.core.ImageCapture', [
        {'methodName': 'takePicture', 'action': action, 'messages': '调用摄像头拍照'},
    ]);

}

//获取网络信息
function getNetwork() {
    var action = '获取网络信息';

    hook('android.net.wifi.WifiInfo', [
        {'methodName': 'getMacAddress', 'action': action, 'messages': '获取Mac地址'},
        {'methodName': 'getSSID', 'action': action, 'messages': '获取wifi SSID'},
        {'methodName': 'getBSSID', 'action': action, 'messages': '获取wifi BSSID'},
    ]);

    hook('android.net.wifi.WifiManager', [
        {'methodName': 'getConnectionInfo', 'action': action, 'messages': '获取wifi信息'},
        {'methodName': 'getConfiguredNetworks', 'action': action, 'messages': '获取wifi信息'},
        {'methodName': 'getScanResults', 'action': action, 'messages': '获取wifi信息'},
        {'methodName': 'getWifiState', 'action': action, 'messages': '获取wifi状态信息'},
    ]);

    hook('java.net.InetAddress', [
        {'methodName': 'getHostAddress', 'action': action, 'messages': '获取IP地址'},
        {'methodName': 'getAddress', 'action': action, 'messages': '获取网络address信息'},
        {'methodName': 'getHostName', 'action': action, 'messages': '获取网络hostname信息'},
    ]);

    hook('java.net.Inet4Address', [
        {'methodName': 'getHostAddress', 'action': action, 'messages': '获取IP地址'},
    ]);

    hook('java.net.Inet6Address', [
        {'methodName': 'getHostAddress', 'action': action, 'messages': '获取IP地址'},
    ]);

    hook('java.net.NetworkInterface', [
        {'methodName': 'getHardwareAddress', 'action': action, 'messages': '获取Mac地址'}
    ]);

    hook('android.net.NetworkInfo', [
        {'methodName': 'getType', 'action': action, 'messages': '获取网络类型'},
        {'methodName': 'getTypeName', 'action': action, 'messages': '获取网络类型名称'},
        {'methodName': 'getExtraInfo', 'action': action, 'messages': '获取网络名称'},
        {'methodName': 'isAvailable', 'action': action, 'messages': '获取网络是否可用'},
        {'methodName': 'isConnected', 'action': action, 'messages': '获取网络是否连接'},
    ]);

    hook('android.net.ConnectivityManager', [
        {'methodName': 'getActiveNetworkInfo', 'action': action, 'messages': '获取网络状态信息'},
    ]);

    hook('java.net.InetSocketAddress', [
        {'methodName': 'getHostAddress', 'action': action, 'messages': '获取网络hostaddress信息'},
        {'methodName': 'getAddress', 'action': action, 'messages': '获取网络address信息'},
        {'methodName': 'getHostName', 'action': action, 'messages': '获取网络hostname信息'},
    ]);

    // ip地址
    try {
        var _WifiInfo = Java.use('android.net.wifi.WifiInfo');
        //获取ip
        _WifiInfo.getIpAddress.implementation = function () {
            var temp = this.getIpAddress();
            var _ip = new Array();
            _ip[0] = (temp >>> 24) >>> 0;
            _ip[1] = ((temp << 8) >>> 24) >>> 0;
            _ip[2] = (temp << 16) >>> 24;
            _ip[3] = (temp << 24) >>> 24;
            var _str = String(_ip[3]) + "." + String(_ip[2]) + "." + String(_ip[1]) + "." + String(_ip[0]);
            alertSend(action, '获取IP地址：' + _str, '');
            return temp;
        }
    } catch (e) {
        console.log(e)
    }
}

//获取蓝牙设备信息
function getBluetooth() {
    var action = '获取蓝牙设备信息';

    hook('android.bluetooth.BluetoothDevice', [
        {'methodName': 'getName', 'action': action, 'messages': '获取蓝牙设备名称'},
        {'methodName': 'getAddress', 'action': action, 'messages': '获取蓝牙设备mac'},
    ]);

    hook('android.bluetooth.BluetoothAdapter', [
        {'methodName': 'getName', 'action': action, 'messages': '获取蓝牙设备名称'}
    ]);
}

//读写文件
function getFileMessage() {
    var action = '文件操作';

    hook('java.io.RandomAccessFile', [
        {'methodName': '$init', 'action': action, 'messages': 'RandomAccessFile写文件'}
    ]);
    hook('java.io.File', [
        {'methodName': 'mkdirs', 'action': action, 'messages': '尝试写入sdcard创建小米市场审核可能不通过'},
        {'methodName': 'mkdir', 'action': action, 'messages': '尝试写入sdcard创建小米市场审核可能不通过'}
    ]);
}

//获取麦克风信息
function getMedia() {
    var action = '获取麦克风'

    hook('android.media.MediaRecorder', [
        {'methodName': 'start', 'action': action, 'messages': '获取麦克风'},
    ]);
    hook('android.media.AudioRecord', [
        {'methodName': 'startRecording', 'action': action, 'messages': '获取麦克风'},
    ]);
}

//获取传感器信息
function getSensor() {
    var action = '获取传感器信息'

    hook('android.hardware.SensorManager', [
        {'methodName': 'getSensorList', 'action': action, 'messages': '获取传感器信息'},
    ]);

}

function customHook() {
    var action = '自定义hook';

    //自定义hook函数，可自行添加。格式如下：
    // 读取日历
    hook('android.provider.CalendarContract.Calendars', [
        {'methodName': 'query', 'action': '读取日历', 'messages': '读取日历'},
    ]);
    // 编辑日历
    hook('android.provider.CalendarContract.Calendars', [
        {'methodName': 'insert', 'action': '编辑日历', 'messages': '编辑日历'},
    ]);
    // 读取通话记录
    hook('android.provider.CallLog$Calls', [
        {'methodName': 'query', 'action': '读取通话记录', 'messages': '读取通话记录'},
    ]);
    // 编辑通话记录
    hook('android.provider.CallLog$Calls', [
        {'methodName': 'add', 'action': '编辑通话记录', 'messages': '编辑通话记录'},
    ]);
    // 查看正在拨打的号码，并监听、控制或中止通话
    hook('android.telephony.PhoneStateListener', [
        {'methodName': 'onCallStateChanged', 'action': '监听电话状态', 'messages': '监听电话状态'},
    ]);
    // 使用摄像头
    hook('android.hardware.Camera', [
        {'methodName': 'open', 'action': '使用摄像头', 'messages': '使用摄像头'},
    ]);
    // 读取通讯录
    hook('android.provider.ContactsContract$Contacts', [
        {'methodName': 'query', 'action': '读取通讯录', 'messages': '读取通讯录'},
    ]);
    // 编辑通讯录
    hook('android.provider.ContactsContract$RawContacts', [
        {'methodName': 'insert', 'action': '编辑通讯录', 'messages': '编辑通讯录'},
    ]);
    // 从账户服务中获取应用账户列表
    hook('android.accounts.AccountManager', [
        {'methodName': 'getAccounts', 'action': '获取应用账户列表', 'messages': '获取应用账户列表'},
    ]);
    // 获取精准地理位置
    hook('android.location.LocationManager', [
        {'methodName': 'requestLocationUpdates', 'action': '获取精准地理位置', 'messages': '获取精准地理位置'},
    ]);
    // 获取粗略地理位置
    hook('android.location.LocationManager', [
        {'methodName': 'requestLocationUpdates', 'action': '获取粗略地理位置', 'messages': '获取粗略地理位置'},
    ]);
    // 后台运行时访问用户的位置
    hook('android.location.LocationManager', [
        {'methodName': 'requestLocationUpdates', 'action': '后台访问位置', 'messages': '后台访问位置'},
    ]);
    // 使用麦克风录音
    hook('android.media.MediaRecorder', [
        {'methodName': 'start', 'action': '使用麦克风录音', 'messages': '使用麦克风录音'},
    ]);
    // 获取设备 IMSI、IMEI 等设备识别码
    hook('android.telephony.TelephonyManager', [
        {'methodName': 'getDeviceId', 'action': '获取设备识别码', 'messages': '获取设备识别码'},
    ]);
    // 获取本机手机号码
    hook('android.telephony.TelephonyManager', [
        {'methodName': 'getLine1Number', 'action': '获取手机号码', 'messages': '获取手机号码'},
    ]);
    // 拨打电话
    hook('android.content.Intent', [
        {'methodName': 'ACTION_CALL_BUTTON', 'action': '拨打电话', 'messages': '拨打电话'},
    ]);
    // 接听电话
    hook('android.telephony.PhoneStateListener', [
        {'methodName': 'onCallStateChanged', 'action': '接听电话', 'messages': '接听电话'},
    ]);
    // 发送短信
    hook('android.telephony.SmsManager', [
        {'methodName': 'sendTextMessage', 'action': '发送短信', 'messages': '发送短信'},
    ]);
    // 接收短信
    hook('android.telephony.SmsReceiver', [
        {'methodName': 'onReceive', 'action': '接收短信', 'messages': '接收短信'},
    ]);
    // 读取短信、彩信
    hook('android.provider.Telephony$Sms', [
        {'methodName': 'query', 'action': '读取短信', 'messages': '读取短信'},
    ]);
    // 读取外置存储器
    hook('android.os.Environment', [
        {'methodName': 'getExternalStorageDirectory', 'action': '读取外置存储器', 'messages': '读取外置存储器'},
    ]);
    // 写入外置存储器
    hook('android.os.Environment', [
        {'methodName': 'getExternalStorageDirectory', 'action': '写入外置存储器', 'messages': '写入外置存储器'},
    ]);
    // 获取传感器数据，如心率传感器数据
    hook('android.hardware.SensorManager', [
        {'methodName': 'registerListener', 'action': '获取传感器数据', 'messages': '获取传感器数据'},
    ]);
    // 读写存储卡权限/所有文件权限(安卓11以上)
    hook('android.os.StorageManager', [
        {'methodName': 'openDirectory', 'action': '读写存储卡权限', 'messages': '读写存储卡权限'},
    ]);
    // 网络权限
    hook('android.net.ConnectivityManager', [
        {'methodName': 'getActiveNetworkInfo', 'action': '网络权限', 'messages': '网络权限'},
    ]);
    // 蓝牙权限
    hook('android.bluetooth.BluetoothAdapter', [
        {'methodName': 'getPairedDevices', 'action': '蓝牙权限', 'messages': '蓝牙权限'},
    ]);
    // 安卓12-蓝牙权限
    hook('android.bluetooth.BluetoothDevice', [
        {'methodName': 'createBond', 'action': '安卓12-蓝牙权限', 'messages': '安卓12-蓝牙权限'},
    ]);
    // 接收彩信
    hook('android.provider.Telephony$Mms', [
        {'methodName': 'query', 'action': '接收彩信', 'messages': '接收彩信'},
    ]);
    // 接收 WAP 推送信息
    hook('android.provider.Telephony$WapPush', [
        {'methodName': 'query', 'action': '接收 WAP 推送信息', 'messages': '接收 WAP 推送信息'},
    ]);
    // 读取媒体文件中的位置信息
    hook('android.provider.MediaStore$MediaColumns', [
        {'methodName': 'openInputStream', 'action': '读取媒体文件中的位置信息', 'messages': '读取媒体文件中的位置信息'},
    ]);
    // 读取图片
    hook('android.provider.MediaStore$Images$Media', [
        {'methodName': 'query', 'action': '读取图片', 'messages': '读取图片'},
    ]);
    // 读取视频
    hook('android.provider.MediaStore$Video$Media', [
        {'methodName': 'query', 'action': '读取视频', 'messages': '读取视频'},
    ]);
    // 读取音频
    hook('android.provider.MediaStore$Audio$Media', [
        {'methodName': 'query', 'action': '读取音频', 'messages': '读取音频'},
    ]);
    // 检测用户动作（例如步行，骑车或坐车)
    hook('android.hardware.Sensor', [
        {'methodName': 'registerListener', 'action': '检测用户动作', 'messages': '检测用户动作'},
    ]);
    // 读写存储卡权限/所有文件权限(安卓11以下)
    hook('android.os.Environment', [
        {
            'methodName': 'getExternalStorageState',
            'action': '读写存储卡权限/所有文件权限(安卓11以下)',
            'messages': '读写存储卡权限/所有文件权限(安卓11以下)'
        },
    ]);
    // 安装包下载权限(提供应用内自升级功能)
    hook('android.content.pm.PackageManager', [
        {'methodName': 'installPackage', 'action': '安装包下载权限', 'messages': '安装包下载权限'},
    ]);
    // 获取系统应用列表权限
    hook('android.content.pm.PackageManager', [
        {'methodName': 'getInstalledPackages', 'action': '获取系统应用列表权限', 'messages': '获取系统应用列表权限'},
    ]);
    // 网络权限
    hook('android.net.ConnectivityManager', [
        {'methodName': 'getActiveNetworkInfo', 'action': '网络权限INTERNET', 'messages': '网络权限INTERNET'},
        {'methodName': 'getNetworkInfo', 'action': '网络权限ACCESS_NETWORK_STATE', 'messages': '网络权限ACCESS_NETWORK_STATE'},
        {'methodName': 'getWifiState', 'action': '网络权限ACCESS_WIFI_STATE', 'messages': '网络权限ACCESS_WIFI_STATE'},
    ]);
    // 运行时权限，需要动态授权
    hook('android.app.NotificationManager', [
        {'methodName': 'notify', 'action': '运行时权限，需要动态授权', 'messages': '运行时权限，需要动态授权'},
    ]);
    // 安卓，悬浮窗权限动态请求
    hook('android.view.WindowManager', [
        {'methodName': 'addView', 'action': '安卓，悬浮窗权限动态请求', 'messages': '安卓，悬浮窗权限动态请求'},
    ]);
    // 蓝牙权限
    hook('android.bluetooth.BluetoothAdapter', [
        {'methodName': 'getName', 'action': '蓝牙权限BLUETOOTH', 'messages': '蓝牙权限BLUETOOTH'},
    ]);
    // 安卓12-蓝牙权限
    hook('android.bluetooth.BluetoothDevice', [
        {'methodName': 'connect', 'action': '安卓12-蓝牙权限BLUETOOTH_CONNECT', 'messages': '安卓12-蓝牙权限BLUETOOTH_CONNECT'},
    ]);
    // 是否调用getDeviceId()获取了imei
    hook('android.telephony.TelephonyManager', [
        {'methodName': 'getDeviceId', 'action': '调用getDeviceId()获取了imei', 'messages': '调用getDeviceId()获取了imei'},
    ]);
    // 是否调用getSubscriberId获取了imsi
    hook('android.telephony.TelephonyManager', [
        {'methodName': 'getSubscriberId', 'action': '调用getSubscriberId获取了imsi', 'messages': '调用getSubscriberId获取了imsi'},
    ]);
    // 是否调用getMacAddress()获取了mac地址
    hook('android.net.wifi.WifiManager', [
        {'methodName': 'getMacAddress', 'action': '调用getMacAddress()获取了mac地址', 'messages': '调用getMacAddress()获取了mac地址'},
    ]);
    // 是否调用getHardwareAddress()获取了mac地址
    hook('java.net.NetworkInterface', [
        {'methodName': 'getHardwareAddress', 'action': '调用getHardwareAddress()获取了mac地址', 'messages': '调用getHardwareAddress()获取了mac地址'},
    ]);
    // 是否调用Settings.Secure.getString获取了android_id
    hook('android.provider.Settings$Secure', [
        {'methodName': 'getString', 'action': '调用Settings.Secure.getString获取了android_id', 'messages': '调用Settings.Secure.getString获取了android_id'},
    ]);
    // 是否调用getLastKnownLocation获取了位置信息
    hook('android.location.LocationManager', [
        {'methodName': 'getLastKnownLocation', 'action': '调用getLastKnownLocation获取了位置信息', 'messages': '调用getLastKnownLocation获取了位置信息'},
    ]);
    // 是否调用getInstalledPackages获取了软件安装列表
    hook('android.content.pm.PackageManager', [
        {
            'methodName': 'getInstalledPackages',
            'action': '调用getInstalledPackages获取了软件安装列表',
            'messages': '调用getInstalledPackages获取了软件安装列表'
        },
    ]);
    // 是否调用queryIntentActivities获取了其他app组件信息
    hook('android.content.pm.PackageManager', [
        {
            'methodName': 'queryIntentActivities',
            'action': '调用queryIntentActivities获取了其他app组件信息',
            'messages': '调用queryIntentActivities获取了其他app组件信息'
        },
    ]);
    // 是否调用getPackageInfo获取了应用信息
    hook('android.content.pm.PackageManager', [
        {'methodName': 'getPackageInfo', 'action': '调用getPackageInfo获取了应用信息', 'messages': '调用getPackageInfo获取了应用信息'},
    ]);
    // 是否调用SystemProperties获取设备序列号(ro.serialno)
    hook('android.os.SystemProperties', [
        {'methodName': 'get', 'action': '调用SystemProperties获取设备序列号(ro.serialno)', 'messages': '调用SystemProperties获取设备序列号(ro.serialno)'},
    ]);
    // 是否调用getRunningAppProcesses读取当前运行应用进程
    hook('android.app.ActivityManager', [
        {
            'methodName': 'getRunningAppProcesses',
            'action': '调用getRunningAppProcesses读取当前运行应用进程',
            'messages': '调用getRunningAppProcesses读取当前运行应用进程'
        },
    ]);
    // 是否调用getSimSerialNumber读取了SIM卡ICCID
    hook('android.telephony.TelephonyManager', [
        {'methodName': 'getSimSerialNumber', 'action': '调用getSimSerialNumber读取了SIM卡ICCID', 'messages': '调用getSimSerialNumber读取了SIM卡ICCID'},
    ]);
    // 是否调用getSimState读取了SIM卡
    hook('android.telephony.TelephonyManager', [
        {'methodName': 'getSimState', 'action': '调用getSimState读取了SIM卡', 'messages': '调用getSimState读取了SIM卡'},
    ]);
    // 是否调用getSSID获取SSID
    hook('android.net.wifi.WifiInfo', [
        {'methodName': 'getSSID', 'action': '调用getSSID获取SSID', 'messages': '调用getSSID获取SSID'},
    ]);
    // 是否调用getBSSID获取wifiBSSID
    hook('android.net.wifi.WifiInfo', [
        {'methodName': 'getBSSID', 'action': '调用getBSSID获取wifiBSSID', 'messages': '调用getBSSID获取wifiBSSID'},
    ]);
    // 麦克风权限弹窗
    hook('android.content.Context', [
        {'methodName': 'checkSelfPermission', 'action': '麦克风权限弹窗', 'messages': '麦克风权限弹窗'},
    ]);
    // 存储权限弹窗
    hook('android.content.Context', [
        {'methodName': 'checkSelfPermission', 'action': '存储权限弹窗', 'messages': '存储权限弹窗'},
    ]);
    // 普通权限-读取和写入“properties”表在checkin数据库中
    hook('android.content.Context', [
        {
            'methodName': 'checkSelfPermission',
            'action': '普通权限-读取和写入“properties”表在checkin数据库中',
            'messages': '读取和写入“properties”表在checkin数据库中'
        },
    ]);
    // 普通权限-访问额外的位置提供命令
    hook('android.location.ILocationManager$Stub', [
        {'methodName': 'asInterface', 'action': '普通权限-访问额外的位置提供命令', 'messages': '访问额外的位置提供命令'},
    ]);
    // 普通权限-获取网络信息状态
    hook('android.net.ConnectivityManager', [
        {'methodName': 'getActiveNetworkInfo', 'action': '普通权限-获取网络信息状态', 'messages': '获取网络信息状态'},
    ]);
    // 普通权限-希望访问通知策略的应用程序的标记许可
    hook('android.app.NotificationManager', [
        {'methodName': 'getNotificationPolicy', 'action': '普通权限-希望访问通知策略的应用程序的标记许可', 'messages': '希望访问通知策略的应用程序的标记许可'},
    ]);
    // 普通权限-获取当前WiFi接入的状态以及WLAN热点的信息
    hook('android.net.wifi.WifiManager', [
        {'methodName': 'getConnectionInfo', 'action': '普通权限-获取当前WiFi接入的状态以及WLAN热点的信息', 'messages': '获取当前WiFi接入的状态以及WLAN热点的信息'},
    ]);
    // 普通权限-通过账户验证方式访问账户管理ACCOUNT_MANAGER相关信息
    hook('android.accounts.AccountManager', [
        {
            'methodName': 'getAccounts',
            'action': '普通权限-通过账户验证方式访问账户管理ACCOUNT_MANAGER相关信息',
            'messages': '通过账户验证方式访问账户管理ACCOUNT_MANAGER相关信息'
        },
    ]);
    // 普通权限-更新手机电池统计信息
    hook('android.os.BatteryManager', [
        {'methodName': 'getBatteryLevel', 'action': '普通权限-更新手机电池统计信息', 'messages': '更新手机电池统计信息'},
    ]);
    // 普通权限-请求accessibilityservice服务
    hook('android.accessibilityservice.AccessibilityService', [
        {'methodName': 'onAccessibilityEvent', 'action': '普通权限-请求accessibilityservice服务', 'messages': '请求accessibilityservice服务'},
    ]);
    // 普通权限-告诉appWidget服务需要访问小插件的数据库
    hook('android.appwidget.AppWidgetManager', [
        {'methodName': 'getAppWidgetIds', 'action': '普通权限-告诉appWidget服务需要访问小插件的数据库', 'messages': '告诉appWidget服务需要访问小插件的数据库'},
    ]);
    // 普通权限-绑定到运营商应用程序中的服务
    hook('android.telephony.CarrierMessagingService', [
        {'methodName': 'onCreate', 'action': '普通权限-绑定到运营商应用程序中的服务', 'messages': '绑定到运营商应用程序中的服务'},
    ]);
    // 普通权限-请求系统管理员receiver
    hook('android.app.admin.DeviceAdminReceiver', [
        {'methodName': 'onReceive', 'action': '普通权限-请求系统管理员receiver', 'messages': '请求系统管理员receiver'},
    ]);
    // 普通权限-由一个DreamService要求的服务
    hook('android.service.dream.DreamService', [
        {'methodName': 'onCreate', 'action': '普通权限-由一个DreamService要求的服务', 'messages': '由一个DreamService要求的服务'},
    ]);
    // 普通权限-请求MidiDeviceService服务
    hook('android.media.midi.MidiDeviceService', [
        {'methodName': 'onCreate', 'action': '普通权限-请求MidiDeviceService服务', 'messages': '请求MidiDeviceService服务'},
    ]);
    // 普通权限-请求InputMethodService服务
    hook('android.inputmethodservice.InputMethodService', [
        {'methodName': 'onCreate', 'action': '普通权限-请求InputMethodService服务', 'messages': '请求InputMethodService服务'},
    ]);
    // 普通权限-由一MidiDeviceService要求的服务
    hook('android.media.midi.MidiDeviceService', [
        {'methodName': 'onCreate', 'action': '普通权限-由一MidiDeviceService要求的服务', 'messages': '由一MidiDeviceService要求的服务'},
    ]);
    // 普通权限-由HostApduServiceOffHostApduService要求的服务
    hook('android.nfc.cardemulation.HostApduService', [
        {'methodName': 'onCreate', 'action': '普通权限-由HostApduServiceOffHostApduService要求的服务', 'messages': '由HostApduServiceOffHostApduService要求的服务'},
    ]);
    // 普通权限-由notificationlistenerservice要求的服务
    hook('android.service.notification.NotificationListenerService', [
        {'methodName': 'onCreate', 'action': '普通权限-由notificationlistenerservice要求的服务', 'messages': '由notificationlistenerservice要求的服务'},
    ]);
    // 普通权限-由printservice要求的服务
    hook('android.printservice.PrintService', [
        {'methodName': 'onCreate', 'action': '普通权限-由printservice要求的服务', 'messages': '由printservice要求的服务'},
    ]);
    // 普通权限-通过RemoteViewsService服务请求
    hook('android.inputmethodservice.RemoteViewsFactory', [
        {'methodName': 'onCreate', 'action': '普通权限-通过RemoteViewsService服务请求', 'messages': '通过RemoteViewsService服务请求'},
    ]);
    // 普通权限-由ConnectionService要求的服务
    hook('android.telecom.ConnectionService', [
        {'methodName': 'onCreate', 'action': '普通权限-由ConnectionService要求的服务', 'messages': '由ConnectionService要求的服务'},
    ]);
    // 普通权限-由textservice要求的服务
    hook('android.service.textservice.TextServicesManager', [
        {'methodName': 'getCurrentSpellChecker', 'action': '普通权限-由textservice要求的服务', 'messages': '由textservice要求的服务'},
    ]);
    // 普通权限-由TvInputService要求的服务
    hook('android.media.tv.TvInputService', [
        {'methodName': 'onCreate', 'action': '普通权限-由TvInputService要求的服务', 'messages': '由TvInputService要求的服务'},
    ]);
    // 普通权限-由VoiceInteractionService要求的服务
    hook('android.service.voice.VoiceInteractionService', [
        {'methodName': 'onCreate', 'action': '普通权限-由VoiceInteractionService要求的服务', 'messages': '由VoiceInteractionService要求的服务'},
    ]);
    // 普通权限-通过VpnService服务请求
    hook('android.net.VpnService', [
        {'methodName': 'protect', 'action': '普通权限-通过VpnService服务请求', 'messages': '通过VpnService服务请求'},
    ]);
    // 普通权限-通过WallpaperService服务请求
    hook('android.service.wallpaper.WallpaperService', [
        {'methodName': 'onCreate', 'action': '普通权限-通过WallpaperService服务请求', 'messages': '通过WallpaperService服务请求'},
    ]);
    // 普通权限-连接配对过的蓝牙设备
    hook('android.bluetooth.BluetoothAdapter', [
        {'methodName': 'getBondedDevices', 'action': '普通权限-连接配对过的蓝牙设备', 'messages': '连接配对过的蓝牙设备'},
    ]);
    // 普通权限-发现和配对新的蓝牙设备
    hook('android.bluetooth.BluetoothAdapter', [
        {'methodName': 'startDiscovery', 'action': '普通权限-发现和配对新的蓝牙设备', 'messages': '发现和配对新的蓝牙设备'},
    ]);
    // 普通权限-配对蓝牙设备，无需用户交互
    hook('android.bluetooth.BluetoothDevice', [
        {'methodName': 'createBond', 'action': '普通权限-配对蓝牙设备，无需用户交互', 'messages': '配对蓝牙设备，无需用户交互'},
    ]);
    // 普通权限-广播一个提示消息在一个应用程序包已经移除后
    hook('android.content.Context', [
        {'methodName': 'sendBroadcast', 'action': '普通权限-广播一个提示消息在一个应用程序包已经移除后', 'messages': '广播一个提示消息在一个应用程序包已经移除后'},
    ]);
    // 普通权限-当收到短信时触发广播
    hook('android.content.Context', [
        {'methodName': 'sendBroadcast', 'action': '普通权限-当收到短信时触发广播', 'messages': '当收到短信时触发广播'},
    ]);
    // 普通权限-收到广播后快速收到下一个广播
    hook('android.content.Context', [
        {'methodName': 'sendStickyBroadcast', 'action': '普通权限-收到广播后快速收到下一个广播', 'messages': '收到广播后快速收到下一个广播'},
    ]);
    // 普通权限-WAP PUSH服务收到后触发广播
    hook('android.content.Context', [
        {'methodName': 'sendStickyBroadcast', 'action': '普通权限-WAP PUSH服务收到后触发广播', 'messages': 'WAP PUSH服务收到后触发广播'},
    ]);
    // 普通权限-拨打电话，替换系统的拨号器界面
    hook('android.content.Intent', [
        {'methodName': 'ACTION_CALL_BUTTON', 'action': '普通权限-拨打电话，替换系统的拨号器界面', 'messages': '拨打电话，替换系统的拨号器界面'},
    ]);
    // 普通权限-捕获音频输出
    hook('android.media.AudioRecord', [
        {'methodName': 'startRecording', 'action': '普通权限-捕获音频输出', 'messages': '捕获音频输出'},
    ]);
    // 普通权限-捕获视频输出
    hook('android.media.MediaRecorder', [
        {'methodName': 'start', 'action': '普通权限-捕获视频输出', 'messages': '捕获视频输出'},
    ]);
    // 普通权限-改变组件是否启用状态
    hook('android.content.pm.PackageManager', [
        {'methodName': 'setComponentEnabledSetting', 'action': '普通权限-改变组件是否启用状态', 'messages': '改变组件是否启用状态'},
    ]);
    // 普通权限-改变配置信息
    hook('android.content.res.Configuration', [
        {'methodName': 'updateFrom', 'action': '普通权限-改变配置信息', 'messages': '改变配置信息'},
    ]);
    // 普通权限-改变网络状态，如是否联网
    hook('android.net.ConnectivityManager', [
        {'methodName': 'setNetworkPreference', 'action': '普通权限-改变网络状态，如是否联网', 'messages': '改变网络状态，如是否联网'},
    ]);
    // 普通权限-改变WiFi多播状态
    hook('android.net.wifi.WifiManager', [
        {'methodName': 'setWifiMulticastEnabled', 'action': '普通权限-改变WiFi多播状态', 'messages': '改变WiFi多播状态'},
    ]);
    // 普通权限-改变WiFi状态
    hook('android.net.wifi.WifiManager', [
        {'methodName': 'setWifiEnabled', 'action': '普通权限-改变WiFi状态', 'messages': '改变WiFi状态'},
    ]);
    // 普通权限-清除应用缓存
    hook('android.content.pm.PackageManager', [
        {'methodName': 'clearApplicationCache', 'action': '普通权限-清除应用缓存', 'messages': '清除应用缓存'},
    ]);
    // 普通权限-获得移动网络定位信息
    hook('android.telephony.TelephonyManager', [
        {'methodName': 'getCellLocation', 'action': '普通权限-获得移动网络定位信息', 'messages': '获得移动网络定位信息'},
    ]);
    // 普通权限-删除缓存文件
    hook('java.io.File', [
        {'methodName': 'delete', 'action': '普通权限-删除缓存文件', 'messages': '删除缓存文件'},
    ]);
    // 普通权限-删除应用
    hook('android.content.pm.PackageManager', [
        {'methodName': 'deletePackage', 'action': '普通权限-删除应用', 'messages': '删除应用'},
    ]);
    // 普通权限-结束后台进程
    hook('android.app.ActivityManager', [
        {'methodName': 'killBackgroundProcesses', 'action': '普通权限-结束后台进程', 'messages': '结束后台进程'},
    ]);
    // 普通权限-使用定位功能的硬件
    hook('android.hardware.location.GeofenceHardwareService', [
        {'methodName': 'addCircularFence', 'action': '普通权限-使用定位功能的硬件', 'messages': '使用定位功能的硬件'},
    ]);
    // 普通权限-管理文档访问
    hook('android.provider.DocumentsContract', [
        {'methodName': 'buildDocumentUriUsingTree', 'action': '普通权限-管理文档访问', 'messages': '管理文档访问'},
    ]);
    // 普通权限-执行软格式化，删除系统配置信息
    hook('android.os.RecoverySystem', [
        {'methodName': 'rebootWipeUserData', 'action': '普通权限-执行软格式化，删除系统配置信息', 'messages': '执行软格式化，删除系统配置信息'},
    ]);
    // 普通权限-控制播放和内容
    hook('android.media.session.MediaSessionManager', [
        {'methodName': 'getActiveSessions', 'action': '普通权限-控制播放和内容', 'messages': '控制播放和内容'},
    ]);
    // 普通权限-修改声音设置信息
    hook('android.media.AudioManager', [
        {'methodName': 'setStreamVolume', 'action': '普通权限-修改声音设置信息', 'messages': '修改声音设置信息'},
    ]);
    // 普通权限-修改电话状态
    hook('android.telephony.TelephonyManager', [
        {'methodName': 'listen', 'action': '普通权限-修改电话状态', 'messages': '修改电话状态'},
    ]);
    // 普通权限-格式化可移动文件系统
    hook('android.os.storage.StorageManager', [
        {'methodName': 'mount', 'action': '普通权限-格式化可移动文件系统', 'messages': '格式化可移动文件系统'},
    ]);
    // 普通权限-挂载、反挂载外部文件系统
    hook('android.os.storage.StorageManager', [
        {'methodName': 'mount', 'action': '普通权限-挂载外部文件系统', 'messages': '挂载外部文件系统'},
        {'methodName': 'unmount', 'action': '普通权限-反挂载外部文件系统', 'messages': '反挂载外部文件系统'},
    ]);
    // 普通权限-执行NFC近距离通讯操作
    hook('android.nfc.NfcAdapter', [
        {'methodName': 'enableReaderMode', 'action': '普通权限-执行NFC近距离通讯操作', 'messages': '执行NFC近距离通讯操作'},
    ]);
    // 普通权限-设置他的activities显示
    hook('android.app.usage.UsageStatsManager', [
        {'methodName': 'queryUsageStats', 'action': '普通权限-设置他的activities显示', 'messages': '设置他的activities显示'},
    ]);
    // 普通权限-创建一个永久的Activity
    hook('android.app.Activity', [
        {'methodName': 'moveTaskToBack', 'action': '普通权限-创建一个永久的Activity', 'messages': '创建一个永久的Activity'},
    ]);
    // 普通权限-读取帧缓存
    hook('android.view.Surface', [
        {'methodName': 'lockCanvas', 'action': '普通权限-读取帧缓存', 'messages': '读取帧缓存'},
    ]);
    // 普通权限-读取当前键的输入状态
    hook('android.view.KeyEvent', [
        {'methodName': 'dispatch', 'action': '普通权限-读取当前键的输入状态', 'messages': '读取当前键的输入状态'},
    ]);
    // 普通权限-读取系统底层日志
    hook('android.util.Log', [
        {'methodName': 'd', 'action': '普通权限-读取系统底层日志', 'messages': '读取系统底层日志'},
    ]);
    // 普通权限-读取同步设置
    hook('android.content.ContentResolver', [
        {'methodName': 'getIsSyncable', 'action':  '普通权限-读取同步设置', 'messages': '读取同步设置'},
    ]);
    // 普通权限-读取同步状态
    hook('android.content.ContentResolver', [
        {'methodName': 'getSyncState', 'action': '普通权限-读取同步状态', 'messages': '读取同步状态'},
    ]);
    // 普通权限-读取语音邮件
    hook('android.telephony.SmsManager', [
        {'methodName': 'getVoiceMailAlphaTag', 'action': '普通权限-读取语音邮件', 'messages': '读取语音邮件'},
    ]);
    // 普通权限-重新启动设备
    hook('android.os.PowerManager', [
        {'methodName': 'reboot', 'action': '普通权限-重新启动设备', 'messages': '重新启动设备'},
    ]);
    // 普通权限-开机自动运行
    hook('android.content.BroadcastReceiver', [
        {'methodName': 'onReceive', 'action': '普通权限-开机自动运行', 'messages': '开机自动运行'},
    ]);
    // 普通权限-重新排序系统Z轴运行中的任务
    hook('android.app.ActivityManager', [
        {'methodName': 'moveTaskToFront', 'action': '普通权限-重新排序系统Z轴运行中的任务', 'messages': '重新排序系统Z轴运行中的任务'},
    ]);
    // 普通权限-请求忽略电池优化
    hook('android.os.PowerManager', [
        {'methodName': 'requestIgnoreBatteryOptimizations', 'action': '普通权限-请求忽略电池优化', 'messages': '请求忽略电池优化'},
    ]);
    // 普通权限-请求安装包
    hook('android.content.pm.PackageManager', [
        {'methodName': 'installPackage', 'action': '普通权限-请求安装包', 'messages': '请求安装包'},
    ]);
    // 普通权限-结束任务
    hook('android.app.ActivityManager', [
        {'methodName': 'removeTask', 'action': '普通权限-请求安装包', 'messages': '结束任务'},
    ]);
    // 普通权限-即时的短信息回复
    hook('android.telephony.SmsManager', [
        {'methodName': 'injectSmsPdu', 'action': '普通权限-即时的短信息回复', 'messages': '即时的短信息回复'},
    ]);
    // 普通权限-设置闹铃提醒
    hook('android.app.AlarmManager', [
        {'methodName': 'set', 'action': '普通权限-设置闹铃提醒', 'messages': '设置闹铃提醒'},
    ]);
    // 普通权限-程序在后台是否总是退出
    hook('android.app.ActivityManager', [
        {'methodName': 'setAlwaysFinish', 'action': '普通权限-程序在后台是否总是退出', 'messages': '程序在后台是否总是退出'},
    ]);
    // 普通权限-设置全局动画缩放
    hook('android.view.animation.Animation', [
        {'methodName': 'setAnimationScale', 'action': '普通权限-设置全局动画缩放', 'messages': '设置全局动画缩放'},
    ]);
    // 普通权限-设置调试程序
    hook('android.os.Debug', [
        {'methodName': 'waitForDebugger', 'action': '普通权限-设置调试程序', 'messages': '设置调试程序'},
    ]);
    // 普通权限-设置应用的参数
    hook('android.content.pm.PackageManager', [
        {'methodName': 'setComponentEnabledSetting', 'action': '普通权限-设置应用的参数', 'messages': '设置应用的参数'},
    ]);
    // 普通权限-设置最大的进程数量的限制
    hook('android.app.ActivityManager', [
        {'methodName': 'setProcessLimit', 'action': '普通权限-设置最大的进程数量的限制', 'messages': '设置最大的进程数量的限制'},
    ]);
    // 普通权限-设置系统时间
    hook('android.content.Context', [
        {'methodName': 'setTime', 'action': '普通权限-设置系统时间', 'messages': '设置系统时间'},
    ]);
    // 普通权限-设置系统时区
    hook('java.util.TimeZone', [
        {'methodName': 'setDefault', 'action': '普通权限-设置系统时区', 'messages': '设置系统时区'},
    ]);
    // 普通权限-设置桌面壁纸
    hook('android.app.WallpaperManager', [
        {'methodName': 'setBitmap', 'action': '普通权限-设置桌面壁纸', 'messages': '设置桌面壁纸'},
    ]);
    // 普通权限-设置壁纸建议
    hook('android.app.WallpaperManager', [
        {'methodName': 'setDimensionHints', 'action': '普通权限-设置壁纸建议', 'messages': '设置壁纸建议'},
    ]);
    // 普通权限-发送一个永久的进程信号
    hook('android.os.Process', [
        {'methodName': 'killProcess', 'action': '普通权限-发送一个永久的进程信号', 'messages': '发送一个永久的进程信号'},
    ]);
    // 普通权限-打开、关闭、禁用状态栏
    hook('android.view.WindowManager$LayoutParams', [
        {'methodName': 'setFlags', 'action': '普通权限-打开、关闭、禁用状态栏', 'messages': '打开、关闭、禁用状态栏'},
    ]);
    // 普通权限-显示系统窗口
    hook('android.view.WindowManager', [
        {'methodName': 'addView', 'action': '普通权限-显示系统窗口', 'messages': '显示系统窗口'},
    ]);
    // 普通权限-使用设备的红外发射器
    hook('android.hardware.Sensor', [
        {'methodName': 'getMaxRange', 'action': '普通权限-使用设备的红外发射器', 'messages': '使用设备的红外发射器'},
    ]);
    // 普通权限-删除快捷方式
    hook('android.content.pm.LauncherApps', [
        {'methodName': 'removePin', 'action': '普通权限-删除快捷方式', 'messages': '删除快捷方式'},
    ]);
    // 普通权限-更新设备状态
    hook('android.os.Build', [
        {'methodName': 'VERSION', 'action': '普通权限-更新设备状态', 'messages': '更新设备状态'},
    ]);
    // 普通权限-使用指纹硬件
    hook('android.hardware.fingerprint.FingerprintManager', [
        {'methodName': 'authenticate', 'action': '普通权限-使用指纹硬件', 'messages': '使用指纹硬件'},
    ]);
    // 普通权限-允许程序振动
    hook('android.os.Vibrator', [
        {'methodName': 'vibrate', 'action': '普通权限-允许程序振动', 'messages': '允许程序振动'},
    ]);
    // 普通权限-允许程序在手机屏幕关闭后后台进程仍然运行
    hook('android.app.KeyguardManager', [
        {
            'methodName': 'requestDismissKeyguard',
            'action': '普通权限-允许程序在手机屏幕关闭后后台进程仍然运行',
            'messages': '允许程序在手机屏幕关闭后后台进程仍然运行'
        },
    ]);
    // 普通权限-允许程序写入网络GPRS接入点设置
    hook('android.net.ConnectivityManager', [
        {'methodName': 'setGlobalProxy', 'action': '普通权限-允许程序写入网络GPRS接入点设置', 'messages': '允许程序写入网络GPRS接入点设置'},
    ]);
    // 普通权限-允许程序修改Google服务地图
    hook('android.location.LocationManager', [
        {'methodName': 'requestLocationUpdates', 'action': '普通权限-允许程序修改Google服务地图', 'messages': '允许程序修改Google服务地图'},
    ]);
    // 普通权限-允许应用程序读取或写入安全系统设置
    hook('android.provider.Settings$Secure', [
        {'methodName': 'putString', 'action': '普通权限-允许应用程序读取或写入安全系统设置', 'messages': '允许应用程序读取或写入安全系统设置'},
    ]);
    // 普通权限-允许程序读取或写入系统设置
    hook('android.provider.Settings$System', [
        {'methodName': 'putString', 'action': '普通权限-允许程序读取或写入系统设置', 'messages': '允许程序读取或写入系统设置'},
    ]);
    // 普通权限-允许程序写入同步设置
    hook('android.content.ContentResolver', [
        {'methodName': 'addPeriodicSync', 'action': '普通权限-允许程序写入同步设置', 'messages': '允许程序写入同步设置'},
    ]);
    // 普通权限-允许应用程序修改和删除系统中的现有的语音邮件，只有系统才能使用
    hook('android.telephony.SmsManager', [
        {
            'methodName': 'deleteMessageFromIcc',
            'action': '普通权限-允许应用程序修改和删除系统中的现有的语音邮件，只有系统才能使用',
            'messages': '允许应用程序修改和删除系统中的现有的语音邮件，只有系统才能使用'
        },
    ]);
}
function useModule(moduleList) {
    var _module = {
        'permission': [checkRequestPermission],
        'phone': [getPhoneState],
        'system': [getSystemData],
        'app': [getPackageManager],
        'location': [getGSP],
        'network': [getNetwork],
        'camera': [getCamera],
        'bluetooth': [getBluetooth],
        'file': [getFileMessage],
        'media': [getMedia],
        'sensor': [getSensor],
        'custom': [customHook]
    };
    var _m = Object.keys(_module);
    var tmp_m = []
    if (moduleList['type'] !== 'all') {
        var input_module_data = moduleList['data'].split(',');
        for (i = 0; i < input_module_data.length; i++) {
            if (_m.indexOf(input_module_data[i]) === -1) {
                send({'type': 'noFoundModule', 'data': input_module_data[i]})
            } else {
                tmp_m.push(input_module_data[i])
            }
        }
    }
    switch (moduleList['type']) {
        case 'use':
            _m = tmp_m;
            break;
        case 'nouse':
            for (var i = 0; i < input_module_data.length; i++) {
                for (var j = 0; j < _m.length; j++) {
                    if (_m[j] == input_module_data[i]) {
                        _m.splice(j, 1);
                        j--;
                    }
                }
            }
            break;
    }
    send({'type': 'loadModule', 'data': _m})
    if (_m.length !== 0) {
        for (i = 0; i < _m.length; i++) {
            for (j = 0; j < _module[_m[i]].length; j++) {
                _module[_m[i]][j]();
            }
        }
    }
}

function main() {
    try {
        Java.perform(function () {
            console.log('[*] ' + get_format_time() + ' 隐私合规检测敏感接口开始监控...');
            send({"type": "isHook"})
            console.log('[*] ' + get_format_time() + ' 检测到安卓版本：' + Java.androidVersion);
            var moduleList;
            recv(function (received_json_object) {
                moduleList = received_json_object.use_module;
            }).wait();
            useModule(moduleList);
        });
    } catch (e) {
        console.log(e)
    }
}

// 绕过TracerPid检测 默认关闭，有必要时再自行打开
// setImmediate(ByPassTracerPid);

//在spawn模式下，hook系统API时如javax.crypto.Cipher建议使用setImmediate立即执行，不需要延时
//在spawn模式下，hook应用自己的函数或含壳时，建议使用setTimeout并给出适当的延时(500~5000)

// main();
//setImmediate(main)
// setTimeout(main, 3000);
