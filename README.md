# Static HTTP server

* Respond to `GET` with status code in `{200,404,403}`
* Respond to `HEAD` with status code in `{200,404,403}`
* Respond to all other request methods with status code `405`
* Directory index file name `index.html`
* Respond to requests for `/<file>.html` with the contents of `DOCUMENT_ROOT/<file>.html`
* Requests for `/<directory>/` should be interpreted as requests for `DOCUMENT_ROOT/<directory>/index.html`
* Respond with the following header fields for all requests:
  * `Server`
  * `Date`
  * `Connection`
* Respond with the following additional header fields for all `200` responses to `GET` and `HEAD` requests:
  * `Content-Length`
  * `Content-Type`
* Respond with correct `Content-Type` for `.html, .css, js, jpg, .jpeg, .png, .gif, .swf`
* Respond to percent-encoding URLs
* Correctly serve a 2GB+ files
* No security vulnerabilities

---------------------------
# Build docker containers

```
docker build -t server -f Dockerfile .
docker run -p 80:80 server
```

```
docker build -t nginx -f nginx.Dockerfile .
docker run -p 90:90 nginx
```

--------------------------
# Functional testing
### `pyhon3 httptest.py`
<details><summary>Ran 24 tests in 42.988s - OK<br>
(click to see all)</summary>
  <code>

    test_directory_index (__main__.HttpServer)
    directory index file exists ... ok
    test_document_root_escaping (__main__.HttpServer)
    document root escaping forbidden ... ok
    test_empty_request (__main__.HttpServer)
    Send empty line ... ok
    test_file_in_nested_folders (__main__.HttpServer)
    file located in nested folders ... ok
    test_file_not_found (__main__.HttpServer)
    absent file returns 404 ... ok
    test_file_type_css (__main__.HttpServer)
    Content-Type for .css ... ok
    test_file_type_gif (__main__.HttpServer)
    Content-Type for .gif ... ok
    test_file_type_html (__main__.HttpServer)
    Content-Type for .html ... ok
    test_file_type_jpeg (__main__.HttpServer)
    Content-Type for .jpeg ... ok
    test_file_type_jpg (__main__.HttpServer)
    Content-Type for .jpg ... ok
    test_file_type_js (__main__.HttpServer)
    Content-Type for .js ... ok
    test_file_type_png (__main__.HttpServer)
    Content-Type for .png ... ok
    test_file_type_swf (__main__.HttpServer)
    Content-Type for .swf ... ok
    test_file_urlencoded (__main__.HttpServer)
    urlencoded filename ... ok
    test_file_with_dot_in_name (__main__.HttpServer)
    file with two dots in name ... ok
    test_file_with_query_string (__main__.HttpServer)
    query string with get params ... ok
    test_file_with_slash_after_filename (__main__.HttpServer)
    slash after filename ... ok
    test_file_with_spaces (__main__.HttpServer)
    filename with spaces ... ok
    test_head_method (__main__.HttpServer)
    head method support ... ok
    test_index_not_found (__main__.HttpServer)
    directory index file absent ... ok
    test_large_file (__main__.HttpServer)
    large file downloaded correctly ... ok
    test_post_method (__main__.HttpServer)
    post method forbidden ... ok
    test_request_without_two_newlines (__main__.HttpServer)
    Send GET without to newlines ... ok
    test_server_header (__main__.HttpServer)
    Server header exists ... ok

    ----------------------------------------------------------------------
    Ran 24 tests in 42.988s
    
    OK
  </code>
</details>

----------------------
# Highload testing
### Using [Apache Benchmark](https://httpd.apache.org/docs/2.4/programs/ab.html)
Download ab: `sudo apt-get install apache2-utils`

Using: `ab -n requests -c at_same address`

## This server:80
Test:
`ab -n 10000 -c 20 127.0.0.1:80/httptest/wikipedia_russia.html`

<details>
<summary>Result: <code>Total: min:2 mean:6 [+/-sd]:2.5 median:6 max:24</code><br>
(click to see all)</summary>
<code>

    This is ApacheBench, Version 2.3 <$Revision: 1843412 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/
    
    Benchmarking 127.0.0.1 (be patient)
    Completed 1000 requests
    Completed 2000 requests
    Completed 3000 requests
    Completed 4000 requests
    Completed 5000 requests
    Completed 6000 requests
    Completed 7000 requests
    Completed 8000 requests
    Completed 9000 requests
    Completed 10000 requests
    Finished 10000 requests
    
    
    Server Software:        SergTyapkin's
    Server Hostname:        127.0.0.1
    Server Port:            80
    
    Document Path:          /httptest/wikipedia_russia.html
    Document Length:        954828 bytes
    
    Concurrency Level:      20
    Time taken for tests:   38.825 seconds
    Complete requests:      10000
    Failed requests:        0
    Total transferred:      9550180000 bytes
    HTML transferred:       9548280000 bytes
    Requests per second:    257.57 [#/sec] (mean)
    Time per request:       77.649 [ms] (mean)
    Time per request:       3.882 [ms] (mean, across all concurrent requests)
    Transfer rate:          240216.66 [Kbytes/sec] received
    
    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    0   0.1      0       3
    Processing:    18   77  13.8     76     153
    Waiting:        3   21   8.0     19      76
    Total:         18   78  13.8     76     153
    
    Percentage of the requests served within a certain time (ms)
      50%     76
      66%     81
      75%     85
      80%     88
      90%     96
      95%    102
      98%    111
      99%    116
     100%    153 (longest request)
</code>
</details>

## Nginx:90

Test:
`ab -n 10000 -c 20 127.0.0.1:90/httptest/wikipedia_russia.html`

<details>
<summary>Result: <code>Total: min:41 mean:79 [+/-sd]:12.6 median:78 max:174</code><br>
(click to see all)</summary>
<code>

    This is ApacheBench, Version 2.3 <$Revision: 1843412 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/
    
    Benchmarking 127.0.0.1 (be patient)
    Completed 1000 requests
    Completed 2000 requests
    Completed 3000 requests
    Completed 4000 requests
    Completed 5000 requests
    Completed 6000 requests
    Completed 7000 requests
    Completed 8000 requests
    Completed 9000 requests
    Completed 10000 requests
    Finished 10000 requests
    
    
    Server Software:        nginx/1.21.3
    Server Hostname:        127.0.0.1
    Server Port:            90
    
    Document Path:          /httptest/wikipedia_russia.html
    Document Length:        954824 bytes
    
    Concurrency Level:      20
    Time taken for tests:   39.710 seconds
    Complete requests:      10000
    Failed requests:        0
    Total transferred:      9550620000 bytes
    HTML transferred:       9548240000 bytes
    Requests per second:    251.83 [#/sec] (mean)
    Time per request:       79.420 [ms] (mean)
    Time per request:       3.971 [ms] (mean, across all concurrent requests)
    Transfer rate:          234873.68 [Kbytes/sec] received
    
    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    0   0.1      0       5
    Processing:    41   79  12.6     78     174
    Waiting:        1   11   3.7     10      44
    Total:         41   79  12.6     78     174
    
    Percentage of the requests served within a certain time (ms)
      50%     78
      66%     83
      75%     86
      80%     89
      90%     95
      95%    101
      98%    109
      99%    116
     100%    174 (longest request)

</code>
</details>

----------------------
## Conclusion
Judging by the tests, this server is almost as good as Nginx.
