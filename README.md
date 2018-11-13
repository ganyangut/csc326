# csc326

a search engine project

note: all shell scripts are written in bash syntax
If you are in a csh, please run bash first.

## Lab 3

### Bonus

We implemented the multiprocess crawler and page ranker. You can set number_processes in lab3_group_20/backend/run_backend_test.py
We tested it with these three urls in lab3_group_20/backend/urls.txt:
    http://www.eecg.toronto.edu/
    https://www.utoronto.ca/
    http://www.amazon.ca/
It would take 112 seconds to finish the crawl and rank process in single process (almost equal to the sum of time used by each url). 
If we use three proceses, the time reduced to 62 seconds (almost the same as the time for the most time-consuming url https://www.utoronto.ca/)
The detailed results is in lab3_group_20/backend/multi_processing_time_improvement.txt

### Frontend

* How to run our search engine:
  * ~/lab3_group_20$ python frontend.py

* How to test the web page
  * in a web browser, enter:
    * localhost:8081

### Backend

* How to run backend:
  * ~/lab3_group_20$ cd backend
  * ~/lab3_group_20/backend$ python run_backend_test.py

### AWS related

* How to access the web page currently running on our aws instance
  * in a web browser, enter:
    * http://52.87.155.235/

### Benchmark

* Frontend benchmark setup
  * send concurrent identical requests with keywords “helloworld foo bar” to our web page with different concurrency level in 2 seconds
  * ~/lab3_group_20$ ab -c 10 -t 2 http://52.87.155.235/?keywords=helloworld+foo+bar
  * ~/lab3_group_20$ ab -c 50 -t 2 http://52.87.155.235/?keywords=helloworld+foo+bar
  * ~/lab3_group_20$ ab -c 200 -t 2 http://52.87.155.235/?keywords=helloworld+foo+bar
  * ~/lab3_group_20$ ab -c 500 -t 2 http://52.87.155.235/?keywords=helloworld+foo+bar

* Test results

  Maximum number of connections that can be handled by the server before any connection drops
      500 (tested, may be more)

  Maximum number of requests per second (RPS) that can be sustained by the server when operating with maximum number of connections
      125.24 [#/sec]

  Average and 99 percentile of response time or latency per request 
      50%    261 ms
      99%   1262 ms

  Utilization of CPU, memory, disk IO, and network when max performance is sustained
      Max CPU usage           21%
      Max memory usage        less than 32.0M
      Max disk I/O            387k/40k
      Max network read/write  66k/329k

  * Compared to Lab2, the response time, CPU usage, and disk I/O increased.
    The reason is that the frontend is reading the database on disk, and this process consumes CPU and costs time.

## Lab 2

### Local version (with Google Login)

* install necessary packages (including packages for AWS and benchmark):
  * ~/lab2_group_20$ source setup.sh

* add awscli path to your $PATH:
  * in a python terminal or file
    * import awecli
    * print awecli.\_\_path\_\_
  * <your_local_awecli_path> should be printed
  * use your favorite editor to edit ~/.bashrc
    * add a line: export PATH=$PATH:<your_local_awecli_path>

* run aws configure in terminal
  * fill in the appropriate values
  * use us-east-1 as the location
  * the format can be left as the default None

* How to run our search engine:
  * ~/lab2_group_20$ python frontend.py

* How to test the web page
  * in a web browser, enter:
    * localhost:8081

* Troubleshoot
  * we already tested the web application, but in case there's anything doesn't work, you can try: 
    * remove data folder
    * clear cache in a web browser

### AWS related

* How to test the web page currently running on our aws instance
  * in a web browser, enter:
    * http://54.196.143.244/

* How to deploy a instance and run our search engine on aws:
  * source the shell script
    * ~/lab2_group_20$ source lab2_run_page_on_aws.sh
    * <public_ip_address> should be printed out on the terminal
    * <public_ip_address> is also avaliable in lab2_group_20/instance_deployment/public_ip.txt
  * close the treminal
  * test the web page
    * in a web browser, enter:
      * <public_ip_address>:80

* How to check the information of all instances:
  * ~/lab2_group_20/instance_deployment$ python check_all_instances.py

* How to stop all instances:
  * ~/lab2_group_20/instance_deployment$ python stop_all_instances.py

* How to terminate all instances:
  * ~/lab2_group_20/instance_deployment$ python terminate_all_instances.py

### Benchmark

* How to monitor resource utilization:
  * ~/lab2_group_20$ source monitor_aws_resource_utilization.sh

* How to evaluate the performance of the web application on AWS:
  * ab -n <numberof request to perform>  -c <number of concurrent connection> http://hostname/path
  * eg. this command sends 50 concurrent identical requests with keywords “helloworld foo bar” to our web page with a total of 1000 requests
    * ~/lab2_group_20$ ab -n 1000 -c 50 http://54.196.143.244/?keywords=helloworld+foo+bar

* Preliminary test results is in RESULT.txt

## Lab 1

* How to run front end:
  * in terminal, under lab1_group_20:
    * ~/lab1_group_20$ python frontend.py
  * in browser:
    * localhost:8081

* How to run tests for backend:
  * in terminal, under lab1_group_20/backend:
    * ~/lab1_group_20/backend$ python test.py

* How to run crawler:
  * in terminal, under lab1_group_20/backend:
    * ~/lab1_group_20/backend$ python crawler.py

* database framework:
  * document index # that keeps information about each document
    * dict {document id: document}
    * document
      * list [url, depth, title, short_description, words, links]
      * words
        * list [word]
        * word
          * tuple (word id, font size)
      * links
        * dict {to_doc_id: number of links}
  * lexicon # keeps a list of words
    * dict {word id: word string}
  * inverted index # that returns a list of document Ids given a word id
    * dict {word id: set([document id0, document id1, document id2, ..., ])}
  * resolved inverted index # that returns a list of document urls given a word string
    * dict {word string: set([document url0, document url1, document url2, ..., ])}
  * _word_id_cache
    * dict {word string: word id}
  * _doc_id_cache
    * dict {document url: document id}

* backup test urls:
  * http://www.eecg.toronto.edu/~csc467/
  * http://www.petergoodman.me/
  * http://dsrg.utoronto.ca/csc467/index.html

http://dsrg.utoronto.ca/csc467/midterm/midterm11.pdf
    
    Traceback (most recent call last):
      File "crawler.py", line 444, in <module>
        bot.crawl(depth=1)
      File "crawler.py", line 384, in crawl
        soup = BeautifulSoup(socket.read())
      File "/usr/lib/python2.7/dist-packages/BeautifulSoup.py", line 1522, in __init__
        BeautifulStoneSoup.__init__(self, *args, **kwargs)
      File "/usr/lib/python2.7/dist-packages/BeautifulSoup.py", line 1147, in __init__
        self._feed(isHTML=isHTML)
      File "/usr/lib/python2.7/dist-packages/BeautifulSoup.py", line 1189, in _feed
        SGMLParser.feed(self, markup)
      File "/usr/lib/python2.7/sgmllib.py", line 104, in feed
        self.goahead(0)
      File "/usr/lib/python2.7/sgmllib.py", line 143, in goahead
        k = self.parse_endtag(i)
      File "/usr/lib/python2.7/sgmllib.py", line 320, in parse_endtag
        self.finish_endtag(tag)
      File "/usr/lib/python2.7/sgmllib.py", line 358, in finish_endtag
        method = getattr(self, 'end_' + tag)
    UnicodeEncodeError: 'ascii' codec can't encode character u'\xed' in position 4: ordinal not in range(128)