vigoss.fang写的一些简单的python脚本

1、hashcollision.py
简单描述：用于应用对敏感操作中签名参数的碰撞，使用用户指定的参数和分隔符（默认可以不提供）进行各种组合和多种算法计算哈希，希望能找到与签名一样的一个结果，从而逆向出应用中签名参数的明文。

		C:\Users\Administrator\Desktop\My scripts>python hashcollision.py -h
		Usage: hashcollision.py -p <params> --hash <hash>

		Options:
		  -h, --help            show this help message and exit
		  -p PARAMS             specify the params to generate hash, separated by
		                        comma
		  --hash=HASH           the target hash to collision
		  --extra=EXTRA         manually specify extra separators, separated by comma
		  --extraonly           tell program to use manually separators only
		  --mode=MODE           specify the running mode        1--fast mode    2--
		                        slow mode(more tests)
		  -v VERBOSE, --verbose=VERBOSE
		                        specify the verbosity level, default is 0

		e.g.
		C:\Users\Administrator\Desktop\My scripts>python hashcollision.py -p a,b,c,d --h
		ash 9c3af0f389fa0a31ceb308a65599c47b4b8fc1b0217cf70602fad58a559aee34 --mode 2
		[!] Collision is about to start, please fasten your seat belts!
		[+] Collision Success!
		[+] sha256(b-c-d) : 9c3af0f389fa0a31ceb308a65599c47b4b8fc1b0217cf70602fad58a559aee34



2、collaborator.py
简单描述：一款用于实现collorator everywhere类似功能的脚本，可以批量向指定域名发送collorator everywhere的类似payload，配合Burpsuite中的colloborator client，期望能实现James Kettle在《Cracking the Lens: Targeting HTTP's Hidder Attack Surface》中类似的效果

		G:\python\bash>python collaborator.py -h
		Usage: collaborator.py [-h] [-d domain] [-f file] -c collboratorserver [-t threads] 
		[-v verbose] [--timeout] -[p port]

		Options:
  		-h, --help            	show this help message and exit
  		-d DOMAIN, --domain=DOMAIN 						
					Domain name to test
  		-f FILE, --file=FILE  File contains domain names
  		-c COLLABORATOR, --collaborator=COLLABORATOR
                        		Collaborator server address
  		-t THREADS, --threads=THREADS
                        		specify threads to run
  		--timeout=TIMEOUT     	specify timeout for HTTP/HTTPS connection, default is
                        10
  		-p PORT, --port=PORT  	specify a port for HTTP/HTTPS connection, default is
                        		80(HTTP) and 443(HTTPS)
  		-v, --verbose         	show verbose messages
